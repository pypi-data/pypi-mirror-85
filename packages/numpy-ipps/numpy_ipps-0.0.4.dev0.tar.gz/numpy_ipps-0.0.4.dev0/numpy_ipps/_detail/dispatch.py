import logging

import numpy
import numpy.ctypeslib

import numpy_ipps._detail.debug
import numpy_ipps._detail.libipp
import numpy_ipps.policies


def as_type_tag(
    dtype,
    policies=numpy_ipps.policies.keep_all,
):
    if dtype == numpy.complex64:
        return "32fc"
    elif dtype == numpy.complex128:
        return "64fc"
    else:
        ctype_type = numpy.ctypeslib.as_ctypes_type(dtype)
        for (
            policy,
            ctype_ref_u,
            ctype_ref_s,
            ctype_ref_f,
            _ctype_ref_down,
        ) in (
            policies.bytes1,
            policies.bytes2,
            policies.bytes4,
            policies.bytes8,
        ):
            if ctype_type == ctype_ref_u:
                if policy in (
                    numpy_ipps.policies.TagPolicy.KEEP,
                    numpy_ipps.policies.TagPolicy.UNSIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_KEEP,
                    numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
                    numpy_ipps.policies.TagPolicy.INTEGER_UNSIGNED,
                ):
                    return "{}u".format(8 * numpy.dtype(ctype_ref_u).itemsize)
                elif policy in (
                    numpy_ipps.policies.TagPolicy.SIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
                    numpy_ipps.policies.TagPolicy.INTEGER_SIGNED,
                ):
                    return "{}s".format(8 * numpy.dtype(ctype_ref_u).itemsize)
                elif policy in (
                    numpy_ipps.policies.TagPolicy.DOWN_KEEP,
                    numpy_ipps.policies.TagPolicy.DOWN_UNSIGNED,
                ):
                    return "{}u".format(4 * numpy.dtype(ctype_ref_u).itemsize)
                elif policy == numpy_ipps.policies.TagPolicy.DOWN_SIGNED:
                    return "{}s".format(4 * numpy.dtype(ctype_ref_u).itemsize)
                elif policy == numpy_ipps.policies.TagPolicy.FLOAT:
                    return "{}f".format(8 * numpy.dtype(ctype_ref_u).itemsize)
                else:
                    numpy_ipps._detail.debug.log_and_raise(
                        RuntimeError,
                        "Unknown policy for {} : {}".format(dtype, policy),
                        name=__name__,
                    )
            if ctype_type == ctype_ref_s:
                if policy in (
                    numpy_ipps.policies.TagPolicy.KEEP,
                    numpy_ipps.policies.TagPolicy.SIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_KEEP,
                    numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
                    numpy_ipps.policies.TagPolicy.INTEGER_SIGNED,
                ):
                    return "{}s".format(8 * numpy.dtype(ctype_ref_s).itemsize)
                elif policy in (
                    numpy_ipps.policies.TagPolicy.UNSIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
                    numpy_ipps.policies.TagPolicy.INTEGER_UNSIGNED,
                ):
                    return "{}u".format(8 * numpy.dtype(ctype_ref_s).itemsize)
                elif policy in (
                    numpy_ipps.policies.TagPolicy.DOWN_KEEP,
                    numpy_ipps.policies.TagPolicy.DOWN_SIGNED,
                ):
                    return "{}s".format(4 * numpy.dtype(ctype_ref_u).itemsize)
                elif policy == numpy_ipps.policies.TagPolicy.DOWN_UNSIGNED:
                    return "{}u".format(4 * numpy.dtype(ctype_ref_u).itemsize)
                elif policy == numpy_ipps.policies.TagPolicy.FLOAT:
                    return "{}f".format(8 * numpy.dtype(ctype_ref_u).itemsize)
                else:
                    numpy_ipps._detail.debug.log_and_raise(
                        RuntimeError,
                        "Unknown policy for {} : {}".format(dtype, policy),
                        name=__name__,
                    )
            if ctype_type == ctype_ref_f:
                if policy in (
                    numpy_ipps.policies.TagPolicy.KEEP,
                    numpy_ipps.policies.TagPolicy.SCALE_KEEP,
                    numpy_ipps.policies.TagPolicy.FLOAT,
                    numpy_ipps.policies.TagPolicy.INTEGER_SIGNED,
                    numpy_ipps.policies.TagPolicy.INTEGER_UNSIGNED,
                ):
                    return "{}f".format(8 * numpy.dtype(ctype_ref_s).itemsize)
                elif policy in (
                    numpy_ipps.policies.TagPolicy.UNSIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
                ):
                    return "{}u".format(8 * numpy.dtype(ctype_ref_s).itemsize)
                elif policy in (
                    numpy_ipps.policies.TagPolicy.SIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
                ):
                    return "{}s".format(8 * numpy.dtype(ctype_ref_s).itemsize)
                else:
                    numpy_ipps._detail.debug.log_and_raise(
                        RuntimeError,
                        "Unknown policy for {} : {}".format(dtype, policy),
                        name=__name__,
                    )
        else:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError, "Unknown dtype: {}".format(dtype), name=__name__
            )


