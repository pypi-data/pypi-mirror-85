#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################


class IndexAlreadyExists(Exception):
    pass


class FailedToWriteMetadata(Exception):
    pass


class DocumentAlreadyExists(Exception):
    pass


class FailedToWriteData(Exception):
    pass


class DocumentDoesntExist(Exception):
    pass


class NoIndexFunction(Exception):
    pass


class FailedToPutRecord(Exception):
    pass


class InvalidKeySpecifier(Exception):
    pass


class NoSuchIndex(Exception):
    pass


class NoSuchTable(Exception):
    pass


class NotDuplicateIndex(Exception):
    pass


class DuplicateKey(Exception):
    pass


class IndexWriteError(Exception):
    pass


class TableNotOpen(Exception):
    pass


class TrainingDataExists(Exception):
    pass


class InvalidId(ValueError):
    pass


class InvalidSerialiser(Exception):
    pass


class UnableToReplicate(Exception):
    pass
