# Copyright 2020 - 2020 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#

import logging
import ssl
import socket
from struct import *

from ._config import _ssl_auth_config, _logging_config, HOST, RPC_PORT, RPC_SERVICE, RPC_TIMEOUT, SSL_MODE, \
    CLIENT_AUTH_REQUIRED, SERVER_CERT, CLIENT_CERT, CLIENT_KEY, CHECK_HOSTNAME, LOG_UNIRPC_DEBUG
from ._errorcodes import ErrorCodes
from ._logger import get_logger
from ._uoerror import UOError

__all__ = ["UniRPCPacket", "UniRPCConnection"]

_logger = get_logger(__name__)

_RPC_VERSION = 2
_RPC_NO_ENCRYPTION = 0
_RPC_MAX_ARGS = 2048
_RPC_MAX_READ_SIZE = 10 * 1024 * 1024

_PACKET_MSG_HDR_FMT = '!BBHIIBBBBIHH'
_PACKET_MSG_DATA_FMT = '!II'
_PACKET_INT = 0
_PACKET_DOUBLE = 1
_PACKET_CHAR = 2
_PACKET_STRING = 3
_PACKET_INT_PTR = 4
_PACKET_DOUBLE_PTR = 5
_PACKET_FUNCNAME = 6
_PACKET_INT_LENGTH = 1
_PACKET_DOUBLE_LENGTH = 1
_PACKET_HEADER_SIZE = 24
_PACKET_HEADER_ARGS = 12
_PACKET_DEFAULT_PACKET_TYPE = 0
_PACKET_PATT_CHECK = 0x6c
_PACKET_UNCOMPRESSED = 0x00
_PACKET_COMPRESSED = 0x01


class _UniRPC(object):
    def __init__(self):
        self.version = _RPC_VERSION


class UniRPCConnection(_UniRPC):

    def __init__(self, config):
        super().__init__()

        self.config = config
        self.is_connected = False
        self.rpc_socket = None
        self.host = self.config[HOST]
        self.port = self.config[RPC_PORT]
        self.rpc_service = self.config[RPC_SERVICE]
        self.server_id = ""
        self.ssl_mode = self.config[SSL_MODE]
        self.timeout = self.config[RPC_TIMEOUT]

    def health_check(self):
        if not self.is_connected:
            return False;

        return self.rpc_socket.health_check()

    def call(self, in_packet, out_packet, encryption_type=_RPC_NO_ENCRYPTION):
        if self.is_connected:
            self._write_packet(out_packet, encryption_type)
            self._read_packet(in_packet)
        else:
            _logger.warn("connection has not been made.")
            raise UOError(ErrorCodes.UOE_RPC_NO_CONNECTION)

    def read_packet(self, in_packet):
        self._read_packet(in_packet)

    def close(self):
        if self.is_connected:
            self.rpc_socket.close()
            self.is_connected = False
        else:
            _logger.warn("connection has not been made or already closed.")

    def connect(self):
        if self.is_connected:
            _logger.warn("connection has already been made.")
            return

        self.rpc_socket = _UniRPCSocket(self.host, self.port, self.timeout)

        out_packet = UniRPCPacket()
        in_packet = UniRPCPacket()

        out_packet.write_char_array(0, self.rpc_service.encode('utf-8'))

        if self.ssl_mode:
            out_packet.write(1, 1)  # request ssl connection

        self._write_packet(out_packet, _RPC_NO_ENCRYPTION)
        self._read_packet(in_packet)

        if in_packet.get_argument_count() == 2:
            response = in_packet.read(1)
            self.server_id = in_packet.read(0)
        else:
            response = in_packet.read(0)

        if response == 0:
            self.is_connected = True
            if self.ssl_mode:
                self.rpc_socket.make_secure()
        else:
            raise UOError(response)

    def _write_packet(self, out_packet, encryption_type=_RPC_NO_ENCRYPTION):
        out_packet.send(self.rpc_socket, encryption_type)

    def _read_packet(self, in_packet):
        in_packet.reset()
        in_packet.receive(self.rpc_socket)


