#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from lmdb import Cursor as LMDBCursor, Transaction as TXN
from pynndb.decorators import wrap_reader
from pynndb.doc import Doc


if TYPE_CHECKING:
    from .index import Index  # pragma: no cover


class Cursor:
    """
    The Cursor class is a simple wrapper for the LMDB cursor object, it's
    primary goal is to ensure that functions returning with "keyonly" set employ
    proper Python strings rather than 'bytes' arrays.

    This class provides the following properties;
    ---
    key   - the current key
    val   - the associated value which is the key of the associated data in the main table
    count - the number of duplicates that exist for this key value
    """

    def __init__(self, index: Index, cursor: LMDBCursor) -> None:
        """
        Simply set the "key" and "val" attributes of the object to the values
        we want to make available to the library user.

        index - a reference to the index this cursor object relates to
        cursor - an LMDB cursor object which has a reference to both the data key and value
        """
        self._index = index
        self.env = index.env
        self.key = cursor.key()
        self.val = cursor.value().decode()
        self.count = cursor.count() if self._index.duplicates else 1

    @wrap_reader
    def fetch(self, txn: Optional[TXN]=None) -> Doc:
        """
        Recover the data item that is associated with this key

        txn - an optional transaction to wrap this operation
        """
        return Doc(None, self.val).get(self._index._table, txn=txn)
