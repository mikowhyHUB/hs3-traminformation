import requests
import json
'''
1. ściągnąć dane przez api
2. potrzebujemy trzy informacje wyświetlane na tablicy: tramwaj, w jaką stronę jedzie, szacowany czas przyjazdu
- czas przyjazdu będzie trzeba edytowac. Po pierwsze spieszy się o godzinę, po drugie chccemy by na tablicy wyswietlało nam się dane ile zostało do odjechania tramwaju
- czas przyjazdu będzie trzbea najprawdopodobniej odjąć naszą godz
- gdy czas przyjazdu wynosić bedzie <1, wtedy jakąś ikonkę printować zamiast czasu
3. Jako, ze interesują nas tramwaje w obydwie storny, musimy połączyć dwa url
4. Interesuje nas tylko np. 5 następnych tramwajów
5. Znalźć sposób na samouruchamianie się terminala. Chodzi o to, by się na wyświetlaczu sam wywoływał i aktualizował'''

url = requests.get(
    'https://ckan2.multimediagdansk.pl/departures?stopId=2030')
data = json.loads(url.text)
