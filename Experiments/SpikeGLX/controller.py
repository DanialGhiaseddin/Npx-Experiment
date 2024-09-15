# -*- coding: utf-8 -*-

import SpikeGLX.sglx_pkg.sglx as sglx
from ctypes import byref, POINTER, c_int, c_short, c_bool, c_char_p


class SpikeGLXHandler:
    def __init__(self, logger, ip_addr="10.115.0.254", port=4142):

        self.sglx_addr = ip_addr
        self.sglx_port = port

        self.logger = logger

        self.hSglx = sglx.c_sglx_createHandle()

    def connect(self):

        if sglx.c_sglx_connect(self.hSglx, self.sglx_addr.encode(), self.sglx_port):
            self.logger.info("SpikeGLX Successful connection version <{}>\n".format(sglx.c_sglx_getVersion(self.hSglx)))
        else:
            self.logger.error("SpikeGLX Connection Failed [{}]\n".format(sglx.c_sglx_getError(self.hSglx)))

    def bool_test(self):

        hid = c_bool()
        ok = sglx.c_sglx_isConsoleHidden(byref(hid), self.hSglx)

    def start_recording(self):
        return sglx.c_sglx_setRecordingEnable(self.hSglx, True)

    def stop_recording(self):
        return sglx.c_sglx_setRecordingEnable(self.hSglx, False)

    def close(self):
        sglx.c_sglx_close(self.hSglx)

    def destroy(self):
        sglx.c_sglx_destroyHandle(self.hSglx)

    def __del__(self):
        self.destroy()

# Edit the server address/port here

#
# def set_neuropixel_recording(enable=True):
#     print("\nCalling connect...\n\n")
#     hSglx = sglx.c_sglx_createHandle()
#
#     # Using default loopback address and port
#     if sglx.c_sglx_connect(hSglx, sglx_addr.encode(), sglx_port):
#         print("version <{}>\n".format(sglx.c_sglx_getVersion(hSglx)))
#     else:
#         print("error [{}]\n".format(sglx.c_sglx_getError(hSglx)))
#
#     result = sglx.c_sglx_setRecordingEnable(hSglx, enable)
#     print(result)
#
#     sglx.c_sglx_close(hSglx)
#     sglx.c_sglx_destroyHandle(hSglx)
