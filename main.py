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


def converte_hrs_to_sec(item):
    return ((item[0] * 60) + item[1]) * 60 + item[2]


# prepering data from e.g: "2022-11-18T15:01:28Z"
eta = [i['estimatedTime'][11:19].split(':')
       for i in data_zajezdnia02['departures']]
eta = [[int(i) for i in eta] for eta in eta]
# converted arrival estimated time list in seconds
eta = [converte_hrs_to_sec(eta[i]) for i in range(0, len(eta))]
print('w sek przed deley: ', eta)
# updating eta with delay data
delay_list = [i['delayInSeconds']
              for i in data_zajezdnia02['departures']]
print('jaki delay:       ', delay_list)
after_delay = []
for i, j in zip(delay_list, eta):
    if i != None:
        if i < 0:
            after_delay.append(j + (-abs(i)))
        else:
            after_delay.append(j + (abs(i)))
    else:
        after_delay.append(j)
# print(' po delayu lista:', after_delay)
after_delay = sorted(after_delay)
# print('s po delayu lista:', after_delay)


current_time = datetime.now().time()
# changing current time to seconds
converted_time = ((current_time.hour * 60) - 60 +
                  current_time.minute) * 60 + current_time.second
# subtracting both data and converting to minutes
lst = [round((i - converted_time)/60) for i in after_delay]
outcome = [(i['routeId'], i['headsign'], j)
           for i, j in zip(data_zajezdnia02['departures'], lst)]
print(tabulate(outcome))

# ''' do poprawy: pomimo dodania delay nie zgadza się z tablicą na stronie'''
