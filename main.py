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
- znalezc time z godzina wczesniej by mozna uzyc drugi raz tej samej funkcji
3. Jako, ze interesują nas tramwaje w obydwie storny, musimy połączyć dwa url
4. Interesuje nas tylko np. 5 następnych tramwajów
5. Znalźć sposób na samouruchamianie się terminala. Chodzi o to, by się na wyświetlaczu sam wywoływał i aktualizował'''

url = requests.get(
    'https://ckan2.multimediagdansk.pl/departures?stopId=2030')
data = json.loads(url.text)


def converte_hrs_to_sec(item):
    return ((item[0] * 60) + item[1]) * 60 + item[2]


# def delay_tramp(data):
#     test = [i['delayInSeconds'] for i in data['departures']]
#     print(test)
#     y = []
#     for i in test:
#         if i != None:
#             if i < 0:
#                 y.append(abs(i))
#             else:
#                 y.append(-abs(i))
#     return (y)


# print(delay_tramp(data))


lst = [i['estimatedTime'][11:19].split(':') for i in data['departures']]
lst = [[int(i) for i in lst] for lst in lst]
lst = [converte_hrs_to_sec(lst[i]) for i in range(0, len(lst))]
# converted arrival estimated time list in seconds
print('bez delay: ', lst)
test = [i['delayInSeconds'] for i in data['departures']]
print('lista dealy: ', test)
y = []
for i, j in zip(test, lst):
    if i != None:
        if i < 0:
            y.append(j + i)
        else:
            y.append(j - i)
    else:
        y.append(j)

print('lista po delay: ', y)


current_time = datetime.now().time()
converted_time = ((current_time.hour * 60) - 60 +
                  current_time.minute) * 60 + current_time.second

lst = [round((i - converted_time)/60) for i in lst]


# x = [(i['routeId'], i['headsign'], j)
#      for i, j in zip(data['departures'], lst)]
# # dodać listę x do y(zajezdnia 01)
# print(tabulate(x))

# lst2 = [round((i - converted_time)/60) for i in y]
# z = [(i['routeId'], i['headsign'], j)
#      for i, j in zip(data['departures'], lst2)]
# # dodać listę x do y(zajezdnia 01)
# print(tabulate(z))
