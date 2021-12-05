import requests
import os
import sys
import json
from bs4 import BeautifulSoup
from datetime import date, datetime
from typing import List, Dict

def read_session() -> Dict[str, str]:
    with open('../config/login.json', 'r') as file:
        return json.load(file)

USER_AGENT = {"User-Agent": "advent-of-code-data v1.1.1"} # Stolen from https://github.com/wimglenn/advent-of-code-data/
SESSION = read_session()
BASE_URL = 'https://adventofcode.com' # /year/day/date/input


def get_webpage(year: str, day: str) -> List[str]:
    res = requests.get(url = f'{BASE_URL}/{year}/day/{day}', cookies=SESSION, headers=USER_AGENT)
    articles = [str(_) for _ in BeautifulSoup(res.text, 'html.parser').find_all('article')]
    return articles

def get_data(year: str, day: str) -> str:
    return requests.get(url = f'{BASE_URL}/{year}/day/{day}/input', cookies=SESSION, headers=USER_AGENT).text

def create_dirs_if_not_exists(year: str, day: str) -> None:
    if not os.path.isdir(f'../{year}'):
        os.mkdir(f'../{year}')
    if not os.path.isdir(f'../{year}/{day}'):
        os.mkdir(f'../{year}/{day}')


def save_markdown_file(content: List[str], year: str, day: str) -> None:
    if int(day) < 10:
        day = f'0{day}'
    create_dirs_if_not_exists(year, day)
    path = f'../{year}/{day}/readme.md'
    with open(path, 'w') as file:
        print(f'Writing to file: {path}')
        for part in content:
            file.write(part)


def save_data_file(content: str, year: str, day: str) -> None:
    if int(day) < 10:
        day = f'0{day}'
    path = f'../{year}/{day}/input'
    with open(path, 'w') as file:
        print(f'Writing to file: {path}')
        file.write(content)


def scrape_day(year: str, day: str) -> None:
    pages = get_webpage(year, day)
    save_markdown_file(pages, year, day)
    data = get_data(year, day)
    save_data_file(data, year, day)


def scrape_all() -> None:
    cur_date = date.today()
    max_day = 26
    for year in range(2015, cur_date.year + 1):
        if year == cur_date.year and cur_date.month == 12 and cur_date.day < 26:
            max_day = cur_date.day + 1
        for day in range(1, max_day):
            scrape_day(str(year), str(day))


def main():
    try:
        option = sys.argv[1]
        if option == 'all':
            scrape_all()
        elif option == 'today':
            _today = date.today()
            scrape_day(str(_today.year), str(_today.day))
        else:
            _date = datetime.strptime(option, '%Y-%m-%d')
            assert(_date.month == 12 and _date.day < 26 and _date.year >= 2015 and _date.year <= _date.today().year)
            scrape_day(str(_date.year), str(_date.day))
    except IndexError:
        print('Must provide one of the following arguments:\nall\ntoday\ndate of format yyyy-mm-dd (must be a date in december')
    except ValueError:
        print('Must provide date in format: yyyy-mm-dd')


if __name__ == '__main__':
    main()
