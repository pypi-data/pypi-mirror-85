import copy
import struct
from bitflags import bitflags, BitFlags
from collections import OrderedDict


__all__ = ['Field', 'BytesField', 'StrField',
           'IntField', 'Int8Field', 'Int16Field', 'Int32Field', 'FloatField', 'ScalarFloatField',
           'BitFlagField']


BYTEORDER_CONVERTER = {'little': 'little', '<': 'little',
                       'big': 'big', '>': 'big'}
ENDIAN_CONVERTER = {'little': '<', '<': '<',
                    'big': '>', '>': '>'}


class Field(object):
    """General base Field that can customize how and attributes value is set or returned."""
    DEFAULT_LENGTH = 1
    DEFAULT_BYTEORDER = 'little'
    DEFAULT_SIGNED = False

    def __init__(self, name, index, length=None, byteorder=None, signed=None,
                 get_converter=None, set_converter=None, d_names=None, d_values=None,
                 fget=None, fset=None, fdel=None, doc=None):
        """Construct the field object

        Args:
            name (str): Variable name
            index (int): Start index for this value
            length (int)[None]: Number of bytes for this field. If None use DEFAULT_LENGTH
            byteorder (str)[None]: 'little' or 'big' byteorder endianess. If None use DEFAULT_BYTEORDER
            signed (bool)[None]: If an integer is signed or unsigned. If None use DEFAULT_SIGNED.

            get_converter (callable/function) [None]: Get the real value by calling this function to convert units.
                *Signature* get_converter(value: Union[int, bytes], default:Union[int, bytes]=value) -> object
            set_converter (callable/function) [None]: Set the value by first calling this function to deconstruct units.
                *Signature* set_converter(value: Union[int, bytes], default:Union[int, bytes]=value) -> object
            d_names (dict)[None]: Dictionary that convert's string names to integers (automatically set set_converter).
                If d_values is given this is automatically created.
            d_values (dict)[None]: Dictionary that convert's integers to string names (automatically set get_converter).
                If d_names is given this is automatically created.

            fget (callable/function)[None]: Function to override which return the value.
            fset (callable/function)[None]: Function to override which sets the value.
            fdel (callable/function)[None]: Function to override which deletes the value.
            doc (str)[None]: Property docstring.
        """
        super().__init__()

        if length is None:
            length = self.DEFAULT_LENGTH
        if byteorder is None:
            byteorder = self.DEFAULT_BYTEORDER
        if signed is None:
            signed = self.DEFAULT_SIGNED

        # Automatically set_converter or get_converter
        if (d_names is not None or d_values is not None) and set_converter is None:
            if d_names is None:
                d_names = OrderedDict([(v, k) for k, v in d_values.items()])
            elif d_values is None:
                d_values = OrderedDict([(v, k) for k, v in d_names.items()])
            set_converter = d_names.get
        if d_values is not None and get_converter is None:
            get_converter = d_values.get

        if fget is None:
            fget = self.get_value
            if doc is None:
                doc = "Return the {} value for message position {}".format(name, index)
            try:
                fget.__doc__ = "Return the {} value for message position {}".format(name, index)
            except (AttributeError, Exception):
                pass
        if fset is None:
            fset = self.set_value
            try:
                fset.__doc__ = "Set the {} value for message position {}".format(name, index)
            except (AttributeError, Exception):
                pass
        if doc is None and fget is not None:
            doc = fget.__doc__

        self.name = name
        self.index = index
        self.length = length
        self.byteorder = byteorder
        self.signed = signed

        self.get_converter = get_converter
        self.set_converter = set_converter

        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def get_value(self, obj):
        """Return the value for the instance object.

        If the set length is 1 and integer will be used else bytes will be used.

        Args:
            obj (object): Instance object to set the value for.
        """
        value = obj[self.index: self.index + self.length]
        if self.get_converter:
            return self.get_converter(value, value)
        return value

    def set_value(self, obj, value):
        """Set the value for the instance object.

        Args:
            obj (object): Instance object to set the value for.
            value (bytes/int/str/float/object): Value to convert to bytes and set the bytes in the object.
        """
        if self.set_converter:
            value = self.set_converter(value, value)
        value = self.to_bytes(value, length=self.length, byteorder=self.byteorder, signed=self.signed)
        obj[self.index: self.index + len(value)] = value

    @staticmethod
    def to_bytes(value, length=None, byteorder='little', signed=False):
        if isinstance(value, (bytes, bytearray, list, tuple)):
            byts = bytes(value)
        elif isinstance(value, str):
            byts = value.encode('utf-8')
        elif isinstance(value, float):
            try:
                byts = struct.pack('<f', value)
            except (OverflowError, Exception):
                byts = struct.pack('<d', value)  # double 8 bytes
        else:
            value = int(value)
            if length is None:
                length = int((value.bit_length() + 7) // 8)
            try:
                byts = value.to_bytes(length, byteorder, signed=signed)
            except (OverflowError, Exception):
                byts = value.to_bytes(length, byteorder, signed=not signed)

        return byts[:length]

    # ===== Property interface =====
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        self.fget = fget
        if not self.__doc__:
            self.__doc__ = getattr(self.fget, '__doc__', '')
        return self

    def setter(self, fset):
        self.fset = fset
        return self

    def deleter(self, fdel):
        self.fdel = fdel
        return self


class BytesField(Field):
    """Field for multiple bytes."""
    DEFAULT_LENGTH = None
    DEFAULT_BYTEORDER = 'little'
    DEFAULT_SIGNED = False


class StrField(Field):
    DEFAULT_SIGNED = False

    def get_value(self, obj):
        byts = obj[self.index: self.index + self.length]
        value = byts.decode('utf-8')
        if self.get_converter:
            return self.get_converter(value, value)
        return value
        

class IntField(Field):
    """Use this field when a user sets the attribute as an Integer and wants to see the integer value in return."""
    DEFAULT_LENGTH = 1
    DEFAULT_BYTEORDER = 'little'
    DEFAULT_SIGNED = False

    def get_value(self, obj):
        byts = obj[self.index: self.index + self.length]
        value = int.from_bytes(byts, self.byteorder, signed=self.signed)
        if self.get_converter:
            return self.get_converter(value, value)
        return value

    def set_value(self, obj, value):
        if self.set_converter:
            value = self.set_converter(value, value)
        value = self.to_bytes(value, length=self.length, byteorder=self.byteorder, signed=self.signed)
        obj[self.index: self.index + len(value)] = value


class Int8Field(IntField):
    pass


class Int16Field(IntField):
    DEFAULT_LENGTH = 2
    DEFAULT_BYTEORDER = 'little'
    DEFAULT_SIGNED = False


class Int32Field(IntField):
    DEFAULT_LENGTH = 4
    DEFAULT_BYTEORDER = 'little'
    DEFAULT_SIGNED = False


class FloatField(Field):
    """Use this field when an attribute's field is a float and that float is converted to byte in a traditional way.

    If you scale the float to an integer before converting to bytes it would be easier to use the Int32Field.
    """

    DEFAULT_LENGTH = 4
    DEFAULT_BYTEORDER = 'little'

    def __init__(self, name, index, length=None, byteorder=None, signed=None,
                 get_converter=None, set_converter=None,
                 fget=None, fset=None, fdel=None, doc=None):
        """Construct the field object

        Args:
            name (str): Variable name
            index (int): Start index for this value
            length (int)[None]: Number of bytes for this field. If None use DEFAULT_LENGTH
            byteorder (str)[None]: 'little' or 'big' byteorder endianess. If None use DEFAULT_BYTEORDER
            signed (bool)[None]: If an integer is signed or unsigned. If None use DEFAULT_SIGNED.

            get_converter (callable/function) [None]: Get the real value by calling this function to convert units.
                *Signature* get_converter(value: Union[int, bytes], default:Union[int, bytes]=value) -> object
            set_converter (callable/function) [None]: Set the value by first calling this function to deconstruct units.
                *Signature* set_converter(value: Union[int, bytes], default:Union[int, bytes]=value) -> object

            fget (callable/function)[None]: Function to override which return the value.
            fset (callable/function)[None]: Function to override which sets the value.
            fdel (callable/function)[None]: Function to override which deletes the value.
            doc (str)[None]: Property docstring.
        """
        super().__init__(name, index, length, byteorder, signed, get_converter, set_converter,
                         fget, fset, fdel, doc)

        if self.length != 4 and self.length != 8:
            raise ValueError('Invalid length set! Float values must be 4 or 8 bytes.')

    def get_value(self, obj):
        byts = obj[self.index: self.index + self.length]
        if self.length == 4:
            value = struct.unpack('<f', byts)
        elif self.length == 8:
            value = struct.unpack('<d', byts)
        else:
            value = self.to_bytes(byts, length=self.length, byteorder=self.byteorder, signed=self.signed)

        if self.get_converter:
            return self.get_converter(value, value)
        return value


class ScalarFloatField(FloatField):
    """FloatField that uses a scalar to convert the float to an integer before convert to and from bytes."""

    DEFAULT_LENGTH = 4
    DEFAULT_BYTEORDER = 'little'
    DEFAULT_SIGNED = False
    DEFAULT_SCALAR = 1.0

    def __init__(self, name, index, length=None, scalar=None, byteorder=None, signed=None,
                 get_converter=None, set_converter=None,
                 fget=None, fset=None, fdel=None, doc=None):
        """Construct the field object

        Args:
            name (str): Variable name
            index (int): Start index for this value
            length (int)[None]: Number of bytes for this field. If None use DEFAULT_LENGTH
            scalar (int/float)[None]: Number to multiply/divide by before converting. If None use DEFAULT_SCALAR.
            byteorder (str)[None]: 'little' or 'big' byteorder endianess. If None use DEFAULT_BYTEORDER
            signed (bool)[None]: If an integer is signed or unsigned. If None use DEFAULT_SIGNED.

            get_converter (callable/function) [None]: Get the real value by calling this function to convert units.
                *Signature* get_converter(value: Union[int, bytes], default:Union[int, bytes]=value) -> object
            set_converter (callable/function) [None]: Set the value by first calling this function to deconstruct units.
                *Signature* set_converter(value: Union[int, bytes], default:Union[int, bytes]=value) -> object

            fget (callable/function)[None]: Function to override which return the value.
            fset (callable/function)[None]: Function to override which sets the value.
            fdel (callable/function)[None]: Function to override which deletes the value.
            doc (str)[None]: Property docstring.
        """
        try:
            super().__init__(name, index, length, byteorder, signed, get_converter, set_converter,
                             fget, fset, fdel, doc)
        except ValueError:
            pass  # Ignore length only being 2 or 4 value error

        if scalar is None:
            scalar = self.DEFAULT_SCALAR
        self.scalar = scalar

    def get_value(self, obj):
        byts = obj[self.index: self.index + self.length]
        value = int.from_bytes(byts, self.byteorder, signed=self.signed)
        value = value / self.scalar  # Convert to float units with scalar
        if self.get_converter:
            return self.get_converter(value, value)
        return value

    def set_value(self, obj, value):
        if self.set_converter:
            value = self.set_converter(value, value)

        if isinstance(value, (int, float)):
            value = int(value * self.scalar)
        value = self.to_bytes(value, length=self.length, byteorder=self.byteorder, signed=self.signed)
        obj[self.index: self.index + len(value)] = value


# Convert BitFlags printing.
BitFlags.__str__ = BitFlags.__repr__


class BitFlagField(IntField):
    def __init__(self, name, index, length=None, byteorder=None, signed=None,
                 get_converter=None, set_converter=None, flags=None,
                 fget=None, fset=None, fdel=None, doc=None):
        """Construct the field object

        Example:

            class MyMessage(Message):
                flags = BitFlagField('flags', 3, flags={0: 'zero', 1: 'one', 2: 'two', 3: 'three'})

            m = MyMessage()
            print(m.flags.zero)  # will be 0 or 1
            print(m.flags.one)  # will be 0 or 1
            print(m.flags.two)  # will be 0 or 1

        Args:
            name (str): Variable name
            index (int): Start index for this value
            length (int)[None]: Number of bytes for this field. If None use DEFAULT_LENGTH
            byteorder (str)[None]: 'little' or 'big' byteorder endianess. If None use DEFAULT_BYTEORDER
            signed (bool)[None]: If an integer is signed or unsigned. If None use DEFAULT_SIGNED.

            get_converter (callable/function) [None]: Get the real value by calling this function to convert units.
                *Signature* get_converter(value: Union[int, bytes], default:Union[int, bytes]=value) -> object
            set_converter (callable/function) [None]: Set the value by first calling this function to deconstruct units.
                *Signature* set_converter(value: Union[int, bytes], default:Union[int, bytes]=value) -> object

            flags (dict): Dictionary of {bit position (int): "flag_variable_name"}

            fget (callable/function)[None]: Function to override which return the value.
            fset (callable/function)[None]: Function to override which sets the value.
            fdel (callable/function)[None]: Function to override which deletes the value.
            doc (str)[None]: Property docstring.
        """
        self.flags = bitflags(options=flags)
        super().__init__(name, index, length=length, byteorder=byteorder, signed=signed,
                         get_converter=get_converter, set_converter=set_converter,
                         fget=fget, fset=fset, fdel=fdel, doc=doc)

    def get_value(self, obj):
        """Return the value for the instance object.

        If the set length is 1 and integer will be used else bytes will be used.

        Args:
            obj (object): Instance object to set the value for.
        """
        value = super().get_value(obj)

        flags = copy.copy(self.flags)
        flags.set_flags(value)

        return flags

    def set_value(self, obj, value):
        """Set the value for the instance object.

        Args:
            obj (object): Instance object to set the value for.
            value (bytes/int/str/float/object): Value to convert to bytes and set the bytes in the object.
        """
        if self.set_converter:
            value = self.set_converter(value, value)

        if isinstance(value, (str, int)):
            self.flags.set_flags(value)
            value = self.to_bytes(self.flags.value, length=self.length, byteorder=self.byteorder, signed=self.signed)
        else:
            value = self.to_bytes(value, length=self.length, byteorder=self.byteorder, signed=self.signed)
        obj[self.index: self.index + len(value)] = value
