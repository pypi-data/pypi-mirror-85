# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

"""UniObjects for Python is a Python package from Rocket Software. It is a client API that allows Python applications
to access Rocket MV Databases over the network.

Specifically, it enables Python developers to:

    1) remotely connect to MV databases

    1) call BASIC catalogued subroutines

    2) run TCL commands

    3) read/write MV files

    4) handle MV dynamic arrays

    5) manage MV SELECT lists

    6) control MV transactions

Configuration:

    UOPY supports a list of configuration parameters. They are grouped into 4 categories: connection, pooling, logging,
    and ssl_auth. Internally all the configuration parameters are preset to default values deemed to work for a minimal
    UOPY application development environment. To override these default values, UOPY supports an external
    configuration file - 'uopy.ini', in which a user can specify different values for some or all of the parameters. In
    some cases, this enables users to change how the application behaves without having to make any code changes, such
    as turning connection pooling on and off or making all connections to the database secure.

    For example, on Windows 10 (US-English), the default parameter values are:

        connection: {'host': 'localhost', 'account': 'XDEMO', 'port': 31438, 'timeout': 300, 'service': 'defcs',
        'encoding': 'cp1252', 'ssl': False}

        pooling: {'pooling_on': False, 'min_pool_size': 1, 'max_pool_size': 10, 'max_wait_time': 30,
        'idle_remove_threshold': 300, 'idle_remove_interval': 300}

        logging: {'level': 'WARNING', 'format': 'standard', 'dir': './logs', 'file_name': 'uopy.log', 'max_size': 524288,
        'backup_count': 5, 'unirpc_debug': False, 'log_data_max_size': 1024}

        ssl_auth: {'client_auth_required': False, 'server_cert_file': '', 'client_cert_file': '', 'client_key_file': '',
        'check_hostname': False}

    If the uopy.ini file is present in the current working directory with the following settings:

        [connection]
        host = uv1211.rocketsoftware.com
        account = XDEMO
        port = 41438
        timeout = 100
        service = udcs
        ssl = True

        [ssl_auth]
        server_cert_file="c:\\temp\\desktop-ppdt4ds.crt"

        [pooling]
        pooling_on = True
        max_wait_time = 60
        idle_remove_threshold = 300
        idle_remove_interval = 300
        min_pool_size = 5
        max_pool_size = 15

        [logging]
        level = DEBUG
        backup_count = 10
        log_data_max_size = 256

    then when uopy is imported, it will combine uopy.ini with the internal default configuration, resulting in the
    actual runtime configuration (see the Examples below). Please note that most of these configuration values cannot
    be changed by the application at runtime, with the exception of the values in the connection category and the pool
    size values in the pooling category, which can be passed in with different values to uopy.connect().


Logging:

    UOPY uses a rotating log strategy which is configurable in uopy.ini as shown above.

    Specifically,
        level: the logging level, can be CRITICAL(50), ERROR(40), WARNING (30, default), INFO(20), DEBUG(10).

        format: can be standard or simple - the difference is that source code line no is provided in the standard format.

        dir: the directory where log files are stored.

        file_name: the log file name.

        max_size: the maximum size of a single log file.

        backup_count: the number of backup log files to rotate through.

        unirpc_debug: if set to True and the logging level is DEBUG, all UniRPC packets are dumped into the log files.

        log_data_max_size: the maximum length for any data logged when logging level is DEBUG - the default is 1k.
            For instance, if a subroutine parameter is a XML string greater than 1K in size, it will be truncated to 1K
            in the log file.


Constants:

    UV_SERVICE, UD_SERVICE, DEFAULT_SERVICE: standard service names for back-end UO servers.

    DATA_FILE, DICT_FILE: used when creating a File object to indicate which part of the file should be opened.

    LOCK_WAIT, LOCK_RETAIN, LOCK_EXCLUSIVE, LOCK_SHARED: locking behaviors when working with records of hashed files.

    EXEC_COMPLETE, EXEC_REPLY, EXEC_MORE_OUTPUT: Command execution status codes.

    AtVar: an enum of supported MV @variables.

    UOLocale(Enum): an enum of UniVerse locale definitions.

    DEFAULT_MARKS: a named tuple containing the default MV delimiters (marks).


Examples:

    >>> import uopy
    >>> uopy.config.connection
    {'host': 'uv1211.rocketsoftware.com', 'account': 'XDEMO', 'port': 41438, 'timeout': 100, 'service': 'udcs',
    'encoding': 'cp1252', 'ssl': True}

    >>> uopy.config.pooling
    {'pooling_on': True, 'min_pool_size': 5, 'max_pool_size': 15, 'max_wait_time': 60, 'idle_remove_threshold': 300,
    'idle_remove_interval': 300}

    >>> uopy.config.logging
    {'level': 'DEBUG', 'format': 'standard', 'dir': './logs', 'file_name': 'uopy.log', 'max_size': 524288,
    'backup_count': 10, 'unirpc_debug': False, 'log_data_max_size': 256}

    >>> uopy.config.ssl_auth
    {'client_auth_required': False, 'server_cert_file': 'c:\\temp\\desktop-ppdt4ds.crt', 'client_cert_file': '',
    'client_key_file': '', 'check_hostname': False}

    >>> with uopy.connect(user='test', password='test'):
    >>>     cmd = uopy.Command("LIST VOC")
    >>>     cmd.run()
    >>>     print(cmd.response[-20:])
    '68 records listed.\r\n'

"""

from ._uopy import connect, config, Session
from ._constants import *
from ._command import Command
from ._dynarray import DynArray
from ._uoerror import UOError
from ._sequentialfile import SequentialFile
from ._subroutine import Subroutine
from ._file import File
from ._dictionary import Dictionary
from ._list import List

__all__ = ['connect', 'config', 'Session', 'Command', 'DynArray', 'UOError', 'File', 'SequentialFile',
           'Dictionary', 'List', 'Subroutine']