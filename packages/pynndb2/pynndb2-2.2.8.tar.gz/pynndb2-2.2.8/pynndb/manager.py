"""
    _    ____ ___   ____
   / \\  |  _ \\_ _| |  _ \\  ___   ___ ___
  / _ \\ | |_) | |  | | | |/ _ \\ / __/ __|
 / ___ \\|  __/| |  | |_| | (_) | (__\\__ \\
/_/   \\_\\_|  |___| |____/ \\___/ \\___|___/

Copyright &copy;2020 - Mad Penguin Consulting Limited
"""
from atexit import register
from collections import UserDict
from typing import Optional
from pynndb.database import Database
from pynndb.types_ import Config


class Manager(UserDict):
    """
    Manager is a dictionary like object the holds references to all the databases currently
    registered with the running instance. If you only ever reference one database then
    technically you can skip this object and just use the Database object.
    """

    def __init__(self, *args, **kwargs):
        self._paths = {}
        super().__init__(*args, **kwargs)
        register(self.exit_handler)

    def exit_handler(self):          # pragma: no cover
        for name in self.data:       # pragma: no cover
            self.data[name].close()  # pragma: no cover

    def __getitem__(self, name: str) -> Database:
        """
        Get a reference to an already open database

        name - the name of database

        Returns the Database object associated with the supplied name
        """
        if name not in self.data:
            self.data[name] = Database()
        return self.data[name]

    def database(self, name: str, path: Optional[str]=None, config: Optional[Config]=None) -> Database:
        """
        Open a database creating it if necessary

        name - an arbitrary name to reference the database by
        path - the path to the database files
        config - a dictionary containing configuration specifics for this database

        Returns a reference to an open Database
        """
        if name in self.data:
            database = self.data[name]
            if not database.isopen:
                database.open(database._path)
            return database
        if name and not path:
            path = name
            name = None
            if path in self._paths:
                return self._paths[path]
        database = Database()
        if config:
            database.configure(config)
        database.open(path)
        if not name:
            name = database.replication.uuid
        self.data[name] = database
        self._paths[path] = database
        return database
