"""
Tests for PDF Writer module
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_processor.writer import PDFWriter


def test_create_simple_pdf():
    """Test creation of simple PDF"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.pdf"
        
        writer = PDFWriter(str(output_path))
        content = ["Test content"]
        writer.create_simple_pdf("Test Title", content)
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0


def test_create_canvas_pdf():
    """Test creation of canvas PDF"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "canvas_test.pdf"
        
        writer = PDFWriter(str(output_path))
        writer.create_canvas_pdf(200, 200)
        writer.add_canvas_text(10, 190, "Test")
        writer.save_canvas()
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0


def test_canvas_without_init():
    """Test that canvas methods fail without initialization"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.pdf"
        writer = PDFWriter(str(output_path))
        
        with pytest.raises(RuntimeError):
            writer.add_canvas_text(10, 10, "Test")
