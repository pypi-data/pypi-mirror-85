"""Vector Initialization Functions."""
import enum as _enum

import numpy as _numpy

import numpy_ipps._detail.debug as _debug
import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps.policies
import numpy_ipps.support
import numpy_ipps.utils


_init_policies = numpy_ipps.policies.Policies(
    bytes1=numpy_ipps.policies.TagPolicy.UNSIGNED,
    bytes2=numpy_ipps.policies.TagPolicy.SIGNED,
    bytes4=numpy_ipps.policies.TagPolicy.INTEGER_SIGNED,
    bytes8=numpy_ipps.policies.TagPolicy.INTEGER_SIGNED,
)


class Assign:
    """Assign Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.default_candidates

    def __init__(self, dtype=float, overlap=False):
        if overlap:
            self._ipps_backend = _dispatch.ipps_function(
                "Move",
                ("void*", "void*", "int"),
                dtype,
                policies=_init_policies,
            )
        else:
            self._ipps_backend = _dispatch.ipps_function(
                "Copy",
                ("void*", "void*", "int"),
                dtype,
                policies=_init_policies,
            )

    def __call__(self, src, dst):
        assert (
            src.ndarray.size == dst.ndarray.size
        ), "src and dst size not compatible."

        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
        )

    def _numpy_backend(self, src, dst):
        assert (
            src.ndarray.size == dst.ndarray.size
        ), "src and dst size not compatible."

        _numpy.copyto(dst.ndarray, src.ndarray)


class Endian(_enum.Enum):
    """Endianess Enum."""

    LITTLE = 1
    BIG = 2


class BitShift:
    """BitShift Function."""

    __slots__ = ("_ipps_backend", "src_bit_offset", "dst_bit_offset")
    _ipps_candidates = (_numpy.uint8,)

    def __init__(
        self,
        src_bit_offset=0,
        dst_bit_offset=0,
        endian=Endian.LITTLE,
    ):
        self.src_bit_offset = numpy_ipps.utils.cast("int", src_bit_offset)
        self.dst_bit_offset = numpy_ipps.utils.cast("int", dst_bit_offset)

        if endian == Endian.LITTLE:
            self._ipps_backend = _dispatch.ipps_function(
                "CopyLE_1u",
                ("void*", "int", "void*", "int", "int"),
                policies=_init_policies,
            )
        elif endian == Endian.BIG:
            self._ipps_backend = _dispatch.ipps_function(
                "CopyBE_1u",
                ("void*", "int", "void*", "int", "int"),
                policies=_init_policies,
            )
        else:
            _debug.log_and_raise(
                RuntimeError,
                "Unknown endianess: {}".format(endian),
                name=__name__,
            )

    def __call__(self, src, dst, size):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            self.src_bit_offset,
            dst.cdata,
            self.dst_bit_offset,
            size,
        )

    def _numpy_backend(self, src, dst):
        raise NotImplementedError


class _SetToIPPSImpl:
    """SetTo Function -- Intel IPPS implementation."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.default_candidates

    def __init__(self, dtype=float, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Set",
            (
                _dispatch.as_ctype_str(dtype, policies=_init_policies),
                "void*",
                "int",
            ),
            dtype,
            policies=_init_policies,
        )

    def __call__(self, src, value):
        numpy_ipps.status = self._ipps_backend(value, src.cdata, src.size)

    def _numpy_backend(self, src, value):
        src.ndarray[:] = value


class _SetToNumpyImpl:
    """SetTo Function -- Numpy implementation."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.default_candidates

    def __init__(self, dtype=float, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            "Set",
            (
                _dispatch.as_ctype_str(dtype, policies=_init_policies),
                "void*",
                "int",
            ),
            dtype,
            policies=_init_policies,
        )

    def __call__(self, src, value):
        src.ndarray[:] = value

    def _numpy_backend(self, src, value):
        src.ndarray[:] = value


def SetTo(size, dtype=float):
    """SetTo Function."""
    return (
        _SetToIPPSImpl(dtype=dtype, size=None)
        if size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (2, 4)
        else _SetToNumpyImpl(dtype=dtype, size=None)
    )


SetTo._ipps_candidates = _SetToIPPSImpl._ipps_candidates


class Zeros:
    """Zeros Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.default_candidates

    def __init__(self, dtype=float):
        self._ipps_backend = _dispatch.ipps_function(
            "Zero", ("void*", "int"), dtype, policies=_init_policies
        )

    def __call__(self, src):
        numpy_ipps.status = self._ipps_backend(src.cdata, src.size)

    def _numpy_backend(self, src):
        src.ndarray[:] = 0
