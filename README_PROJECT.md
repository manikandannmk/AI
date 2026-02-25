# PDF Processor

A comprehensive Python project for PDF file processing with utilities for reading, writing, and manipulating PDF files.

## Features

- **PDF Reading**: Extract text, metadata, tables, and images from PDF files
- **PDF Writing**: Create new PDFs with formatted text and canvas-based drawings
- **PDF Manipulation**: Merge, split, and rotate PDF files
- **Metadata Extraction**: Get comprehensive information about PDF files
- **Table Extraction**: Extract structured data from PDF tables
- **Image Extraction**: Export images embedded in PDFs

## Project Structure

```
pdf_processor/
├── pdf_processor/           # Main package
│   ├── __init__.py         # Package initialization
│   ├── reader.py           # PDFReader class for reading PDFs
│   ├── writer.py           # PDFWriter class for creating PDFs
│   ├── utils.py            # Utility functions for PDF manipulation
│   └── config.py           # Configuration settings
├── examples/               # Example scripts
│   └── example_basic.py    # Basic usage examples
├── tests/                  # Test files
│   ├── test_reader.py      # Tests for reader module
│   └── test_writer.py      # Tests for writer module
├── requirements.txt        # Project dependencies
├── setup.py               # Setup configuration
└── README.md              # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
cd /workspaces/AI
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install the package in development mode:
```bash
pip install -e .
```

## Usage

### Extract Text from PDF

```python
from pdf_processor import PDFReader

reader = PDFReader("path/to/your/file.pdf")

# Extract all text
text = reader.extract_text()
print(text)

# Extract text by page
pages = reader.extract_text_by_page()
for i, page_text in enumerate(pages):
    print(f"Page {i+1}: {page_text[:100]}...")

# Get page count
count = reader.get_page_count()
print(f"Total pages: {count}")
```

### Create a PDF

```python
from pdf_processor import PDFWriter

writer = PDFWriter("output/my_document.pdf")

content = [
    "This is the first paragraph.",
    "This is the second paragraph.",
    "You can add as many paragraphs as you want."
]

writer.create_simple_pdf("My Document", content)
```

### Merge PDFs

```python
from pdf_processor.utils import merge_pdfs

pdfs = ["file1.pdf", "file2.pdf", "file3.pdf"]
output = merge_pdfs(pdfs, "output/merged.pdf")
print(f"Merged PDF: {output}")
```

### Split PDF

```python
from pdf_processor.utils import split_pdf

files = split_pdf("input.pdf", "output/split", start_page=0, end_page=5)
print(f"Created {len(files)} PDF files")
```

### Extract Tables

```python
from pdf_processor import PDFReader

reader = PDFReader("path/to/your/file.pdf")
tables = reader.extract_tables(page_num=0)

for table in tables:
    for row in table:
        print(row)
```

### Get PDF Information

```python
from pdf_processor.utils import get_pdf_info

info = get_pdf_info("path/to/your/file.pdf")
print(f"Pages: {info['total_pages']}")
print(f"Metadata: {info['metadata']}")
print(f"Encrypted: {info['is_encrypted']}")
```

### Draw with Canvas

```python
from pdf_processor import PDFWriter

writer = PDFWriter("output/canvas_drawing.pdf")
writer.create_canvas_pdf(600, 400)
writer.add_canvas_text(50, 350, "Hello, World!", font_size=20)
writer.add_canvas_rectangle(50, 200, 500, 100, stroke=1, fill=0)
writer.add_canvas_text(60, 250, "This is a rectangle", font_size=12)
writer.save_canvas()
```

## Running Examples

Run the basic examples:
```bash
python examples/example_basic.py
```

## Running Tests

Run the test suite:
```bash
pytest tests/
```

Run specific test file:
```bash
pytest tests/test_reader.py
```

Run with coverage report:
```bash
pytest --cov=pdf_processor tests/
```

## Dependencies

- **PyPDF2**: PDF reading and manipulation
- **pdfplumber**: Advanced PDF data extraction
- **reportlab**: PDF creation and generation
- **Pillow**: Image processing
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework

## API Reference

### PDFReader

```python
class PDFReader:
    def __init__(self, pdf_path: str)
    def extract_text() -> str
    def extract_text_by_page() -> List[str]
    def extract_metadata() -> Dict
    def extract_tables(page_num: int = 0) -> List
    def get_page_count() -> int
    def extract_images(output_dir: str, page_num: Optional[int] = None) -> List[str]
```

### PDFWriter

```python
class PDFWriter:
    def __init__(self, output_path: str, page_size=letter)
    def create_simple_pdf(title: str, content: List[str]) -> None
    def create_canvas_pdf(width: int = 500, height: int = 500) -> PDFWriter
    def add_canvas_text(x: float, y: float, text: str, font_size: int = 12) -> PDFWriter
    def add_canvas_rectangle(x: float, y: float, width: float, height: float, ...) -> PDFWriter
    def save_canvas() -> Path
```

### Utility Functions

```python
extract_text(pdf_path: str) -> str
merge_pdfs(pdf_list: List[str], output_path: str) -> Path
split_pdf(pdf_path: str, output_dir: str, start_page: int = 0, end_page: int = None) -> List[Path]
rotate_pdf(pdf_path: str, output_path: str, rotation: int = 90) -> Path
get_pdf_info(pdf_path: str) -> dict
```

## Configuration

Configuration is managed in `pdf_processor/config.py`:

- `MAX_PDF_SIZE_MB`: Maximum allowed PDF file size (default: 100 MB)
- `LOG_LEVEL`: Logging level (default: INFO)
- Output directories for data, logs, and results

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `pytest`
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature/your-feature`
6. Submit a pull request

## License

MIT License

## Support

For issues, questions, or suggestions, please open an issue in the repository.

## Changelog

### Version 1.0.0 (Initial Release)
- PDFReader for text, metadata, and table extraction
- PDFWriter for creating new PDFs
- Utility functions for merging, splitting, and rotating PDFs
- Comprehensive test suite
- Example scripts and documentation

## Roadmap

- [ ] Support for PDF encryption/decryption
- [ ] Advanced text formatting options
- [ ] Batch processing utilities
- [ ] PDF annotation support
- [ ] OCR integration for scanned PDFs
- [ ] Performance optimizations for large files
