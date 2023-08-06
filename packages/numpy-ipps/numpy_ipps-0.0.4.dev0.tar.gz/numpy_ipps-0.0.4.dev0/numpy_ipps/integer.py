"""Arithmetic Integer Functions."""
import enum as _enum

import numpy as _numpy

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.support
import numpy_ipps.utils


_binaryInt_candidates = (
    _numpy.uint8,
    _numpy.int16,
    _numpy.uint16,
    _numpy.int32,
)
_unarySignedInt_candidates = (_numpy.int16, _numpy.int32)
_unaryUnsignedInt_candidates = (_numpy.uint8, _numpy.int16, _numpy.uint16)


class Polarity(_enum.Enum):
    """Polarity enumeration."""

    NORMAL = 1
    REVERSE = 2


class AddInteger(
    metaclass=_binaries.Binary,
    ipps_backend="Add",
    numpy_backend=_numpy.add,
    policies=numpy_ipps.policies.Policies(
        bytes1=numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
        bytes4=numpy_ipps.policies.TagPolicy.INTEGER_UNSIGNED,
        bytes8=numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
    ),
    candidates=(
        _numpy.int8,
        _numpy.uint8,
        _numpy.int16,
        _numpy.uint16,
        _numpy.int32,
        _numpy.uint32,
    ),
):
    """Add Function."""

    pass


class AddInteger_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Add_I",
    numpy_backend=_numpy.add,
    policies=numpy_ipps.policies.Policies(
        bytes1=numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
        bytes2=numpy_ipps.policies.TagPolicy.SIGNED,
        bytes4=numpy_ipps.policies.TagPolicy.INTEGER_UNSIGNED,
    ),
    candidates=(
        _numpy.int8,
        _numpy.uint8,
        _numpy.int16,
        _numpy.uint16,
        _numpy.int32,
        _numpy.uint32,
    ),
):
    """Add_I Function."""

    pass


class _AddIntegerCIPPSImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="AddC",
    numpy_backend=_numpy.add,
    policies=numpy_ipps.policies.Policies(
        bytes1=numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
        bytes2=numpy_ipps.policies.TagPolicy.SCALE_KEEP,
        bytes4=numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
        bytes8=numpy_ipps.policies.TagPolicy.SCALE_KEEP,
    ),
    candidates=numpy_ipps.policies.int_candidates,
):
    """AddC Function -- Intel IPPS implementation."""

    pass


class _AddIntegerCNumpyImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="AddC",
    numpy_backend=_numpy.add,
    policies=numpy_ipps.policies.Policies(
        bytes1=numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
        bytes2=numpy_ipps.policies.TagPolicy.SCALE_KEEP,
        bytes4=numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
        bytes8=numpy_ipps.policies.TagPolicy.SCALE_KEEP,
    ),
    candidates=numpy_ipps.policies.int_candidates,
    force_numpy=True,
):
    """AddC Function -- Numpy implementation."""

    pass


def AddIntegerC(size, dtype=_numpy.uint32):
    """AddC Function."""
    return (
        _AddIntegerCIPPSImpl(dtype=dtype, size=size)
        if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (4, 8)
        else _AddIntegerCNumpyImpl(dtype=dtype, size=size)
    )


AddIntegerC._ipps_candidates = _AddIntegerCIPPSImpl._ipps_candidates


class _AddIntegerCIIPPSImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="AddC_I",
    numpy_backend=_numpy.add,
    policies=numpy_ipps.policies.Policies(
        bytes1=numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
        bytes2=numpy_ipps.policies.TagPolicy.SCALE_KEEP,
        bytes4=numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
    ),
    candidates=(
        _numpy.int8,
        _numpy.uint8,
        _numpy.int16,
        _numpy.uint16,
        _numpy.int32,
        _numpy.uint32,
    ),
):
    """AddC_I Function -- Intel IPPS implementation."""

    pass


class _AddIntegerCINumpyImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="AddC_I",
    numpy_backend=_numpy.add,
    policies=numpy_ipps.policies.Policies(
        bytes1=numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
        bytes2=numpy_ipps.policies.TagPolicy.SCALE_KEEP,
        bytes4=numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
    ),
    candidates=(
        _numpy.int8,
        _numpy.uint8,
        _numpy.int16,
        _numpy.uint16,
        _numpy.int32,
        _numpy.uint32,
    ),
    force_numpy=True,
):
    """AddC_I Function -- Numpy implementation."""

    pass