class _UniRPCSocket(object):
    """
    UniRPCSocket is the TCP/IP socket wrapper class for the uopython.unirpc package.
    The primary purpose of this class is to provide an abstraction layer around the
    socket class so we can implement reference counts and using different types of
    socket objects in the future.
    Although we currently derive from the Socket class, if we start using more than
    one type of socket we will have to go to a different model such as deriving from
    Object and having a socket instance maintained within the class.
    """

    def __init__(self, host, port, timeout):
        try:
            self._socket = socket.create_connection((host, port), timeout)
            self.host = host
            self.port = port
            self.timeout = timeout
        except socket.gaierror as e:
            _logger.error(e)
            raise UOError(ErrorCodes.UOE_RPC_UNKNOWN_HOST) from e
        except Exception as e:
            _logger.error(e)
            raise UOError(ErrorCodes.UOE_RPC_FAILED) from e

    def health_check(self):
        try:
            self._socket.settimeout(0)
            self._socket.recv(1)
        except BlockingIOError:
            return True
        except ssl.SSLWantReadError:
            return True
        except Exception as e:
            _logger.error(e)
        finally:
            self._socket.settimeout(self.timeout)

        _logger.debug("Failed")
        return False

    def send(self, msg):
        try:
            self._socket.send(msg)
        except socket.timeout as e:
            _logger.error(e)
            raise UOError(ErrorCodes.UOE_RPC_TIMEOUT) from e
        except Exception as e:
            _logger.error(e)
            raise UOError(ErrorCodes.UOE_RPC_FAILED) from e

    def receive(self, buf_size):
        try:
            return self._socket.recv(buf_size)
        except socket.timeout as e:
            _logger.error(e)
            raise UOError(ErrorCodes.UOE_RPC_TIMEOUT) from e
        except Exception as e:
            _logger.error(e)
            raise UOError(ErrorCodes.UOE_RPC_FAILED) from e

    def close(self):
        try:
            self._socket.close()
        except Exception as e:
            _logger.error(e)
            raise UOError(ErrorCodes.UOE_RPC_FAILED) from e
        finally:
            self._socket = None

    def make_secure(self):
        server_cert = _ssl_auth_config[SERVER_CERT]
        try:
            if server_cert:
                context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
            else:
                context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

            context.check_hostname = _ssl_auth_config[CHECK_HOSTNAME]

            if _ssl_auth_config[CLIENT_AUTH_REQUIRED]:
                client_cert = _ssl_auth_config[CLIENT_CERT]
                client_key = _ssl_auth_config[CLIENT_KEY]
                context.load_cert_chain(certfile=client_cert, keyfile=client_key)

            self._socket = context.wrap_socket(self._socket,
                                               server_hostname=self.host if context.check_hostname else None)
        except Exception as e:
            _logger.error(e)
            raise UOError(ErrorCodes.UOE_RPC_FAILED) from e


def _get_dump_from_bytes(message, bytes_array):
    header_str = ""
    for count, a_byte in enumerate(bytes_array):
        header_str += '{:02x}'.format(a_byte) if (count == 0 or (count % 4) != 0) else " "

        if count != 0 and count % 32 == 0:
            header_str += "\n"

    return message + header_str


