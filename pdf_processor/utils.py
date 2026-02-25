"""
Utility functions for PDF processing
"""

from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pathlib import Path
from typing import List


def extract_text(pdf_path: str) -> str:
    """
    Extract text from a PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text
    """
    from .reader import PDFReader
    reader = PDFReader(pdf_path)
    return reader.extract_text()


def merge_pdfs(pdf_list: List[str], output_path: str) -> Path:
    """
    Merge multiple PDF files into one
    
    Args:
        pdf_list: List of PDF file paths to merge
        output_path: Path for the merged PDF
        
    Returns:
        Path to the merged PDF file
    """
    merger = PdfMerger()
    
    for pdf in pdf_list:
        if not Path(pdf).exists():
            raise FileNotFoundError(f"PDF file not found: {pdf}")
        merger.append(pdf)
    
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    merger.write(str(output))
    merger.close()
    
    return output


def split_pdf(pdf_path: str, output_dir: str, start_page: int = 0, end_page: int = None) -> List[Path]:
    """
    Split a PDF file into separate pages
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save split PDF files
        start_page: Starting page (0-indexed)
        end_page: Ending page (0-indexed, None for last page)
        
    Returns:
        List of created PDF file paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    if end_page is None:
        end_page = total_pages - 1
    
    if start_page < 0 or end_page >= total_pages or start_page > end_page:
        raise ValueError(f"Invalid page range: {start_page}-{end_page} (total pages: {total_pages})")
    
    created_files = []
    
    for page_num in range(start_page, end_page + 1):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])
        
        output_file = output_path / f"page_{page_num + 1}.pdf"
        with open(output_file, 'wb') as f:
            writer.write(f)
        created_files.append(output_file)
    
    return created_files


def rotate_pdf(pdf_path: str, output_path: str, rotation: int = 90) -> Path:
    """
    Rotate pages in a PDF file
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Path for the rotated PDF
        rotation: Rotation angle (90, 180, 270)
        
    Returns:
        Path to the rotated PDF file
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        page.rotate(rotation)
        writer.add_page(page)
    
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output, 'wb') as f:
        writer.write(f)
    
    return output


def get_pdf_info(pdf_path: str) -> dict:
    """
    Get information about a PDF file
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with PDF information
    """
    reader = PdfReader(pdf_path)
    
    return {
        'total_pages': len(reader.pages),
        'metadata': reader.metadata,
        'is_encrypted': reader.is_encrypted,
    }
