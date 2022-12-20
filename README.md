# AdventOfCodeScraper
## Overview
This is a script that downloads the daily prompt and the data files for Eric Watsl's [Advent Of Code](https://adventofcode.com/) challenge. The script converts raw HTML into a Markdown file, and if configured correctly, will also download input data as a text file. If there is an ongoing AOC event, you can run the script each day to download the current day's AOC challenge. Otherwise, you can select from past AOC events (starting from 2015) and download the entire year's challenges.


# Usage and intended behavior

```python aoc_scrape.py```
- Download the current year's challenges. If the current year's AOC has not been released yet, the script will default to downloading the entire previous year's challenges.
- In the case of connection errors, the script will terminate.
- By default the script will generate folders for each year in the directory above where the `aoc_scrape.py` file is located.
  
```python aoc_scrape.py -c CONFIG_FILE```
- Specify a configuration file. Details below.
- This argument must be specified in order to retrieve input data files.

### Example Output File Structure

```
target_directory
├── 2022
│   ├── day1
│   │   ├── challenge.md
│   │   └── data.txt
│   ├── day2
│   │   ├── challenge.md
│   │   └── data.txt
│   ├── day3
│   │   ├── challenge.md
│   │   └── data.txt
│   └── ...
└── AdventOfCodeScraper
    ├── aoc_scraper.py
    ├── config.json
    ├── LICENSE
    ├── README.md
    └── scraper_tools.py  
```

## Configuration
This script can be configured using a `.json` file. A template file is provided with default values.

- `target_directory` is an optional `string` value that stores the directory where you intend to place the folder containing all AOC years.
  - Default value is `null`.
- `years` is an optional `array` value that stores the years that you wish to download for.
  - Default value is an empty array, `[]`, which will be interpreted as the current year.
  - You can specify multiple years at a time (`[2015,2016,...]`). Invalid years and duplicates will be ignored.
- `auth_token` is intended to be a `string` value, default value is `null`.
  - In order to get your input data for AOC, you need to authenticate with your own session cookie. [Follow the instructions here to obtain it](https://github.com/wimglenn/advent-of-code-wim/issues/1).
  - Append the session ID cookie, e.g. `0123456789abcdef...` to this field.
  - Default behavior if no token is provided is to not retrieve input data.

### `.json` Config File Format
```json
{
    "config": {
        "years": [],
        "targetDir": null
    }, 
    "auth": {
        "authToken": null
    }
}
```


## Dependencies
- Python Standard Library
- [Requests](https://pypi.org/project/requests/), `pip install requests`
- [pytz](https://pypi.org/project/pytz/), `pip install pytz`
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/), `pip install beautifulsoup4`
- [Markdownify](https://pypi.org/project/markdownify/), `pip install markdownify`