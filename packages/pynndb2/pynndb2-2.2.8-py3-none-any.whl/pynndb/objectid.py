"""
  ___  _     _           _   ___    _
 / _ \\| |__ (_) ___  ___| |_|_ _|__| |
| | | | '_ \\| |/ _ \\/ __| __|| |/ _` |
| |_| | |_) | |  __/ (__| |_ | | (_| |
 \\___/|_.__// |\\___|\\___|\\__|___\\__,_|
          |__/

Copyright &copy;2020 - Mad Penguin Consulting Limited
"""
from __future__ import annotations
from os import getpid
from time import time
from socket import gethostname
from struct import pack, unpack
from typing import Any, Optional
from pynndb.exceptions import InvalidId


def _fnv_1a_24(data: bytes):
    """FNV-1a 24 bit hash"""
    hash_size = 2 ** 32
    fnv_32_prime = 16777619
    fnv_1a_hash = 2166136261  # 32-bit FNV-1 offset basis
    for elt in data:
        fnv_1a_hash = fnv_1a_hash ^ elt
        fnv_1a_hash = (fnv_1a_hash * fnv_32_prime) % hash_size
    return (fnv_1a_hash >> 24) ^ (fnv_1a_hash & 0xffffff)


MACHINE_BYTES = _fnv_1a_24(gethostname().encode())


class ObjectId:
    """
    An ObjectId is a 14-byte unique identifier consisting of:

    - a 8-byte value representing the nano seconds since the Unix epoch
    - a 4-byte machine identifier
    - a 2-byte process id

    This code is based on the ObjectId class found in the Python BSON module.
    """

    def __init__(self, oid: Optional[bytes, str]=None) -> None:
        """
        Generate a new ObjectId either from a pre-existing sequence if bytes, or
        based on information from this machine including the time, the machine
        identifier, and the current process id.

        oid - can be a bytes(14) or a str(28) which should represent an ObjectId
        """
        if oid is None:
            self.__id = pack(">dIH", time(), MACHINE_BYTES, getpid() % 0xFFFF)
        elif isinstance(oid, bytes) and len(oid) == 14:
            self.__id = oid
        elif isinstance(oid, str) and len(oid) == 28:
            self.__id = bytes.fromhex(oid)
        else:
            raise InvalidId(
                f'{oid!r} is not a valid ObjectId, it must be a 14-byte input'
                ' or a 28-character hex string'
            )

    @property
    def generation_time(self) -> float:
        """
        Return the generation time of this ObjectId as a float (timestamp)
        """
        return unpack('>d', self.__id[:8])[0]

    @property
    def binary(self) -> bytes:
        """
        14-byte binary representation of this ObjectId.
        """
        return self.__id

    def __getstate__(self) -> bytes:
        """
        Return value of object for pickling.
        needed explicitly because __slots__() defined.
        """
        return self.__id

    def __setstate__(self, value: bytes) -> None:
        """
        explicit state set from pickling
        """
        self.__id = value

    def __str__(self) -> str:
        """
        Return the value id as a hex string
        """
        return self.__id.hex()

    def __eq__(self, other: Any) -> bool:
        """
        Boolean Equality check: EQ
        """
        if isinstance(other, ObjectId):
            return self.__id == other.binary
        return NotImplemented  # pragma: no cover

    def __ne__(self, other: Any) -> bool:
        """
        Boolean Equality check: NE
        """
        if isinstance(other, ObjectId):
            return self.__id != other.binary
        return NotImplemented  # pragma: no cover

    def __lt__(self, other: Any) -> bool:
        """
        Boolean Equality check: LT
        """
        if isinstance(other, ObjectId):
            return self.__id < other.binary
        return NotImplemented  # pragma: no cover

    def __le__(self, other: Any) -> bool:
        """
        Boolean Equality check: LE
        """
        if isinstance(other, ObjectId):
            return self.__id <= other.binary
        return NotImplemented  # pragma: no cover

    def __gt__(self, other: Any) -> bool:
        """
        Boolean Equality check: GT
        """
        if isinstance(other, ObjectId):
            return self.__id > other.binary
        return NotImplemented  # pragma: no cover

    def __ge__(self, other: Any) -> bool:
        """
        Boolean Equality check: GE
        """
        if isinstance(other, ObjectId):
            return self.__id >= other.binary
        return NotImplemented  # pragma: no cover

    def __hash__(self) -> int:
        """
        Get a hash value for this :class:`ObjectId`
        """
        return hash(self.__id)
