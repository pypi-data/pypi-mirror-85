# -*- coding: utf-8 -*-
# context.py
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))),
)  # isort:skip # noqa # pylint: disable=wrong-import-position
sys.path.append(
    os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)),
)  # isort: skip # noqa # pylint: disable=wrong-import-position

from persontitles import (  # type: ignore # isort:skip # noqa # pylint: disable=unused-import, wrong-import-position
    academic_german,
    academic_german_wiki,
    academic_german_drtitel,
    academic_uk,
    academic_us,
    academic_degrees,
    peertitles,
)  # pylint: disable=unused-import  # noqa
