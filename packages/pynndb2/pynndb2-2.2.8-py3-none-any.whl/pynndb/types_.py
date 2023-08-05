#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from typing import Any, Mapping, TypeVar, Collection

Config = Mapping[str, Any]
OID = TypeVar('OID', str, bytes)
OIDS = Collection[OID]