class UniRPCPacket(_UniRPC):

    def __init__(self):
        super().__init__()
        self.data_buffer = b''
        self.header_buffer = b''
        self.header_fields = _PACKET_HEADER_ARGS * [0]
        self.data_info = []
        self.data_fields = []
        self.data_buffer_compressed = None
        self.data_buffer_encrypted = None
        self.is_compressed = False
        self.is_encrypted = False
        self.data_length = 0
        self.argument_count = 0
        self.compression_threshold = 0
        self._reset_header()
        self._reset_data()

    def receive(self, rpc_socket):
        if rpc_socket is None:
            raise UOError(ErrorCodes.UOE_RPC_NO_CONNECTION)

        self.header_buffer = rpc_socket.receive(_PACKET_HEADER_SIZE)
        self._unpack_header()

        self.data_length = self.header_fields[3]
        self.argument_count = self.header_fields[10]

        self.data_buffer = bytearray(rpc_socket.receive(self.data_length))
        while len(self.data_buffer) < self.data_length:
            self.data_buffer.extend(rpc_socket.receive(self.data_length - len(self.data_buffer)))

        self._decompress()
        self._decrypt()

        if _logger.getEffectiveLevel() >= logging.DEBUG and _logging_config[LOG_UNIRPC_DEBUG]:
            self._dump()

    def send(self, rpc_socket, encryption_type=_RPC_NO_ENCRYPTION):
        if rpc_socket is None:
            raise UOError(ErrorCodes.UOE_RPC_NO_CONNECTION)

        if self.is_encrypted is False:
            self._encrypt(encryption_type)
            self.is_encrypted = True
        if self.is_compressed is False:
            self._compress()
            self.is_compressed = True

        self._pack_header()
        if _logger.getEffectiveLevel() >= logging.DEBUG and _logging_config[LOG_UNIRPC_DEBUG]:
            self._dump()

        rpc_socket.send(self.header_buffer)
        rpc_socket.send(self.data_buffer_compressed)

        self.is_encrypted = False
        self.is_compressed = False

    def get_data_length(self):
        return self.argument_count * 8 + self.data_length

    def read(self, index):
        if index >= self.argument_count:
            raise UOError(ErrorCodes.UOE_RPC_BAD_PARAMETER, 'The requested item does NOT exist.')
        return self.data_fields[index]

    def _check_index(self, index):
        if index == 0:
            self._reset_data()

        elif index != self.argument_count:
            raise UOError(ErrorCodes.UOE_RPC_ARG_COUNT, "All packet arguments must be inserted in order, "
                                                        "starting with zero.")

        elif index > _RPC_MAX_ARGS:
            raise UOError(ErrorCodes.UOE_RPC_ARG_COUNT,
                          "A maximum of " + str(_RPC_MAX_ARGS) + " packet arguments are supported.")

    def write(self, index, data_value):
        self._check_index(index)

        if isinstance(data_value, int):
            self.data_info.insert(index, (_PACKET_INT_LENGTH, _PACKET_INT))
            i_bytes_array = pack("!i", data_value)
            self.data_fields.insert(index, i_bytes_array)

        elif isinstance(data_value, bytes) or isinstance(data_value, bytearray):
            data_len = len(data_value)
            self.data_info.insert(index, (data_len, _PACKET_STRING))

            # align to integer boundary
            padding = ((data_len + 3) & ~3) - data_len
            tmp_bytes = data_value + b'\x00' * padding
            self.data_fields.insert(index, tmp_bytes)

        self.argument_count += 1
        index += 1

    def write_char_array(self, index, byte_array):
        self._check_index(index)

        s_len = len(byte_array)
        self.data_info.insert(index, (s_len, _PACKET_CHAR))

        # align to integer boundary
        padding = ((s_len + 1 + 3) & ~3) - s_len
        tmp_bytes = byte_array + b'\x00' * padding
        self.data_fields.insert(index, tmp_bytes)

        self.argument_count += 1

    def get_argument_count(self):
        self._unpack_header()
        self.argument_count = self.header_fields[10]
        return self.argument_count

    def reset(self):
        self._reset_header()
        self._reset_data()

    def _reset_data(self):
        self.data_length = 0
        self.argument_count = 0
        self.is_compressed = False
        self.is_encrypted = False
        self.data_fields = []
        self.data_info = []

    def _reset_header(self):
        self.header_fields = _PACKET_HEADER_ARGS * [0]
        self.header_fields[0] = _PACKET_PATT_CHECK
        self.header_fields[1] = self.version
        # 2: SeqNo
        # 3: Length
        self.header_fields[4] = _PACKET_DEFAULT_PACKET_TYPE  # Type
        self.header_fields[5] = _RPC_VERSION  # High Ver.
        self.header_fields[6] = _PACKET_UNCOMPRESSED  # C. Mask
        self.header_fields[7] = _RPC_NO_ENCRYPTION  # E. Mask
        # 7: Future
        # 8: Return Code
        # 9: Arg Count
        # 10: Proc Length

    def _decompress(self):
        pass

    def _compress(self):
        # no compression support at this time
        # we just transfer buffer references in both cases.
        if (self.compression_threshold > 0) and (self.get_data_length() > self.compression_threshold):
            self.data_buffer_compressed = self.data_buffer_encrypted
            self._write_header_length(len(self.data_buffer_compressed))
            self._write_compression_mask(_PACKET_COMPRESSED)
        else:
            self.data_buffer_compressed = self.data_buffer_encrypted
            self._write_header_length(len(self.data_buffer_compressed))
            self._write_compression_mask(_PACKET_UNCOMPRESSED)

    def _decrypt(self):
        self._unpack_data()

    def _encrypt(self, encryption_type=_RPC_NO_ENCRYPTION):
        self._pack_data()
        self.data_buffer_encrypted = self.data_buffer
        self._write_encryption_mask(encryption_type)
        self._write_argument_count(self.argument_count)

    def _unpack_header(self):
        self.header_fields = unpack(_PACKET_MSG_HDR_FMT, self.header_buffer)

    def _pack_header(self):
        self.header_buffer = pack(_PACKET_MSG_HDR_FMT, *self.header_fields)

    def _unpack_data(self):
        current_index = 0
        offset = 0
        arg_count = self.get_argument_count()

        if len(self.data_buffer) > 0:
            # build data_info array
            while current_index < arg_count:
                tmp_data = self.data_buffer[offset:]
                d_length, d_type = unpack(_PACKET_MSG_DATA_FMT, tmp_data[0:8])
                self.data_info.insert(current_index, (d_length, d_type))
                offset += 8
                current_index += 1

            # build data_fields array
            for d_length, d_type in self.data_info:
                tmp_data = self.data_buffer[offset:]
                if d_type == _PACKET_INT:
                    # convert byte to integer
                    value = unpack('!i', tmp_data[0:4])[0]
                    offset += 4

                elif d_type == _PACKET_INT_PTR:
                    value = unpack('!' + 'I' * d_length, *tmp_data)
                    offset += 4 * d_length

                elif d_type == _PACKET_DOUBLE:
                    # convert byte to double
                    value = unpack('!d', tmp_data[0:8])[0]
                    offset += 8

                elif d_type == _PACKET_DOUBLE_PTR:
                    value = unpack('!' + 'd' * d_length, *tmp_data)
                    offset += 8 * d_length

                elif (d_type == _PACKET_CHAR) or \
                        (d_type == _PACKET_FUNCNAME):
                    tmp_len = d_length + 1
                    tmp_len = (tmp_len + 3) & ~3
                    value = tmp_data[0:tmp_len]
                    offset += tmp_len

                elif d_type == _PACKET_STRING:
                    # convert byte to String
                    value = tmp_data[0:d_length]  # nls ??
                    offset += d_length
                    offset += ((d_length + 3) & ~3) - d_length

                else:
                    # convert byte to String
                    value = tmp_data[0:d_length]  # nls ??
                    offset += d_length
                    offset += ((d_length + 3) & ~3) - d_length

                self.data_fields.append(value)

    def _pack_data(self):
        # put together the data_buffer_encrypted
        self.data_buffer = b''
        data_index = 0
        tmp_data_info = b''
        tmp_data = b''
        while data_index < self.argument_count:
            tmp_buf = pack(_PACKET_MSG_DATA_FMT,
                           self.data_info[data_index][0],
                           self.data_info[data_index][1])
            tmp_data_info += tmp_buf
            tmp_data += self.data_fields[data_index]
            data_index += 1

        self.data_buffer = tmp_data_info + tmp_data

    def _write_encryption_mask(self, encryption_type=_RPC_NO_ENCRYPTION):
        self.header_fields[7] = encryption_type

    def _write_argument_count(self, current_argument_count):
        self.header_fields[10] = current_argument_count

    def _dump(self):
        type_dict = {
            0: "Int",
            1: "Double",
            2: "Char",
            3: "String",
            4: "IntPtr",
            5: "DoublePtr",
            6: "FuncName"
        }

        header_str = _get_dump_from_bytes("Header :", self.header_buffer)
        data_str = _get_dump_from_bytes("Data   :", self.data_buffer)

        parsed_header = "\n"
        parsed_header += "Version = {}\n".format(self.header_fields[1])
        parsed_header += "Sequence = {}\n".format(self.header_fields[2])
        parsed_header += "Length = {}\n".format(self.header_fields[3])
        parsed_header += "Packet type = {}\n".format(self.header_fields[4])
        parsed_header += "High Ver = {}\n".format(self.header_fields[5])
        parsed_header += "Compression Mask = {}\n".format(self.header_fields[6])
        parsed_header += "Encryption Mask = {}\n".format(self.header_fields[7])
        parsed_header += "Return Code = {}\n".format(self.header_fields[9])
        parsed_header += "Argument Count= {}\n".format(self.header_fields[10])
        parsed_header += "Proc Length = {}\n".format(self.header_fields[11])

        value = info_tuple = idx = None
        for idx, info_tuple in enumerate(self.data_info):
            value = self.data_fields[idx]
            if info_tuple[1] == _PACKET_CHAR or info_tuple[1] == _PACKET_STRING:
                try:
                    value = value.decode()
                except:
                    # codelist = [str(hex(ord(v))) for v in value]
                    code_list = [str(hex(v)) if type(v) is int else str(hex(ord(v))) for v in value]
                    value = "".join(code_list)

        if type(value) == str:
            try:
                value = value.encode()
                pass
            except:
                code_list = [str(hex(v)) if type(v) is int else str(hex(ord(v))) for v in value]
                value = "".join(code_list)
                pass

        parsed_header += "Arguments[{}] = {} type = {}({}) Length={}\n".format(idx, value, info_tuple[1],
                                                                               type_dict[info_tuple[1]], info_tuple[0])

        _logger.debug("\n{}\n{}\n{}".format(header_str, data_str, parsed_header))

    def _write_header_length(self, length):
        self.header_fields[3] = length

    def _write_compression_mask(self, mask):
        self.header_fields[6] = mask