def AddIntegerC_I(size, dtype=_numpy.uint32):
    """AddC_I Function."""
    return (
        _AddIntegerCIIPPSImpl(dtype=dtype, size=size)
        if size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (4,)
        else _AddIntegerCINumpyImpl(dtype=dtype, size=size)
    )


AddIntegerC_I._ipps_candidates = _AddIntegerCIIPPSImpl._ipps_candidates


class _MulIntegerIPPSImpl(
    metaclass=_binaries.Binary,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
):
    """Mul Function -- Intel IPPS implementation."""

    pass


class _MulIntegerNumpyImpl(
    metaclass=_binaries.Binary,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    force_numpy=True,
):
    """Mul Function -- Numpy implementation."""

    pass


def MulInteger(size, dtype=_numpy.int32):
    """Mul Function."""
    return (
        _MulIntegerIPPSImpl(dtype=dtype, size=size)
        if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (2, 4)
        else _MulIntegerNumpyImpl(dtype=dtype, size=size)
    )


MulInteger._ipps_candidates = _MulIntegerIPPSImpl._ipps_candidates


class _MulIntegerIIPPSImpl(
    metaclass=_binaries.Binary_I,
    ipps_backend="Mul_I",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
):
    """Mul_I Function -- Intel IPPS implementation."""

    pass


class _MulIntegerINumpyImpl(
    metaclass=_binaries.Binary_I,
    ipps_backend="Mul_I",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    force_numpy=True,
):
    """Mul_I Function -- Numpy implementation."""

    pass


def MulInteger_I(size, dtype=_numpy.int32):
    """Mul Function."""
    return (
        _MulIntegerIIPPSImpl(dtype=dtype, size=size)
        if size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (2, 4)
        else _MulIntegerINumpyImpl(dtype=dtype, size=size)
    )


MulInteger_I._ipps_candidates = _MulIntegerIIPPSImpl._ipps_candidates


class MulIntegerC(
    metaclass=_binaries.BinaryC,
    ipps_backend="MulC",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
):
    """MulC Function."""

    pass


class MulIntegerC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="MulC_I",
    numpy_backend=_numpy.multiply,
    policies=numpy_ipps.policies.scaled_all,
    candidates=(
        _numpy.uint8,
        _numpy.int16,
        _numpy.uint16,
        _numpy.int32,
        _numpy.int64,
    ),
):
    """MulC_I Function."""

    pass


class SubInteger(
    metaclass=_binaries.Binary,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
):
    """Sub Function."""

    pass


class SubInteger_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Sub_I",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
):
    """Sub_I Function."""

    pass


class _SubIntegerCIPPSImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="SubC",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
):
    """SubC Function -- Intel IPPS implementation."""

    pass


class _SubIntegerCNumpyImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="SubC",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    force_numpy=True,
):
    """SubC Function -- Numpy implementation."""

    pass


class _SubIntegerCIIPPSImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="SubC_I",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
):
    """SubC_I Function -- Intel IPPS implementation."""

    pass


class _SubIntegerCINumpyImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="SubC_I",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    force_numpy=True,
):
    """SubC_I Function -- Numpy implementation."""

    pass


class _SubIntegerCRevIPPSImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="SubCRev",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
):
    """SubCRev Function -- Intel IPPS implementation."""

    pass


class _SubIntegerCRevNumpyImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="SubCRev",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
    force_numpy=True,
):
    """SubCRev Function -- Numpy implementation."""

    pass


class _SubIntegerCRevIIPPSImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="SubCRev_I",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
):
    """SubCRev_I Function -- Intel IPPS implementation."""

    pass


class _SubIntegerCRevINumpyImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="SubCRev_I",
    numpy_backend=_numpy.subtract,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
    force_numpy=True,
):
    """SubCRev_I Function -- Numpy implementation."""

    pass


def SubIntegerC(size, dtype=_numpy.int32, polarity=Polarity.NORMAL):
    """SubC Function."""
    if polarity is Polarity.NORMAL:
        return (
            _SubIntegerCIPPSImpl(dtype=dtype, size=size)
            if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
            or _numpy.dtype(dtype).itemsize not in (4,)
            else _SubIntegerCNumpyImpl(dtype=dtype, size=size)
        )
    elif polarity is Polarity.REVERSE:
        return (
            _SubIntegerCRevIPPSImpl(dtype=dtype, size=size)
            if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
            or _numpy.dtype(dtype).itemsize not in (4,)
            else _SubIntegerCRevNumpyImpl(dtype=dtype, size=size)
        )
    else:
        raise RuntimeError("Unknown polarity.")


