#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_peertitles.py
"""Tests for peertitles."""
import os

from context import peertitles


def test_peertitles_is_dict():
    os.remove('./persontitles/peertitles.json')
    PEERTITLES = peertitles.peertitles()
    assert isinstance(PEERTITLES, dict)


def test_keys():
    LANGUAGES = [
        'German',
        'Latin',
        'French',
        'Italian',
        'Spanish',
        'English',
        'Danish',
        'Greek',
        'Dutch',
        'Czech',
        'Hungarian',
        'Russian',
        'Persian',
        'Arab',
        'Chinese',
        'Amharic',
    ]

    PEERTITLES = peertitles.peertitles()
    for k, v in PEERTITLES.items():
        assert k in LANGUAGES
