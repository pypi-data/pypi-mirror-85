#!/usr/bin/env python
# -*- coding: utf-8 -*-
# academic_german_wiki.py
"""Collection of German academic degrees listed in Wikipedia."""
# import itertools
import requests
import unicodedata

from bs4 import BeautifulSoup


def degrees_ger_wiki() -> list:
    try:
        with open('./persontitles/academic_german_wiki.txt', mode='r', encoding='utf-8') as fin:  # noqa
            DEGREES = fin.read().split('\n')
    except FileNotFoundError:
        DEGREES = _degrees()
        with open('./persontitles/academic_german_wiki.txt', mode='a', encoding='utf-8') as fout:  # noqa
            fout.write('\n'.join(item for item in DEGREES))

    return DEGREES


def get_lines(soup) -> list:
    lines = []
    for tr in soup.find_all('tr'):
        line = [td.text for td in tr.find_all('td')]
        try:
            if line[0].startswith('...'):
                pass
            else:
                lines.append(line[0].strip())
        except IndexError:
            # print("IndexError:", values)
            pass
    return lines


def split_lines(lines) -> list:
    lines_with_added_splits = []

    for line in lines:
        line = line.strip()
        if '/Kunstvermittlung' in line:
            lines_with_added_splits.append(line)
        elif '/' in line:
            splits = line.split('/')
            for split in splits:
                lines_with_added_splits.append(split.strip())
        elif 'oder' in line:
            splits = line.split('oder')
            for split in splits:
                lines_with_added_splits.append(split.strip())
        elif 'bzw.' in line:
            splits = line.split('bzw.')
            for split in splits:
                lines_with_added_splits.append(split.strip())
        else:
            lines_with_added_splits.append(line)

    return lines_with_added_splits


def declutter_lines(lines) -> list:
    lines_wo_clutter = []

    for line in lines:
        if line.endswith(']'):
            line = line.split('[')[0].strip()
            lines_wo_clutter.append(line)
        elif line.endswith(')'):
            bracket_content = line.split('(')[-1]
            if bracket_content.startswith('M') and bracket_content != 'Med.)':
                lines_wo_clutter.append(bracket_content[:-1])
            else:
                lines_wo_clutter.append(line)
        else:
            lines_wo_clutter.append(line)

    return lines_wo_clutter


def lines_wo_brackets(lines) -> list:
    lines_wo_brackets = []

    for line in lines:
        splits = line.split('(')
        if len(splits) > 1:
            bracket_content = splits[-1].strip()
            if bracket_content[:-1] in ['FH', 'DH', 't.o.', 'Med.']:
                lines_wo_brackets.append(line)
            elif '.' not in bracket_content:
                lines_wo_brackets.append(splits[0].strip())
            elif bracket_content.endswith('Dr.)'):
                lines_wo_brackets.append(splits[0].strip())
                lines_wo_brackets.append(bracket_content[:-1])
            else:
                lines_wo_brackets.append(splits[0].strip())
                lines_wo_brackets.append(bracket_content)
        elif line.endswith('])'):
            pass
        else:
            lines_wo_brackets.append(line)

    return lines_wo_brackets


def final_degrees(lines_wo_brackets) -> list:
    lines_ = lines_wo_brackets
    lines_wo_brackets = []
    for line in lines_:
        if '(' in line:
            lines_wo_brackets.append(line)
        # because there is no bracket pair (otherwise len(splits) would have
        # been greater than 1, it is possible to look for solitary brackets
        elif line.endswith(')'):
            if 'altertümlich' in line:
                pass
            else:
                lines_wo_brackets.append(line[:-1])
        else:
            lines_wo_brackets.append(line)

    return lines_wo_brackets


def normalize_degrees(degrees) -> list:
    normalized_degrees = []
    for degree in set(degrees):
        degree = unicodedata.normalize('NFKD', degree)
        normalized_degrees.append(degree)

    return normalized_degrees


def _degrees() -> list:
    data = requests.get('https://de.wikipedia.org/wiki/Liste_akademischer_Grade_(Deutschland)')  # noqa
    soup = BeautifulSoup(data.text, 'lxml')
    lines = get_lines(soup)
    lines = split_lines(lines)
    lines = declutter_lines(lines)
    degrees = lines_wo_brackets(lines)
    degrees = final_degrees(degrees)
    normalized_degrees = normalize_degrees(degrees)

    return normalized_degrees


if __name__ == '__main__':
    ACADEMIC = degrees_ger_wiki()
    for i, degree in enumerate(sorted(ACADEMIC)):
        print(i, degree)
