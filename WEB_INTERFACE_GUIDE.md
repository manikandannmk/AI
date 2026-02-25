# PDF Upload Web Interface Guide

## Overview

The PDF Processor includes a modern, user-friendly web interface for uploading and processing PDF files. This guide covers all features and usage instructions.

## Features

### 📤 File Upload
- **Drag-and-Drop**: Simply drag PDF files onto the upload area
- **Click to Select**: Click the upload box or button to browse files
- **Multi-file Support**: Upload multiple PDF files at once
- **File Validation**: Automatic validation for PDF format and file size
- **Progress Tracking**: Visual feedback during uploads

### 🔧 Processing Options
After uploading, choose which operations to perform:
- **Extract Text**: Extract all text content from PDFs
- **Extract Metadata**: Get PDF information (title, author, creation date, etc.)
- **Extract Tables**: Identify and extract structured data
- **Extract Images**: Export images embedded in PDFs

### 📊 Results Display
- Detailed results for each processed file
- Text preview (first 800 characters)
- Metadata display with page count
- Download processed files
- Error messages with clear descriptions

## Getting Started

### 1. Start the Flask Application

```bash
# Option 1: Basic application
python app.py

# Option 2: Advanced application with more features
python app_advanced.py
```

The application will start on `http://localhost:5000`

### 2. Access the Upload Interface

Open your browser and navigate to:
```
http://localhost:5000/
```

### 3. Upload Files

1. **Drag and Drop Method**:
   - Drag PDF files into the upload box
   - Files will automatically be validated

2. **Click to Browse**:
   - Click the upload button
   - Select PDF files from your computer
   - You can select multiple files at once

### 4. Configure Processing Options

Before processing, select which operations you want:
- ☑ Extract Text
- ☑ Extract Metadata
- ☐ Extract Tables
- ☐ Extract Images

### 5. Process Files

1. Click "Process Files" button
2. Watch the progress bar as files are being processed
3. View results once complete

### 6. Download Results

Each processed file shows download options for the extracted content.

## File Management

### File Requirements
- **Format**: PDF files only (.pdf)
- **Size Limit**: 100 MB per file
- **Multiple Files**: Supported (process up to your server's capacity)

### Remove Files
- Click "Remove" next to any file to delete it from the queue
- Click "Clear All" to remove all selected files

### Start Over
- Click "Upload More Files" from the results page
- This clears all data and resets the form

## Web Application Files

### Structure
```
pdf_processor/
├── app.py                   # Basic Flask application
├── app_advanced.py          # Advanced Flask application
├── templates/
│   └── upload.html         # HTML interface
└── static/
    ├── css/
    │   └── style.css       # Styling
    └── js/
        └── upload.js       # JavaScript logic
```

### API Endpoints

#### Basic endpoints (app.py)
- `GET /` - Upload page
- `POST /api/upload` - Upload files
- `POST /api/process` - Process uploaded files
- `POST /api/merge` - Merge multiple PDFs
- `POST /api/split` - Split a PDF

#### Advanced endpoints (app_advanced.py)
All of the above plus:
- `POST /api/rotate` - Rotate PDF pages
- `POST /api/info` - Get PDF information
- `GET /api/download/<path>` - Download processed file
- `GET /api/health` - Health check

## Configuration

### Upload Directory
Default: `./uploads`
All uploaded files are temporarily stored here.

### Output Directory
Default: `./output`
Processed files are saved here.

### Maximum File Size
Default: 100 MB per file
Edit in `app.py` or `app_advanced.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
```

### Logging
Logs are stored in `./logs/app.log`
Check logs for debugging and monitoring.

## Troubleshooting

### Upload Fails
- **Problem**: File too large
  - **Solution**: Ensure file is under 100 MB

- **Problem**: Not a PDF file
  - **Solution**: Only .pdf files are supported

- **Problem**: Duplicate file
  - **Solution**: File with same name and size already uploaded

### Processing Errors
- **Problem**: "File not found"
  - **Solution**: Ensure file is uploaded successfully first

- **Problem**: Memory issues with large PDFs
  - **Solution**: Process files one at a time, or increase available RAM

### Connection Issues
- **Problem**: "Connection refused"
  - **Solution**: Ensure Flask app is running on correct port

- **Problem**: Slow processing
  - **Solution**: Check server resources, reduce number of files

## Security Considerations

1. **File Uploads**: Only PDF files allowed
2. **File Size Limits**: 100 MB maximum per file
3. **Temporary Storage**: Uploaded files stored in `uploads/` directory
4. **Clean Up**: Regularly delete old files to save space
5. **CORS**: Configured for development only

## Performance Tips

1. **Batch Processing**: Process similar-sized files together
2. **Memory Management**: Monitor server memory usage
3. **Cleanup**: Periodically delete old processed files
4. **Concurrent Uploads**: Limit to 5-10 concurrent uploads per server instance

## Keyboard Shortcuts

- **Enter** when file selected: Start upload
- **Ctrl+A** in upload area: Select multiple files
- **Esc** in dialog: Cancel file selection

## Browser Compatibility

- Chrome/Chromium: ✓ Full support
- Firefox: ✓ Full support
- Safari: ✓ Full support
- Edge: ✓ Full support
- Internet Explorer: ✗ Not supported

## Advanced Usage

### Custom Processing

Edit `app_advanced.py` to add custom processing:

```python
@app.route('/api/custom', methods=['POST'])
def custom_processing():
    # Your custom logic here
    pass
```

### Batch Processing

Create a batch file list and process multiple PDFs:
```python
from pdf_processor.utils import extract_text

pdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf']
for pdf in pdf_files:
    text = extract_text(pdf)
    print(text)
```

### Integration with Other Tools

The API endpoints can be called from other applications:

```bash
# Upload a file
curl -F "files=@document.pdf" http://localhost:5000/api/upload

# Process file
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"files": ["uploads/document.pdf"], "options": {"extractText": true}}'
```

## Support

For issues or questions:
1. Check the logs: `tail -f logs/app.log`
2. Verify file format and size
3. Ensure PDF is not corrupted
4. Test with a known good PDF file

## Best Practices

1. ✓ Validate file types before upload
2. ✓ Compress large PDFs before processing
3. ✓ Use meaningful filenames
4. ✓ Monitor server resources
5. ✓ Back up important files
6. ✓ Regularly clean up old files
7. ✓ Use HTTPS in production
8. ✓ Implement rate limiting for public deployments
