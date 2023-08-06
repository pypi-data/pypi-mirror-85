#!/usr/bin/env python
# -*- coding: utf-8 -*-
# academic_german.py
"""Collection of German academic degrees combining wiki and drtitel."""
import os
import sys
import re

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))),
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)),
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from persontitles.academic_german_wiki import degrees_ger_wiki  # noqa
from persontitles.academic_german_drtitel import degrees_ger_drtitel  # noqa


def degrees_ger() -> list:
    try:
        with open('./persontitles/academic_german.txt', mode='r', encoding='utf-8') as fin:  # noqa
            DEGREES = fin.read().split('\n')
    except FileNotFoundError:
        DEGREES_WIKI = set(degrees_ger_wiki())
        DEGREES_DRTITEL = set(degrees_ger_drtitel())
        DEGREES = [dgr for dgr in DEGREES_WIKI | DEGREES_DRTITEL]

        with open('./persontitles/academic_german.txt', mode='a', encoding='utf-8') as fout:  # noqa
            fout.write('\n'.join(item for item in DEGREES))

    return DEGREES


def no_empty_space_in_degree(degrees):
    """
    Because there is no coherent writing of German degrees and some are written
    with empty spaces and some without, all degrees that potentially could
    have a space/s or other way round will be replicated with/without empty
    space/s.
    To make sure that writing a degree without empty spaces is covered, all
    degrees get reduced of their whitespace.
    """

    degrees_wo_empty_space = []
    for degree in degrees:
        degree = re.sub(r'\. ', '.', degree)
        degrees_wo_empty_space.append(degree)

    return degrees_wo_empty_space


def add_empty_space(degrees) -> list:
    """
    A degree like "Dipl.agr.biol." has no empty spaces between the grade of
    the degree (Dipl.) and its specification (agr. biol.). To make sure that
    both ways of writing are covered, the degree will be replicated as "Dipl.
    agr. biol.".
    """

    degrees_w_empty_space = []
    for degree in degrees:
        degree_w_space = ''
        dot_counter = 1
        max = len(degree) - 1
        for i, ch in enumerate(degree):
            if ch == '.' and i == max:
                if degree_w_space != '':
                    degrees_w_empty_space.append(degree_w_space.strip())
                else:
                    degrees_w_empty_space.append(degree.strip())
            elif ch == '.' and i < max:
                if degree[i + 1] not in ['-', ')']:
                    if degree_w_space == '':
                        degree_w_space = degree[:i + 1] + ' ' + degree[i + 1:]
                        dot_counter += 1
                    else:
                        degree_w_space = degree_w_space[:i+dot_counter] + ' ' + degree_w_space[i+dot_counter:]  # noqa
                        dot_counter += 1
            elif i == max:
                if degree_w_space != '':
                    degrees_w_empty_space.append(degree_w_space.strip())
                else:
                    degrees_w_empty_space.append(degree.strip())

    return degrees_w_empty_space


def german_abbrevs(DEGREES) -> list:
    """
    Because the aim of this module is to find the compounds of a person's name
    or degree or even peer title, the fact that German degrees are more often
    than not written with empty spaces between the degree and its specification
    makes it necessary to collect both those solitary specs like "rer.",
    "nat.", "oec.", and "med." (there are more), and also the degrees like
    "Dr." or "Dipl.".
    """

    degrees = add_empty_space(DEGREES)
    abbrevs = []

    for degree in degrees:
        elements = degree.split(' ')
        for element in elements:
            if element not in abbrevs:
                abbrevs.append(element)

    abbrevs = [element for element in abbrevs if element.strip()]
    return abbrevs


if __name__ == '__main__':
    DEGREES_WIKI = set(degrees_ger_wiki())
    DEGREES_DRTITEL = set(degrees_ger_drtitel())
    DEGREES = [dgr for dgr in DEGREES_WIKI | DEGREES_DRTITEL]
#    for i, degree in enumerate(sorted(DEGREES)):
#        print(i, degree)
    print()
    print('Count degrees from wiki:', len(DEGREES_WIKI))
    print('Count degrees from drtitel:', len(DEGREES_DRTITEL))

    print('Common degrees from both sets:', len(DEGREES_WIKI & DEGREES_DRTITEL))  # noqa
    print('Degrees only from wiki:', len(DEGREES_WIKI - DEGREES_DRTITEL))
    print('Degrees only from drtitel:', len(DEGREES_DRTITEL - DEGREES_WIKI))

    print('Sum of degrees of both sets:', len(DEGREES))

    degrees_wo = no_empty_space_in_degree(DEGREES)
    degrees_w = add_empty_space(degrees_wo)

    abbrevs = german_abbrevs(DEGREES)
    print('Number of abbreviations:', len(abbrevs))

    for degree in sorted(DEGREES):
        print(degree)
