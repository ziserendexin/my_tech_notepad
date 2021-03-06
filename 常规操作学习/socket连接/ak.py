# -*- coding: utf-8 -*-

from __future__ import absolute_import

import binascii
import logging
import socket
import struct

logger = logging.getLogger('ak')

STX = 0x02
ETX = 0x03
BLANK = 0x20
K = ord('K')

AK_CONNECTED = 1
AK_DISCONNECTED = 0


class AKClient(object):
    """ AK Client """

    def __init__(self, conf):
        """ init """

        self.conf = conf

        self.host = conf["host"]
        self.port = conf["port"]
        self.timeout = conf["timeout"]
        self.allowed_cmds = set()

        for item in conf["allowed_cmds"]:
            self.allowed_cmds.add(item.upper())

        logger.debug(self.allowed_cmds)

        self.status = AK_DISCONNECTED
        self.error_msg = None

    def connect(self):
        """ connect """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.settimeout(self.timeout)

        try:

            self.sock.connect((self.host, self.port))
            self.status = AK_CONNECTED
        except:
            self.status = AK_DISCONNECTED

    def __del__(self):
        """   """

        logger.debug("__del__")
        self.sock.close()

    def _send(self, buf):
        """ send """

        try:
            self.sock.sendall(buf)
        except Exception as ex:
            # logger.debug(ex)
            self.error_msg = ex.message
            raise (Exception(ex))

    def _recv(self):
        """ recv """

        try:
            data = self.sock.recv(1024)

        except Exception as ex:
            logger.debug(ex)
            self.error_msg = ex.message
            raise (Exception(ex))
        return data

    def validate(self, cmd):
        """   """

        if cmd in self.allowed_cmds:
            return True
        else:
            return False

    def query(self, cmd):
        """ query """

        # channel number for build struct
        channel_number = 0

        data = {}

        # cmds_set = set()

        # for cmd in cmds:

        cmd = cmd.upper()

        if True:  # self.validate(cmd):
            # cmds_set.add(cmd)
            # pass

            # continue

            # logger.debug(cmds_set)

            msg = self.pack(cmd, channel_number)

            # print "------ ak.py-msg--- %s" % (msg)
            self._send(msg)

            data_recv = self._recv()
            # print "------ ak.py-data_recv--- %s" % (data_recv)
            out = self.unpack(data_recv)
            # print(len(out))

            if len(out) > 6:
                data[cmd] = out[6]
            else:
                data[cmd] = cmd

            return data

        else:
            logger.warning("not allowed:[%s]" % cmd)
            return {}

    def query_all(self, cmds):
        """ query """

        # channel number for build struct
        channel_number = 0

        data = {}

        cmds_set = set()

        for cmd in cmds:

            cmd = cmd.upper()

            if self.validate(cmd):
                cmds_set.add(cmd)
            else:
                logger.warning("not allowed:[%s]" % cmd)
                continue

        logger.debug(cmds_set)

        for cmd in cmds_set:

            msg = self.pack(cmd, channel_number)

            self._send(msg)

            data_recv = self._recv()
            # print(data_recv)
            out = self.unpack(data_recv)
            # print(len(out))

            if len(out) > 6:
                data[cmd] = out[6]
            else:
                data[cmd] = cmd

        return data

    def pack(self, cmd, channel_number, code=None):
        """ AK command pack """

        # cmd = "AVFI"
        # print(channel_number, cmd, code)
        # cmd = cmd.upper()

        if cmd.count('AFLT') == 1:
            """ The dyno will return the fault text within double quotes (102 characters max data.)
                If the fault number is not found, just the two double quotes will be returned.
            """
            code = cmd.split(" ")[1]
            if code is None:
                raise (Exception("The fault number must be specified with the AFLT request."))

            else:

                clen = len(cmd)

                # AK Command telegram
                fmt = "!2b%ds5b" % clen
                # print fmt
                # channel_number = 0

                buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, K, channel_number, BLANK, ETX)
                # logger.debug(buf)
                return buf

        else:

            clen = len(cmd)

            # AK Command telegram
            fmt = "!2b%ds5b" % clen
            # print fmt
            # channel_number = 0

            buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, K, channel_number, BLANK, ETX)
            # logger.debug(buf)
            return buf

    def unpack(self, data):
        """ AK unpack """

        dlen = len(data) - 10

        if dlen < 0:
            # raise Exception("struct error")
            fmt = "!2b4s3b"

        else:
            # AK Response telegram !2b4s4b%ds1d
            fmt = "!2b4s3b%ds1b" % dlen

        try:
            val = struct.unpack(fmt, data)

            # print(type(val))
            # tuple
            logger.debug(val)
            return val
        except Exception as ex:
            # logger.error(ex.message)
            b64 = binascii.b2a_base64(data)
            logger.error(b64)
            return {"error": ex.message, "base64": b64}
            # raise Exception("unpack exception")
