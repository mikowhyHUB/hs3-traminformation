import requests
import json
from datetime import datetime
from tabulate import tabulate


def estimated_time(data_zajezdnia):
    # function to convert time
    def converte_hrs_to_sec(time):
        return ((time[0] * 60) + time[1]) * 60 + time[2]

    # prepering estimated time of arrival"
    eta = [i['estimatedTime'][11:19].split(
        ':') for i in data_zajezdnia['departures']]
    eta = [[int(i) for i in eta] for eta in eta]
    # converting ETA list to seconds
    eta = list(map(converte_hrs_to_sec, eta))
    return eta


def delay_time(data_zajezdnia):
    eta = estimated_time(data_zajezdnia)
    # updating estimated time with delay data
    delay_list = [i['delayInSeconds'] for i in data_zajezdnia['departures']]
    eta_with_delay = []
    for i, j in zip(delay_list, eta):
        if i != None:
            if i < 0:
                eta_with_delay.append(j + (-abs(i)))
            else:
                eta_with_delay.append(j + (abs(i)))
        else:
            eta_with_delay.append(j)
    return sorted(eta_with_delay)


def substracted_time(data_zajezdnia):
    eta_with_delay = delay_time(data_zajezdnia)
    # changing current time (-1hour) to seconds
    current_time = datetime.utcnow().time()
    converted_time = ((current_time.hour * 60) +
                      current_time.minute) * 60 + current_time.second
    # subtracting both data and converting to minutes
    eta_min = [round((i - converted_time)/60) for i in eta_with_delay]
    # replacing minutes with emoji when the estimated time is less than one minute
    eta_min = ['\U0001F68A' if i < 1 else i for i in eta_min]
    return eta_min

# todo: think I can do one func for those 3 above


def table_eta(time01, time02):
    # zipping two ETA lines directions
    eta = [(i, j) for i, j in zip(time01, time02)]
    return list(sum(eta, ()))


def table_tram_nums(data01, data02):
    # zipping two tram numbers lines directions
    tram_nums = [(i['routeId'], j['routeId'])
                 for i, j in zip(data01['departures'], data02['departures'])]
    return list(sum(tram_nums, ()))


def table_headsigns(data01, data02):
    # zipping two headsing lines directions
    headsigns = [(i['headsign'], j['headsign'])
                 for i, j in zip(data01['departures'], data02['departures'])]
    return list(sum(headsigns, ()))


def main():
    # api
    url1 = requests.get(
        'https://ckan2.multimediagdansk.pl/departures?stopId=2031')
    url2 = requests.get(
        'https://ckan2.multimediagdansk.pl/departures?stopId=2030')
    data_zajezdnia01 = json.loads(url1.text)
    data_zajezdnia02 = json.loads(url2.text)

    # preparing ETA table content
    eta_zajezdnia01 = substracted_time(data_zajezdnia01)
    eta_zajezdnia02 = substracted_time(data_zajezdnia02)
    # table content
    tram_nums = table_tram_nums(data_zajezdnia01, data_zajezdnia02)
    headsigns = table_headsigns(data_zajezdnia01, data_zajezdnia02)
    eta = table_eta(eta_zajezdnia01, eta_zajezdnia02)

    # printing tram information table for both directions
    outcome = [(i, j, k) for i, j, k in zip(tram_nums, headsigns, eta)]
    # choosing how many lines of data we want
    outcome = [outcome[i] for i in range(5)]

    print(tabulate(outcome))


if __name__ == '__main__':
    main()
