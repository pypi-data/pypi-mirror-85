#!/usr/bin/env python
# -*- coding: utf-8 -*-
# academic_german.py
"""Collection of German academic degrees as found on www.drtitel.de."""
import bs4
import re
import requests
import unicodedata
from bs4 import BeautifulSoup


def degrees_ger_drtitel() -> list:
    try:
        with open('./persontitles/academic_german_drtitel.txt', mode='r', encoding='utf-8') as fin:  # noqa
            DEGREES_DRTITEL = fin.read().split('\n')
    except FileNotFoundError:
        DEGREES_DRTITEL = dr_degrees()
        with open('./persontitles/academic_german_drtitel.txt', mode='a', encoding='utf-8') as fout:  # noqa
            fout.write('\n'.join(item for item in DEGREES_DRTITEL))

    return DEGREES_DRTITEL


def dr_degrees() -> list:
    soup = get_soup()
    lines = get_less_lines(soup)
    lines, degrees = get_part_of_degrees(lines)
    lines, degrees = get_colon_part_of_degrees(lines, degrees)
    lines, degrees = get_FH_part_of_degrees(lines, degrees)
    lines = get_splitted_degrees(lines)
    lines, degrees = get_degrees_with_dots(lines, degrees)
    lines, degrees = get_degrees_w_abbr(lines, degrees)
    lines, degrees = get_last_degrees(lines, degrees)
    degrees = declutter_degrees(degrees)
    degrees = normalize_degrees(degrees)

    return degrees


def get_soup() -> bs4.element.NavigableString:
    data = requests.get('https://www.drtitel.de/akademische-grade/')
    soup = BeautifulSoup(data.text, 'lxml')

    return soup


def get_less_lines(soup):
    lines = []
    for li in soup.find_all('li'):
        lines.append(li.get_text(strip=True))

    counter = 0
    for i, line in enumerate(lines):
        if line.startswith('B.A.'):
            counter = i
            break
    lines = lines[counter:]

    counter = 0
    for i, line in enumerate(lines):
        if line.startswith('DDr.'):
            counter = i
            break
    lines = lines[:counter + 1]

    print('length lines:', len(lines))
    return lines


def get_part_of_degrees(lines):
    degrees = []
    lines_before = lines[:]
    for line in lines_before:
        if line.startswith('…'):
            degree = line[2:]
            degrees.append(degree.strip())
            lines.remove(line)

    print('length degrees, lines:', len(degrees), len(lines))
    return lines, degrees


def get_colon_part_of_degrees(lines: list, degrees: list):
    lines_ = lines[:]
    for i, line in enumerate(lines_):
        # print(i, line.strip())
        if line.endswith('):'):
            degree = line.split('(')[-1][:-2]
            degrees.append(degree)
            lines.remove(line)

    print('length degrees, lines:', len(degrees), len(lines))
    return lines, degrees


def get_FH_part_of_degrees(lines, degrees):
    lines_ = lines[:]
    for i, line in enumerate(lines_):
        # print(i, line)
        if line.startswith('Dipl.') and '(FH)' in line:
            degree = line.split('(FH)')[0] + ' (FH)'
            degrees.append(degree)
            lines.remove(line)
        elif line.startswith('Dipl.') and '(DH)' in line:
            degree = line.split('(DH)')[0] + ' (DH)'
            degrees.append(degree)
            lines.remove(line)
        elif line.startswith('Dipl.') and '(t.o.)' in line:
            degree = line.split('(t.o.)')[0] + ' (t.o.)'
            degrees.append(degree)
            lines.remove(line)
    print('length degrees, lines:', len(degrees), len(lines))
    return lines, degrees


def get_splitted_degrees(lines):
    lines_ = lines[:]
    for i, line in enumerate(lines_):
        if '/' in line:
            splits = line.split('/')
            for split in splits:
                lines.append(split)
            lines.remove(line)
        elif 'oder' in line:
            splits = line.split('oder')
            for split in splits:
                lines.append(split)
            lines.remove(line)
        elif 'bzw.' in line:
            splits = line.split('bzw.')
            for split in splits:
                lines.append(split)
            lines.remove(line)

    print('length lines:', len(lines))

    return lines


def get_degrees_with_dots(lines, degrees):
    lines_ = lines[:]
    for i, line in enumerate(lines_):
        abbrevs = line.split(' ')
        if '.' in abbrevs[0] and len(abbrevs) > 1:
            if '.' in abbrevs[1]:
                pass
            elif 'Diplom' in line and '+ Fachrichtung' not in line:
                degree = line.split('Diplom')[0].strip()
                degrees.append(degree)
                lines.remove(line)
            elif '(engl.' in line:
                degree = line.split('(engl.')[0].strip()
                degrees.append(degree)
                lines.remove(line)
            else:
                degrees.append(abbrevs[0])
                lines.remove(line)
        elif '.' in abbrevs[0]:
            degrees.append(abbrevs[0])
            lines.remove(line)

    print('length degrees, lines:', len(degrees), len(lines))
    return lines, degrees


def get_degrees_w_abbr(lines, degrees):
    lines_ = lines[:]
    for i, line in enumerate(lines_):
        abbrevs = line.split(' ')
        degree = ''
        for abbr in abbrevs:
            if '.' not in abbr:
                if abbr.strip() in ['in', 'et', 'pol'] and degree != '':  # noqa
                    degree = degree + abbr + ' '
                elif degree != '':
                    degrees.append(degree)
                    lines.remove(line)
                    break
            elif 'DDr.' in abbr:
                degrees.append(abbr)
                degree = ''
            elif '.' in abbr:
                degree = degree + abbr + ' '

    print('length degrees, lines:', len(degrees), len(lines))
    return lines, degrees


def get_last_degrees(lines, degrees):
    lines_ = lines[:]
    for i, line in enumerate(lines_):
        if line.endswith(':'):
            degrees.append(line[:-1])
            lines.remove(line)
        elif line.strip().startswith('Dipl'):
            degrees.append(line)
            lines.remove(line)
        elif 'MLE' in line:
            degrees.append('MLE')
            lines.remove(line)
        elif 'BBA' in line:
            degrees.append('BBA')
            lines.remove(line)
        elif 'Master' in line:
            degrees.append(line)
            lines.remove(line)

    print('length degrees, lines:', len(degrees), len(lines))
    return lines, degrees


def declutter_degrees(degrees) -> list:
    decluttered_degrees = []
    for degree in degrees:
        while '  ' in degree:
            degree = re.sub('  ', ' ', degree)
        degree = degree.strip()
        if degree.endswith('):'):
            degree = degree[:-2]
        elif degree.endswith(':'):
            degree = degree.strip()[:-1]
        elif '+ Fachrichtung' in degree:
            continue
        if degree.strip().startswith('('):
            degree = degree[1:]
        decluttered_degrees.append(degree.strip())

    return decluttered_degrees


def normalize_degrees(degrees) -> list:
    normalized_degrees = []
    for degree in degrees:
        degree = unicodedata.normalize('NFKD', degree.strip())
        degree = degree.strip()
        if degree not in normalized_degrees:
            normalized_degrees.append(degree)

    return normalized_degrees


if __name__ == '__main__':
    degrees = degrees_ger_drtitel()
    for i, degree in enumerate(degrees):
        print(i, degree)
