from data import get_last_update, normalize_times
import pytest


@pytest.fixture
def example_status():
    return {"last_check": "2024-03-23T22:44:06.502Z"}


def test_get_last_update(example_status):
    # Compare get_last_update output to manually translated date string
    assert get_last_update(
        example_status) == "Saturday, March 23, 2024, 3:44:06 PM MST"


@pytest.fixture
def second_delays():
    return [30, 60, 120, 240, 289, 32, 21]


@pytest.fixture
def normalized_second_delays(second_delays):
    return [d for d in second_delays]


@pytest.fixture
def minute_delays():
    return [30, 60, 120, 240, 360, 600, 542, 432, 43]


@pytest.fixture
def normalized_minute_delays(minute_delays):
    return [d / 60 for d in minute_delays]


@pytest.fixture
def hour_delays():
    return [12, 1234, 3600, 18000, 32134, 86400]


@pytest.fixture
def normalized_hour_delays(hour_delays):
    return [d / (60 * 60) for d in hour_delays]


# fmt: off
def test_normalize_times(
    second_delays, normalized_second_delays,
    minute_delays, normalized_minute_delays,
    hour_delays, normalized_hour_delays
):  # fmt: on
    assert normalize_times(second_delays) == (
        normalized_second_delays, 'seconds')
    assert normalize_times(minute_delays) == (
        normalized_minute_delays, 'minutes')
    assert normalize_times(hour_delays) == (normalized_hour_delays, 'hours')
