"""
Flask web application for PDF processing
"""

from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
import json
from pdf_processor import PDFReader, PDFWriter
from pdf_processor.utils import merge_pdfs, split_pdf
import traceback

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max upload
app.config['UPLOAD_FOLDER'] = Path('uploads')
app.config['OUTPUT_FOLDER'] = Path('output')

# Create necessary directories
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)
app.config['OUTPUT_FOLDER'].mkdir(exist_ok=True)


@app.route('/')
def index():
    """Render the upload page"""
    return render_template('upload.html')


@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle file uploads"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400

        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files selected'}), 400

        uploaded_files = []
        for file in files:
            if not file.filename.endswith('.pdf'):
                return jsonify({'error': f'{file.filename} is not a PDF file'}), 400

            # Save file
            filename = Path(file.filename)
            filepath = app.config['UPLOAD_FOLDER'] / filename
            file.save(filepath)
            uploaded_files.append(str(filepath))

        return jsonify({
            'success': True,
            'message': f'Uploaded {len(uploaded_files)} file(s)',
            'files': uploaded_files
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/process', methods=['POST'])
def process_files():
    """Process uploaded PDF files"""
    try:
        data = request.json
        files = data.get('files', [])
        options = data.get('options', {})

        if not files:
            return jsonify({'error': 'No files provided'}), 400

        results = []
        for filepath in files:
            try:
                file_path = Path(filepath)
                if not file_path.exists():
                    results.append({
                        'name': file_path.name,
                        'type': 'error',
                        'error': 'File not found'
                    })
                    continue

                result = {
                    'name': file_path.name,
                    'type': 'success',
                    'size': f'{file_path.stat().st_size / 1024:.2f} KB'
                }

                # Extract text if requested
                if options.get('extractText'):
                    reader = PDFReader(str(file_path))
                    text = reader.extract_text()
                    result['text'] = text[:500] + '...' if len(text) > 500 else text

                # Extract metadata if requested
                if options.get('extractMetadata'):
                    reader = PDFReader(str(file_path))
                    metadata = reader.extract_metadata()
                    result['metadata'] = {
                        'pages': reader.get_page_count(),
                        'producer': metadata.get('/Producer', 'Unknown'),
                        'creator': metadata.get('/Creator', 'Unknown'),
                    }

                # Extract tables if requested
                if options.get('extractTables'):
                    reader = PDFReader(str(file_path))
                    try:
                        tables = reader.extract_tables(0)
                        result['tables'] = len(tables) if tables else 0
                    except:
                        result['tables'] = 0

                results.append(result)

            except Exception as e:
                results.append({
                    'name': Path(filepath).name,
                    'type': 'error',
                    'error': str(e)
                })

        return jsonify({
            'success': True,
            'results': results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/merge', methods=['POST'])
def merge():
    """Merge multiple PDFs"""
    try:
        data = request.json
        files = data.get('files', [])

        if len(files) < 2:
            return jsonify({'error': 'At least 2 files required for merging'}), 400

        output_path = app.config['OUTPUT_FOLDER'] / 'merged.pdf'
        merge_pdfs(files, str(output_path))

        return jsonify({
            'success': True,
            'message': 'PDFs merged successfully',
            'output': str(output_path)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/split', methods=['POST'])
def split():
    """Split a PDF"""
    try:
        data = request.json
        file = data.get('file')
        output_dir = app.config['OUTPUT_FOLDER'] / 'split'

        if not file:
            return jsonify({'error': 'No file provided'}), 400

        output_dir.mkdir(parents=True, exist_ok=True)
        files = split_pdf(file, str(output_dir))

        return jsonify({
            'success': True,
            'message': f'PDF split into {len(files)} files',
            'output': [str(f) for f in files]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
