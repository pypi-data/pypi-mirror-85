"""
This module implements a unit test for our main function. It mocks out the API
call so that it's not dependent on network connectivity or changing results. It
then compares what the function returns to what is expected.
"""

from datetime import datetime, timedelta

import pytest

from ywit_event_countdown import countdown


@pytest.mark.parametrize("from_time, event_date, expected_difference", [
    (datetime(2020, 11, 12), "2020-11-13T16:00:00+00:00", 144000),
    (datetime(2019, 11, 13), "2020-11-13T16:00:00+00:00", 31680000),
    (datetime(2021, 11, 13), "2020-11-13T16:00:00+00:00", -31478400),
    (datetime(2020, 11, 12), "2020-11-16T16:00:00+00:00", 403200),
    (datetime.fromisoformat("2020-11-11T16:00:00-05:00"), "2020-11-16T16:00:00+00:00", 414000),
])
def test_get_time_difference(from_time, event_date, expected_difference, monkeypatch):
    """Validate that our time difference function works as expected when providing
    it with different times to calculate from
    """

    monkeypatch.setattr(countdown, "_get_event_from_api", lambda: event_date)

    diff = countdown.get_time_difference(from_time=from_time)
    diff_seconds = diff // timedelta(seconds=1)
    assert expected_difference == diff_seconds
