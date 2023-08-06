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
def test_ipps_assign(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Assign._ipps_candidates:
        return

    assign = numpy_ipps.Assign(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(assign, src, dst)

    numpy.testing.assert_almost_equal(dst, src)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_numpy_assign(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Assign._ipps_candidates:
        return

    assign = numpy_ipps.Assign(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(assign._numpy_backend, src, dst)

    numpy.testing.assert_almost_equal(dst, src)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_bitshiftLE(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.BitShift._ipps_candidates:
        return

    bitshift_le = numpy_ipps.BitShift(3, 5, numpy_ipps.Endian.LITTLE)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    size = 8 * (1 << order) - 12

    with numpy_ipps.utils.context(src, dst):
        benchmark(bitshift_le, src, dst, size)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_bitshiftBE(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.BitShift._ipps_candidates:
        return

    bitshift_be = numpy_ipps.BitShift(3, 5, numpy_ipps.Endian.BIG)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    size = 8 * (1 << order) - 12

    with numpy_ipps.utils.context(src, dst):
        benchmark(bitshift_be, src, dst, size)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_set0(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Zeros._ipps_candidates:
        return

    zeros = numpy_ipps.Zeros(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src):
        benchmark(zeros, src)

    numpy.testing.assert_almost_equal(src, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_set1(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SetTo._ipps_candidates:
        return

    set_to_1 = numpy_ipps.SetTo(1 << order, dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    value = 1
    if dtype in [numpy.int8, numpy.uint8]:
        value = numpy_ipps.utils.cast("char", value)

    with numpy_ipps.utils.context(src):
        benchmark(set_to_1, src, value)

    numpy.testing.assert_almost_equal(src, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_numpy_set0(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.Zeros._ipps_candidates:
        return

    zeros = numpy_ipps.Zeros(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src):
        benchmark(zeros._numpy_backend, src)

    numpy.testing.assert_almost_equal(src, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_numpy_set1(logger_fixture, benchmark, order, dtype):
    if dtype not in numpy_ipps.SetTo._ipps_candidates:
        return

    set_to_1 = numpy_ipps.SetTo(1 << order, dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    value = 1

    with numpy_ipps.utils.context(src):
        benchmark(set_to_1._numpy_backend, src, value)

    numpy.testing.assert_almost_equal(src, 1)
