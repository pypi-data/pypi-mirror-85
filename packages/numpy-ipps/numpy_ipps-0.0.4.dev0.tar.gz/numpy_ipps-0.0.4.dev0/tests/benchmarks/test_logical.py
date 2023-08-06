import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps
import numpy_ipps.utils


cache_L1 = numpy.min(
    [cache_size for _u0, _u1, cache_size in numpy_ipps.support.cache_params()]
)
orders = (
    6,
    int(numpy.ceil(numpy.log2(cache_L1))),
)
dtypes = (
    numpy.int8,
    numpy.uint8,
    numpy.int16,
    numpy.uint16,
    numpy.int32,
    numpy.uint32,
    numpy.int64,
    numpy.uint64,
    numpy.float32,
    numpy.float64,
    numpy.complex64,
    numpy.complex128,
)
if (
    "NUMPY_IPPS_FAST_TEST" in os.environ
    and os.environ["NUMPY_IPPS_FAST_TEST"] == "ON"
):
    dtypes = (numpy.int32, numpy.float32)


binary_classes = (
    numpy_ipps.And,
    numpy_ipps.Or,
    numpy_ipps.Xor,
)
binaryI_classes = (
    numpy_ipps.And_I,
    numpy_ipps.Or_I,
    numpy_ipps.Xor_I,
)
binaryC_classes = (
    numpy_ipps.AndC,
    numpy_ipps.LShiftC,
    numpy_ipps.RShiftC,
)
binaryCI_classes = (
    numpy_ipps.AndC_I,
    numpy_ipps.OrC_I,
    numpy_ipps.XorC_I,
    numpy_ipps.LShiftC_I,
    numpy_ipps.RShiftC_I,
)

unary_classes = (numpy_ipps.Not,)
unaryI_classes = (numpy_ipps.Not_I,)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_integer.log",
    )
    ch = logging.FileHandler(log_file, mode="w")
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(ch)
    importlib.reload(numpy_ipps)

    yield logger

    logger.removeHandler(ch)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binary_classes)
def test_ipps_binary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src1 = numpy.ones(1 << order, dtype=dtype)
    src2 = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst, dst_ref):
        benchmark(feature_obj, src1, src2, dst)
        feature_obj._numpy_backend(src1, src2, dst_ref)

    numpy.testing.assert_almost_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryI_classes)
def test_ipps_binaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(feature_obj, src, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binary_classes)
def test_numpy_binary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src1 = numpy.ones(1 << order, dtype=dtype)
    src2 = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(feature_obj._numpy_backend, src1, src2, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryI_classes)
def test_numpy_binaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(feature_obj._numpy_backend, src, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryC_classes)
def test_ipps_binaryC(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    value = 1
    if dtype in (numpy.int8, numpy.uint8):
        value = numpy_ipps.utils.cast("char", value)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, value, dst)
        feature_obj._numpy_backend(src, 1, dst_ref)

    numpy.testing.assert_almost_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryCI_classes)
def test_ipps_binaryCI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    value = 1
    if dtype in (numpy.int8, numpy.uint8):
        value = numpy_ipps.utils.cast("char", value)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, value, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryC_classes)
def test_numpy_binaryC(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    value = 1
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj._numpy_backend, src, value, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryCI_classes)
def test_numpy_binaryCI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    value = 1
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj._numpy_backend, value, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", (numpy_ipps.OrC, numpy_ipps.XorC))
def test_ipps_binaryCUnsafe(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    value = 1
    if dtype in (numpy.int8, numpy.uint8):
        value = numpy_ipps.utils.cast("char", value)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, value, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", (numpy_ipps.OrC, numpy_ipps.XorC))
def test_numpy_binaryCUnsafe(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    value = 1
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj._numpy_backend, src, value, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unary_classes)
def test_ipps_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst)
        feature_obj._numpy_backend(src, dst_ref)

    numpy.testing.assert_almost_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unaryI_classes)
def test_ipps_unaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unary_classes)
def test_numpy_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unaryI_classes)
def test_numpy_unaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj._numpy_backend, src_dst)
