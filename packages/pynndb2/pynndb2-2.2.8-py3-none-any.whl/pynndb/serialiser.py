"""
               _       _ _
 ___  ___ _ __(_) __ _| (_)___  ___ _ __
/ __|/ _ \\ '__| |/ _` | | / __|/ _ \\ '__|
\\__ \\  __/ |  | | (_| | | \\__ \\  __/ |
|___/\\___|_|  |_|\\__,_|_|_|___/\\___|_|

Copyright &copy;2020 - Mad Penguin Consulting Limited
"""
from __future__ import annotations
from typing import Optional
from enum import Enum
from lmdb import Transaction as TXN
from json import loads, dumps
from pynndb.doc import Doc
from pynndb.exceptions import InvalidSerialiser

try:
    import ujson
except Exception:   # pragma: no cover
    pass            # pragma: no cover

try:
    import orjson
except Exception:   # pragma: no cover
    pass            # pragma: no cover


class SerialiserType(Enum):
    """
    Serialisers are pluggable via this module, currently we support the following;

    o UJSON     the default historical serialiser
    o ORJSON    the new guy on the block
    """
    JSON = 'json'
    UJSON = 'ujson'
    ORJSON = 'orjson'
    NONE = 'none'


class Serialiser:
    """
    All attempts to serialise or de-serialise data come through this point. Any new serialiser
    that supports "loads" and "dumps" can simplu be imported and plugged into __init__ and that
    should be all there is to it.
    """

    def __init__(self, codec: Optional[SerialiserType]=SerialiserType.NONE, txn: TXN=None):
        """
        Set up handlers for serialisation and de-serialisation.

        codec - module that will supply "dumps" and "loads" methods
        """
        self._generic_loads = loads
        self._generic_dumps = dumps
        self._codec = SerialiserType.JSON

        if not self._meta:
            return

        if not codec or codec == SerialiserType.NONE:
            if 'ujson' in globals():
                codec = SerialiserType.UJSON
            elif 'orjson' in globals():         # pragma: no cover
                codec = SerialiserType.ORJSON   # pragma: no cover

        if codec == SerialiserType.UJSON:
            self._generic_dumps = ujson.dumps
            self._generic_loads = ujson.loads
        elif codec == SerialiserType.ORJSON:
            self._generic_dumps = orjson.dumps
            self._generic_loads = orjson.loads
        elif codec != SerialiserType.JSON:
            raise Exception('No serialisers available ["json", "orjson"]')  # pragma: no cover
        #
        self._codec = codec
        #
        #   Sentinel - make sure we don't use a serialiser on data that's already been
        #              written with a different serialsier.
        #
        config = self._meta.fetch_config(self.name, txn=txn)
        if 'codec' not in config:
            config['codec'] = self._codec.value
            self._meta.store_config(self.name, Doc(config), txn=txn)
        else:
            if self._codec.value != config._codec:
                raise InvalidSerialiser(f'trying to use "{self._codec.value}" but data encoded with "{config._codec}"')

    def serialise(self, doc: dict) -> bytes:
        """
        Generic serialiser interface
        """
        dump = self._generic_dumps(doc)
        return dump if isinstance(dump, bytes) else dump.encode()

    def deserialise(self, blob: bytes) -> dict:
        """
        Generic deserialiser interface
        """
        return self._generic_loads(blob)

    @property
    def codec(self) -> SerialiserType:
        """
        Return the serialiser currently in use for this table
        """
        return self._codec
