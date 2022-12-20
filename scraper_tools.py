import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

AOC_URL = 'https://adventofcode.com'

def download_day(year, day, auth_token) -> tuple:
    url = f'{AOC_URL}/{year}/day/{day}'
    raw = requests.get(url, timeout=3)

    if raw.status_code != 200:
        print(f'AOC {year} Day {day} could not be downloaded')
        return False
    
    soup = BeautifulSoup(raw.content, 'html.parser')
    article = md(str(soup.find('article')))
    article = article.split('\n')
    article[0] = '#' + article[0].replace('-', '')
    article[1] = f'> [adventofcode.com/{year}/day/{day}](url)'
    content = '\n'.join(article)

    if auth_token is not None:
        try:
            raw = requests.get(f'{url}/input', timeout=3, cookies={'session': auth_token}).content
            data = str(raw.decode('utf8'))

        except:
            print(f'AOC {year} Day {day} input data could not be downloaded')
            data = None
    else:
        data = None

    return (content, data)

def download_year(year, auth_token, start=1, stop=26) -> list:
    challenges = {}

    for day in range(start, stop + 1):
        download = download_day(year, day, auth_token)
        
        if download is False:
            break
        else:
            challenges[str(day)] = download

    if len(challenges) == 0:
        return False
        
    return challenges
