"""
Advanced Flask application for PDF processing with additional features
"""

from flask import Flask, render_template, request, jsonify, send_file, stream_with_context
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
import logging
from datetime import datetime
import json
from threading import Thread

from pdf_processor import PDFReader, PDFWriter
from pdf_processor.utils import merge_pdfs, split_pdf, rotate_pdf, get_pdf_info
from pdf_processor.database import db, PDFDocument, TextChunk, Embedding, SearchQuery, init_db
from pdf_processor.embeddings import PDFEmbeddingProcessor
from pdf_processor.response_validator import validate_all_responses, validate_response
import numpy as np

# Configuration
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Flask configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB max upload
app.config['UPLOAD_FOLDER'] = Path('uploads')
app.config['OUTPUT_FOLDER'] = Path('output')
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pdf_processor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create directories
app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)
app.config['OUTPUT_FOLDER'].mkdir(parents=True, exist_ok=True)
Path('logs').mkdir(exist_ok=True)

# Initialize database
init_db(app)

# Logging setup
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def process_pdf_embeddings(file_path: str, original_filename: str):
    """
    Background task to process PDF and generate embeddings
    
    Args:
        file_path: Path to uploaded PDF file
        original_filename: Original filename
    """
    try:
        logger.info(f'Starting PDF processing for {original_filename}')
        
        # Initialize embedding processor
        processor = PDFEmbeddingProcessor(model_name="all-MiniLM-L6-v2")
        
        # Process PDF: read, chunk, embed, and store
        doc, total_embeddings = processor.process_pdf(
            file_path,
            original_filename,
            chunk_size=500,
            overlap=100
        )
        
        logger.info(f'Completed PDF processing: {original_filename} - {total_embeddings} embeddings created')
        
    except Exception as e:
        logger.error(f'Error processing PDF {original_filename}: {str(e)}')
        # Update document status to failed
        try:
            with app.app_context():
                doc = PDFDocument.query.filter_by(original_filename=original_filename).first()
                if doc:
                    doc.processing_status = 'failed'
                    doc.error_message = str(e)
                    db.session.commit()
        except:
            pass


@app.route('/')
def index():
    """Render the upload page"""
    logger.info('User accessed upload page')
    return render_template('upload.html')


@app.route('/chat')
def chat():
    """Render the chat page"""
    logger.info('User accessed chat page')
    return render_template('chat.html')


@app.route('/search')
def search():
    """Render the semantic search page"""
    logger.info('User accessed search page')
    return render_template('search.html')


