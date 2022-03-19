import requests
import re

url = 'https://query.wikidata.org/sparql'
query = '''
SELECT DISTINCT ?article ?label
WHERE {
  ?concept wdt:P31 ?type .
  ?type wdt:P279* wd:Q24034552 . # is a mathematical concept
  FILTER(NOT EXISTS { ?concept wdt:P585 ?something }) # does not have a point in time
  FILTER(NOT EXISTS { ?type wdt:P279* wd:Q1656682 }) # is not an event
  FILTER(NOT EXISTS { ?type wdt:P279* wd:Q309314 }) # is not a quantity
  ?article schema:about ?concept .
  ?article schema:inLanguage "en" .
  FILTER (SUBSTR(str(?article), 1, 25) = "https://en.wikipedia.org/") .
  ?concept rdfs:label ?label .
  FILTER(LANG(?label) = "en")
}
'''
r = requests.get(url, headers={'Accept': 'text/csv'}, params = {'query': query})
data = r.text

with open("temp.csv", "w", newline="", encoding='utf-8') as f:
    for x in data:
        if not x == '"':
            f.write(x)

with open("temp.csv", "r", encoding="utf-8") as fin:
    with open("math_concepts.csv", "w", encoding="utf-8") as fout:
        for row in fin:
            fout.write(re.sub(',(?!_)', ';', row, 1))