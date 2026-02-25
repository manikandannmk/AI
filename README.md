# PDF Processor - Complete Project

A comprehensive Python project for PDF file processing with both command-line and web-based interfaces.

## 🎯 Overview

PDF Processor is a full-featured application that allows you to:
- Upload and process PDF files through a modern web interface
- Extract text, metadata, tables, and images from PDFs
- Merge, split, and rotate PDF documents
- Create new PDFs with formatted content
- Use a Python library for programmatic access

## ✨ Features

### Web Interface
- 🎨 Modern, responsive UI with drag-and-drop support
- 📤 Multiple file uploads with real-time validation
- ⚙️ Configurable processing options
- 📊 Real-time progress tracking
- 📥 Download processed results
- 🔒 File size validation and security

### PDF Processing
- 📖 Extract text from PDFs
- 📋 Extract metadata and document information
- 📊 Extract tables and structured data
- 🖼️ Extract embedded images
- 🔗 Merge multiple PDFs
- ✂️ Split PDFs by page
- 🔄 Rotate PDF pages
- ✍️ Create new PDFs with formatted content

### Python Library
- Easy-to-use API
- Comprehensive documentation
- Full test coverage
- Type hints and docstrings
- Example scripts included

## 📁 Project Structure

```
pdf_processor_project/
├── pdf_processor/              # Main Python package
│   ├── __init__.py            # Package exports
│   ├── reader.py              # PDFReader class
│   ├── writer.py              # PDFWriter class
│   ├── utils.py               # Utility functions
│   └── config.py              # Configuration
├── templates/                 # Web interface templates
│   └── upload.html           # Upload interface
├── static/                    # Static web files
│   ├── css/
│   │   └── style.css         # Styling
│   └── js/
│       └── upload.js         # Client-side logic
├── app.py                     # Basic Flask application
├── app_advanced.py            # Advanced Flask application
├── run_web.py                 # Quick start script
├── tests/                     # Test files
│   ├── test_reader.py
│   └── test_writer.py
├── examples/                  # Example scripts
│   └── example_basic.py
├── requirements.txt           # Python dependencies
├── config.py                  # Flask configuration
├── .env.example              # Environment variables example
├── README.md                  # This file
├── README_PROJECT.md          # Detailed project documentation
├── WEB_INTERFACE.md          # Web interface documentation
└── WEB_INTERFACE_GUIDE.md    # Web interface usage guide
```

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python run_web.py
   ```

3. **Open browser**:
   Navigate to `http://localhost:5000`

4. **Upload and process**:
   - Drag PDF files into the upload area
   - Select processing options
   - Click "Process Files"
   - Download results

### Option 2: Python Library

```python
from pdf_processor import PDFReader, PDFWriter
from pdf_processor.utils import merge_pdfs, split_pdf

# Extract text from PDF
reader = PDFReader("document.pdf")
text = reader.extract_text()
print(text)

# Create new PDF
writer = PDFWriter("output.pdf")
writer.create_simple_pdf("Title", ["Content paragraph 1", "Content paragraph 2"])

# Merge PDFs
merge_pdfs(["file1.pdf", "file2.pdf"], "merged.pdf")

# Split PDF
split_pdf("document.pdf", "output_folder", start_page=0, end_page=5)
```

## 📚 Documentation

### For Web Interface Users
- **[WEB_INTERFACE.md](WEB_INTERFACE.md)** - Web interface overview and features
- **[WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md)** - Complete usage guide with troubleshooting

### For Developers
- **[README_PROJECT.md](README_PROJECT.md)** - Detailed project documentation
- **[examples/example_basic.py](examples/example_basic.py)** - Python usage examples

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pdf_processor
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Install in development mode:
   ```bash
   pip install -e .
   ```

## 🖥️ Web Interface

### Start the Server

```bash
# Using quick start script (recommended)
python run_web.py

# Or directly with Flask
python app_advanced.py  # Full features
python app.py           # Basic features
```

### Access the Interface
```
http://localhost:5000
```

### Features
- **Drag-and-drop upload**: Simply drag PDF files onto the interface
- **Multiple file support**: Upload and process many files at once
- **Real-time validation**: File format and size checking
- **Processing options**: Choose what to extract (text, metadata, tables, images)
- **Progress tracking**: Visual progress bar during processing
- **Results preview**: See extracted content immediately
- **Download results**: Save processed files to your computer

