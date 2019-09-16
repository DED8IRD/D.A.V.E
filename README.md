# D.A.V.E.
Meet DAVE, the screenwriting bot. 
DAVE generates formatted screenplays from other screenplays.


## Install
```
pip install davebot
```

## Use
### Stanley module
#### Generate screenplays
`DAVE.nlp.Stanley` uses all the modules below (except web scraping) to generate formatted screenplays (PDF and plaintext).

Example:
```py
from DAVE.nlp.Stanley import Stanley
characters = ['HAL', 'DAVE', 'Stanley Kubrick', 'Discovery One', 
              'Arthur C. Clarke', 'The Sentinel']
source = ['2001-A-Space-Odyssey.txt', '2012.txt']

director = Stanley(source, characters, destination='output', title='2013', author='DAVE')
director.direct(length=100)
```

DAVE will create two files in the `destination` directory: `<title>.pdf` and `<title>.txt`.

### Scraper module
#### Scraping Screenplays
`DAVE.scraper.DiscoveryOne` scrapes from IMSDB using BeautifulSoup
```py
from DAVE.scraper import DiscoveryOne, Sentinel
DiscoveryOne.crawl(path, directory='.', pattern=GENRE):
```

#### Parse
`DAVE.scraper.Sentinel`  and parses screenplays into subsections: headings, transitions, actions, parentheticals, and dialogue, to be further prepared into Markov models.
```py
Sentinel.parse(*sources, destination='.', write=True)
```

Or, parse recursively using `Sentinel.parse_directory`
```py
Sentinel.parse_directory(source='.', destination='parsed_categories', genre='All')`
```

### NLP module
#### Serialize markov models
`DAVE.nlp.HAL` generates Markov chains from the parsed categories made by `DAVE.scraper.Sentinel` and serializes the models into JSON.

To create the Markov models:
```py
from DAVE.nlp.HAL import HAL
HAL.generate_models(source='parsed_categories', destination='.')
```


## Inspiration
#### A Space Odyssey
Inspiration from the name D.A.V.E. came from Stanley Kubrick's masterpiece film *2001: A Space Odyssey*. The names of this package's modules all reflect characters, creators, texts, and important people involved in A Space Odyssey. 


#### Sunspring
The original inspiration for this project comes from a short science fiction film: *Sunspring*.

Description (from Ars Technica):

> In the wake of Google's AI Go victory, filmmaker Oscar Sharp turned to his technologist collaborator Ross Goodwin to build a machine that could write screenplays. They created "Jetson" and fueled him with hundreds of sci-fi TV and movie scripts. Building a team including Thomas Middleditch, star of HBO's Silicon Valley, they gave themselves 48 hours to shoot and edit whatever Jetson decided to write.


<a href="http://www.youtube.com/watch?feature=player_embedded&v=LY7x2Ihqjmc" target="_blank"><img src="http://img.youtube.com/vi/LY7x2Ihqjmc/0.jpg" 
alt="Sunspring Short Film" width="240" height="180" border="10" /></a>

Click the image above to see the full video.
