#!/usr/bin/env python
# -*- coding: utf-8 -*-
# academic_uk.py
"""Collection of UK academic degrees."""
import unicodedata

import requests
from bs4 import BeautifulSoup


def degrees_uk() -> list:
    try:
        with open('./persontitles/academic_uk.txt', mode='r', encoding='utf-8') as fin:  # noqa
            DEGREES = fin.read().split('\n')
    except FileNotFoundError:
        DEGREES = uk_degrees()
        with open('./persontitles/academic_uk.txt', mode='a', encoding='utf-8') as fout:  # noqa
            fout.write('\n'.join(item for item in DEGREES))
    return DEGREES


def uk_degrees():
    data = requests.get('https://en.wikipedia.org/wiki/British_degree_abbreviations')  # noqa
    soup = BeautifulSoup(data.text, 'lxml')
    lines = get_lines(soup)
    uk_degrees = []
    for i, degree in enumerate(lines):
        if i > 19 and i < 440:
            uk_degrees.append(degree)
    abbrevs = strip_degrees(uk_degrees)
    fnl_degrees = final_degrees(abbrevs)
    degrees = normalize_degrees(fnl_degrees)

    return degrees


def get_lines(soup):
    lines = []
    for li in soup.find_all('li'):
        values = [li.get_text(strip=True)]
        lines.append(values[0])
    return lines


def strip_degrees(degrees) -> list:
    abbrevs = []
    for i, degree in enumerate(degrees):
        abbr = degree.split('-')[0].strip()
        abbrevs.append(abbr.strip())
    return abbrevs


def final_degrees(abbrevs):
    final_degrees = []
    for abbr in abbrevs:
        if ' or ' in abbr:
            abbrs = abbr.split('or')
            for ab in abbrs:
                final_degrees.append(ab.strip())
        elif ',' in abbr:
            abbrs = abbr.split(',')
            for ab in abbrs:
                final_degrees.append(ab.strip())
        elif ') ' in abbr:
            abbrs = abbr.split(') ')
            ab = abbrs[0].strip()
            if ab[-1] != ')':
                ab = ab + ')'
            final_degrees.append(ab)
        else:
            final_degrees.append(abbr.strip())

    return final_degrees


def normalize_degrees(degrees):
    DEGREES = []
    for abbr in set(degrees):
        abbr = unicodedata.normalize('NFKD', abbr)
        DEGREES.append(abbr)

    return DEGREES


if __name__ == '__main__':
    ACADEMIC_UK = degrees_uk()
    for i, degree in enumerate(ACADEMIC_UK):
        print(i, degree)
