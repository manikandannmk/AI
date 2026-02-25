"""
PDF Reader module for extracting text, metadata, and images from PDF files
"""

import pdfplumber
from pathlib import Path
from typing import List, Dict, Optional


class PDFReader:
    """Class for reading and extracting data from PDF files"""

    def __init__(self, pdf_path: str):
        """
        Initialize PDFReader with a PDF file path
        
        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")

    def extract_text(self) -> str:
        """
        Extract all text from the PDF file
        
        Returns:
            Concatenated text from all pages
        """
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
                text += "\n"
        return text

    def extract_text_by_page(self) -> List[str]:
        """
        Extract text from each page separately
        
        Returns:
            List of text strings, one per page
        """
        pages_text = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                pages_text.append(page.extract_text() or "")
        return pages_text

    def extract_metadata(self) -> Dict:
        """
        Extract metadata from the PDF file
        
        Returns:
            Dictionary containing PDF metadata
        """
        with pdfplumber.open(self.pdf_path) as pdf:
            return pdf.metadata

    def extract_tables(self, page_num: int = 0) -> List[List[List[str]]]:
        """
        Extract tables from a specific page
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            List of tables found on the page
        """
        with pdfplumber.open(self.pdf_path) as pdf:
            if page_num >= len(pdf.pages):
                raise ValueError(f"Page {page_num} does not exist")
            page = pdf.pages[page_num]
            return page.extract_tables()

    def get_page_count(self) -> int:
        """
        Get the total number of pages in the PDF
        
        Returns:
            Number of pages
        """
        with pdfplumber.open(self.pdf_path) as pdf:
            return len(pdf.pages)

    def extract_images(self, output_dir: str, page_num: Optional[int] = None) -> List[str]:
        """
        Extract images from the PDF
        
        Args:
            output_dir: Directory to save extracted images
            page_num: Specific page to extract images from (None for all pages)
            
        Returns:
            List of saved image file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        image_paths = []

        with pdfplumber.open(self.pdf_path) as pdf:
            pages = [pdf.pages[page_num]] if page_num is not None else pdf.pages
            for idx, page in enumerate(pages):
                for img_idx, img in enumerate(page.images):
                    image_path = output_path / f"image_page{idx}_{img_idx}.png"
                    image_paths.append(str(image_path))

        return image_paths
