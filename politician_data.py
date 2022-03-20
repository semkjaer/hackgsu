import requests

url = 'https://query.wikidata.org/sparql'
query = '''
SELECT ?article ?label
WHERE {
  ?politician wdt:P106 wd:Q82955 .
  ?article schema:about ?politician .
  ?article schema:inLanguage "en" .
  FILTER (SUBSTR(str(?article), 1, 25) = "https://en.wikipedia.org/") .
  ?politician rdfs:label ?label .
  FILTER(LANG(?label) = "en")
}
'''
r = requests.get(url, headers={'Accept': 'text/csv'}, params = {'query': query})
data = r.text

with open("politicians.csv", "w", newline="", encoding='utf-8') as f:
    for x in data:
        if not x == '"':
            f.write(x)