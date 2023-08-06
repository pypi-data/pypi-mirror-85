import sys
from dynamicmethod import dynamicmethod
from pybk8500.__meta__ import version as __version__


__all__ = ['ChecksumError', 'MessageTypeError', 'Parser']


class ChecksumError(Exception):
    pass


class MessageTypeError(Exception):
    pass


class Parser(object):
    NAME = 'pybk8500'
    VERSION = __version__
    MAX_BUFFER_SIZE = 2**16

    START_BYTE = 0xAA
    COMMAND_INDEX = 2
    MSG_LENGTH = 26

    msg_types_lookup = {}

    def __init__(self, name=None):
        # Copy the message types lookup into the instance that can be modified without the class being modified
        self.msg_types_lookup = self.__class__.msg_types_lookup.copy()

        if name is None:
            name = self.NAME

        self._buffer = bytearray()
        self.name = name
        self.error = Parser.error

    @classmethod
    def startindex(cls, data):
        """Return the start index if found. -1 if not found.

        Args:
            data (bytes): Data that you want to find the start of a message for

        Returns:
            index (int): Index of the start position. -1 if not found
        """
        return data.find(cls.START_BYTE)

    @classmethod
    def stopindex(cls, data):
        """Return the stop index if found. -1 if not found.

        Args:
            data (bytes): Data that you want to find the end of a message for. data[0] should be the start index

        Returns:
            index (int): Index of the stop position. -1 if not found
        """
        if len(data) >= cls.MSG_LENGTH:
            return cls.MSG_LENGTH
        else:
            return -1

    @dynamicmethod
    def gen_msg(self, msg_id, raw=None, address=None, **kwargs):
        """Generate a message and return the message bytes.

        It is suggested that this makes a message and sends that message into Parser.to_bytes() to reuse code.

        Returns:
            msg (Message/bytes): Message object
        """
        msg_type = self.lookup(msg_id)
        return msg_type(raw=raw, address=address, **kwargs)

    @staticmethod
    def calc_checksum(byts):
        """Calculate the checksum for the message."""
        byts = byts[:25]  # Do not use the checksum to calculate the checksum
        value = sum(byts)
        return value & 0xFF

    def process_msg(self, byts):
        """Callback to take the parsed message data and create a message object.

        If a message object is successfully created `message_parsed` is called else `error` is called.

        Args:
             byts (bytes): Bytes to convert to a message object and call message_parsed with.
        """
        msg_id = byts[self.COMMAND_INDEX]
        msg_type = self.lookup(msg_id)
        if msg_type is None:
            raise MessageTypeError('Invalid command type {}'.format(msg_id))

        # Create the message from the raw data
        msg = msg_type(raw=byts)

        # Calculate the Checkums
        calc_check = self.calc_checksum(byts)
        if calc_check != msg.checksum:
            raise ChecksumError('The calculated checksum does not match ({} != {})!'.format(calc_check, msg.checksum))

        return msg

    @staticmethod
    def message_parsed(msg):
        """Default "parse" callback function if one is not given."""
        print(msg)

    @staticmethod
    def error(error):
        """Callback to indicate that an error happened.

        Args:
            error (Exception): Optional error object if applicable (C parsers do not create error objects).
        """
        print('{}: {}'.format(type(error).__name__, error), file=sys.stderr)

    def parse(self,  byts, callback=None):
        """Parse the messages in the given bytes use the given callback to use the messages.

        Args:
            byts (bytes): Data to handle
            callback (function)[None]: Function that takes in a parsed message when the message is parsed.

        Returns:
            buffer (bytes): Unused bytes
        """
        if callback is None:
            callback = self.message_parsed

        for msg, remain in self.parse_iter(byts):
            callback(msg)

    def parse_iter(self, byts):
        """Parse the messages in the given bytes.

        Handle errors by overriding the Parser().error callback function.

        Args:
            byts (bytes): Message bytes

        Yields:
            message (Message): The message that was parsed.
            remain (bytes): Remaining bytes
        """
        self._buffer.extend(byts)
        remain = self._buffer

        while True:
            msg, error, remain = self.parse_msg(remain)
            if msg is not None:
                yield msg, remain
            elif error is None:
                break

        self._buffer = bytearray(remain)
        self.check_buffer_size()

    def parse_msg(self, byts):
        """Parse a single message and return the remaining bytes.

        Args:
            byts (bytes): Message bytes

        Returns:
            message (Message)[None]: The message that was parsed.
            error (Exception)[None]: Error that occurred.
            remaining (bytes)[b'']: The remaining bytes
        """
        msg = None
        error = None

        # Find the start index
        startindex = self.startindex(byts)
        if startindex == -1:
            # Trim the buffer, but keep the last few bytes to check for an incomplete start byte
            return msg, error, byts[-int(self.MSG_LENGTH - 1):]

        # Move the buffer
        byts = byts[startindex:]

        # Look for a stop index to see if we have a full message
        stopindex = self.stopindex(byts)
        if stopindex == -1:
            return msg, error, byts

        # Try parsing the message bytes
        try:
            msg = self.process_msg(bytes(byts[0: stopindex]))
            byts = byts[stopindex:]
        except (ChecksumError, MessageTypeError, Exception) as err:
            # Move remaining bytes only by 1 byte. Could be misaligned start byte
            msg = None
            error = err
            byts = byts[1:]
            self.error(error)

        return msg, error, byts

    def check_buffer_size(self):
        """Check the buffer size and limit the amount of data that we hold."""
        if len(self._buffer) > self.MAX_BUFFER_SIZE:
            try:
                raise OverflowError("Overflow Error: Too much data has been given without a valid message!")
            except OverflowError as error:
                self.error(error)
            self._buffer = self._buffer[-int(self.MSG_LENGTH - 1):]

    def flush(self):
        """Flush the buffer."""
        self._buffer = bytearray()

    # ========== Helper Methods ==========
    @dynamicmethod
    def lookup(self, msg_id):
        """Return the message class type for the given message identifier.

        Args:
            msg_id (str/int/bytes/MessageType): Some form of message identifier.

        Returns:
            msg_type (MessageType/callable): MessageType class or function that creates a message with a decode method.
        """
        return self.msg_types_lookup.get(msg_id, None)

    @dynamicmethod
    def add_lookup(self, msg_type=None, msg_id=None, msg_name=None):
        """Add a custom external message type (that the Packet can parse) to the lookup function.

        Args:
            msg_type (MessageType/class/type): Message type class that you want to add
            msg_id (str/bytes/int/bool)[None]: Message ID. If this is not given it will use msg_type.ID
            msg_name (str/bool)[None]: Message type display name. If this is not given it will use msg_type.NAME

        Returns:
            msg_type (MessageType/class/type): Message type that was added.

        Returns:
            decorator (function/callable): Only returns this decorator function if a 'msg_type' was not given!
        """
        # If message type not given return a decorator
        if msg_type is None:
            def decorator(msg_type, msg_id=msg_id, msg_name=msg_name):
                return self.add_lookup(msg_type, msg_id, msg_name)
            return decorator

        if msg_id is None:
            try:
                msg_id = msg_type.ID
            except AttributeError:
                pass
        if msg_name is None:
            try:
                msg_name = msg_type.__name__
            except AttributeError:
                pass

        self.msg_types_lookup[msg_type] = msg_type
        if msg_id:
            self.msg_types_lookup[msg_id] = msg_type
        if msg_name:
            self.msg_types_lookup[msg_name] = msg_type
        return msg_type

    @dynamicmethod
    def remove_lookup(self, msg_type=None, msg_id=None, msg_name=None):
        """Remove a message type from the lookup.

        Args:
            msg_type (MessageType/class)[None]: Message type class that you want to add
            msg_id (str/bytes/int)[None]: Message ID. If this is not given it will use msg_type.ID
            msg_name (str)[None]: Message type display name. If this is not given it will use msg_type.NAME
        """
        if msg_id is None:
            try:
                msg_id = msg_type.ID
            except AttributeError:
                pass
        if msg_name is None:
            try:
                msg_name = msg_type.__name__
            except AttributeError:
                pass

        try:
            msg = None
            if msg_name:
                msg = self.msg_types_lookup.pop(msg_name, msg)
            if msg_id:
                msg = self.msg_types_lookup.pop(msg_id, msg)
            if msg_type:
                msg = self.msg_types_lookup.pop(msg_type, msg)
            return msg
        except KeyError:
            pass

    def __getstate__(self):
        """Return the objects variables for serialization/pickling, so this object can be recreated in a
        separate process.
        """
        d = {'name': self.name}
        if self.msg_types_lookup != self.__class__.msg_types_lookup:
            d['msg_types_lookup'] = self.msg_types_lookup
        if self.error != self.__class__.error:
            d['error'] = self.error
        return d

    def __setstate__(self, state):
        """After deserialization/pickling in a separate process reset this object's values from the state."""
        self.msg_types_lookup = self.__class__.msg_types_lookup.copy()
        self._buffer = bytearray()
        self.name = self.NAME
        self.error = Parser.error

        for k, v in state.items():
            setattr(self, k, v)
