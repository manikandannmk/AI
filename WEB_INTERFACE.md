# PDF Upload Web Interface

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Easiest way - uses advanced Flask app
python run_web.py

# Or directly with Flask
python app_advanced.py

# Or the basic version
python app.py
```

### 3. Open in Browser
Navigate to: `http://localhost:5000`

## 📋 File Structure

### Templates
- **`templates/upload.html`** - Main upload interface HTML
  - Modern, responsive design
  - Drag-and-drop support
  - Real-time file validation
  - Progress tracking

### Static Files
- **`static/css/style.css`** - Comprehensive styling
  - Gradient background
  - Smooth animations
  - Responsive layout
  - Dark mode ready

- **`static/js/upload.js`** - Client-side JavaScript
  - File upload handling
  - Drag-and-drop functionality
  - Form validation
  - Progress updates
  - Result rendering

### Flask Applications

#### `app.py` - Basic Application
```python
@app.route('/')                    # Upload page
@app.route('/api/upload', methods=['POST'])      # File upload handler
@app.route('/api/process', methods=['POST'])     # Process files
@app.route('/api/merge', methods=['POST'])       # Merge PDFs
@app.route('/api/split', methods=['POST'])       # Split PDFs
```

#### `app_advanced.py` - Advanced Application
Includes all basic endpoints plus:
```python
@app.route('/api/rotate', methods=['POST'])      # Rotate pages
@app.route('/api/info', methods=['POST'])        # Get PDF info
@app.route('/api/download/<path>', methods=['GET'])  # Download files
@app.route('/api/health', methods=['GET'])       # Health check
```

### Configuration
- **`config.py`** - Flask configuration
  - Upload/output folders
  - File size limits
  - Logging configuration
  - Security settings

## ✨ Features

### Upload Interface
- ✓ Drag-and-drop support
- ✓ Multiple file selection
- ✓ Real-time validation
- ✓ File preview
- ✓ Progress bar
- ✓ Error messages
- ✓ Success notifications

### Processing Options
- ✓ Extract Text
- ✓ Extract Metadata
- ✓ Extract Tables
- ✓ Extract Images (advanced)
- ✓ Merge PDFs
- ✓ Split PDFs
- ✓ Rotate Pages (advanced)

### Results Display
- ✓ Detailed results per file
- ✓ Text preview
- ✓ Metadata display
- ✓ Error reporting
- ✓ Download options
- ✓ Copy to clipboard

## 🎨 UI Features

### Modern Design
- Gradient purple background
- Clean white interface
- Smooth animations
- Responsive buttons
- Icon integration

### User Experience
- Intuitive layout
- Clear instructions
- Visual feedback
- Error handling
- Success messages
- Loading indicators

### Responsive Design
- Desktop optimized
- Tablet friendly
- Mobile compatible
- Touch-enabled
- Adaptive layout

## 📱 Browser Support

| Browser | Support |
|---------|---------|
| Chrome  | ✓ Full  |
| Firefox | ✓ Full  |
| Safari  | ✓ Full  |
| Edge    | ✓ Full  |
| IE11    | ✗ No    |

## 🔧 Configuration

### Environment Variables
Create a `.env` file:
```env
FLASK_DEBUG=True
FLASK_TESTING=False
SECRET_KEY=your-secret-key
HOST=0.0.0.0
PORT=5000
MAX_PDF_SIZE_MB=100
LOG_LEVEL=INFO
```

### Custom Directories
Edit `config.py`:
```python
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('output')
```

### File Size Limit
```python
max_size = 100 * 1024 * 1024  # 100 MB
```

## 🚀 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn --workers 4 --threads 2 app_advanced:app
```

### Using Docker
```bash
docker build -t pdf-processor .
docker run -p 5000:5000 pdf-processor
```

### Nginx Configuration
```nginx
upstream pdf_processor {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://pdf_processor;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/static;
    }
}
```

## 🔒 Security Best Practices

1. **HTTPS**: Always use HTTPS in production
2. **Rate Limiting**: Implement rate limiting for uploads
3. **File Validation**: Validate all uploads
4. **Size Limits**: Enforce maximum file sizes
5. **Cleanup**: Regularly delete old files
6. **Logging**: Monitor uploads and processing
7. **CORS**: Configure CORS appropriately
8. **Authentication**: Add user authentication if needed

## 📊 API Reference

### POST /api/upload
Upload PDF files
```json
{
  "files": [file1, file2, ...]
}
```

### POST /api/process
Process uploaded files
```json
{
  "files": ["uploads/file.pdf"],
  "options": {
    "extractText": true,
    "extractMetadata": true,
    "extractTables": false,
    "extractImages": false
  }
}
```

### POST /api/merge
Merge multiple PDFs
```json
{
  "files": ["uploads/file1.pdf", "uploads/file2.pdf"]
}
```

### POST /api/split
Split a PDF
```json
{
  "file": "uploads/file.pdf"
}
```

### POST /api/rotate (Advanced)
Rotate PDF pages
```json
{
  "file": "uploads/file.pdf",
  "angle": 90
}
```

### POST /api/info (Advanced)
Get PDF information
```json
{
  "file": "uploads/file.pdf"
}
```

## 🐛 Troubleshooting

### Application Won't Start
```bash
# Check if port is in use
lsof -i :5000

# Use different port
python app_advanced.py --port 5001
```

### Files Not Uploading
- Check file size (max 100 MB)
- Verify PDF format
- Check disk space
- Review error logs

### Processing Hangs
- Check PDF for corruption
- Reduce file size
- Increase timeout
- Monitor system resources

### Performance Issues
- Enable caching
- Use load balancer
- Optimize PDF files
- Add more workers

## 📝 Logs

View application logs:
```bash
tail -f logs/app.log
```

View specific errors:
```bash
grep ERROR logs/app.log
```

## 🤝 Contributing

To add features:
1. Edit HTML in `templates/upload.html`
2. Update JavaScript in `static/js/upload.js`
3. Update CSS in `static/css/style.css`
4. Add endpoints to `app_advanced.py`
5. Test thoroughly

## 📚 Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- PDF Processing: See `README_PROJECT.md`
- Web Guide: See `WEB_INTERFACE_GUIDE.md`

## 📞 Support

For issues or features:
1. Check error logs in `logs/`
2. Review uploaded files
3. Test with sample PDF
4. Check browser console for JS errors

## 📄 License

MIT License - See LICENSE file for details