SubIntegerC._ipps_candidates = _SubIntegerCIPPSImpl._ipps_candidates


def SubIntegerC_I(size, dtype=_numpy.int32, polarity=Polarity.NORMAL):
    """SubC_I Function."""
    if polarity is Polarity.NORMAL:
        return (
            _SubIntegerCIIPPSImpl(dtype=dtype, size=size)
            if size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
            or _numpy.dtype(dtype).itemsize not in (4,)
            else _SubIntegerCINumpyImpl(dtype=dtype, size=size)
        )
    elif polarity is Polarity.REVERSE:
        return (
            _SubIntegerCRevIIPPSImpl(dtype=dtype, size=size)
            if size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
            or _numpy.dtype(dtype).itemsize not in (4,)
            else _SubIntegerCRevINumpyImpl(dtype=dtype, size=size)
        )
    else:
        raise RuntimeError("Unknown polarity.")


SubIntegerC_I._ipps_candidates = _SubIntegerCIIPPSImpl._ipps_candidates


class DivInteger(
    metaclass=_binaries.Binary,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
):
    """Div Function."""

    pass


class _DivIntegerIIPPSImpl(
    metaclass=_binaries.Binary_I,
    ipps_backend="Div_I",
    numpy_backend=_numpy.divide,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
):
    """Div_I Function -- Intel IPPS implementation."""

    pass


class _DivIntegerINumpyImpl(
    metaclass=_binaries.Binary_I,
    ipps_backend="Div_I",
    numpy_backend=_numpy.divide,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_binaryInt_candidates,
    numpy_swap=True,
    force_numpy=True,
):
    """Div_I Function -- Numpy implementation."""

    pass


def DivInteger_I(size, dtype=_numpy.int32):
    """DivC_I Function."""
    return (
        _DivIntegerIIPPSImpl(dtype=dtype, size=size)
        if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (4,)
        else _DivIntegerINumpyImpl(dtype=dtype, size=size)
    )


DivInteger_I._ipps_candidates = _DivIntegerIIPPSImpl._ipps_candidates


class _DivIntegerCIPPSImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="DivC",
    numpy_backend=_numpy.divide,
    policies=numpy_ipps.policies.scaled_all,
    candidates=(
        _numpy.uint8,
        _numpy.int16,
        _numpy.uint16,
    ),
):
    """DivC Function -- Intel IPPS implementation."""

    pass


class _DivIntegerCIIPPSImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="DivC_I",
    numpy_backend=_numpy.divide,
    policies=numpy_ipps.policies.scaled_all,
    candidates=(
        _numpy.uint8,
        _numpy.int16,
        _numpy.uint16,
        _numpy.int64,
    ),
):
    """DivC_I Function -- Intel IPPS implementation."""

    pass


class _DivIntegerCRevIPPSImpl(
    metaclass=_binaries.BinaryC,
    ipps_backend="DivCRev",
    numpy_backend=_numpy.divide,
    candidates=(_numpy.uint16,),
    numpy_swap=True,
):
    """DivCRev Function -- Intel IPPS implementation."""

    pass


class _DivIntegerCRevIIPPSImpl(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="DivCRev_I",
    numpy_backend=_numpy.divide,
    candidates=(_numpy.uint16,),
    numpy_swap=True,
):
    """DivCRev_I Function -- Intel IPPS implementation."""

    pass


def DivIntegerC(size, dtype=_numpy.uint16, polarity=Polarity.NORMAL):
    """DivC Function."""
    if polarity is Polarity.NORMAL:
        return _DivIntegerCIPPSImpl(dtype=dtype, size=size)
    elif polarity is Polarity.REVERSE:
        return _DivIntegerCRevIPPSImpl(dtype=dtype, size=size)
    else:
        raise RuntimeError("Unknown polarity.")


DivIntegerC._ipps_candidates = _DivIntegerCIPPSImpl._ipps_candidates


def DivIntegerC_I(size, dtype=_numpy.uint16, polarity=Polarity.NORMAL):
    """DivC_I Function."""
    if polarity is Polarity.NORMAL:
        return _DivIntegerCIIPPSImpl(dtype=dtype, size=size)
    elif polarity is Polarity.REVERSE:
        return _DivIntegerCRevIIPPSImpl(dtype=dtype, size=size)
    else:
        raise RuntimeError("Unknown polarity.")


DivIntegerC_I._ipps_candidates = _DivIntegerCIIPPSImpl._ipps_candidates


