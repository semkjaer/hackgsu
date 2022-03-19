import requests
import re

# queries wikidata.org SPARQL endpoint for mathematical concepts
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
        # there's random cases of " in text so we remove those
        if not x == '"':
            f.write(x)

# default format uses ',' as a delimiter but sometimes there's a ',' in a url so we change the delimiter to ';'
with open("temp.csv", "r", encoding="utf-8") as fin:
    with open("math_concepts.csv", "w", encoding="utf-8") as fout:
        for row in fin:
            # cases of ',' in urls are always followed by '_' so we take the first instance of ',' that isn't followed by '_' and replace it
            fout.write(re.sub(',(?!_)', ';', row, 1))
