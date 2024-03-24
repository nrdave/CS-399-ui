from data import get_mirror_info, get_last_update, normalize_times
import pytest
from requests import get


@pytest.fixture
def example_status():
    """
    Get a dictionary that can be passed to get_last_update
    """
    return {"last_check": "2024-03-23T22:44:06.502Z"}


def test_get_last_update(example_status):
    """Test the get_last_update function in data"""
    # Compare get_last_update output to manually translated date string
    assert get_last_update(
        example_status) == "Saturday, March 23, 2024, 3:44:06 PM MST"


@pytest.fixture
def second_delays():
    """
    Get example times (in seconds) that should stay in units of seconds
    """
    return [30, 60, 120, 240, 289, 32, 21]


@pytest.fixture
def normalized_second_delays(second_delays):
    """
    Normalize the second delays properly to compare with normalize_times output
    """
    return [d for d in second_delays]


@pytest.fixture
def minute_delays():
    """
    Get example times (in seconds) that should be normalized to minutes
    """
    return [30, 60, 120, 240, 360, 600, 542, 432, 43]


@pytest.fixture
def normalized_minute_delays(minute_delays):
    """
    Normalize the minute delays properly to compare with normalize_times output
    """
    return [d / 60 for d in minute_delays]


@pytest.fixture
def hour_delays():
    """
    Get example times (in seconds) that should be normalized to hours
    """
    return [12, 1234, 3600, 18000, 32134, 86400]


@pytest.fixture
def normalized_hour_delays(hour_delays):
    """
    Normalize the hour delays properly to compare with normalize_times output
    """
    return [d / (60 * 60) for d in hour_delays]


# fmt: off
def test_normalize_times(
    second_delays, normalized_second_delays,
    minute_delays, normalized_minute_delays,
    hour_delays, normalized_hour_delays
):  # fmt: on
    """Test the normalize_times function with various delays"""
    assert normalize_times(second_delays) == (
        normalized_second_delays, 'seconds')
    assert normalize_times(minute_delays) == (
        normalized_minute_delays, 'minutes')
    assert normalize_times(hour_delays) == (normalized_hour_delays, 'hours')


@pytest.fixture
def mirror_status_fields():
    """Get the data fields in the Mirror Status file from archlinux.org"""
    return ["cutoff", "last_check", "num_checks",
            "check_frequency", "urls", "version"]


@pytest.fixture
def mirror_info_fields():
    """Get the data fields for each mirror in the Mirror Status file"""
    return ["url", "protocol", "last_sync", "completion_pct", "delay",
            "duration_avg", "duration_stddev", "score", "active", "country",
            "country_code", "isos", "ipv4", "ipv6", "details"]


def test_mirror_data(mirror_status_fields, mirror_info_fields):
    """
    Check that the JSON fields from the Arch Linux Mirror Status website match
    what the program expects"""
    try:
        MIRROR_STATUS_URL = "https://archlinux.org/mirrors/status/json/"

        # Get mirror status manually, as get_mirror_info returns just
        # the statistics for each mirror
        mirror_status = get(MIRROR_STATUS_URL, timeout=5).json()

        assert list(mirror_status.keys()) == mirror_status_fields

        # Check the data version number - another check for possible
        # breaking changes in the API
        assert mirror_status["version"] == 3

        # Check that each mirror contains the fields the program expects
        # it to
        mirrors = get_mirror_info()

        for m in mirrors:
            assert list(m.keys()) == mirror_info_fields

    except ConnectionError:
        return
