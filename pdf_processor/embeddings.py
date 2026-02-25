"""
PDF processing with chunking and embedding generation
"""

import re
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from .reader import PDFReader
from .database import db, PDFDocument, TextChunk, Embedding


class PDFEmbeddingProcessor:
    """Process PDF files and generate embeddings"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding processor
        
        Args:
            model_name: HuggingFace model name for embeddings
                       Options: 'all-MiniLM-L6-v2', 'all-mpnet-base-v2', 'distiluse-base-multilingual-cased-v2'
        """
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.embedding_dimension = self.model.get_sentence_embedding_dimension()

    def read_pdf_pages(self, pdf_path: str) -> List[str]:
        """
        Read all pages from PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of text content per page
        """
        try:
            reader = PDFReader(pdf_path)
            pages_text = reader.extract_text_by_page()
            return pages_text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks in characters
            
        Returns:
            List of text chunks
        """
        if not text or len(text.strip()) == 0:
            return []

        # Clean text
        text = self._clean_text(text)
        
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end].strip()
            
            if chunk:  # Only add non-empty chunks
                chunks.append(chunk)
            
            start = end - overlap if end - overlap > start else end

        return chunks

    def _clean_text(self, text: str) -> str:
        """Clean text by removing extra whitespace and special characters"""
        # Remove multiple whitespaces
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-]', '', text)
        return text.strip()

    def generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for text chunks
        
        Args:
            texts: List of text chunks
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")

    def process_pdf(self, pdf_path: str, original_filename: str, 
                   chunk_size: int = 500, overlap: int = 100) -> Tuple[PDFDocument, int]:
        """
        Complete PDF processing pipeline: read, chunk, embed, and store
        
        Args:
            pdf_path: Path to PDF file
            original_filename: Original filename
            chunk_size: Size of text chunks
            overlap: Overlap between chunks
            
        Returns:
            Tuple of (PDFDocument object, number of embeddings created)
        """
        try:
            # Read PDF pages
            pages = self.read_pdf_pages(pdf_path)
            
            # Create document record
            doc = PDFDocument(
                filename=pdf_path.split('/')[-1],
                original_filename=original_filename,
                file_path=pdf_path,
                total_pages=len(pages),
                processing_status='processing'
            )
            db.session.add(doc)
            db.session.flush()  # Get the document ID
            
            total_embeddings = 0
            total_chunks = 0

            # Process each page
            for page_num, page_text in enumerate(pages, 1):
                # Split page into chunks
                chunks = self.chunk_text(page_text, chunk_size, overlap)
                
                for chunk_idx, chunk_text in enumerate(chunks):
                    if not chunk_text.strip():
                        continue

                    # Create chunk record
                    text_chunk = TextChunk(
                        document_id=doc.id,
                        page_number=page_num,
                        chunk_index=chunk_idx,
                        chunk_text=chunk_text,
                        chunk_length=len(chunk_text)
                    )
                    db.session.add(text_chunk)
                    db.session.flush()

                    # Generate embedding
                    embedding_vector = self.model.encode(chunk_text, convert_to_numpy=True)
                    
                    # Store embedding
                    embedding = Embedding(
                        chunk_id=text_chunk.id,
                        embedding_model=self.model_name,
                        embedding_vector=embedding_vector.tolist(),
                        embedding_dimension=self.embedding_dimension
                    )
                    db.session.add(embedding)
                    
                    total_chunks += 1
                    total_embeddings += 1

            # Update document
            doc.total_chunks = total_chunks
            doc.total_embeddings = total_embeddings
            doc.processing_status = 'completed'
            
            from datetime import datetime
            doc.processing_date = datetime.utcnow()
            
            db.session.commit()
            
            return doc, total_embeddings

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error processing PDF: {str(e)}")

    def search_similar_chunks(self, query: str, document_id: int = None, 
                             top_k: int = 5, threshold: float = 0.5) -> List[dict]:
        """
        Search for similar chunks based on semantic similarity
        
        Args:
            query: Search query
            document_id: Optional document ID to limit search
            top_k: Number of top results to return
            threshold: Minimum similarity score (0-1)
            
        Returns:
            List of similar chunks with scores
        """
        try:
            # Generate query embedding
            query_embedding = self.model.encode(query, convert_to_numpy=True)
            
            # Get all embeddings
            if document_id:
                embeddings_data = db.session.query(Embedding).join(TextChunk).filter(
                    TextChunk.document_id == document_id
                ).all()
            else:
                embeddings_data = db.session.query(Embedding).all()

            results = []
            
            for embedding in embeddings_data:
                # Calculate cosine similarity
                embedding_vector = np.array(embedding.embedding_vector)
                similarity = self._cosine_similarity(query_embedding, embedding_vector)
                
                if similarity >= threshold:
                    chunk = embedding.chunk
                    results.append({
                        'chunk_id': chunk.id,
                        'document_id': chunk.document_id,
                        'document_filename': chunk.document.filename,
                        'page_number': chunk.page_number,
                        'chunk_index': chunk.chunk_index,
                        'chunk_text': chunk.chunk_text,
                        'similarity_score': float(similarity)
                    })

            # Sort by similarity score and return top_k
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            return results[:top_k]

        except Exception as e:
            raise Exception(f"Error searching chunks: {str(e)}")

    @staticmethod
    def _cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = np.dot(vec1, vec2) / (norm1 * norm2)
        return similarity


def create_processor(model_name: str = "all-MiniLM-L6-v2") -> PDFEmbeddingProcessor:
    """Factory function to create embedding processor"""
    return PDFEmbeddingProcessor(model_name)
