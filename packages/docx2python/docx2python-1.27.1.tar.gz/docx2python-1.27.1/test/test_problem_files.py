#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""Run problem files I come across.

:author: Shay Hill
:created: 7/17/2019
"""

from docx2python.main import docx2python


def test_dop_1013a() -> None:
    """Misidentifies ``word/document.xml`` as ``word/word/document.xml``"""
    docx2python("resources/example.docx")
    # noinspection SpellCheckingInspection
    docx2python("resources/240-DOP-1013A Lay Down Tubulars.docx")
