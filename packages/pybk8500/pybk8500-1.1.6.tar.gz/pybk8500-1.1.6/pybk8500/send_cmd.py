"""
Manage communications between the PC and the device.

Requirements:
    * pyserial
    * continuous_threading

"""
import sys
import time
import serial
import functools
import contextlib
import continuous_threading
from pybk8500.parser import Parser


__all__ = ['CommunicationManager', 'send_msg', 'main']


def pop_messages(msg_list, msg_type=None):
    """Iterate and remove messages with the message type."""
    off = 0
    for i in range(len(msg_list)):
        msg = msg_list[i-off]
        if msg_type is None or isinstance(msg, msg_type):
            yield msg
            msg_list.pop(i-off)
            off += 1


class CommunicationManager(object):
    Parser = Parser
    DEFAULT_READ_SIZE = 26

    def __init__(self, connection=None, parser=None, com=None, baudrate=None, **kwargs):
        super().__init__()

        if parser is None:
            parser = self.Parser()
        if connection is None:
            connection = serial.Serial()
            if com is not None:
                connection.port = com
            if baudrate is not None:
                connection.baudrate = baudrate
            # connection.rts = True  # Documentation states needed. Did not work
            # connection.dtr = True  # Documentation states needed. Did not work

        self._parser = None
        self._process = None
        self._in_enter = False
        self._enter_started = False
        self._enter_connected = False
        self.read_delay = 0.0001
        self.wait_delay = 0.01
        self.read_size = None  # Use in_waiting if None

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.ack_lock = continuous_threading.RLock()
        self.ack_list = []
        self.response_types = []
        self.connection = connection
        self.set_parser(parser)

    def get_parser(self):
        """Return the parser."""
        return self._parser

    def set_parser(self, parser):
        """Set the parser.

        Args:
            parser (object/None/Parser)[None]: Parser object to parse incoming messages.
        """
        self._parser = parser
        if self._parser is not None:
            self._parser.message_parsed = self.message_parsed
            self._parser.error = self.error

    parser = property(get_parser, set_parser)

    def save_ack(self, msg):
        """Save the response messages in the available response_types."""
        if len(self.response_types) == 0 or any(isinstance(msg, rtype) for rtype in self.response_types):
            with self.ack_lock:
                self.ack_list.append(msg)

    message_parsed = save_ack

    @contextlib.contextmanager
    def change_message_parsed(self, callback):
        """Change the message parsed function while in this with block."""
        old = self.message_parsed
        self.message_parsed = callback

        yield

        self.message_parsed = old

    @staticmethod
    def error(error):
        """Callback to indicate that an error happened.

        Args:
            error (Exception): Optional error object if applicable (C parsers do not create error objects).
        """
        print('{}: {}'.format(type(error).__name__, error), file=sys.stderr)

    @contextlib.contextmanager
    def change_connection(self):
        """Change the connection properties safely."""
        is_connected = self.is_connected()
        if is_connected:
            self.disconnect()

        yield

        if is_connected:
            self.connect()

    def get_baudrate(self):
        """Return the baudrate."""
        return self.connection.baudrate

    def set_baudrate(self, value, *args, **kwargs):
        """Set the baudrate."""
        with self.change_connection():
            self.connection.baudrate = value

    def get_com(self):
        """Return the serial com port."""
        return self.connection.port

    def set_com(self, value, *args, **kwargs):
        """Set the serial com port and try to connect."""
        with self.change_connection():
            self.connection.port = value

        if not self.is_connected():
            try:
                self.connect()
                if self._in_enter:
                    self._enter_connected = True
            except Exception as err:
                print('Warning: Could not connect! {}'.format(err), file=sys.stderr)

    get_port = get_com
    set_port = set_com

    def get_rts(self):
        """Return if the RTS Hardware Flow Control is set."""
        try:
            return self.connection.rts
        except (AttributeError, Exception):
            return False

    def set_rts(self, value, *args, **kwargs):
        """Set the RTS Hardware Flow Control."""
        with self.change_connection():
            self.connection.rts = bool(value)

    def get_dtr(self):
        """Return if the DTR Hardware Flow Control is set."""
        try:
            return self.connection.dtr
        except (AttributeError, Exception):
            return False

    def set_dtr(self, value, *args, **kwargs):
        """Set the DTR Hardware Flow Control."""
        with self.change_connection():
            self.connection.dtr = bool(value)

    def is_connected(self):
        """Return if the connection/serial port is connected."""
        try:
            if isinstance(self.connection, serial.Serial):
                return self.connection.is_open
        except (AttributeError, Exception):
            pass
        return False

    def connect(self, com=None, baudrate=None, **kwargs):
        """Connect the connection/serial port."""
        if com is not None or baudrate is not None:
            self.disconnect()
        if com is not None:
            self.connection.port = com
        if baudrate is not None:
            self.connection.baudrate = baudrate

        if not self.is_connected():
            self.flush()
            if isinstance(self.connection, serial.Serial):
                self.connection.open()

    def disconnect(self, *args, **kwargs):
        """Disconnect the connection/serial port."""
        if isinstance(self.connection, serial.Serial):
            self.connection.close()

    def flush(self):
        """Clear the message buffer and input buffer."""
        with self.ack_lock:
            self.ack_list.clear()
        try:
            self.connection.flush()
        except (AttributeError, Exception):
            pass
        try:
            self.connection.reset_input_buffer()
        except (AttributeError, Exception):
            pass
        try:
            self.connection.reset_output_buffer()
        except (AttributeError, Exception):
            pass

    def read(self):
        """Read data from the connection."""
        if isinstance(self.connection, serial.Serial):
            read_size = self.read_size
            if read_size is None or read_size <= 0:
                read_size = self.connection.in_waiting
            return self.connection.read(read_size)
        else:
            return b''

    def write(self, byts):
        """Write the bytes (or message) data to the connection."""
        return self.connection.write(bytes(byts))

    def read_and_parse(self):
        """Read data from the connection and parse it."""
        try:
            if self.is_connected():
                byts = self.read()
                if byts:
                    self.parser.parse(byts, self.message_parsed)
                time.sleep(self.read_delay)
            else:
                time.sleep(0.1)
        except (ConnectionAbortedError, Exception) as err:
            print(str(err), file=sys.stderr)

    @contextlib.contextmanager
    def listen_for_messages(self, *msg_types):
        """Context manager to listen for certain message types."""
        # Ensure connected and running
        is_connected = self.is_connected()
        is_running = self.is_running()
        if not is_connected:
            self.connect()
        if not is_running:
            self.start()

        # Start listening for responses
        for msg_type in msg_types:
            if msg_type is not None:
                self.response_types.append(msg_type)

        try:
            # Yield with block
            yield

        finally:
            # Remove message types
            for msg_type in msg_types:
                try:
                    self.response_types.remove(msg_type)
                except (KeyError, IndexError, Exception):
                    pass

            # If connected and/or started then stop and/or disconnect
            if not is_running:
                self.stop()
            if not is_connected:
                self.disconnect()

    @classmethod
    def listener(cls, *msg_types, attr=None, func=None):
        """Decorator to have a function run with listen_for_messages"""
        if func is None:
            def decorator(f):
                return cls.listener(*msg_types, func=f)
            return decorator

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            msg_mngr = self
            if attr is not None:
                msg_mngr = getattr(self, msg_mngr)
            with msg_mngr.listen_for_messages(*msg_types):
                return func(self, *args, **kwargs)

        return wrapper

    def wait_for_response(self, timeout, msg_type=None):
        """Wait for a response message and return True if a message was received.

        Args:
            timeout (float/int): Number of seconds to wait for a message.
            msg_type (Message/object)[None]: Message type class to wait for.

        Returns:
            success (bool): True if a message was received within the timeout.
        """
        start = time.time()
        while (time.time() - start) < timeout:
            with self.ack_lock:
                if (msg_type is None and len(self.ack_list) > 0) or \
                        any(isinstance(msg, msg_type) for msg in self.ack_list):
                    return True
            time.sleep(self.wait_delay)
        return False

    def send_wait(self, msg, timeout=0, msg_type=None, attempts=3, print_msg=True, print_recv=None):
        """Send a message and wait for a response.

        Args:
            msg (Message): Message to convert to bytes and send.
            timeout (float/int): Number of seconds to wait for a message on each attempt.
            msg_type (Message/object)[None]: Message type class to wait for.
            attempts (int)[3]: Number of attempts to send the message and wait for the response.
            print_msg (bool)[True]: If True print out that you are sending the message.
            print_recv (bool)[print_msg]: If True print all received messages.

        Returns:
            ack_list (list): List of received messages.
        """
        if print_recv is None:
            print_recv = print_msg

        with self.listen_for_messages(msg_type):
            trials = 0
            success = False
            pout = 'Sending {} ...'.format(msg)
            while (trials < attempts) and not success:
                if print_msg:
                    print(pout)
                self.write(bytes(msg))
                success = self.wait_for_response(timeout, msg_type=msg_type)
                pout = 'Retry sending {} ...'.format(msg)
                trials += 1

            if not success and timeout > 0:
                raise TimeoutError('Attempts sending {} failed!'.format(msg))

        # Clear and return messages
        with self.ack_lock:
            msgs = list(pop_messages(self.ack_list, msg_type))

        if print_recv:
            for msg in msgs:
                print('Received:', msg)

        return msgs

    send_wait_for_response = send_wait

    def is_running(self):
        """Return if the reading thread is running."""
        return self._process is not None and self._process.is_running()

    def start(self):
        """Start reading and parsing the connection."""
        if self._process is None:
            self._process = continuous_threading.PausableThread(target=self.read_and_parse)

        self.flush()
        self._process.start()

        # Wait for the thread to start reading
        time.sleep(0.01)

        return self

    def stop(self):
        """Stop reading and parsing the connection."""
        try:
            self._process.stop()
        except (AttributeError, Exception):
            pass
        return self

    def close(self):
        """Close the process."""
        self.disconnect()
        try:
            self._process.close()
        except (AttributeError, Exception):
            pass
        self._process = None
        return self

    def __enter__(self):
        """Enter the 'with' context manager."""
        self._in_enter = True
        if not self.is_connected():
            try:
                self.connect()
                self._enter_connected = True
            except Exception as err:
                print('Warning: Could not connect! {}'.format(err), file=sys.stderr)
        if not self.is_running():
            self.start()
            self._enter_started = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the 'with' context manager."""
        self._in_enter = False
        if self._enter_started:
            self._enter_started = False
            self.stop()
        if self._enter_connected:
            self._enter_connected = False
            self.disconnect()
        return exc_type is None


def send_msg(com, baudrate, cmd_id, timeout=1, attempts=1, **kwargs):
    """Send a command to the device.

    Args:
        com (str): Com port to connect to
        baudrate (int): Baudrate to connect with.
        cmd_id (int/str/Message): Command identifier to send.
        timeout (float/int)[1]: Timeout to wait for the response.
        attempts (int)[1]: Number of times to send the message expecting a response.
        **kwargs (dict): Dictionary of Command keyword arguments (variable names with values).
    """
    cmd_type = Parser.lookup(cmd_id)
    if cmd_type is None:
        raise ValueError('Invalid cmd_id given! No matching command for {}'.format(cmd_id))

    cmd = cmd_type(**kwargs)

    with CommunicationManager(com=com, baudrate=baudrate) as ser:
        try:
            msgs = ser.send_wait(cmd, timeout=timeout, msg_type=cmd.RESPONSE_TYPE, attempts=attempts)
        except TimeoutError:
            # Timeout error with no response for the expected type.
            with ser.ack_lock:
                msgs = [ser.ack_list.pop(0) for _ in range(len(ser.ack_list))]

        for msg in msgs:
            print('Received {}:'.format(msg.NAME))
            for field, value in msg.fields().items():
                print('\t{} = {}'.format(field, value))
            print()


main = send_msg


def cli_to_kwargs(cli_args):
    """Convert command line arguments to a dictionary.

    Args:
        cli_args (list): List of command line arguments ["--address", "1", "--value", 2]
    """
    return {get_name(cli_args[i]): get_value(cli_args[i+1]) for i in range(0, len(cli_args), 2)}


def get_name(name):
    """Get a command line argument name by removing all '-'."""
    return str(name).replace('-', '')


def get_value(value):
    """Convert the given string value to a proper python object.

    ast.literal_eval may work better.
    """
    try:
        if str(value).startswith('0x'):
            return int(value, 16)  # Was given hex. This allows "0x12" = 18
        else:
            return int(value)
    except (ValueError, TypeError, Exception):
        try:
            return float(value)
        except (ValueError, TypeError, Exception):
            return value


if __name__ == '__main__':
    import argparse

    P = argparse.ArgumentParser(description='Send a command to the device.')
    P.add_argument('com', type=str, help='Com port to connect to.')
    P.add_argument('baudrate', type=int, help='Baudrate to connect with.')
    P.add_argument('cmd_id', type=str,
                   help='Command ID as the string NAME or integer ID '
                        '(Example: "Command Status" String, 0x12 Hex, or 18 Dec).')
    P.add_argument('--timeout', type=float, default=1, help='Timeout to wait for the response.')
    P.add_argument('--attempts', type=int, default=1, help='Number of times to send the message expecting a response.')
    ARGS, REMAINDER = P.parse_known_args()

    main(ARGS.com, ARGS.baudrate, get_value(ARGS.cmd_id), timeout=ARGS.timeout, attempts=ARGS.attempts,
         **cli_to_kwargs(REMAINDER))
