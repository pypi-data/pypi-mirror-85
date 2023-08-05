#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from __future__ import annotations
from lmdb import Transaction as TXN, Cursor
from typing import TYPE_CHECKING, Optional, Callable
from pynndb.doc import Doc
from pynndb.decorators import wrap_reader
from pynndb.exceptions import DuplicateKey
from pynndb.types_ import Config

if TYPE_CHECKING:
    from .table import Table  # pragma: no cover


class Index:
    """
    The Index class models individual indexes of which a table may have zero or more. There
    are two crucial parameters supplied when setting up an index and are passed via "conf".

    o dupsort    this controls whether the index will allow duplicate values to be inserted
    o func       this is the anonymous function used to generate key values from the date record
    """

    def __init__(self, table: Table, name: str, conf: Config) -> None:
        """
        When we instantiate an Index we primarily need a back-reference to the database we're
        working with, the name of the index we're instantiating, and a definition of the indexing
        function. The indexing function is held in the 'func' item in the conf dictionary. By
        default the indexing function will be a python format string, hoever you can also supply
        a 'proper' python function if you prefix it with 'def '

        database - a reference to the database we're working with
        name - the name of the index we're creating a reference to
        conf - a configuration dict containing information specific to this dictionary
        """
        conf = dict(conf)
        super().__init__()
        self.env = table.env
        self._table = table
        self.name = name
        self._conf = conf
        self._db = None
        self.func = func = conf.get('func')
        if func[:4] == 'def ':
            self._func = self.anonymous_full(func)
        else:
            self._func = self.anonymous('(r): return "{}".format(**r).encode()'.format(conf.get('func')))
        self.duplicates = conf.get('dupsort', False)
        del conf['func']

    def open(self, txn: TXN) -> None:
        """
        Open the index and make it available to the table

        txn = an optional transaction
        """
        options = dict(self._conf, **{'key': self._conf['key'].encode()})
        self._db = self.env.open_db(**options, txn=txn)

    @wrap_reader
    def records(self, txn: Optional[TXN]=None) -> int:
        """
        Return the number of records in this index

        txn - an optional transaction
        """
        return txn.stat(self._db).get('entries', 0)

    def save(self, old_doc: Doc, new_doc: Doc, txn: TXN) -> None:
        """
        Update a pre-existing index entry, we need both the old version of the record in
        order to remove the old index entries, and the new record to generate and insert
        the new ones.

        old_doc - the previous version of the record
        new_doc - the new version of the record
        txn - an optional transaction
        """
        try:
            old_key = self._func(old_doc.doc)
        except KeyError:  # pragma: no cover
            old_key = []  # pragma: no cover
        try:
            new_key = self._func(new_doc.doc)
        except KeyError:
            new_key = []
        if old_key != new_key:
            if not isinstance(old_key, list):
                old_key = [old_key]
            if not isinstance(new_key, list):
                new_key = [new_key]
            for key in new_key:
                txn.put(key, new_doc.oid, db=self._db)
            for key in old_key:
                txn.delete(key, old_doc.oid, db=self._db)

    def get(self, doc: Doc, txn: TXN) -> Optional[bytes]:
        """
        Get an entry from this index

        doc - the record template for the data to retrieve
        txn - an optional transaction
        """
        return txn.get(self._func(doc.doc), db=self._db)

    def put(self, doc: Doc, txn: TXN) -> None:
        """
        Put a new entry in this index, used when createing new records

        doc - the document associated with this index entry
        txn - an optional transaction
        """
        try:
            keys = self._func(doc.doc)
        except KeyError:
            return
        if not isinstance(keys, list):
            keys = [keys]
        for key in keys:
            if not txn.put(key, doc.oid, db=self._db, overwrite=self.duplicates):
                if not self.duplicates:
                    raise DuplicateKey

    def put_cursor(self, cursor: Cursor, txn: TXN) -> None:
        """
        Put a new index entry based on a Cursor rather than a Doc object. This is here
        mainly to make "reindex" more elegant / readable.

        cursor - an LMDB Cursor object
        txn - an optional transaction
        """
        self.put(Doc(self._table.deserialise(cursor.value()), cursor.key()), txn=txn)

    def delete(self, doc: Doc, txn: TXN) -> None:
        """
        Delete an entry from this index

        doc - record associated with the index entry to delete
        txn - an optional transaction
        """
        try:
            keys = self._func(doc.doc)
        except KeyError:  # pragma: no cover
            return        # pragma: no cover
        if not isinstance(keys, list):
            keys = [keys]
        for key in keys:
            txn.delete(key, doc.oid, self._db)

    def empty(self, txn: TXN) -> None:
        """
        Remove all entries from this index

        txn - an optional transaction
        """
        txn.drop(self._db, delete=False)

    def drop(self, txn: TXN) -> None:
        """
        Remove all entries from this index and then remove the index

        txn - an optional transaction
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        transaction.drop(self._db, delete=True)

    def map_key(self, doc: Doc) -> str:
        """
        Return the key derived from the supplied record for this particular index

        doc - the record from which we want to derive a key
        """
        return self._func(doc.doc)

    @staticmethod
    def anonymous(text: str) -> Callable:
        """
        An function used to generate anonymous functions for database indecies

        text - a Python lambda function
        """
        scope = {}
        exec('def func{0}'.format(text), scope)
        return scope['func']

    @staticmethod
    def anonymous_full(text: str) -> Callable:
        """
        An function used to generate anonymous functions for database indecies

        text - a Python lambda function
        """
        scope = {}
        exec(text, scope)
        return scope['func']

    @staticmethod
    def index_path(table_name: str, index_name: str) -> str:
        """
        Produce an index "path" name for this index based on the table name and index name
        """
        return f'_{table_name}_{index_name}'