@app.route('/api/upload', methods=['POST'])
@validate_response('upload')
def upload_files():
    """Handle file uploads and start embedding processing"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400

        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400

        uploaded_files = []
        errors = []

        for file in files:
            if not allowed_file(file.filename):
                errors.append(f'{file.filename} is not a valid PDF file')
                continue

            filename = secure_filename(file.filename)
            filepath = app.config['UPLOAD_FOLDER'] / filename
            
            try:
                file.save(filepath)
                
                # Start background task for PDF processing and embedding
                thread = Thread(
                    target=process_pdf_embeddings,
                    args=(str(filepath), file.filename)
                )
                thread.daemon = True
                thread.start()
                
                uploaded_files.append({
                    'name': filename,
                    'path': str(filepath),
                    'size': filepath.stat().st_size,
                    'status': 'uploaded - processing embeddings'
                })
                logger.info(f'File uploaded: {filename}')
            except Exception as e:
                errors.append(f'Error uploading {filename}: {str(e)}')
                logger.error(f'Upload error for {filename}: {str(e)}')

        return jsonify({
            'success': len(uploaded_files) > 0,
            'uploaded': uploaded_files,
            'errors': errors,
            'message': f'Successfully uploaded {len(uploaded_files)} of {len(files)} files. Processing embeddings in background.'
        })

    except Exception as e:
        logger.error(f'Upload error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/process', methods=['POST'])
@validate_response('process')
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
                    'timestamp': datetime.now().isoformat()
                }

                reader = PDFReader(str(file_path))

                # Extract text
                if options.get('extractText'):
                    text = reader.extract_text()
                    result['text'] = text[:800] + '...' if len(text) > 800 else text

                # Extract metadata
                if options.get('extractMetadata'):
                    metadata = reader.extract_metadata()
                    result['metadata'] = {
                        'total_pages': reader.get_page_count(),
                        'metadata': dict(metadata) if metadata else {}
                    }

                # Extract tables
                if options.get('extractTables'):
                    try:
                        tables = reader.extract_tables(0)
                        result['tables_count'] = len(tables) if tables else 0
                    except:
                        result['tables_count'] = 0

                results.append(result)
                logger.info(f'Processed: {file_path.name}')

            except Exception as e:
                results.append({
                    'name': Path(filepath).name,
                    'type': 'error',
                    'error': str(e)
                })
                logger.error(f'Processing error for {filepath}: {str(e)}')

        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })

    except Exception as e:
        logger.error(f'Process error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/merge', methods=['POST'])
@validate_response('merge')
def merge():
    """Merge multiple PDFs"""
    try:
        data = request.json
        files = data.get('files', [])

        if len(files) < 2:
            return jsonify({'error': 'At least 2 files required'}), 400

        for f in files:
            if not Path(f).exists():
                return jsonify({'error': f'{f} does not exist'}), 400

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = app.config['OUTPUT_FOLDER'] / f'merged_{timestamp}.pdf'
        
        merge_pdfs(files, str(output_path))
        logger.info(f'PDFs merged: {output_path}')

        return jsonify({
            'success': True,
            'message': 'PDFs merged successfully',
            'output': str(output_path)
        })

    except Exception as e:
        logger.error(f'Merge error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/split', methods=['POST'])
@validate_response('split')
def split():
    """Split a PDF"""
    try:
        data = request.json
        file = data.get('file')

        if not file or not Path(file).exists():
            return jsonify({'error': 'File not found'}), 400

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = app.config['OUTPUT_FOLDER'] / f'split_{timestamp}'
        output_dir.mkdir(parents=True, exist_ok=True)

        files = split_pdf(file, str(output_dir))
        logger.info(f'PDF split into {len(files)} files')

        return jsonify({
            'success': True,
            'message': f'PDF split into {len(files)} files',
            'files': [str(f) for f in files]
        })

    except Exception as e:
        logger.error(f'Split error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/rotate', methods=['POST'])
@validate_response('rotate')
def rotate():
    """Rotate PDF pages"""
    try:
        data = request.json
        file = data.get('file')
        angle = int(data.get('angle', 90))

        if not file or not Path(file).exists():
            return jsonify({'error': 'File not found'}), 400

        if angle not in [90, 180, 270]:
            return jsonify({'error': 'Angle must be 90, 180, or 270'}), 400

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = app.config['OUTPUT_FOLDER'] / f'rotated_{angle}_{timestamp}.pdf'
        
        rotate_pdf(file, str(output_path), angle)
        logger.info(f'PDF rotated: {output_path}')

        return jsonify({
            'success': True,
            'message': f'PDF rotated {angle} degrees',
            'output': str(output_path)
        })

    except Exception as e:
        logger.error(f'Rotate error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/info', methods=['POST'])
@validate_response('info')
def info():
    """Get PDF information"""
    try:
        data = request.json
        file = data.get('file')

        if not file or not Path(file).exists():
            return jsonify({'error': 'File not found'}), 400

        pdf_info = get_pdf_info(file)
        logger.info(f'Retrieved info: {file}')

        return jsonify({
            'success': True,
            'info': pdf_info
        })

    except Exception as e:
        logger.error(f'Info error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<path:filepath>', methods=['GET'])
def download(filepath):
    """Download processed file"""
    try:
        file_path = Path(app.config['OUTPUT_FOLDER']) / filepath
        
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404

        logger.info(f'Downloaded: {filepath}')
        return send_file(str(file_path), as_attachment=True)

    except Exception as e:
        logger.error(f'Download error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
@validate_response('health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/api/documents', methods=['GET'])
@validate_response('documents')
def get_documents():
    """Get all uploaded documents with their embedding status"""
    try:
        documents = PDFDocument.query.all()
        return jsonify({
            'success': True,
            'documents': [doc.to_dict() for doc in documents],
            'total': len(documents)
        })
    except Exception as e:
        logger.error(f'Error fetching documents: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/documents/<int:doc_id>', methods=['GET'])
@validate_response('document')
def get_document(doc_id):
    """Get specific document details"""
    try:
        document = PDFDocument.query.get(doc_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        return jsonify({
            'success': True,
            'document': document.to_dict(),
            'chunks': [chunk.to_dict() for chunk in document.chunks]
        })
    except Exception as e:
        logger.error(f'Error fetching document: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['POST'])
@validate_response('search')
def search_embeddings():
    """Search for similar chunks using semantic similarity"""
    try:
        data = request.json
        query = data.get('query')
        document_id = data.get('document_id')
        top_k = data.get('top_k', 5)
        threshold = data.get('threshold', 0.5)

        if not query:
            return jsonify({'error': 'Query text required'}), 400

        # Initialize processor
        processor = PDFEmbeddingProcessor(model_name="all-MiniLM-L6-v2")
        
        # Search similar chunks
        results = processor.search_similar_chunks(
            query=query,
            document_id=document_id,
            top_k=top_k,
            threshold=threshold
        )

        # Store search query
        try:
            search = SearchQuery(
                query_text=query,
                results_count=len(results),
                results=results,
                score=np.mean([r['similarity_score'] for r in results]) if results else 0
            )
            db.session.add(search)
            db.session.commit()
        except:
            pass

        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'results_count': len(results)
        })

    except Exception as e:
        logger.error(f'Search error: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/chunks/<int:doc_id>', methods=['GET'])
@validate_response('chunks')
def get_chunks(doc_id):
    """Get all chunks for a document"""
    try:
        document = PDFDocument.query.get(doc_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        chunks = TextChunk.query.filter_by(document_id=doc_id).paginate(
            page=page,
            per_page=per_page
        )

        return jsonify({
            'success': True,
            'document': document.to_dict(),
            'chunks': [chunk.to_dict() for chunk in chunks.items],
            'total': chunks.total,
            'pages': chunks.pages,
            'current_page': page
        })

    except Exception as e:
        logger.error(f'Error fetching chunks: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/embeddings/stats', methods=['GET'])
@validate_response('stats')
def get_embedding_stats():
    """Get embedding statistics"""
    try:
        total_documents = PDFDocument.query.count()
        total_chunks = TextChunk.query.count()
        total_embeddings = Embedding.query.count()
        
        # Calculate statistics
        completed_docs = PDFDocument.query.filter_by(processing_status='completed').count()
        failed_docs = PDFDocument.query.filter_by(processing_status='failed').count()
        processing_docs = PDFDocument.query.filter_by(processing_status='processing').count()

        return jsonify({
            'success': True,
            'statistics': {
                'total_documents': total_documents,
                'total_chunks': total_chunks,
                'total_embeddings': total_embeddings,
                'completed_documents': completed_docs,
                'failed_documents': failed_docs,
                'processing_documents': processing_docs,
                'embedding_dimension': 384  # MiniLM dimension
            }
        })

    except Exception as e:
        logger.error(f'Error fetching stats: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/api/chunk/<int:chunk_id>', methods=['GET'])
@validate_response('chunk')
def get_chunk(chunk_id):
    """Get specific chunk details with embeddings"""
    try:
        chunk = TextChunk.query.get(chunk_id)
        if not chunk:
            return jsonify({'error': 'Chunk not found'}), 404

        embeddings = Embedding.query.filter_by(chunk_id=chunk_id).all()

        return jsonify({
            'success': True,
            'chunk': chunk.to_dict(),
            'embeddings': [emb.to_dict() for emb in embeddings]
        })

    except Exception as e:
        logger.error(f'Error fetching chunk: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f'Server error: {str(error)}')
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info('Starting PDF Processor Flask Application')
    app.run(debug=True, host='0.0.0.0', port=5000)
