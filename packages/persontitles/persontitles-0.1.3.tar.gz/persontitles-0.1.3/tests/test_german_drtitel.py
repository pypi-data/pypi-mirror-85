#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_german_drtitel.py
"""Tests for drtitel module."""
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))),
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)),
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from context import academic_german_drtitel  # noqa


def test_filenotfound():
    os.remove('./persontitles/academic_german_drtitel.txt')
    ACADEMIC = academic_german_drtitel.degrees_ger_drtitel()
    assert isinstance(ACADEMIC, list)


def test_academic_is_list():

    ACADEMIC = academic_german_drtitel.degrees_ger_drtitel()
    assert isinstance(ACADEMIC, list)


def test_degree_in_list():

    ACADEMIC = academic_german_drtitel.degrees_ger_drtitel()
    assert 'MBA' in ACADEMIC
    assert 'Dipl.-Inf.' in ACADEMIC
    assert 'Dr. e. h' not in ACADEMIC
