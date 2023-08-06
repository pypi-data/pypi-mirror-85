#!/usr/bin/env python
# -*- coding: utf-8 -*-
# academic_austria.py
"""Collection of German academic degrees."""
import unicodedata

import requests
from bs4 import BeautifulSoup


def degrees_austria() -> set:
    try:
        with open('./persontitles/academic_austrian.txt', mode='r', encoding='utf-8') as fin:  # noqa
            ACADEMIC = fin.read().split('\n')
    except FileNotFoundError:
        degrees = _degrees()
        ACADEMIC = []
        for abbr in degrees:
            ACADEMIC.append(abbr)
        with open('./persontitles/academic_austrian.txt', mode='a', encoding='utf-8') as fout:  # noqa
            fout.write('\n'.join(item for item in set(ACADEMIC)))

    return set(ACADEMIC)


def get_degrees(soup):
    degrees = []
    for tr in soup.find_all('tr'):
        values = [td.text for td in tr.find_all('td')]
        try:
            degrees.append(values[0])
        except IndexError:
            # print("IndexError:", values)
            pass
    return degrees


def strip_degrees(degrees) -> list:
    abbrevs = []
    for degree in degrees:
        if '(' in degree:
            bracket_content = degree.split('(')[-1]
            if 'Master' in degree:
                degree = bracket_content.split(')')[0]
                abbrevs.append(degree)
            elif 'FH' in bracket_content:
                degree = degree.split(')')[0]
                degree = degree + ')'
                abbrevs.append(degree)
            elif 'Med.' in bracket_content:
                degree = degree.split(')')[0]
                degree = degree + ')'
                abbrevs.append(degree)
            elif 't.o.' in bracket_content:
                degree = degree.split(')')[0]
                degree = degree + ')'
                abbrevs.append(degree)
            else:
                degree = degree.split('(')[0]
                if '/' in degree:
                    for ttle in degree.split('/'):
                        abbrevs.append(ttle)
                else:
                    abbrevs.append(degree)
        elif len(set(degree)) == 1:
            pass
        elif 'oder' in degree:
            for ttle in degree.split('oder'):
                abbrevs.append(ttle.strip())
        elif '/' in degree:
            for ttle in degree.split('/'):
                if ttle == 'Kunstvermittlung':
                    abbrevs.append('Dipl. Kunstpädagogik/Kunstvermittlung')
                else:
                    abbrevs.append(ttle.strip())
        elif '[' in degree:
            abbrevs.append(degree.split('[')[0])
        else:
            abbrevs.append(degree)

    return abbrevs


def final_degrees(abbrevs):
    final_degrees = []
    for abbr in abbrevs:
        # get rid of unicode's \xa0 for the empty spaces
        # https://stackoverflow.com/a/34669482/6597765
        abbr = unicodedata.normalize('NFKD', abbr)
        if len(set(abbr)) == 1:
            pass
        elif '[' in abbr:
            abbr = abbr.split('[')[0]
            final_degrees.append(abbr.strip())
        elif '...' in abbr:
            pass
        else:
            final_degrees.append(abbr.strip())
    return final_degrees


def _degrees():
    urls = ['https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/1/Seite.1730512.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/1/Seite.1730513.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/1/Seite.1730514.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/3/Seite.1730515.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/3/Seite.1730516.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/3/Seite.1730522.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/4/Seite.1730517.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/4/Seite.1730518.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/Seite.1730507.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/2.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/2/Seite.1730519.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/Seite.1730505.html',  # noqa
            'https://www.oesterreich.gv.at/themen/leben_in_oesterreich/titel_und_auszeichnungen/1/Seite.1730508.html'  # noqa
            ]
    data = requests.get(urls[0])  # noqa
    soup = BeautifulSoup(data.text, 'lxml')
    degrees = get_degrees(soup)
    abbrevs = strip_degrees(degrees)
    degrees = final_degrees(abbrevs)

    return degrees


if __name__ == '__main__':
    ACADEMIC = degrees_austria()
    for i, degree in enumerate(ACADEMIC):
        print(i, degree)
