#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from __future__ import annotations
from lmdb import Transaction as TXN, Cursor
from typing import TYPE_CHECKING
from pynndb.index import Index
from pynndb.doc import Doc

if TYPE_CHECKING:
    from .table import Table  # pragma: no cover


class FilterResult:
    """
    Wrapper for results returned from the "filter" API call, use the "doc" method
    to access the resulting data.
    """

    def __init__(self, table: Table, index: Index, cursor: Cursor, txn: TXN) -> None:
        """
        Instantiate a FilterResult instance, used by the filter() API call to
        return a result to the caller. If we're searching on a primary key then
        we effectively have the data we want already, but if we're searching on
        an index, we implement a lazy-loader, so we store the real primary key
        OID, then use it to recover the actual record when the user calls the
        "doc" method.

        index - the index we were searching on (None for primary key)
        cursor - the LMDB cursor object we're using
        txn - a transaction to wrap this operation
        ---
        Properties:

        o count   the number of duplicate keys that apply to this result
        o key     the key used to acquire this result
        """
        self._txn = txn
        self._table = table
        if index is None:
            self._oid = cursor.key()
            self._dat = cursor.value()
        else:
            self.key = cursor.key()  # this is used by filter() / context
            self._oid = cursor.value()
            self._dat = None
            self.count = cursor.count() if index.duplicates else 1

    @property
    def doc(self) -> Doc:
        """
        Returns the uncompressed data associted with this search result.
        """
        if not self._dat:
            self._dat = self._txn.get(self._oid, db=self._table._db)
        return Doc(None, self._oid, self._table._decompressor(self._dat), integerkey=self._table.integerkey)

    @property
    def raw(self) -> bytes:
        """
        Returns the raw serialised data directly from the KV store
        """
        if not self._dat:
            self._dat = self._txn.get(self._oid, db=self._table._db)  # pragma: no cover
        return self._dat
