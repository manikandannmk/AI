"""
Basic PDF processing examples
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_processor import PDFReader, PDFWriter
from pdf_processor.utils import merge_pdfs, split_pdf


def example_extract_text():
    """Example: Extract text from PDF"""
    print("=" * 50)
    print("Example 1: Extract Text from PDF")
    print("=" * 50)
    
    # This would work with an actual PDF file
    # pdf_path = "path/to/your/file.pdf"
    # reader = PDFReader(pdf_path)
    # text = reader.extract_text()
    # print(f"Extracted text:\n{text[:200]}...")
    
    print("To use this example, provide a valid PDF file path")
    print()


def example_create_pdf():
    """Example: Create a simple PDF"""
    print("=" * 50)
    print("Example 2: Create a Simple PDF")
    print("=" * 50)
    
    output_path = "output/sample_document.pdf"
    
    writer = PDFWriter(output_path)
    content = [
        "This is a sample PDF created with PDF Processor.",
        "You can add multiple paragraphs to your document.",
        "The library supports text formatting and layout control.",
    ]
    
    writer.create_simple_pdf("Sample Document", content)
    print(f"✓ Created PDF: {output_path}")
    print()


def example_pdf_info():
    """Example: Get PDF information"""
    print("=" * 50)
    print("Example 3: Get PDF Information")
    print("=" * 50)
    
    # This would work with an actual PDF file
    # from pdf_processor.utils import get_pdf_info
    # pdf_path = "path/to/your/file.pdf"
    # info = get_pdf_info(pdf_path)
    # print(f"PDF Info: {info}")
    
    print("To use this example, provide a valid PDF file path")
    print()


def example_canvas_drawing():
    """Example: Create PDF with canvas drawing"""
    print("=" * 50)
    print("Example 4: Create PDF with Canvas")
    print("=" * 50)
    
    output_path = "output/canvas_example.pdf"
    
    writer = PDFWriter(output_path)
    writer.create_canvas_pdf(600, 400)
    writer.add_canvas_text(50, 350, "Canvas PDF Example", font_size=20)
    writer.add_canvas_text(50, 300, "You can draw shapes and add text", font_size=12)
    writer.add_canvas_rectangle(50, 200, 500, 80, stroke=1, fill=0)
    writer.add_canvas_text(60, 230, "This is a rectangle", font_size=12)
    writer.save_canvas()
    
    print(f"✓ Created PDF: {output_path}")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("PDF Processor - Basic Examples")
    print("=" * 50 + "\n")
    
    example_extract_text()
    example_create_pdf()
    example_pdf_info()
    example_canvas_drawing()
    
    print("=" * 50)
    print("Examples completed!")
    print("=" * 50)
