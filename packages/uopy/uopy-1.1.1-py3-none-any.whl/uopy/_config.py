# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

import configparser
import copy
import locale
import os

from ._constants import DEFAULT_SERVICE

_CONFIG_FILE_NAME = "uopy.ini"

CONFIG_CONNECTION = "connection"
CONFIG_SSL_AUTH = 'ssl_auth'
CONFIG_POOLING = "pooling"
CONFIG_LOGGING = "logging"

# Connection Section
HOST = "host"
RPC_PORT = "port"
USER = "user"
PASSWORD = "password"
ACCOUNT = "account"
RPC_SERVICE = "service"
RPC_TIMEOUT = "timeout"
ENCODING = 'encoding'
SSL_MODE = "ssl"

# Security Section
CLIENT_AUTH_REQUIRED = 'client_auth_required'
SERVER_CERT = "server_cert_file"
CLIENT_CERT = "client_cert_file"
CLIENT_KEY = 'client_key_file'
CHECK_HOSTNAME = "check_hostname"

# Pooling Section
POOLING_ON = "pooling_on"
MIN_POOL_SIZE = "min_pool_size"
MAX_POOL_SIZE = "max_pool_size"
MAX_WAIT_TIME = "max_wait_time"
IDLE_REMOVE_THRESHOLD = "idle_remove_threshold"
IDLE_REMOVE_INTERVAL = "idle_remove_interval"

# Logging Section
LOG_LEVEL = 'level'
LOG_FORMAT = 'format'
LOG_FILE_MAXSIZE = 'max_size'
LOG_BACKUP_COUNT = 'backup_count'
LOG_DIR = 'dir'
LOG_FILE_NAME = 'file_name'
LOG_UNIRPC_DEBUG = "unirpc_debug"
LOG_DATA_MAXSIZE = "log_data_max_size"

_DEFAULT_CONFIG = {
    CONFIG_CONNECTION: {
        HOST: 'localhost',
        ACCOUNT: 'XDEMO',
        RPC_PORT: 31438,
        RPC_TIMEOUT: 300,
        RPC_SERVICE: DEFAULT_SERVICE,
        ENCODING: locale.getpreferredencoding(),
        SSL_MODE: False,
    },

    CONFIG_SSL_AUTH: {
        CLIENT_AUTH_REQUIRED: False,
        SERVER_CERT: '',
        CLIENT_CERT: '',
        CLIENT_KEY: '',
        CHECK_HOSTNAME: False
    },

    CONFIG_POOLING: {
        POOLING_ON: False,
        MIN_POOL_SIZE: 1,
        MAX_POOL_SIZE: 10,
        MAX_WAIT_TIME: 30,
        IDLE_REMOVE_THRESHOLD: 300,
        IDLE_REMOVE_INTERVAL: 300,
    },

    CONFIG_LOGGING: {
        LOG_LEVEL: 'WARNING',
        LOG_FORMAT: 'standard',
        LOG_DIR: './logs',
        LOG_FILE_NAME: 'uopy.log',
        LOG_FILE_MAXSIZE: 1024 * 512,
        LOG_BACKUP_COUNT: 5,
        LOG_UNIRPC_DEBUG: False,
        LOG_DATA_MAXSIZE: 1024
    }
}


def _eval_config(config):
    import ast
    for k in config:
        v = config[k]
        try:
            v = ast.literal_eval(v)
            config[k] = v
        except:
            pass
    return config


_default_cfg = configparser.ConfigParser()
_default_cfg.read_dict(_DEFAULT_CONFIG)
config_path = os.path.join(os.getcwd(), _CONFIG_FILE_NAME)
_default_cfg.read(config_path)

_connection_config = _eval_config(dict(_default_cfg.items(CONFIG_CONNECTION)))
_pooling_config = _eval_config(dict(_default_cfg.items(CONFIG_POOLING)))
_ssl_auth_config = _eval_config(dict(_default_cfg.items(CONFIG_SSL_AUTH)))
_logging_config = _eval_config(dict(_default_cfg.items(CONFIG_LOGGING)))


class _Config:
    """ A configuration object for UOPY that combines system default settings with ones defined in uopy.ini.

        Properties:
            connection: database connection parameters
            pooling: connection pooling parameters.
            ssl_auth: secure connection parameters
            logging: client side logging parameters
    """

    def __init__(self):
        pass

    @property
    def connection(self):
        return copy.deepcopy(_connection_config)

    @property
    def pooling(self):
        return copy.deepcopy(_pooling_config)

    @property
    def ssl_auth(self):
        return copy.deepcopy(_ssl_auth_config)

    @property
    def logging(self):
        return copy.deepcopy(_logging_config)


config = _Config()
