import requests
import json
from datetime import datetime
from tabulate import tabulate

'''
2. potrzebujemy trzy informacje wyświetlane na tablicy: tramwaj, w jaką stronę jedzie, szacowany czas przyjazdu 
- gdy czas przyjazdu wynosić bedzie <1, wtedy jakąś ikonkę printować zamiast czasu
- znalezc time z godzina wczesniej by mozna uzyc drugi raz funkcji converte dla czystości kodu
3. Jako, ze interesują nas tramwaje w obydwie storny, musimy połączyć dwa url
4. Interesuje nas tylko np. 5 następnych tramwajów
5. Znalźć sposób na samouruchamianie się terminala. Chodzi o to, by się na wyświetlaczu sam wywoływał i aktualizował'''

url1 = requests.get(
    'https://ckan2.multimediagdansk.pl/departures?stopId=2030')
data_zajezdnia02 = json.loads(url1.text)


def converte_hrs_to_sec(time):
    return ((time[0] * 60) + time[1]) * 60 + time[2]


# prepering data from e.g: "2022-11-18T15:01:28Z"
eta = [i['estimatedTime'][11:19].split(':')
       for i in data_zajezdnia02['departures']]
eta = [[int(i) for i in eta] for eta in eta]
# converted arrival estimated time list in seconds
eta = [converte_hrs_to_sec(eta[i]) for i in range(0, len(eta))]

# print('w sek przed deley:  ', eta)
# updating eta with delay data
delay_list = [i['delayInSeconds']
              for i in data_zajezdnia02['departures']]
# print('jaki delay:        ', delay_list)
eta_with_delay = []
for i, j in zip(delay_list, eta):
    if i != None:
        if i < 0:
            eta_with_delay.append(j + (-abs(i)))
        else:
            eta_with_delay.append(j + (abs(i)))
    else:
        eta_with_delay.append(j)
# print('   po delayu lista:', eta_with_delay)
eta_sorted = sorted(eta_with_delay)
# print('sorted delayu lista:', eta_with_delay)


current_time = datetime.utcnow().time()
print(current_time)
# changing current time to seconds
converted_time = ((current_time.hour * 60) +
                  current_time.minute) * 60 + current_time.second

# test1 = [round((i - converted_time)/60) for i in eta]
# print('Przed delay:     ', test1)
# test3 = [round((i - converted_time)/60) for i in eta_with_delay]
# print('Po delay         ', test3)
# test2 = [round((i - converted_time)/60) for i in eta_sorted]
# print('Po delay sorted: ', test2)

# subtracting both data and converting to minutes
eta_min = [round((i - converted_time)/60) for i in eta_sorted]
for i in eta_min:
    if i < 1:
        eta_min[i] = '\U0001F68A'
outcome = [(i['routeId'], i['headsign'], j)
           for i, j in zip(data_zajezdnia02['departures'], eta_min)]
print(tabulate(outcome))
