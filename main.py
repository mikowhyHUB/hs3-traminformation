import requests
import json
from datetime import datetime
from tabulate import tabulate
'''
1. ściągnąć dane przez api
2. potrzebujemy trzy informacje wyświetlane na tablicy: tramwaj, w jaką stronę jedzie, szacowany czas przyjazdu
- czas przyjazdu będzie trzeba edytowac. Po pierwsze spieszy się o godzinę, po drugie chccemy by na tablicy wyswietlało nam się dane ile zostało do odjechania tramwaju
- czas przyjazdu będzie trzbea najprawdopodobniej odjąć naszą godz
- gdy czas przyjazdu wynosić bedzie <1, wtedy jakąś ikonkę printować zamiast czasu
- dodać dealy
3. Jako, ze interesują nas tramwaje w obydwie storny, musimy połączyć dwa url
4. Interesuje nas tylko np. 5 następnych tramwajów
5. Znalźć sposób na samouruchamianie się terminala. Chodzi o to, by się na wyświetlaczu sam wywoływał i aktualizował'''

url = requests.get(
    'https://ckan2.multimediagdansk.pl/departures?stopId=2030')
data = json.loads(url.text)


def converte_hrs_to_sec(item):
    return ((item[0] * 60) + item[1]) * 60 + item[2]


# to pewnie zrobi się jako funkcja
lst = [i['estimatedTime'][11:19].split(':') for i in data['departures']]
lst = [[int(i) for i in lst] for lst in lst]
lst = [converte_hrs_to_sec(lst[i]) for i in range(0, len(lst))]

current_time = datetime.now().time()
converted_time = ((current_time.hour * 60) - 60 +
                  current_time.minute) * 60 + current_time.second

lst = [round((i - converted_time)/60) for i in lst]

# for i, j in zip(data['departures'], lst):
#     # print(i['routeId'], i['headsign'] + '\t', j, sep='\t')
#

x = [(i['routeId'], i['headsign'], j) for i, j in zip(data['departures'], lst)]
print(tabulate(x))
