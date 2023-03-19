import json
import requests
import re
import dataclasses
import typing as t
import datetime
from requests import Response

ISO8601_DATE: t.Pattern[str] = re.compile(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z$")


def convert_to_datetime(date_str: str) -> datetime.datetime:
    match: t.Match[str] = ISO8601_DATE.match(date_str)
    assert match
    return datetime.datetime(*map(int, match.groups()), tzinfo=datetime.timezone.utc)


@dataclasses.dataclass(kw_only=True, frozen=True, order=True)
class TramInformation:
    eta: datetime.datetime
    line_number: int
    direction: str

    def minutes_till_departure(self, now: datetime.datetime) -> int:
        now: datetime = now or datetime.datetime.utcnow()
        seconds: float = (self.eta - now).total_seconds()
        return abs(round(seconds / 60))


class TramFinder:
    def __init__(self, stop_ids: list, lines_to_show: int) -> None:
        self.stop_ids = stop_ids
        self.lines_to_show = lines_to_show

    @staticmethod
    def get_departures(stop_id: int) -> t.Sequence[TramInformation]:
        response: Response = requests.get(
            f'https://ckan2.multimediagdansk.pl/departures?stopId={stop_id}')
        data: int | slice = response.json()
        return [TramInformation(eta=convert_to_datetime(item["estimatedTime"]),
                                line_number=item["routeId"],
                                direction=item["headsign"])
                for item in data["departures"]]

    def json_file(self):
        departures: list = sorted([departure for stop in self.stop_ids for departure in self.get_departures(stop)])
        departure_dict, json_dict, list_of_dicts = {}, {}, []
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        for departure in departures[:self.lines_to_show]:
            minutes_till_departure = departure.minutes_till_departure(now)
            departure_dict = {'n': departure.line_number, 'd': departure.direction,
                              't': minutes_till_departure}
            list_of_dicts.append(departure_dict)
            json_dict['ztm'] = list_of_dicts
        payload = json.dumps(json_dict)
        return payload
