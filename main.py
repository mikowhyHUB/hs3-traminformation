import requests
import json
from datetime import datetime
from tabulate import tabulate

'''
3. Jako, ze interesują nas tramwaje w obydwie storny, musimy połączyć dwa url
4. Interesuje nas tylko np. 5 następnych tramwajów
5. Znalźć sposób na samouruchamianie się terminala. Chodzi o to, by się na wyświetlaczu sam wywoływał i aktualizował'''


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
    # for i in eta_min:
    #     if i < 1:
    #         # sometimes works, sometimes aint. To solve
    #         eta_min[i] = '\U0001F68A'
    return eta_min


def test_eta(time01, time02):
    eta = [(i, j) for i, j in zip(time01, time02)]
    suum = list(sum(eta, ()))
    return suum


def test_tramwaj(data01, data02):
    nr_tram = [(i['routeId'], j['routeId'])
               for i, j in zip(data01['departures'], data02['departures'])]
    suum = list(sum(nr_tram, ()))
    return suum


def test_destynacja(data01, data02):
    desty = [(i['headsign'], j['headsign'])
             for i, j in zip(data01['departures'], data02['departures'])]
    suum = list(sum(desty, ()))
    return suum


def main():
    url1 = requests.get(
        'https://ckan2.multimediagdansk.pl/departures?stopId=2031')
    url2 = requests.get(
        'https://ckan2.multimediagdansk.pl/departures?stopId=2030')
    data_zajezdnia01 = json.loads(url1.text)
    data_zajezdnia02 = json.loads(url2.text)

    zajezdnia01 = substracted_time(data_zajezdnia01)
    zajezdnia02 = substracted_time(data_zajezdnia02)

    nr = test_tramwaj(data_zajezdnia01, data_zajezdnia02)
    desty = test_destynacja(data_zajezdnia01, data_zajezdnia02)
    eta = test_eta(zajezdnia01, zajezdnia02)

    test_outcome = [(i, j, k) for i, j, k in zip(nr, desty, eta)]
    print(tabulate(test_outcome))
    # print('01', zajezdnia01)
    # print('02', zajezdnia02)

    outcome = [(i['routeId'], i['headsign'], j)
               for i, j in zip(data_zajezdnia02['departures'], zajezdnia02)]
    # print(outcome)

    # print(tabulate(outcome))


main()

'''
pomysł. a co jakby uzyc funkcji filter i stowrzyc funkcje co bedzie filtorwac oby dwa przystanki'''
