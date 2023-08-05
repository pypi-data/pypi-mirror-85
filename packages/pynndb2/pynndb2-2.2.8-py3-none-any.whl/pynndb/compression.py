#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from __future__ import annotations
from enum import Enum
from lmdb import Transaction as TXN
from typing import Dict, Optional
from sys import modules
from pynndb.doc import Doc
from pynndb.decorators import wrap_reader, transparent_resize, WriteTransaction
from pynndb.exceptions import TableNotOpen, TrainingDataExists


try:
    from zstandard import ZstdCompressionDict, ZstdCompressor, ZstdDecompressor, \
        train_dictionary, ZstdError
except ImportError:   # pragma: no cover
    pass  # pragma: no cover

try:
    from snappy import compress as snappy_compress, uncompress as snappy_decompress
except ImportError:   # pragma: no cover
    pass  # pragma: no cover


COMPRESSORS = {}


class CompressionType(Enum):
    """
    Enumeration of the different compression types we've implemented. Note that although
    we support these types, the only ones that will be available are the ones we have
    back-end library support for. Compression libraries are not included in the dependency
    list for PyNNDB so it's up to you to install any libraries you wish to use.

    o ZSTD     the Zstandard compression algorithm (pip install zstandard)
    o SNAPPY   the Snappy compression library by Google (pip install python-snappy)
    """
    ZSTD = 'zstd'
    SNAPPY = 'snappy'
    NONE = None


