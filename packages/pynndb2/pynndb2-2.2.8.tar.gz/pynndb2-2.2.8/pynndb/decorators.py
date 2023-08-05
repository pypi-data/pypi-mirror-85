#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from typing import Any, Callable, Generator
from lmdb import MapResizedError, MapFullError, Transaction
import functools

SIZE_MULTIPLIER = 1.2   # how much to scale the map_size by
PAGE_SIZE = 4096        # page size to round to

try:
    from loguru import logger as log
except Exception:   # pragma: no cover
    pass            # pragma: no cover


class PyNNDBTransaction:

    def __init__(self, database, write):
        self._env = database.env
        self._flush = database.replication.flush
        self._write = write
        self.journal = []

    def __enter__(self):
        while True:
            try:
                self.txn = Transaction(env=self._env, write=self._write)
                return self
            except MapResizedError:  # pragma: no cover
                if 'log' in globals():
                    log.warning(f'database RESIZED')  # pragma: no cover
                self._env.set_mapsize(0)  # pragma: no cover

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if self.journal:
                self._flush(self.journal, self.txn)
            else:
                self.txn.commit()
        else:
            self.txn.abort()


class ReadTransaction(PyNNDBTransaction):

    def __init__(self, database):
        super().__init__(database, False)


class WriteTransaction(PyNNDBTransaction):

    def __init__(self, database):
        super().__init__(database, True)


def transparent_resize(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        if kwargs.get('txn'):
            return func(*args, **kwargs)
        while True:
            try:
                with WriteTransaction(getattr(args[0], '_database', args[0])) as kwargs['txn']:
                    return func(*args, **kwargs)
            except MapFullError:
                txn = kwargs['txn']
                del kwargs['txn']
                try:
                    transaction = txn if isinstance(txn, Transaction) else txn.txn
                    transaction.abort()
                except Exception:  # pragma: no cover
                    raise  # pragma: no cover
                database = getattr(args[0], '_database', args[0])
                if not database.auto_resize:
                    log.error(f'MapFullError and auto_resize disabled')  # pragma: no cover
                    raise  # pragma: no cover
                #
                old_mapsize = database.env.info()['map_size']
                new_mapsize = int(old_mapsize * SIZE_MULTIPLIER // PAGE_SIZE * PAGE_SIZE)
                #
                if 'log' in globals():
                    log.warning(f'db ({database.name}) extended {old_mapsize} -> {new_mapsize}')  # pragma: no cover
                database.env.set_mapsize(new_mapsize)
                database._conf['map_size'] = new_mapsize
                database.reopen()
    return wrapped


def wrap_reader_yield(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Generator[Any, None, None]:
        if kwargs.get('txn'):
            yield from func(*args, **kwargs)
        else:
            while True:
                try:
                    with args[0].env.begin() as kwargs['txn']:
                        yield from func(*args, **kwargs)
                        return
                except MapResizedError:
                    args[0].env.set_mapsize(0)                         # pragma: no cover
    return wrapped


def wrap_reader(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        if kwargs.get('txn'):
            return func(*args, **kwargs)
        else:
            while True:
                try:
                    with args[0].env.begin() as kwargs['txn']:
                        return func(*args, **kwargs)
                except MapResizedError:
                    args[0].env.set_mapsize(0)                         # pragma: no cover
    return wrapped
