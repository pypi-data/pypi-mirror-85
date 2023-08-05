#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################

__version__ = '2.2.8'

from pynndb.manager import Manager
from pynndb.database import Database
from pynndb.table import Table, FilterResult
from pynndb.index import Index
from pynndb.doc import Doc, JournalType
from pynndb.compression import CompressionType
from pynndb.objectid import ObjectId
from pynndb.decorators import transparent_resize, WriteTransaction, ReadTransaction
from pynndb.serialiser import Serialiser, SerialiserType
from pynndb.exceptions import IndexAlreadyExists, FailedToWriteMetadata, DocumentAlreadyExists, FailedToWriteData, \
    DocumentDoesntExist, InvalidKeySpecifier, NoSuchIndex, NotDuplicateIndex, NoSuchTable, \
    DuplicateKey, IndexWriteError, TableNotOpen, TrainingDataExists, InvalidSerialiser, InvalidId


__all__ = [
    Manager,
    Database,
    Table,
    Index,
    Doc,
    CompressionType,
    ObjectId,
    FilterResult,
    transparent_resize,
    WriteTransaction,
    ReadTransaction,
    JournalType,
    Serialiser,
    SerialiserType,
    IndexAlreadyExists,
    FailedToWriteMetadata,
    DocumentAlreadyExists,
    FailedToWriteData,
    DocumentDoesntExist,
    InvalidId,
    InvalidKeySpecifier,
    InvalidSerialiser,
    NoSuchIndex,
    NotDuplicateIndex,
    NoSuchTable,
    DuplicateKey,
    IndexWriteError,
    TableNotOpen,
    TrainingDataExists
]