def as_ctype_str(
    dtype,
    policies=numpy_ipps.policies.keep_all,
):
    if dtype == numpy.complex64:
        return "float complex"
    elif dtype == numpy.complex128:
        return "double complex"
    else:
        ctype_type = numpy.ctypeslib.as_ctypes_type(dtype)
        for (
            policy,
            ctype_ref_u,
            ctype_ref_s,
            ctype_ref_f,
            ctype_ref_down,
        ) in (
            policies.bytes1,
            policies.bytes2,
            policies.bytes4,
            policies.bytes8,
        ):
            ctype_ref_name = ctype_ref_s.__name__[2:]
            if ctype_ref_down is not None:
                ctype_ref_down_name = ctype_ref_down.__name__[2:]
                if ctype_ref_down_name == "byte":
                    ctype_ref_down_name = "char"
            if ctype_ref_name == "byte":
                ctype_ref_name = "char"
            if ctype_type == ctype_ref_u:
                if policy in (
                    numpy_ipps.policies.TagPolicy.KEEP,
                    numpy_ipps.policies.TagPolicy.UNSIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_KEEP,
                    numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
                    numpy_ipps.policies.TagPolicy.INTEGER_UNSIGNED,
                ):
                    return "unsigned {}".format(ctype_ref_name)
                elif policy in (
                    numpy_ipps.policies.TagPolicy.SIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
                    numpy_ipps.policies.TagPolicy.INTEGER_SIGNED,
                ):
                    return ctype_ref_name
                elif policy in (
                    numpy_ipps.policies.TagPolicy.DOWN_KEEP,
                    numpy_ipps.policies.TagPolicy.DOWN_UNSIGNED,
                ):
                    return "unsigned {}".format(ctype_ref_down_name)
                elif policy == numpy_ipps.policies.TagPolicy.DOWN_SIGNED:
                    return ctype_ref_down_name
                elif policy == numpy_ipps.policies.TagPolicy.FLOAT:
                    return ctype_ref_f.__name__[2:]
                else:
                    numpy_ipps._detail.debug.log_and_raise(
                        RuntimeError,
                        "Unknown policy for {} : {}".format(dtype, policy),
                        name=__name__,
                    )
            if ctype_type == ctype_ref_s:
                if policy in (
                    numpy_ipps.policies.TagPolicy.KEEP,
                    numpy_ipps.policies.TagPolicy.SIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_KEEP,
                    numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
                    numpy_ipps.policies.TagPolicy.INTEGER_SIGNED,
                ):
                    return ctype_ref_name
                elif policy in (
                    numpy_ipps.policies.TagPolicy.UNSIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
                    numpy_ipps.policies.TagPolicy.INTEGER_UNSIGNED,
                ):
                    return "unsigned {}".format(ctype_ref_name)
                elif policy in (
                    numpy_ipps.policies.TagPolicy.DOWN_KEEP,
                    numpy_ipps.policies.TagPolicy.DOWN_SIGNED,
                ):
                    return ctype_ref_down_name
                elif policy == numpy_ipps.policies.TagPolicy.DOWN_UNSIGNED:
                    return "unsigned {}".format(ctype_ref_down_name)
                elif policy == numpy_ipps.policies.TagPolicy.FLOAT:
                    return ctype_ref_f.__name__[2:]
                else:
                    numpy_ipps._detail.debug.log_and_raise(
                        RuntimeError,
                        "Unknown policy for {} : {}".format(dtype, policy),
                        name=__name__,
                    )
            if ctype_type == ctype_ref_f:
                if policy in (
                    numpy_ipps.policies.TagPolicy.KEEP,
                    numpy_ipps.policies.TagPolicy.SCALE_KEEP,
                    numpy_ipps.policies.TagPolicy.FLOAT,
                    numpy_ipps.policies.TagPolicy.INTEGER_SIGNED,
                    numpy_ipps.policies.TagPolicy.INTEGER_UNSIGNED,
                ):
                    return ctype_ref_f.__name__[2:]
                elif policy in (
                    numpy_ipps.policies.TagPolicy.UNSIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_UNSIGNED,
                ):
                    return "unsigned {}".format(ctype_ref_name)
                elif policy in (
                    numpy_ipps.policies.TagPolicy.SIGNED,
                    numpy_ipps.policies.TagPolicy.SCALE_SIGNED,
                ):
                    return ctype_ref_name
                else:
                    numpy_ipps._detail.debug.log_and_raise(
                        RuntimeError,
                        "Unknown policy for {} : {}".format(dtype, policy),
                        name=__name__,
                    )
        else:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError, "Unknown dtype: {}".format(dtype), name=__name__
            )