class Compression:
    """
    This class encapsulates all compression activity and is used
    as a base class for 'Table'. It's designed in such a way that any number of
    compression libraries can be used (or not) on a table by table basis, with
    potentially different types of compression being used on different tables.
    """

    def __init__(self):
        """
        When we instantiate this class, all it does is to set up a default compressor
        and decompressor in advance of being told which (if any) compression library
        to use for this table.
        """
        self.close()

    def _get(self, dat: bytes) -> Dict:
        """
        Base read routine, run any incoming data through the selected decompressor
        then convert it to 'str'

        dat - the incoming binary data
        """
        return self.deserialise(self._decompress(dat))

    def _put(self, doc: Doc) -> None:
        """
        Base write routine, pass all data through the currently selected compressor
        for this table.

        doc - object to write to the table
        """
        return self._compress(self.serialise(doc.doc))

    def close(self):
        """
        Reset the compression routines (to "no" compression) for this table, called
        by Table.close to make sure any subsequent Table.open has a known /
        consistent starting state.
        """
        self._compressor = self._put
        self._decompressor = self._get
        self._compress = lambda doc: doc
        self._decompress = lambda doc: doc

    @wrap_reader
    def compressed(self, txn: Optional[TXN]=None) -> bool:
        """
        Determine whether this table is set to be compressed or not, returns True if the
        table is compressed.

        txn - a transaction to wrap the table read
        """
        config = self._meta.fetch_config(self.name, txn=txn)
        return 'compression' in config

    @wrap_reader
    def compression_type(self, txn: Optional[TXN]=None) -> CompressionType:
        """
        Return the compression type that has been appled to this table, or return an
        empty string if no compression is available.

        txn - a transaction to wrap the table read
        """
        config = self._meta.fetch_config(self.name, txn=txn)
        if config._compression:
            return CompressionType(config._compression.get('type'))
        return CompressionType.NONE

    def open(self, txn: TXN) -> None:
        """
        Called as part of Table.open, if compression is enabled, set up the required aspects
        of the chosen compression library in advance of any IO requests.

        txn - a write transaction to wrap the operation
        """
        if self._meta:
            config = self._meta.fetch_config(self.name, txn=txn)
            if 'compression' in config:
                compression = config._compression
                ctype = CompressionType(compression.get('type'))
                level = compression.get('level')
                if ctype == CompressionType.ZSTD:
                    cbyte = self._meta.fetch_tag(self.name, 'zstd_cdict', txn=txn)
                    cdict = ZstdCompressionDict(cbyte or b'')
                    self._decompress = ZstdDecompressor(dict_data=cdict).decompress
                    self._compress = ZstdCompressor(level, dict_data=cdict).compress
                elif ctype == CompressionType.SNAPPY:
                    self._decompress = snappy_decompress
                    self._compress = snappy_compress
                else:
                    raise NotImplemented(f"Sorry, we can't handle ({ctype.value}) compression")  # pragma: no cover

    def compression_select(
            self,
            compression_type: CompressionType,
            level: Optional[int]=3,
            txn: Optional[TXN]=None) -> bool:
        """
        Select the compression type for this table, this routine is called as a part of table open
        is compression has been requested. We return True if the compression setting has changed
        (and as a result we need to compress existing data) or False if nothing has changed.

        compression_type - the type of compression to request
        level - the compression level to apply
        txn - a write transaction to wrap the operation
        """
        if compression_type not in COMPRESSORS or not COMPRESSORS[compression_type]:
            raise NotImplemented(f'Compression mechanism not available: {compression_type}')

        config = self._meta.fetch_config(self.name, txn=txn)
        if config._compression:
            if CompressionType(config._compression.get('type')) == compression_type:
                return False  # We're already turned on!

        config._compression = {
            'type': compression_type.value,
            'level': level
        }
        self._meta.store_config(self.name, Doc(config), txn=txn)
        return True

    def compress_existing_data(self, txn: TXN=None):
        """
        Compress all pre-existing data in this table and is called by Table.open when
        compression has been turned on for the first time. Table operations rely on
        all data either being compressed, or uncompressed, so interrupting this routine
        would not be advisable. If possible, always run "open" within a write transaction.

        txn - a write transaction to wrap the operation
        """
        with txn.cursor(db=self._db) as cursor:
            while cursor.next():
                Doc(self.deserialise(cursor.value()), cursor.key()).put(self, txn=txn)

    @transparent_resize
    def zstd_train(
            self,
            training_record_count: Optional[int]=None,
            training_samples: Optional[list]=None,
            training_dict_size: Optional[int]=4096,
            threads: Optional[int]=-1,
            txn: Optional[TXN, WriteTransaction]=None) -> None:
        """
        This is a ZSTD specific routine to generate a training dict to aid in the compression
        process. Compression will work without this, however in theory you will get better
        compression if you provide some training. Note that once you have run the training
        routine and generated a compression dict, this is stored permemantly in the database
        meta data and is "required" to decompress data that has been compressed using this
        dict. If you lose (or overwrite) this "compression dict", it will render your
        compressed data useless. Any attempt to re-train a table should raise an exception.

        training_record_count - the number of records to sample from the current table
        training_samples - if supplied these will be used instead of reading data from the table
        training_dict_size - the maximum size allowable for the compression dictionary
        threads - the number of threads to use for training
        txn - an optional transaction to wrap the operation
        ```
        db = Manager()['mydb'].open('.database')
        people = db['people'].open()
        (add data)
        people.zstd_train(10)
        people.close()
        people.open(CompressionType.ZSTD, 22)
        ```
        The last line will re-open the table with compression enabled, using the compression
        dict generated by 'zstd_train', then compress all existing data using this dict.
        """
        if not self.isopen:
            raise TableNotOpen(self.name)

        if self._meta.fetch_tag(self.name, 'zstd_cdict', txn=txn) is not None:
            raise TrainingDataExists

        if training_samples and training_record_count:
            raise ValueError('Please use training_record_count OR training_samples, not both')

        transaction = txn if isinstance(txn, TXN) else txn.txn
        count = 0
        error = None
        samples = training_samples if training_samples else []
        if not training_samples:
            if not training_record_count:
                training_record_count = 100
            with transaction.cursor(db=self._db) as cursor:
                while cursor.next() and count < training_record_count:
                    count += 1
                    record = self._decompress(cursor.value())
                    samples.append(record)
        try:
            cdict_bytes = train_dictionary(
                samples=samples,
                dict_size=training_dict_size,
                threads=threads
            ).as_bytes()
        except ZstdError as e:
            cdict_bytes = b''
            error = e
        finally:
            self._meta.store_tag(self.name, 'zstd_cdict', cdict_bytes, txn=txn)

        return error


COMPRESSORS[CompressionType.ZSTD] = True if 'zstandard' in modules else False
COMPRESSORS[CompressionType.SNAPPY] = True if 'snappy' in modules else False

