# D.A.V.E.
Meet DAVE, the screenwriting bot

## Stanley module
### Generate screenplays
`DAVE.nlp.Stanley` uses all the modules below (except web scraping) to generate formatted screenplays (PDF and plaintext).

Example:
```py
from DAVE.nlp.Stanley import Stanley
characters = ['HAL', 'DAVE', 'Stanley Kubrick', 'Discovery One', 
              'Arthur C. Clarke', 'The Sentinel']
source = ['2001-A-Space-Odyssey.txt']

director = Stanley(source, characters, destination='output', title='2002', author='DAVE')
director.direct(length=100)
```

## Scraper module
### Scraping Screenplays
`Dave.scraper.DiscoveryOne` scrapes from IMSDB using BeautifulSoup
```py
from DAVE.scraper import DiscoveryOne, Sentinel
DiscoveryOne.crawl(path, directory='.', pattern=GENRE):
```

### Parse
`DAVE.scraper.Sentinel`  and parses screenplays into subsections: headings, transitions, actions, parentheticals, and dialogue, to be further prepared into Markov models.
```py
Sentinel.parse(*sources, destination='.', write=True)
```

Or, parse recursively using `Sentinel.parse_directory`
```py
Sentinel.parse_directory(source='.', destination='parsed_categories', genre='All')`
```

## NLP module
### Serialize markov models
`DAVE.nlp.HAL` generates Markov chains from the parsed categories made by `DAVE.scraper.Sentinel` and serializes the models into JSON.

To create the Markov models:
```py
from DAVE.nlp.HAL import HAL
HAL.generate_models(source='parsed_categories', destination='.')
```
