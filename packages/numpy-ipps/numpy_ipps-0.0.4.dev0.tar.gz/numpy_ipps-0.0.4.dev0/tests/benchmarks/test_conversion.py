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


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_initialization.log",
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
def test_ipps_swapbytes(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SwapBytes._ipps_candidates:
        return

    feature_obj = numpy_ipps.SwapBytes(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst)
        feature_obj._numpy_backend(src, dst_ref)

    numpy.testing.assert_almost_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_numpy_swapbytes(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SwapBytes._ipps_candidates:
        return

    feature_obj = numpy_ipps.SwapBytes(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_swapbytesI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SwapBytes_I._ipps_candidates:
        return

    feature_obj = numpy_ipps.SwapBytes_I(dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_numpy_swapbytesI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SwapBytes_I._ipps_candidates:
        return

    feature_obj = numpy_ipps.SwapBytes_I(dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj._numpy_backend, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_flip(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Flip._ipps_candidates:
        return

    feature_obj = numpy_ipps.Flip(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst)
        feature_obj._numpy_backend(src, dst_ref)

    numpy.testing.assert_almost_equal(dst, dst_ref)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_numpy_flip(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Flip._ipps_candidates:
        return

    feature_obj = numpy_ipps.Flip(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_flipI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Flip_I._ipps_candidates:
        return

    feature_obj = numpy_ipps.Flip_I(dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_numpy_flipI(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Flip_I._ipps_candidates:
        return

    feature_obj = numpy_ipps.Flip_I(dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj._numpy_backend, src_dst)
