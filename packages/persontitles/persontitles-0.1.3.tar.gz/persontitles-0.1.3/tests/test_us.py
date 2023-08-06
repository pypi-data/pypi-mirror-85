#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_us.py
"""Tests for academic_us module."""
import os

from context import academic_us


def test_filenotfound():
    os.remove('./persontitles/academic_us.txt')
    ACADEMIC = academic_us.degrees_us()
    assert isinstance(ACADEMIC, set)


def test_academic_is_set():

    ACADEMIC = academic_us.degrees_us()
    assert isinstance(ACADEMIC, set)


def test_degree_in_list():

    ACADEMIC = academic_us.degrees_us()
    assert 'B.F&TV.' in ACADEMIC
    assert 'B.S.-C.I.E.' in ACADEMIC
    assert 'Dr. e. h' not in ACADEMIC
    assert 'B.F&amp;TV.' not in ACADEMIC
