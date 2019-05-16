"""
DiscoveryOne.py

Web scraper that collects screenplays from imsdb.com
"""
from bs4 import BeautifulSoup
import re
import requests
import os
import time


URL = 'https://www.imsdb.com'
GENRE = r'genre'
SCREENPLAYS = r'Movie Scripts'
SCREENPLAY = r'scripts.*\.html'
SCRIPT = 'SCRIPT'
HEADERS = requests.utils.default_headers()
HEADERS.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
MAX_TRIES = 5


def get_title(screenplay):
    """
    returns filename given screenplay href
    """
    pattern = re.compile(r'/scripts/(.*)')
    match = pattern.match(screenplay)
    return match.group(1)


def screenplay_exists(directory, screenplay):
    """
    checks if screenplay exists on disk
    """
    path = f'{directory}/{get_title(screenplay)}'
    return os.path.isfile(path)


def crawl(path, directory='.', pattern=GENRE):
    """
    traverses imsdb for screenplays
    """
    for i in range(MAX_TRIES):
        try:
            start = time.time()
            res = requests.get(URL+path, headers=HEADERS)
            response_delay = time.time() - start
            time.sleep(5*response_delay)
            soup = BeautifulSoup(res.text, 'html')
            break
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(20)
    
    if i == MAX_TRIES:
        return -1

    if pattern == SCRIPT:
        return str(soup.pre)

    elif pattern == SCREENPLAY:
        screenplay = soup.find(href=re.compile(pattern))
        if screenplay:
            screenplay = screenplay['href']
            if not screenplay_exists(directory, screenplay):
                script = crawl(screenplay, directory, SCRIPT)
                filename = os.path.join(directory, get_title(screenplay))
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(script)
            else:
                print(f'Skipping {screenplay}...')

    else:
        children = (tag
                    for tag
                    in soup.find_all(href=re.compile(pattern)))

        if pattern == GENRE:
            for genre in children:
                directory = genre.contents[0]
                print(directory)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                crawl(genre['href'], directory, SCREENPLAYS)

        elif pattern == SCREENPLAYS:
            for screenplay in children:
                print(screenplay.contents)
                crawl(screenplay['href'], directory, SCREENPLAY)


if __name__ == '__main__':
    crawl('/')
