# -*- coding: utf-8 -*-

import SpikeGLX.sglx_pkg.sglx as sglx

# Edit the server address/port here
sglx_addr = "10.115.0.254"
sglx_port = 4142


def set_neuropixel_recording(enable=True):
    print("\nCalling connect...\n\n")
    hSglx = sglx.c_sglx_createHandle()

    # Using default loopback address and port
    if sglx.c_sglx_connect(hSglx, sglx_addr.encode(), sglx_port):
        print("version <{}>\n".format(sglx.c_sglx_getVersion(hSglx)))
    else:
        print("error [{}]\n".format(sglx.c_sglx_getError(hSglx)))

    result = sglx.c_sglx_setRecordingEnable(hSglx, enable)
    print(result)

    sglx.c_sglx_close(hSglx)
    sglx.c_sglx_destroyHandle(hSglx)