class AbsInteger(
    metaclass=_unaries.Unary,
    ipps_backend="Abs",
    numpy_backend=_numpy.fabs,
    candidates=_unarySignedInt_candidates,
):
    """Abs Function."""

    pass


class AbsInteger_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Abs_I",
    numpy_backend=_numpy.fabs,
    candidates=_unarySignedInt_candidates,
):
    """Abs_I Function."""

    pass


class _SqrIntegerIPPSImpl(
    metaclass=_unaries.Unary,
    ipps_backend="Sqr",
    numpy_backend=_numpy.square,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unaryUnsignedInt_candidates,
):
    """Sqr Function -- Intel IPPS implementation."""

    pass


class _SqrIntegerNumpyImpl(
    metaclass=_unaries.Unary,
    ipps_backend="Sqr",
    numpy_backend=_numpy.square,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unaryUnsignedInt_candidates,
    force_numpy=True,
):
    """Sqr Function -- Numpy implementation."""

    pass


def SqrInteger(size, dtype=_numpy.uint8):
    """Sqr Function."""
    return (
        _SqrIntegerIPPSImpl(dtype=dtype, size=size)
        if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (2,)
        else _SqrIntegerNumpyImpl(dtype=dtype, size=size)
    )


SqrInteger._ipps_candidates = _SqrIntegerIPPSImpl._ipps_candidates


class SqrInteger_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Sqr_I",
    numpy_backend=_numpy.square,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unaryUnsignedInt_candidates,
):
    """Sqr_I Function."""

    pass


class SqrtInteger(
    metaclass=_unaries.Unary,
    ipps_backend="Sqrt",
    numpy_backend=_numpy.sqrt,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unaryUnsignedInt_candidates,
):
    """Sqrt Function."""

    pass


class SqrtInteger_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Sqrt_I",
    numpy_backend=_numpy.sqrt,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unaryUnsignedInt_candidates,
):
    """Sqrt_I Function."""

    pass


class ExpInteger(
    metaclass=_unaries.Unary,
    ipps_backend="Exp",
    numpy_backend=_numpy.exp,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unarySignedInt_candidates,
):
    """Exp Function."""

    pass


class ExpInteger_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Exp_I",
    numpy_backend=_numpy.exp,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unarySignedInt_candidates,
):
    """Exp_I Function."""

    pass


class _LnIntegerIPPSImpl(
    metaclass=_unaries.Unary,
    ipps_backend="Ln",
    numpy_backend=_numpy.log,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unarySignedInt_candidates,
):
    """Ln Function -- Intel IPPS implementation."""

    pass


class _LnIntegerNumpyImpl(
    metaclass=_unaries.Unary,
    ipps_backend="Ln",
    numpy_backend=_numpy.log,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unarySignedInt_candidates,
    force_numpy=True,
):
    """Ln Function -- Numpy implementation."""

    pass


def LnInteger(size, dtype=_numpy.int32):
    """Ln Function."""
    return (
        _LnIntegerIPPSImpl(dtype=dtype, size=size)
        if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (2,)
        else _LnIntegerNumpyImpl(dtype=dtype, size=size)
    )


LnInteger._ipps_candidates = _LnIntegerIPPSImpl._ipps_candidates


class _LnIntegerIIPPSImpl(
    metaclass=_unaries.Unary_I,
    ipps_backend="Ln_I",
    numpy_backend=_numpy.log,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unarySignedInt_candidates,
):
    """Ln_I Function -- Intel IPPS implementation."""

    pass


class _LnIntegerINumpyImpl(
    metaclass=_unaries.Unary_I,
    ipps_backend="Ln_I",
    numpy_backend=_numpy.log,
    policies=numpy_ipps.policies.scaled_all,
    candidates=_unarySignedInt_candidates,
    force_numpy=True,
):
    """Ln_I Function -- Numpy implementation."""

    pass


def LnInteger_I(size, dtype=_numpy.int32):
    """Ln_I Function."""
    return (
        _LnIntegerIIPPSImpl(dtype=dtype, size=size)
        if size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (2,)
        else _LnIntegerINumpyImpl(dtype=dtype, size=size)
    )


LnInteger_I._ipps_candidates = _LnIntegerIIPPSImpl._ipps_candidates


