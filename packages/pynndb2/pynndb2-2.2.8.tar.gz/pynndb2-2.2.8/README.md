![banner](docs/assets/images/pynndb-banner.png)

This is version 2 of the Python NoSQL database library, for more complete documentation
please visit https://pynndb.madpenguin.uk or browse around the source code in this
repository.

PyNNDB is a NoSQL Database library implemented in Python utilising the LMDB key-value storage store for back-end functionality. Although there might be an immediate perception that this idea might result in something that is a little "slow", it consists of a python layer backed by a powerful engine written in 'C', much like other popular Python database solutions and as a result generally compares favourably.

The idea of database logic coded in Python came about after many years of using both SQL and NoSQL databases with Python to write Cloud based microservices and coming across issued that were difficult to address with current main-stream solutions. Notably, it became apparent that the performance bottleneck in these applications ended up being in the Python layer between the application and the back-end database, a layer often added as a compatibility options to allow Python applications to access the database. This raised the question, "what if we pick a faster back-end, and make this Python layer a first-class component rather than an after-thought?"
![banner](docs/assets/images/pynndb.svg)

### Features

* NoSQL database library written in Python using the LMDB C-extension as a base KV store
* Primary ObjectId() based indexes for all objects
* Mutiple secondary indexes based on Python functions, supporting unique and duplicates
* Transparent compression / decompression (currently zStd and Snappy)
* Powerful and flexible search routines
* Designed to work in a multi-processor environment / multiprocessing IPC
* Inherits the features of LMDB including ACID transaction processing

### About the code

Version 2 is coded for Python 3.7+ and makes use of Python3's new "typing" module with a view to self-documentation. All of
the API documentation (and many of the examples) are documented automatically 100% from source code using the documentation
routes contained within this repository, for example;

![example](docs/assets/images/docs-example.png)

If you have problems or spot any bugs, please feel free to log an issue on the [Bug Tracker](https://gitlab.com/oddjobz/pynndb2/-/issues) or alternatively
connect on [Keybase](https://keybase.io/garethbult)