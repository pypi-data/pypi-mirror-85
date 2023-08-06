"""Arithmetic Integer Functions."""
import numpy as _numpy

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps.policies


class SwapBytes:
    """SwapBytes Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.real_candidates[2:]

    def __init__(self, dtype=_numpy.int16, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "SwapBytes",
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.Policies(
                bytes1=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes2=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes4=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes8=numpy_ipps.policies.TagPolicy.UNSIGNED,
            ),
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
        )

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = src.ndarray.byteswap()


class SwapBytes_I:
    """SwapBytes_I Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.real_candidates[2:]

    def __init__(self, dtype=_numpy.int16, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "SwapBytes_I",
            (
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.Policies(
                bytes1=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes2=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes4=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes8=numpy_ipps.policies.TagPolicy.UNSIGNED,
            ),
        )

    def __call__(self, src_dst):
        numpy_ipps.status = self._ipps_backend(
            src_dst.cdata,
            src_dst.size,
        )

    def _numpy_backend(self, src_dst):
        src_dst.ndarray[:] = src_dst.ndarray.byteswap(True)


class Flip:
    """Flip Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.default_candidates

    def __init__(self, dtype=_numpy.int16, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Flip",
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.Policies(
                bytes1=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes2=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes4=numpy_ipps.policies.TagPolicy.FLOAT,
                bytes8=numpy_ipps.policies.TagPolicy.FLOAT,
            ),
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
        )

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _numpy.flip(src.ndarray)


class Flip_I:
    """Flip_I Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.default_candidates

    def __init__(self, dtype=_numpy.int16, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Flip_I",
            (
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.Policies(
                bytes1=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes2=numpy_ipps.policies.TagPolicy.UNSIGNED,
                bytes4=numpy_ipps.policies.TagPolicy.FLOAT,
                bytes8=numpy_ipps.policies.TagPolicy.FLOAT,
            ),
        )

    def __call__(self, src_dst):
        numpy_ipps.status = self._ipps_backend(
            src_dst.cdata,
            src_dst.size,
        )

    def _numpy_backend(self, src_dst):
        src_dst.ndarray[:] = _numpy.flip(src_dst.ndarray)
