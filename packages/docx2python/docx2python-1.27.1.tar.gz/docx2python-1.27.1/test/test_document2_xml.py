#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""Test hyperlink functionality

:author: Shay Hill
:created: 4/19/2020

The main content file in a docx is usually ``word/document.xml``, but this is not
always the case.
"""

from docx2python.main import docx2python
import os


class TestHyperlink:
    def test_prints(self) -> None:
        """
        Open a docx with ``word/document.xml`` renamed to ``word/blah_blah.xml``
        and all references updated. Test that text extracts as expected."""
        extraction = docx2python(os.path.join("resources", "renamed_document_xml.docx"))
        assert (
            '<a href="http://www.shayallenhill.com/">my website</a>' in extraction.text
        )
