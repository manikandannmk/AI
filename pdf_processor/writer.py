"""
PDF Writer module for creating and modifying PDF files
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from pathlib import Path
from typing import List, Tuple, Optional


class PDFWriter:
    """Class for creating and writing PDF files"""

    def __init__(self, output_path: str, page_size=letter):
        """
        Initialize PDFWriter
        
        Args:
            output_path: Path for the output PDF file
            page_size: Page size (default: letter)
        """
        self.output_path = Path(output_path)
        self.page_size = page_size
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def create_simple_pdf(self, title: str, content: List[str]) -> None:
        """
        Create a simple PDF with title and content
        
        Args:
            title: PDF title
            content: List of text paragraphs
        """
        doc = SimpleDocTemplate(str(self.output_path), pagesize=self.page_size)
        story = []
        styles = getSampleStyleSheet()

        # Add title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='black',
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 0.3 * inch))

        # Add content
        for text in content:
            story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))

        doc.build(story)

    def create_canvas_pdf(self, width: int = 500, height: int = 500) -> 'PDFWriter':
        """
        Create a PDF using canvas for more control
        
        Args:
            width: Canvas width
            height: Canvas height
            
        Returns:
            Self for method chaining
        """
        self.c = canvas.Canvas(str(self.output_path), pagesize=(width, height))
        return self

    def add_canvas_text(self, x: float, y: float, text: str, font_size: int = 12) -> 'PDFWriter':
        """
        Add text to canvas PDF
        
        Args:
            x: X coordinate
            y: Y coordinate
            text: Text to add
            font_size: Font size
            
        Returns:
            Self for method chaining
        """
        if not hasattr(self, 'c'):
            raise RuntimeError("Canvas not initialized. Call create_canvas_pdf first.")
        self.c.setFont("Helvetica", font_size)
        self.c.drawString(x, y, text)
        return self

    def add_canvas_rectangle(self, x: float, y: float, width: float, height: float,
                           stroke: int = 1, fill: int = 0) -> 'PDFWriter':
        """
        Add rectangle to canvas PDF
        
        Args:
            x, y: Top-left coordinates
            width, height: Rectangle dimensions
            stroke: Draw border (1/0)
            fill: Fill rectangle (1/0)
            
        Returns:
            Self for method chaining
        """
        if not hasattr(self, 'c'):
            raise RuntimeError("Canvas not initialized. Call create_canvas_pdf first.")
        self.c.rect(x, y, width, height, stroke=stroke, fill=fill)
        return self

    def save_canvas(self) -> Path:
        """
        Save the canvas PDF
        
        Returns:
            Path to saved file
        """
        if hasattr(self, 'c'):
            self.c.save()
        return self.output_path
