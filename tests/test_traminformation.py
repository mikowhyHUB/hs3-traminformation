import json
import datetime
import pytest
from src.traminformation import TramFinder, TramInformation, convert_to_datetime

def test_convert_to_datetime():
    assert convert_to_datetime("2022-03-19T12:00:00Z") == datetime.datetime(2022, 3, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)
    assert convert_to_datetime("2022-03-19T01:00:00Z") == datetime.datetime(2022, 3, 19, 1, 0, 0, tzinfo=datetime.timezone.utc)
    assert convert_to_datetime("2022-03-19T23:59:59Z") == datetime.datetime(2022, 3, 19, 23, 59, 59, tzinfo=datetime.timezone.utc)
    with pytest.raises(AssertionError):
        convert_to_datetime("2022-03-19")


def test_tram_information_minutes_till_departure():
    now = datetime.datetime(2022, 3, 19, 12, 0, 0, tzinfo=datetime.timezone.utc)
    tram = TramInformation(eta=datetime.datetime(2022, 3, 19, 12, 5, 0, tzinfo=datetime.timezone.utc), line_number=1, direction="North")
    assert tram.minutes_till_departure(now) == 5
    tram = TramInformation(eta=datetime.datetime(2022, 3, 19, 11, 55, 0, tzinfo=datetime.timezone.utc), line_number=2, direction="South")
    assert tram.minutes_till_departure(now) == 5
    tram = TramInformation(eta=datetime.datetime(2022, 3, 19, 12, 0, 0, tzinfo=datetime.timezone.utc), line_number=3, direction="East")
    assert tram.minutes_till_departure(now) == 0
    tram = TramInformation(eta=datetime.datetime(2022, 3, 19, 11, 59, 0, tzinfo=datetime.timezone.utc), line_number=4, direction="West")
    assert tram.minutes_till_departure(now) == 1


def test_tram_finder_get_departures():
    tram_finder = TramFinder([1601], 10)
    departures = tram_finder.get_departures(1601)
    assert len(departures) > 0
    assert isinstance(departures[0], TramInformation)
    assert isinstance(departures[0].eta, datetime.datetime)
    assert isinstance(departures[0].line_number, int)
    assert isinstance(departures[0].direction, str)


def test_tram_finder_json_file():
    tram_finder = TramFinder([1601], 2)
    json_str = tram_finder.json_file()
    json_dict = json.loads(json_str)
    assert isinstance(json_dict, dict)
    assert "ztm" in json_dict
    assert len(json_dict["ztm"]) == 2
    assert all(isinstance(x, dict) for x in json_dict["ztm"])
    assert all("n" in x for x in json_dict["ztm"])
    assert all("d" in x for x in json_dict["ztm"])
    assert all("t" in x for x in json_dict["ztm"])