class _AddProductIntegerIPPSImpl:
    """AddProduct Function -- Intel IPPS implementation."""

    __slots__ = ("_ipps_backend", "_ipps_scale")
    _ipps_candidates = (_numpy.int16, _numpy.int32)

    def __init__(self, dtype=_numpy.int32, size=None):
        self._ipps_scale = numpy_ipps.utils.cast("int", 0)

        self._ipps_backend = _dispatch.ipps_function(
            "AddProduct",
            ("void*", "void*", "void*", "int"),
            dtype,
            policies=numpy_ipps.policies.scaled_all,
        )

    def __call__(self, src1, src2, src_dst):
        numpy_ipps.status = self._ipps_backend(
            src1.cdata,
            src2.cdata,
            src_dst.cdata,
            src_dst.size,
            self._ipps_scale,
        )

    def _numpy_backend(self, src1, src2, src_dst):
        _numpy.multiply(
            src1.ndarray, src2.ndarray, src2.ndarray, casting="unsafe"
        )
        _numpy.add(
            src_dst.ndarray, src2.ndarray, src_dst.ndarray, casting="unsafe"
        )


class _AddProductIntegerNumpyImpl:
    """AddProduct Function -- Numpy implementation."""

    __slots__ = ("_ipps_backend", "_ipps_scale")
    _ipps_candidates = (_numpy.int16, _numpy.int32)

    def __init__(self, dtype=_numpy.int32, size=None):
        self._ipps_scale = numpy_ipps.utils.cast("int", 0)

        self._ipps_backend = _dispatch.ipps_function(
            "AddProduct",
            ("void*", "void*", "void*", "int"),
            dtype,
            policies=numpy_ipps.policies.scaled_all,
        )

    def __call__(self, src1, src2, src_dst):
        _numpy.multiply(
            src1.ndarray, src2.ndarray, src2.ndarray, casting="unsafe"
        )
        _numpy.add(
            src_dst.ndarray, src2.ndarray, src_dst.ndarray, casting="unsafe"
        )

    def _numpy_backend(self, src1, src2, src_dst):
        _numpy.multiply(
            src1.ndarray, src2.ndarray, src2.ndarray, casting="unsafe"
        )
        _numpy.add(
            src_dst.ndarray, src2.ndarray, src_dst.ndarray, casting="unsafe"
        )


def AddProductInteger(size, dtype=_numpy.int32):
    """AddProduct Function."""
    return (
        _AddProductIntegerIPPSImpl(dtype=dtype, size=size)
        if 3 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (4,)
        else _AddProductIntegerNumpyImpl(dtype=dtype, size=size)
    )


AddProductInteger._ipps_candidates = (
    _AddProductIntegerIPPSImpl._ipps_candidates
)


class NormalizeInteger:
    """Normalize Function."""

    __slots__ = ("_ipps_backend", "_ipps_scale")
    _ipps_candidates = (_numpy.int16,)

    def __init__(self, dtype=_numpy.int16, size=None):
        self._ipps_scale = numpy_ipps.utils.cast("int", 0)

        self._ipps_backend = _dispatch.ipps_function(
            "Normalize",
            (
                "void*",
                "void*",
                "int",
                _dispatch.as_ctype_str(
                    dtype, policies=numpy_ipps.policies.scaled_all
                ),
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.scaled_all,
        )

    def __call__(self, src, dst, sub, div):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
            sub,
            div,
            self._ipps_scale,
        )

    def _numpy_backend(self, src, dst, sub, div):
        _numpy.subtract(src.ndarray, sub, dst.ndarray, casting="unsafe")
        _numpy.divide(dst.ndarray, div, dst.ndarray, casting="unsafe")


class NormalizeInteger_I:
    """Normalize_I Function."""

    __slots__ = ("_ipps_backend", "_ipps_scale")
    _ipps_candidates = (_numpy.int16,)

    def __init__(self, dtype=_numpy.int16, size=None):
        self._ipps_scale = numpy_ipps.utils.cast("int", 0)

        self._ipps_backend = _dispatch.ipps_function(
            "Normalize_I",
            (
                "void*",
                "int",
                _dispatch.as_ctype_str(
                    dtype, policies=numpy_ipps.policies.scaled_all
                ),
                "int",
            ),
            dtype,
            policies=numpy_ipps.policies.scaled_all,
        )

    def __call__(self, src_dst, sub, div):
        numpy_ipps.status = self._ipps_backend(
            src_dst.cdata,
            src_dst.size,
            sub,
            div,
            self._ipps_scale,
        )

    def _numpy_backend(self, src_dst, sub, div):
        _numpy.subtract(
            src_dst.ndarray, sub, src_dst.ndarray, casting="unsafe"
        )
        _numpy.divide(src_dst.ndarray, div, src_dst.ndarray, casting="unsafe")
