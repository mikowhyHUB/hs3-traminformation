import requests
import json
import time
from datetime import datetime
from tabulate import tabulate


def converted_raw_eta(data_zajezdnia):
    '''
    Converting raw api informations

    :param data_zajezdnia: dict - all raw informations about stops and trams
    :return: list - changing raw estimated time arrival to seconds
    '''
    def converte_hrs_to_sec(time):
        '''
        Converting hours to seconds

        :param time: list - converted hours of local time to seconds
        :return: list - converted time
        '''
        return ((time[0] * 60) + time[1]) * 60 + time[2]

    eta = [i['estimatedTime'][11:19].split(
        ':') for i in data_zajezdnia['departures']]
    eta = [[int(i) for i in eta] for eta in eta]
    eta = list(map(converte_hrs_to_sec, eta))
    return eta


def eta_final(data_zajezdnia):
    '''
    Prepering time for final outcome. Replacing minutes with the tram emoji when the estimated time is less than one minute

    :param data_zajezdnia: dict - all raw informations about stops and trams
    :return: list - how many minutes left before the tram leaves
    '''
    eta = converted_raw_eta(data_zajezdnia)
    current_time = datetime.utcnow().time()
    converted_time = ((current_time.hour * 60) +
                      current_time.minute) * 60 + current_time.second
    # subtracting both data and converting to minutes
    eta_min = [round((i - converted_time)/60) for i in eta]
    # replacing <1 minute with tram emoji
    eta_min = ['\U0001F68A' if i < 1 else i for i in eta_min]
    return eta_min


def table_tram_nums(data01, data02):
    '''
    Zipping two tram numbers lines directions

    :param data01:dict - all raw informations about tram stop Zajezdnia01
    :param data02:dict - all raw informations about tram stop Zajezdnia02
    :return: list - all the upcoming tram numbers for both directions
    '''

    tram_nums = [(i['routeId'], j['routeId'])
                 for i, j in zip(data01['departures'], data02['departures'])]
    return list(sum(tram_nums, ()))


def table_headsigns(data01, data02):
    '''
    Zipping two headsign lines directions

    :param data01:dict - all raw informations about tram stop Zajezdnia01
    :param data02:dict - all raw informations about tram stop Zajezdnia02
    :return: list - all the upcoming tram numbers for both directions
    '''
    headsigns = [(i['headsign'], j['headsign'])
                 for i, j in zip(data01['departures'], data02['departures'])]
    return list(sum(headsigns, ()))


def table_eta(time01, time02):
    '''
    Taking from eta_final function parameters and zipping ETA lines directions

    :param time01:list - time left in minutes for tram stop Zajezdnia01
    :param time02:list - time left in minutes for tram stop Zajezdnia02
    :return: list - all the ETA informations in minutes for both directions
    '''
    eta = [(i, j) for i, j in zip(time01, time02)]
    return list(sum(eta, ()))


def main():
    # api
    url1 = requests.get(
        'https://ckan2.multimediagdansk.pl/departures?stopId=2031')
    url2 = requests.get(
        'https://ckan2.multimediagdansk.pl/departures?stopId=2030')
    data_zajezdnia01 = json.loads(url1.text)
    data_zajezdnia02 = json.loads(url2.text)

    # preparing ETA table content
    eta_zajezdnia01 = eta_final(data_zajezdnia01)
    eta_zajezdnia02 = eta_final(data_zajezdnia02)
    # table content
    tram_nums = table_tram_nums(data_zajezdnia01, data_zajezdnia02)
    headsigns = table_headsigns(data_zajezdnia01, data_zajezdnia02)
    eta = table_eta(eta_zajezdnia01, eta_zajezdnia02)

    # printing tram information table for both directions
    outcome = [(number, direction, time_left)
               for number, direction, time_left in zip(tram_nums, headsigns, eta)]
    # printing n lines of data
    outcome = [outcome[i] for i in range(5)]
    print(tabulate(outcome, tablefmt='simple', headers='  ', numalign='right'))


if __name__ == '__main__':
    # looping program every n sec
    while True:
        main()
        time.sleep(20)
