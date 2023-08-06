import struct
from abc import ABC, abstractmethod
from functools import partial
from io import BytesIO
from typing import List

from .helpers import SectionScope, read_exactly, write_section_header


class BasicType(ABC):

    @property
    @abstractmethod
    def binary_format(self) -> str:
        pass

    @property
    @abstractmethod
    def value_type(self) -> type:
        pass

    def encode(self, value) -> bytes:
        assert self.binary_format is not None
        return struct.pack(self.binary_format, value)

    def decode(self, data: bytes):
        assert self.binary_format is not None
        result = struct.unpack(self.binary_format, data)
        if len(result) == 1:
            result = result[0]
        return self.value_type(result)


class Unknown(BasicType):

    @property
    def binary_format(self) -> str:
        return None

    @property
    def value_type(self) -> type:
        return bytes

    def encode(self, value: bytes) -> bytes:
        return value

    def decode(self, data: bytes) -> bytes:
        return data


class Float(BasicType):

    @property
    def binary_format(self) -> str:
        return "<f"

    @property
    def value_type(self) -> type:
        return float


class SignedLong(BasicType):

    @property
    def binary_format(self) -> str:
        return "<l"

    @property
    def value_type(self) -> type:
        return int


class UnsignedLong(BasicType):

    @property
    def binary_format(self) -> str:
        return "<L"

    @property
    def value_type(self) -> type:
        return int


class Byte(BasicType):

    @property
    def binary_format(self) -> str:
        return "<b"

    @property
    def value_type(self) -> type:
        return int


class String(BasicType):

    @property
    def binary_format(self) -> str:
        return None

    @property
    def value_type(self) -> type:
        return str

    def encode(self, value: str) -> bytes:
        return value.encode("cp1251") + b"\0"

    def decode(self, data: bytes) -> str:
        return data.strip(b"\0").decode("cp1251")


class ShortString(BasicType):

    @property
    def binary_format(self) -> str:
        return None

    @property
    def value_type(self) -> type:
        return int

    def encode(self, value: str) -> bytes:
        if len(value) > 4:
            raise ValueError
        return value.encode("cp1251") + b"\0" * (4 - len(value))

    def decode(self, data: bytes) -> str:
        if len(data) > 4:
            raise ValueError
        return data.rstrip(b"\0").decode("cp1251")


class ShopsType(BasicType):

    @property
    def binary_format(self) -> str:
        return None

    @property
    def value_type(self) -> type:
        return int

    def encode(self, value: List[bool]) -> bytes:
        if len(value) != 5:
            raise ValueError
        encoded_val = 0
        for i, val in enumerate(value):
            encoded_val |= (int(val) << i)
        return struct.pack('<L', encoded_val)

    def decode(self, data: bytes) -> List[bool]:
        value = struct.unpack('<L', data)[0]
        return [bool(value & (1 << i)) for i in range(5)]


class BasicList(BasicType):

    def __init__(self, base_type, fixed_size=0):
        self._base_type = base_type
        self._fixed_size = fixed_size

    @property
    def binary_format(self) -> str:
        return None

    @property
    def value_type(self) -> type:
        return list

    @property
    def base_type(self) -> type:
        return self._base_type

    def encode(self, value: list) -> bytes:
        if self._fixed_size and len(value) != self._fixed_size:
            raise ValueError

        if isinstance(self._base_type, BasicType) and self._base_type.binary_format is not None:
            result = bytearray()
            for val in value:
                result.extend(self._base_type.encode(val))
            return bytes(result)

        with BytesIO() as f:
            for val in value:
                data = self._base_type.encode(val)
                write_section_header(f, 1, len(data))
                f.write(data)
            f.flush()
            return f.getvalue()

    def decode(self, data: bytes) -> List[bool]:
        if isinstance(self._base_type, BasicType) and self._base_type.binary_format is not None:
            return [v[0] for v in struct.iter_unpack(self._base_type.binary_format, data)]

        f = BytesIO(data)
        result = []
        while f.tell() < len(data):
            with SectionScope(f, 1) as scope:
                chunk = read_exactly(f, scope.size)
                result.append(self._base_type.decode(chunk))

        if self._fixed_size and len(result) != self._fixed_size:
            raise ValueError

        return result


FloatList = partial(BasicList, Float())
SignedLongList = partial(BasicList, SignedLong())
UnsignedLongList = partial(BasicList, UnsignedLong())
ByteList = partial(BasicList, Byte())
StringList = partial(BasicList, String())
ShortStringList = partial(BasicList, ShortString())
ShopsTypeList = partial(BasicList, ShopsType())
