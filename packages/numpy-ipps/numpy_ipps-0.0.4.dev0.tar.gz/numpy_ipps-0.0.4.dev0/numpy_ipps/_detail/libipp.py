import os
import sys

import cffi


ffi = cffi.FFI()

if sys.platform.startswith("win32"):
    ipp_signal = ffi.dlopen("ipps.dll")
elif sys.platform.startswith("darwin"):
    ipp_signal = ffi.dlopen("libipps.dylib")
else:
    try:
        ipp_signal = ffi.dlopen("libipps.so")
    except OSError:
        _base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib"
        )
        ffi.dlopen(os.path.join(_base_path, "libippcore.so"))
        for lib in os.listdir(_base_path):
            ffi.dlopen(os.path.join(_base_path, lib))
        ipp_signal = ffi.dlopen(os.path.join(_base_path, "libipps.so"))

if not hasattr(ffi, "ippInit"):
    ffi.cdef("int ippInit();")
