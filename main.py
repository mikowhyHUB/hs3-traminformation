import requests
import json
from datetime import datetime
from tabulate import tabulate

'''
3. Jako, ze interesują nas tramwaje w obydwie storny, musimy połączyć dwa url
4. Interesuje nas tylko np. 5 następnych tramwajów
5. Znalźć sposób na samouruchamianie się terminala. Chodzi o to, by się na wyświetlaczu sam wywoływał i aktualizował'''
url1 = requests.get(
    'https://ckan2.multimediagdansk.pl/departures?stopId=2031')
url2 = requests.get(
    'https://ckan2.multimediagdansk.pl/departures?stopId=2030')
data_zajezdnia01 = json.loads(url1.text)
data_zajezdnia02 = json.loads(url2.text)


# def converte_hrs_to_sec(time):
#     return ((time[0] * 60) + time[1]) * 60 + time[2]


def estimated_time(data_zajezdnia):
    # little function to convert time
    def converte_hrs_to_sec(time):
        return ((time[0] * 60) + time[1]) * 60 + time[2]

    # prepering estimated time of arrival"
    eta = [i['estimatedTime'][11:19].split(
        ':') for i in data_zajezdnia['departures']]
    eta = [[int(i) for i in eta] for eta in eta]
    # converted arrival estimated time list in seconds
    eta = [converte_hrs_to_sec(eta[i]) for i in range(0, len(eta))]
    return eta


eta_func = estimated_time(data_zajezdnia01)


# # prepering data from e.g: "2022-11-18T15:01:28Z"
# eta = [i['estimatedTime'][11:19].split(':')
#        for i in data_zajezdnia02['departures']]
# eta = [[int(i) for i in eta] for eta in eta]
# # converted arrival estimated time list in seconds
# eta = [converte_hrs_to_sec(eta[i]) for i in range(0, len(eta))]


def test_delay(data_zajezdnia, eta):
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


delay_func = test_delay(data_zajezdnia01, eta_func)

# # updating eta with delay data
# delay_list = [i['delayInSeconds']
#               for i in data_zajezdnia02['departures']]
# eta_with_delay = []
# for i, j in zip(delay_list, eta):
#     if i != None:
#         if i < 0:
#             eta_with_delay.append(j + (-abs(i)))
#         else:
#             eta_with_delay.append(j + (abs(i)))
#     else:
#         eta_with_delay.append(j)
# eta_sorted = sorted(eta_with_delay)

# changing current time to seconds
current_time = datetime.utcnow().time()
converted_time = ((current_time.hour * 60) +
                  current_time.minute) * 60 + current_time.second

# subtracting both data and converting to minutes
eta_min = [round((i - converted_time)/60) for i in eta_sorted]
# replacing minute with emoji when the estimated time is less than one minute
# for i in eta_min:
#     if i < 1:
#         eta_min[i] = '\U0001F68A'
# printing table with data
outcome = [(i['routeId'], i['headsign'], j)
           for i, j in zip(data_zajezdnia02['departures'], eta_min)]
# print(tabulate(outcome))

''' 
# print('w sek przed deley:  ', eta)
# print('jaki delay:        ', delay_list)
# print('   po delayu lista:', eta_with_delay)
# print('sorted delayu lista:', eta_with_delay)
# test1 = [round((i - converted_time)/60) for i in eta]
# print('Przed delay:     ', test1)
# test3 = [round((i - converted_time)/60) for i in eta_with_delay]
# print('Po delay         ', test3)
# test2 = [round((i - converted_time)/60) for i in eta_sorted]
# print('Po delay sorted: ', test2)'''