def is_scale(dtype, policies=numpy_ipps.policies.keep_all):
    ctype_type = None
    try:
        ctype_type = numpy.ctypeslib.as_ctypes_type(dtype)
    except NotImplementedError:
        return False
    return (
        (
            ctype_type
            in (
                policies.bytes1[numpy_ipps.policies.TagAttr.UTYPE],
                policies.bytes1[numpy_ipps.policies.TagAttr.STYPE],
            )
            and policies.bytes1[numpy_ipps.policies.TagAttr.NAME]
            in numpy_ipps.policies.scales_tags
        )
        or (
            ctype_type
            in (
                policies.bytes2[numpy_ipps.policies.TagAttr.UTYPE],
                policies.bytes2[numpy_ipps.policies.TagAttr.STYPE],
            )
            and policies.bytes2[numpy_ipps.policies.TagAttr.NAME]
            in numpy_ipps.policies.scales_tags
        )
        or (
            ctype_type
            in (
                policies.bytes4[numpy_ipps.policies.TagAttr.UTYPE],
                policies.bytes4[numpy_ipps.policies.TagAttr.STYPE],
            )
            and policies.bytes4[numpy_ipps.policies.TagAttr.NAME]
            in numpy_ipps.policies.scales_tags
        )
        or (
            ctype_type
            in (
                policies.bytes8[numpy_ipps.policies.TagAttr.UTYPE],
                policies.bytes8[numpy_ipps.policies.TagAttr.STYPE],
            )
            and policies.bytes8[numpy_ipps.policies.TagAttr.NAME]
            in numpy_ipps.policies.scales_tags
        )
    )


def ipps_function(
    name, signature, *args, policies=numpy_ipps.policies.keep_all
):
    name_split = name.split("_")
    if len(args) > 0 and is_scale(args[0], policies=policies):
        if len(name_split) == 1:
            name_split.append("Sfs")
        else:
            name_split[-1] = "{}Sfs".format(name_split[-1])
        signature = signature + ("int",)

    function_name = "ipps{}".format(
        "_".join(
            name_split[:1]
            + [as_type_tag(arg, policies=policies) for arg in args]
            + name_split[1:]
        )
    )

    if not hasattr(numpy_ipps._detail.libipp.ipp_signal, function_name):
        func_signature = "int {}({});".format(
            function_name, ",".join(signature)
        )
        numpy_ipps._detail.libipp.ffi.cdef(func_signature)
        if hasattr(numpy_ipps._detail.libipp.ipp_signal, function_name):
            logging.getLogger(__name__).info(
                "CFFI: Register [ {} ]".format(func_signature)
            )
        else:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "CFFI: Register [ {} ] FAILED".format(func_signature),
                name=__name__,
            )

    return numpy_ipps._detail.libipp.ipp_signal.__getattr__(function_name)
