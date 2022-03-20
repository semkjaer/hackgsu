import requests

url = 'https://query.wikidata.org/sparql'
query = '''
SELECT ?article ?label
WHERE {
  ?party wdt:P31 wd:Q7278 .
  ?article schema:about ?party .
  ?article schema:inLanguage "en" .
  FILTER (SUBSTR(str(?article), 1, 25) = "https://en.wikipedia.org/") .
  ?party rdfs:label ?label .
  FILTER(LANG(?label) = "en")
}
'''
r = requests.get(url, headers={'Accept': 'text/csv'}, params = {'query': query})
data = r.text

with open("parties.csv", "w", newline="", encoding='utf-8') as f:
    for x in data:
        if not x == '"':
            f.write(x)