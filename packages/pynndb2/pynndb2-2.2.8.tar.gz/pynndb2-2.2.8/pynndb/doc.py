#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, KeysView, ItemsView, ValuesView, Dict
from lmdb import Transaction as TXN
from struct import pack, unpack
from pynndb.objectid import ObjectId

if TYPE_CHECKING:
    from .table import Table  # pragma: no cover


class JournalType(Enum):
    """
    """
    CREATE = 'C'
    UPDATE = 'U'
    APPEND = 'A'
    DELETE = 'D'
    ENSURE = 'E'
    REMOVE = 'R'
    SNAPXX = 'S'


class Doc:
    """
    The Doc object is used to encapsulate data records before they are written to the
    database and after they are read from the database. It performs a number of crucial
    functions including;

    o Associating a data buffer with a key (OID)
    o Tracking updated attributes between the last read record and the current buffer
    o Tracking deleted attributes
    o Serialising and deserialising data between the database and user buffers
    o Providing a dict and object-like interfaces to interact with the data

    Note that this interface is 'slower' than using a raw 'dict' as in version 1, however
    the use of 'Doc' facilitates the new 'C' extension (which should be a drop-in replacement
    for 'Doc') which should be much faster, and this in turn facilitates the new GOBJECT
    serialisation mechanism that should provide a 2-10x performance increase.
    """

    def __init__(
            self,
            doc: Optional[Dict]=None,
            oid: Optional[bytes, str]=None,
            dat: Optional[Dict]=None,
            integerkey=False) -> None:
        """
        Instantiate a Doc object either based on a Dict or Cursor object. In the event a Cursor object
        is supplied, the (upd) field is set to cursor.value() and (oid) is set to cursor.key(). If a dict
        is supplied, (upd) is set to the value of the dict supplied, and oid is either set to the supplied
        oid or left as None by default.

        doc - the data to associate with this object
        oid - a primary key to associate with this object
        """
        if isinstance(oid, str):
            self.oid = oid.encode()
        elif isinstance(oid, int):
            self.oid = pack('>Q', oid)
        else:
            self.oid = oid
        self.integerkey = integerkey
        self.upd = doc or {}
        self.dat = dat or {}
        self.rem = []

    @property
    def changed(self) -> bool:
        """
        Return True is the Doc has changed since it was read from the database. Changes are indicated by
        something in (rem) which signifies a field has been deleted or something in (upd) which
        signifies something has been added or updated.
        """
        return len(self.upd) != 0 or len(self.rem) != 0

    @property
    def key(self) -> str:
        """
        Return the current key (oid) for this document
        """
        if not self.oid:
            return None
        return unpack('>Q', self.oid)[0] if self.integerkey else self.oid.decode()

    def journal_entry(self, jtype: JournalType, table_name: str) -> Dict[str, Dict]:
        return {
            'mod': jtype.value,
            'table': table_name,
            'key': self.key,
            'upd': self.upd,
            'rem': self.rem
        }

    def snapshot_entry(self, jtype: JournalType, table_name: str) -> Dict[str, Dict]:
        return {  # pragma: no cover
            'mod': jtype.value,
            'table': table_name,
            'key': self.key,
            'upd': self.dat
        }

    def __getattr__(self, key: str) -> Any:
        """
        Return the data item associated with 'key' (dropping the '_' prefix)

        key - data item name prefixed with an underscore
        """
        if key[0] == '_':
            key = key[1:]
            return self.upd.get(key, self.dat.get(key))
        raise AttributeError(f'unable to find key: {key}')

    def __setattr__(self, key: str, val: Any) -> None:
        """
        Set the data item associated with 'key' (dropping the '_' prefix)

        key - data item name prefixed with an underscore
        val - actual data item to associate with key
        """
        if key[0] == '_':
            self.upd[key[1:]] = val
        else:
            object.__setattr__(self, key, val)

    def pop(self, key: str) -> None:
        self.__delitem__(key)

    def __repr__(self) -> str:
        """
        Return a string representation of the Doc object
        """
        return f'<Doc object with id={self.oid}>'

    def __len__(self) -> int:
        """
        Return the current length of the output buffer
        """
        return len(self.dat) + len(self.upd)

    def __getitem__(self, key: str) -> Any:
        """
        Return the data item associated with 'key'

        key - data item name
        """
        return self.upd.get(key, self.dat.get(key))

    def __delitem__(self, key: str) -> None:
        """
        Delete the data item associated with key

        key - data item name
        """
        if key in self.upd:
            del self.upd[key]
        if key in self.dat:
            del self.dat[key]
            self.rem.append(key)

    def __setitem__(self, key: str, val: Any) -> None:
        """
        Set the data item associated with 'key' (dropping the '_' prefix)

        key - data item name prefixed with an underscore
        val - actual data item to associate with key
        """
        self.upd[key] = val

    def __contains__(self, key: str) -> bool:
        """
        Return True if the field exists in this instance.

        key - the key to look for
        """
        return key in self.doc

    def __eq__(self, o):
        return (self.__class__ == o.__class__) and (self.oid == o.oid) and (self.doc == o.doc) and (self.rem == o.rem)

    def __ne__(self, o):
        return not self.__eq__(o)

    def __bool__(self):
        return True

    def get(self, table: Table, txn: TXN) -> Optional[Doc]:
        """
        Populate this structure by reading data from the database

        db - open database handle
        txn - active database transaction

        Returns a reference to self
        """
        dat = txn.get(self.oid, db=table._db)
        if dat:
            self.dat = table._decompressor(dat)
            return self
        return None

    def put(self, table: Table, append: bool=False, txn: TXN=None) -> None:
        """
        Store the current output buffer back in the database

        db - open database handle
        append - whether to use "append" mode
        txn - active database transaction
        """
        if not self.oid:
            self.oid = str(ObjectId()).encode()
        txn.put(self.oid, table._compressor(self), append=append, db=table._db)

    def keys(self) -> KeysView:
        """
        Return the equivalent of dict.keys() for our current buffer
        """
        return dict(self.dat, **self.upd).keys()

    def items(self) -> ItemsView:
        """
        Return the equivalent of dict.items() for our current buffer
        """
        return dict(self.dat, **self.upd).items()

    def values(self) -> ValuesView:
        """
        Return the equivalent of dict.values() for our current buffer
        """
        return dict(self.dat, **self.upd).values()

    @property
    def doc(self) -> Dict[str, Any]:
        """
        Return the new buffer as a dictionary, i.e. the old + updates
        """
        return dict(self.dat, **self.upd)
