#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""Test features of DocxContent that weren't tested in test_docx2python.

:author: Shay Hill
:created: 7/6/2019
"""

from docx2python.main import docx2python

INST = docx2python("resources/example.docx")


class TestDocument:
    def test_combine_of_header_body_footer(self) -> None:
        """Return all content combined as instance.document """
        assert (
            INST.document
            == INST.header + INST.body + INST.footer + INST.footnotes + INST.endnotes
        )

    def test_read_only(self) -> None:
        """Document attribute is read only."""
        doc1 = INST.document
        doc1 = doc1[:1]
        assert doc1 != INST.document
        assert (
            INST.document
            == INST.header + INST.body + INST.footer + INST.footnotes + INST.endnotes
        )


class TestText:
    def test_function(self) -> None:
        """Return '\n\n'-delimited paragraphs as instance.text. """
        assert INST.text[:50] == (
            "\n\n\n\nHeader text----media/image1.png----\n\nI)	expect"
        )
        assert INST.text[-51:] == (
            "endnote2)\t\n\n Second endnote----media/image1.png----"
        )


class TestHtmlMap:
    def test_function(self) -> None:
        """Return html tables."""
        assert INST.html_map[:49] == '<html><body><table border="1"><tr><td><pre>(0, 0,'
