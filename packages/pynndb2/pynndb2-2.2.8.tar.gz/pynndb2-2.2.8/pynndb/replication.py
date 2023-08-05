"""
description: replication.py
copyright: Copyright &copy;2020 - Mad Penguin Consulting Limited
"""
from posix_ipc import Semaphore, ExistentialError, O_CREAT
from uuid import uuid1 as uuid1
from pynndb.doc import Doc


class Replication:

    UUID_KEY = '__uuid__'
    REPL_KEY = '__replication__'
    JOURNAL = '__journal__'

    def __init__(self, database):
        self._semaphore = None
        self._database = database
        self._table = None
        self.uuid = None
        self.enabled = False

    def open(self, txn=None):
        """
        Open the __journal__ table and make it available for IO
        """
        doc = self._database.meta.fetch_key(self.UUID_KEY, txn=txn)
        if doc:
            self.uuid = doc._uuid
        else:
            self.uuid = uuid1().hex
            self._database.meta.store_key(self.UUID_KEY, Doc({'uuid': self.uuid}), txn=txn)
        doc = self._database.meta.fetch_key(self.REPL_KEY, txn=txn)
        if (not doc or not doc._enabled) and not self.enabled:
            return None
        if self.enabled and (not doc or not doc._enabled):
            self._database.meta.store_key(self.REPL_KEY, Doc({'enabled': True}), txn=txn)
        self.enabled = True
        if self._table is None:
            self._table = self._database.table(self.JOURNAL, integerkey=True, txn=txn)
            try:
                self._semaphore = Semaphore(self.semaphore_name, flags=O_CREAT)
                self._semaphore.release()
            except ExistentialError as e:  # pragma: no cover
                raise Exception(f'replication is enabled but a manager process not detected: {e}')  # pragma: no cover

    def flush(self, journal, txn):
        self._table.append(Doc({'deltas': journal}, integerkey=True), txn=txn)
        txn.commit()
        self._semaphore.release()

    def close(self):
        if self._semaphore:
            self._semaphore.close()
        self._table = None

    @property
    def semaphore_name(self):
        return f'/pynndb_{self.uuid}'
