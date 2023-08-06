#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_german.py
"""Tests for combined module."""
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))),
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)),
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from context import academic_german  # noqa


def test_no_file():
    os.remove('./persontitles/academic_german.txt')
    ACADEMIC = academic_german.degrees_ger()
    assert isinstance(ACADEMIC, list)


def test_academic_is_list():
    ACADEMIC = academic_german.degrees_ger()
    assert isinstance(ACADEMIC, list)


def test_degree_in_list():
    ACADEMIC = academic_german.degrees_ger()
    assert 'MBA' in ACADEMIC
    assert 'Dipl.-Inf.' in ACADEMIC
    assert 'Dr. e. h' not in ACADEMIC


def test_no_empty_space():
    DEGREES_W_SPACES = ['Dipl.-Ing. agr.', 'B. A.', 'lic. theol. säusel', 'Dr. med.']  # noqa
    DEGREES_WO_SPACES = academic_german.no_empty_space_in_degree(DEGREES_W_SPACES)  # noqa
    for degree in DEGREES_WO_SPACES:
        assert ' ' not in degree


def test_add_empty_space():
    DEGREES_WO_SPACES = ['Dipl.-Ing.agr.', 'B.A.', 'lic.theol.säusel', 'Dr.med.']  # noqa
    DEGREES_W_SPACES = academic_german.add_empty_space(DEGREES_WO_SPACES)
    for degree in DEGREES_W_SPACES:
        assert ' ' in degree


def test_handle_nones():
    DEGREES_WO_SPACES = ['Dr.']  # noqa
    DEGREES_W_SPACES = academic_german.add_empty_space(DEGREES_WO_SPACES)
    for degree in DEGREES_W_SPACES:
        assert degree != ''


def test_handle_no_dots():
    DEGREES_WO_SPACES = ['MBA']  # noqa
    DEGREES_W_SPACES = academic_german.add_empty_space(DEGREES_WO_SPACES)
    for degree in DEGREES_W_SPACES:
        assert degree != ''


def test_find_abbrevs():
    DEGREES = ['Dipl.-Ing. agr.', 'B. A.', 'lic. theol. säusel', 'Dr. med.']  # noqa
    abbrevs = academic_german.german_abbrevs(DEGREES)
    assert abbrevs == ['Dipl.-Ing.', 'agr.', 'B.', 'A.', 'lic.', 'theol.',
                       'säusel', 'Dr.', 'med.']
