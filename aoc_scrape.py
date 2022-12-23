import sys
import os
import argparse
import datetime
import json
from pytz import timezone
import scraper_tools as st

parser = argparse.ArgumentParser()
parser.add_argument('-c', help='Specify settings file location, defaults to settings.json in current directory')
args = parser.parse_args()

if args.c:
    CONFIG_FILE = args.c
else:
    CONFIG_FILE = False


AOC_FIRST_YEAR = 2015
TZ = timezone('EST')

now = datetime.datetime.now(tz=TZ)
if now.month == 12:
    AOC_CURR_YEAR = now.year
else:
    AOC_CURR_YEAR = now.year - 1

if CONFIG_FILE is not False:
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    except IOError as exc:  
        raise IOError(f'Unable to open {CONFIG_FILE}, check file location.') from exc

    target_dir = config['config']['targetDir']
    years = set(config['config']['years'])
    auth_token = config['auth']['authToken']

    # sanity checking
    if target_dir is None:
        print('No target directory specified, downloading files in directory one level up...')
        target_dir = '..'
    elif target_dir[-1] == '/':
        target_dir = target_dir[:-1]

    if auth_token is None:
        print('Session cookie not supplied, no data files will be retrieved...')

    sorted_years = sorted(years.intersection(set(range(AOC_FIRST_YEAR, AOC_CURR_YEAR + 1))))

    if len(years) == 0:
        print('No valid years supplied, defaulting to retrieving only the most recent AOC year...')
        sorted_years = [AOC_CURR_YEAR]
else:
    target_dir = '..'
    auth_token = None
    sorted_years = [AOC_CURR_YEAR]



for year in sorted_years:
    if year < now.year:
        curr_year = st.download_year(year, auth_token)
    elif year == now.year:
        stop = now.day if now.day < 26 else 26
        start = now.day if now.day < 26 else 26
        for day in range(stop, 0, -1):
            if os.path.isdir(f'{target_dir}/{year}/day{start - 1}') is True:
                if stop == day:
                    print("No new challenge is out yet! Please run the script again later")
                    sys.exit()
                break
            start = day - 1
        
        curr_year = st.download_year(year, auth_token, start, stop)

    if curr_year is not False:
        for day in curr_year:
            os.makedirs(f'{target_dir}/{year}/day{day}')

            with open(f'{target_dir}/{year}/day{day}/challenge.md', 'w', encoding='utf8') as challenge:
                challenge.write(curr_year[day][0])
            
            if curr_year[day][1] is not None:
                with open(f'{target_dir}/{year}/day{day}/data.txt','w',encoding='utf8') as data:
                    data.write(curr_year[day][1])
