#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_degrees.py
"""Tests for academic degrees."""
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))),
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)),
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from context import academic_degrees  # noqa


def test_no_file():
    os.remove('./persontitles/degrees.json')
    ACADEMIC = academic_degrees.degrees_ger()
    assert isinstance(ACADEMIC, list)


def test_degrees_is_dict():
    DEGREES = academic_degrees.degrees()
    assert isinstance(DEGREES, dict)


def test_keys():
    DEGREES = academic_degrees.degrees()
    for k, v in DEGREES.items():
        assert k in ['D', 'UK', 'US', 'german_abbrevs']