## 💻 Command Line Interface

### Using the Python Library

```bash
# Extract text from a PDF
python -c "from pdf_processor import PDFReader; print(PDFReader('file.pdf').extract_text())"

# Get PDF information
python -c "from pdf_processor.utils import get_pdf_info; print(get_pdf_info('file.pdf'))"
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/

# With coverage report
pytest --cov=pdf_processor tests/

# Specific test file
pytest tests/test_reader.py -v
```

## 🔌 API Endpoints

### Basic Endpoints (app.py)
- `GET /` - Upload page
- `POST /api/upload` - Upload files
- `POST /api/process` - Process files
- `POST /api/merge` - Merge PDFs
- `POST /api/split` - Split PDF

### Advanced Endpoints (app_advanced.py)
All above plus:
- `POST /api/rotate` - Rotate pages
- `POST /api/info` - Get PDF info
- `GET /api/download/<path>` - Download file
- `GET /api/health` - Health check

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` to customize:
```env
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000
MAX_PDF_SIZE_MB=100
LOG_LEVEL=INFO
```

### Flask Configuration

Edit `config.py` to customize:
- Upload/output directories
- File size limits
- Logging settings
- CORS configuration

## 🔒 Security

- PDF files only - no other formats allowed
- File size validation (100 MB default)
- Secure filename handling
- Input validation on all uploads
- CORS configured for development
- Temporary file cleanup
- Comprehensive logging

## 💡 Usage Examples

### Extract Text
```python
from pdf_processor import PDFReader

reader = PDFReader("document.pdf")
text = reader.extract_text()
```

### Extract Metadata
```python
reader = PDFReader("document.pdf")
metadata = reader.extract_metadata()
pages = reader.get_page_count()
```

### Create PDF
```python
from pdf_processor import PDFWriter

writer = PDFWriter("output.pdf")
content = ["First paragraph", "Second paragraph"]
writer.create_simple_pdf("Title", content)
```

### Merge PDFs
```python
from pdf_processor.utils import merge_pdfs

files = ["file1.pdf", "file2.pdf", "file3.pdf"]
merge_pdfs(files, "output/merged.pdf")
```

### Split PDF
```python
from pdf_processor.utils import split_pdf

split_pdf("document.pdf", "output/", start_page=0, end_page=10)
```

## 📊 System Requirements

### Minimum
- CPU: 2 cores
- RAM: 2 GB
- Disk: 500 MB
- OS: Linux, macOS, or Windows

### Recommended
- CPU: 4+ cores
- RAM: 4+ GB
- Disk: 5 GB+
- OS: Linux (Ubuntu 20.04+)

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
python app_advanced.py --port 5001
```

### File Upload Fails
- Check file size (max 100 MB)
- Verify PDF format
- Check disk space
- Review error logs in `logs/app.log`

### Processing Hangs
- Check PDF for corruption
- Reduce file size
- Increase timeout in configuration
- Monitor system resources

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit pull request

## 📄 License

MIT License - See LICENSE file for details

## 📞 Support

For help:
1. Check the documentation files
2. Review example scripts in `examples/`
3. Check logs in `logs/app.log`
4. Open an issue in the repository

## 🎉 Features Coming Soon

- [ ] OCR support for scanned PDFs
- [ ] PDF annotation editor
- [ ] Batch processing scheduler
- [ ] Database for file history
- [ ] User authentication
- [ ] PDF encryption/decryption
- [ ] Watermark addition
- [ ] Advanced text formatting
- [ ] Integration with cloud storage
- [ ] Mobile app

## 📈 Performance

- Processes PDFs up to 100 MB
- Supports concurrent uploads
- Optimized for large batch operations
- Memory efficient
- Fast text extraction
- Handles complex layouts

## 🌟 Key Highlights

✨ **Modern UI** - Beautiful, intuitive web interface
🚀 **Easy to Use** - No technical knowledge required
💪 **Powerful** - Professional-grade PDF processing
🔒 **Secure** - File validation and validation
📚 **Well Documented** - Comprehensive guides and examples
🧪 **Tested** - Full test coverage
🔧 **Flexible** - Extensible architecture
⚡ **Fast** - Optimized performance

---

**Happy PDF Processing! 📄**