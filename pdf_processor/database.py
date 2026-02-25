"""
Database models for storing PDF embeddings
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class PDFDocument(db.Model):
    """Model for storing PDF document metadata"""
    __tablename__ = 'pdf_documents'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)  # in bytes
    total_pages = db.Column(db.Integer)
    total_chunks = db.Column(db.Integer, default=0)
    total_embeddings = db.Column(db.Integer, default=0)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    processing_status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    processing_date = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    doc_metadata = db.Column(db.JSON)  # Store additional metadata

    # Relationship
    chunks = db.relationship('TextChunk', backref='document', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'total_pages': self.total_pages,
            'total_chunks': self.total_chunks,
            'total_embeddings': self.total_embeddings,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'processing_status': self.processing_status,
            'processing_date': self.processing_date.isoformat() if self.processing_date else None,
        }


class TextChunk(db.Model):
    """Model for storing text chunks from PDF pages"""
    __tablename__ = 'text_chunks'

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('pdf_documents.id'), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    chunk_index = db.Column(db.Integer, nullable=False)  # Order of chunks within page
    chunk_text = db.Column(db.Text, nullable=False)
    chunk_length = db.Column(db.Integer)  # Length of the chunk in characters
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    embeddings = db.relationship('Embedding', backref='chunk', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'document_filename': self.document.filename if self.document else None,
            'page_number': self.page_number,
            'chunk_index': self.chunk_index,
            'chunk_text': self.chunk_text,
            'chunk_length': self.chunk_length,
        }


class Embedding(db.Model):
    """Model for storing embeddings of text chunks"""
    __tablename__ = 'embeddings'

    id = db.Column(db.Integer, primary_key=True)
    chunk_id = db.Column(db.Integer, db.ForeignKey('text_chunks.id'), nullable=False)
    embedding_model = db.Column(db.String(100), default='sentence-transformers')
    embedding_vector = db.Column(db.JSON)  # Store embedding as JSON array
    embedding_dimension = db.Column(db.Integer)  # Dimension of the embedding
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'chunk_id': self.chunk_id,
            'embedding_model': self.embedding_model,
            'embedding_dimension': self.embedding_dimension,
            'created_date': self.created_date.isoformat() if self.created_date else None,
        }


class SearchQuery(db.Model):
    """Model for storing search queries and results"""
    __tablename__ = 'search_queries'

    id = db.Column(db.Integer, primary_key=True)
    query_text = db.Column(db.Text, nullable=False)
    query_embedding = db.Column(db.JSON)
    results_count = db.Column(db.Integer)
    results = db.Column(db.JSON)  # Store top results
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float)  # Average similarity score

    def to_dict(self):
        return {
            'id': self.id,
            'query_text': self.query_text,
            'results_count': self.results_count,
            'score': self.score,
            'created_date': self.created_date.isoformat() if self.created_date else None,
        }


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
