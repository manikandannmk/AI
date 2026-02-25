"""
PDF Processor - A comprehensive Python package for PDF file processing
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .reader import PDFReader
from .writer import PDFWriter
from .utils import extract_text, merge_pdfs, split_pdf

__all__ = [
    "PDFReader",
    "PDFWriter",
    "extract_text",
    "merge_pdfs",
    "split_pdf",
]
