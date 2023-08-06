#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_uk.py
"""Tests for academic_uk module."""
import os

from context import academic_uk


def test_filenotfound():
    os.remove('./persontitles/academic_uk.txt')
    ACADEMIC = academic_uk.degrees_uk()
    assert isinstance(ACADEMIC, list)


def test_academic_is_set():

    ACADEMIC = academic_uk.degrees_uk()
    assert isinstance(ACADEMIC, list)


def test_degree_in_list():

    ACADEMIC = academic_uk.degrees_uk()
    assert 'MBA' in ACADEMIC
    assert 'BSc(HealthSc)' in ACADEMIC
    assert 'Dr. e. h' not in ACADEMIC
