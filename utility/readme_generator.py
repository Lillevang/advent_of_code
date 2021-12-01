import requests
import bs4
import os
from bs4 import BeautifulSoup
from typing import List
from datetime import date


BASE_URL = 'https://adventofcode.com'


def format_code(tag: bs4.element.Tag) -> str:
    return f'`{tag.text}`'


def format_emphasis(tag: bs4.element.Tag) -> str:
    return f'**{tag.text}**'


def format_list(tag: bs4.element.Tag) -> str:
    list_str = '- '
    for _li in tag.contents:
        if _li.name == 'code':
            list_str += format_code(_li)
        elif _li.name == 'a':
            list_str += format_link(_li)
        else:
            list_str += _li
    return f'{list_str}'


def format_link(tag: bs4.element.Tag) -> str:
    pass

def convert_paragraph_with_emphasis(tag: bs4.element.Tag) -> str:
    output = ''
    for _ in tag.contents:
        if _.name == 'em':
            output += format_emphasis(_)
        elif _.name == 'code':
            output += format_code(_)
        elif _.name == 'span':
            output += _.text
        elif _.name == 'li':
            output += format_list(_)
        elif _.name == 'a':
            output += format_link(_)
        else:
            output += _
    return output


def convert_html_to_markdown(tag: bs4.element.Tag) -> str:
    html_to_markdown_converter = {'h1': '#', 'h2': '##'}
    if tag.name in html_to_markdown_converter.keys():
        _ = f'{html_to_markdown_converter[tag.name]} {tag.text}\n'
    elif tag == '\n':
        _ = tag
    elif tag.name == 'pre':
        _ = f'```\n{tag.text}\n```'
    else:
        _ = convert_paragraph_with_emphasis(tag)
    return _


def get_daily_description(base_url: str, year: str, day: str) -> List[str]:
    lines = []
    res = requests.get(f'{base_url}/{year}/day/{day}')
    article = BeautifulSoup(res.text, 'html.parser').article
    for child in article.children:
        lines.append(convert_html_to_markdown(child) + '\n')
    return lines


def create_dirs_if_not_exists(year: str, day: str) -> None:
    if not os.path.isdir(f'../{year}'):
        os.mkdir(f'../{year}')
    if not os.path.isdir(f'../{year}/{day}'):
        os.mkdir(f'../{year}/{day}')


def save_markdown_file(markdown_lines: List[str], year: str, day: str) -> None:
    if int(day) < 10:
        day = f'0{day}'
    create_dirs_if_not_exists(year, day)
    path = f'../{year}/{day}/readme.md'
    with open(path, 'w') as file:
        print(f'Writing to file: {path}')
        for l in markdown_lines:
            file.write(l)


def main():
    day_lim = 25
    for year in range(2015, 2022):
        if year == 2021:
            day_lim = date.today().day + 1
        for day in range(1, day_lim):
            save_markdown_file(get_daily_description(BASE_URL, str(year), str(day)), str(year), str(day))
        # TODO download input and handle part 2 (hidden behind login).

if __name__ == '__main__':
    main()
