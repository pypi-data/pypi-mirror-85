#!/usr/bin/env python
# -*- coding: utf-8 -*-
# academic_us.py
"""Collection of US academic degrees."""
import unicodedata

import requests
from bs4 import BeautifulSoup


def degrees_us():

    try:
        with open('./persontitles/academic_us.txt', mode='r', encoding='utf-8') as fin:  # noqa
            ACADEMIC = fin.read().split('\n')
    except FileNotFoundError:
        ACADEMIC = []
        ACADEMIC_1 = academic_degrees_1()
        degrees_1 = get_degrees_1(ACADEMIC_1)
        ACADEMIC_2 = academic_degrees_2()
        degrees_2 = get_degrees_2(ACADEMIC_2)
        degrees_2 = revise_degrees_2(degrees_2)
        abbrevs = _degrees()

        DEGREES = abbrevs + degrees_1 + degrees_2
        for abbr in DEGREES:
            abbr = unicodedata.normalize('NFKD', abbr)
            ACADEMIC.append(abbr)

        with open('./persontitles/academic_us.txt', mode='a', encoding='utf-8') as fout:  # noqa
            fout.write('\n'.join(item for item in set(ACADEMIC)))

    return set(ACADEMIC)


def academic_degrees_1() -> list:
    # collected from here:
    # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwih6eSh_uHsAhXRzqQKHXOuChAQFjAAegQIBBAC&url=https%3A%2F%2Fwww2.ed.gov%2Fabout%2Foffices%2Flist%2Fous%2Finternational%2Fusnei%2Fus%2Fmaster.doc&usg=AOvVaw3dwR4LfY5S4eN2jcGrkCA-
    # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwih6eSh_uHsAhXRzqQKHXOuChAQFjABegQIBhAC&url=https%3A%2F%2Fwww2.ed.gov%2Fabout%2Foffices%2Flist%2Fous%2Finternational%2Fusnei%2Fus%2Fbachelor.doc&usg=AOvVaw22CyjpUN5Z639pCUEqPpfu
    # https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiTiqrK_-HsAhUG_KQKHRW_AL0QFjACegQIBBAC&url=https%3A%2F%2Fwww2.ed.gov%2Fabout%2Foffices%2Flist%2Fous%2Finternational%2Fusnei%2Fus%2Fdoctorate.doc&usg=AOvVaw2PGDESFOCKJpbUol7vRaFq
    with open('./persontitles/resources/academic_us1.txt', mode='r', encoding='utf-8') as fin:  # noqa
        ACADEMIC_1 = fin.read().split('\n')
    return ACADEMIC_1


def academic_degrees_2() -> list:
    with open('./persontitles/resources/academic_us2.txt', mode='r', encoding='utf-8') as fin:  # noqa
        ACADEMIC_2 = fin.read().split('\n')
    return ACADEMIC_2


def get_degrees_1(ACADEMIC_1):
    degrees = []
    for degree in ACADEMIC_1:
        degree = degree.split('-')[0].strip()
        if len(degree.split('. ')) > 1:
            degree = degree.split('. ')[0]
        if ' or ' in degree:
            for ttle in degree.split(' or '):
                degrees.append(ttle.strip())
        elif len(degree) < 3:
            pass
        else:
            degrees.append(degree.strip())
    return degrees


def get_degrees_2(ACADEMIC_2):
    degrees = []
    for i, degree in enumerate(ACADEMIC_2):
        degree_brackets = degree.split('(')
        for degr in degree_brackets:
            if ')' in degr:
                abbr = degr.split(')')[0].strip()
                degrees.append(abbr)
    return degrees


def revise_degrees_2(degrees):
    rev_degrees = []
    for i, degree in enumerate(degrees):
        if '/' in degree:
            abbrevs = degree.split('/')
            for abbr in abbrevs:
                rev_degrees.append(abbr.strip())
        elif ',' in degree:
            abbrevs = degree.split(',')
            for abbr in abbrevs:
                if 'or ' in abbr:
                    abbr = abbr.split('or ')[-1].strip()
                rev_degrees.append(abbr.strip())
        elif ' or ' in degree:
            abbrevs = degree.split(' or ')
            for abbr in abbrevs:
                rev_degrees.append(abbr.strip())
        else:
            rev_degrees.append(degree)

    return rev_degrees


def get_degrees(soup):
    degrees = []
    script = soup.find_all('li')
    for line in script:
        strgline = str(line)
        splitline = strgline.split('-')
        if '.' in splitline[0][:8]:
            degrees.append(splitline[0].split('<li>')[-1])

    return degrees


def final_degrees(abbrevs):
    final_degrees = []
    for degree in abbrevs:
        if 'F&amp;TV' in degree:
            degree = 'B.F&TV.'
            final_degrees.append(degree)
        elif ' or ' in degree:
            abbrs = degree.split(' or ')
            for abbr in abbrs:
                final_degrees.append(abbr.strip())
        elif '</li>' in degree:
            degree = degree.split(' ')[0]
            final_degrees.append(degree.strip())
        else:
            final_degrees.append(degree.strip())
    return final_degrees


def _degrees():
    data = requests.get('https://abbreviations.yourdictionary.com/articles/degree-abbreviations.html')  # noqa
    soup = BeautifulSoup(data.text, 'lxml')
    degrees = get_degrees(soup)
    abbrevs = final_degrees(degrees)

    return abbrevs


if __name__ == '__main__':
    try:
        with open('./persontitles/academic_us.txt') as fin:
            ACADEMIC = fin.read().split('\n')
            for i, degree in enumerate(ACADEMIC):
                print(i, degree)
    except FileNotFoundError:
        ACADEMIC_US = degrees_us()
        for i, degree in enumerate(ACADEMIC_US):
            print(i, degree)
