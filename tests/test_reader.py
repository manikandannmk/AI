"""
Tests for PDF Reader module
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_processor.reader import PDFReader


def test_reader_file_not_found():
    """Test that PDFReader raises error for non-existent file"""
    with pytest.raises(FileNotFoundError):
        PDFReader("non_existent_file.pdf")


@pytest.mark.skip(reason="Requires actual PDF file")
def test_extract_text():
    """Test text extraction"""
    reader = PDFReader("path/to/test.pdf")
    text = reader.extract_text()
    assert isinstance(text, str)
    assert len(text) > 0


@pytest.mark.skip(reason="Requires actual PDF file")
def test_get_page_count():
    """Test page count retrieval"""
    reader = PDFReader("path/to/test.pdf")
    count = reader.get_page_count()
    assert isinstance(count, int)
    assert count > 0


@pytest.mark.skip(reason="Requires actual PDF file")
def test_extract_metadata():
    """Test metadata extraction"""
    reader = PDFReader("path/to/test.pdf")
    metadata = reader.extract_metadata()
    assert isinstance(metadata, dict)
