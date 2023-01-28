import requests
import time
import re
import dataclasses
import typing as t
import datetime

STOP_ID = [2031, 2030]
ISO8601 = re.compile(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z$")
ICON = '\U0001F68A'  # icon is too wide


def converting_to_datetime(date_str: str) -> datetime.datetime:
    match = ISO8601.match(date_str)
    assert (match)
    return datetime.datetime(*map(int, match.groups()), tzinfo=datetime.timezone.utc)


@dataclasses.dataclass(kw_only=True, frozen=True, order=True)
class Trams:
    eta: datetime.datetime
    line_number: int
    direction: str

    def minutes_till_departure(self, now: datetime.datetime) -> int:
        now = now or datetime.datetime.utcnow()
        seconds = (self.eta - now).total_seconds()
        return round(seconds / 60)


def get_departures(stop_id: int) -> t.Sequence[Trams]:
    response = requests.get(
        f'https://ckan2.multimediagdansk.pl/departures?stopId={stop_id}')
    data = response.json()
    return [Trams(eta=converting_to_datetime(item["estimatedTime"]),
                  line_number=item["routeId"],
                  direction=item["headsign"])
            for item in data["departures"]]


def main():
    departures = sorted([departure for stop in STOP_ID for departure in get_departures(stop)])

    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    for departure in departures[:5]:
        minutes_till_departure = departure.minutes_till_departure(now)
        print(
            f'{departure.line_number:2d} {departure.direction:20.20s} '
            + (f"{minutes_till_departure:2d}" if minutes_till_departure > 1
               else ICON))


if __name__ == '__main__':
    while True:
        main()
        time.sleep(20)
