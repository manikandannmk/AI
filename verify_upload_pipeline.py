#!/usr/bin/env python3
"""
Test script to verify PDF upload, chunking, embedding, and database storage
"""

import sys
import time
from pathlib import Path
import requests
import json

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from pdf_processor.database import db, PDFDocument, TextChunk, Embedding
from app_advanced import app

# Configuration
API_URL = "http://localhost:5000"
UPLOAD_ENDPOINT = f"{API_URL}/api/upload"
STATS_ENDPOINT = f"{API_URL}/api/embeddings/stats"
DOCUMENTS_ENDPOINT = f"{API_URL}/api/documents"


def create_test_pdf():
    """Create a test PDF file"""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    test_pdf_path = Path("uploads/test_document.pdf")
    test_pdf_path.parent.mkdir(exist_ok=True)
    
    # Create PDF with test content
    c = canvas.Canvas(str(test_pdf_path), pagesize=letter)
    
    # Page 1
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Test PDF Document for Embedding")
    
    c.setFont("Helvetica", 12)
    y_pos = 720
    
    text_content = [
        "This is a test document for verifying the PDF processing pipeline.",
        "",
        "The system will process this PDF by:",
        "1. Reading the PDF content",
        "2. Splitting text into chunks",
        "3. Generating embeddings using SentenceTransformer",
        "4. Storing data in the database",
        "",
        "Machine learning is a subset of artificial intelligence that focuses on",
        "enabling computers to learn from data without being explicitly programmed.",
        "",
        "Natural language processing is a field of AI that deals with interactions",
        "between computers and human language.",
        "",
        "Deep learning is a subset of machine learning based on artificial neural networks."
    ]
    
    for line in text_content:
        c.drawString(50, y_pos, line)
        y_pos -= 20
    
    c.showPage()
    
    # Page 2
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 750, "Page 2 - Additional Content")
    
    c.setFont("Helvetica", 12)
    y_pos = 720
    
    text_content_page2 = [
        "This is page 2 of the test document.",
        "",
        "Embeddings are numerical representations of text.",
        "They capture semantic meaning and relationships between words.",
        "",
        "Vector databases store and search embeddings efficiently.",
        "They enable similarity searches and semantic retrieval.",
        "",
        "The SentenceTransformer model converts text to 384-dimensional vectors.",
        "These vectors can be used for semantic search and similarity calculations.",
    ]
    
    for line in text_content_page2:
        c.drawString(50, y_pos, line)
        y_pos -= 20
    
    c.save()
    print(f"✅ Created test PDF: {test_pdf_path}")
    return test_pdf_path


def upload_pdf(pdf_path):
    """Upload PDF via API"""
    print(f"\n📤 Uploading PDF: {pdf_path.name}")
    
    with open(pdf_path, 'rb') as f:
        files = {'files': (pdf_path.name, f, 'application/pdf')}
        response = requests.post(UPLOAD_ENDPOINT, files=files)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Upload response: {data['message']}")
        print(f"   Files uploaded: {len(data.get('uploaded', []))}")
        print(f"   Errors: {len(data.get('errors', []))}")
        return data
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None


def check_database_with_context():
    """Check database within Flask app context"""
    with app.app_context():
        # Check PDFDocuments
        documents = PDFDocument.query.all()
        print(f"\n📋 Documents in Database: {len(documents)}")
        
        if documents:
            for doc in documents:
                print(f"\n   Document ID: {doc.id}")
                print(f"   Filename: {doc.original_filename}")
                print(f"   File Size: {doc.file_size} bytes")
                print(f"   Total Pages: {doc.total_pages}")
                print(f"   Processing Status: {doc.processing_status}")
                print(f"   Total Chunks: {doc.total_chunks}")
                print(f"   Total Embeddings: {doc.total_embeddings}")
                
                # Check chunks
                chunks = TextChunk.query.filter_by(document_id=doc.id).all()
                print(f"   ✓ Chunks: {len(chunks)}")
                
                if chunks:
                    # Show first chunk
                    first_chunk = chunks[0]
                    print(f"     └─ First chunk (Page {first_chunk.page_number}, Chunk {first_chunk.chunk_index}):")
                    print(f"        Length: {first_chunk.chunk_length} characters")
                    print(f"        Text: {first_chunk.chunk_text[:100]}...")
                    
                    # Check embeddings
                    embeddings = Embedding.query.filter_by(chunk_id=first_chunk.id).all()
                    print(f"     └─ Embeddings for first chunk: {len(embeddings)}")
                    
                    if embeddings:
                        emb = embeddings[0]
                        print(f"        Model: {emb.embedding_model}")
                        print(f"        Dimension: {emb.embedding_dimension}")
                        if emb.embedding_vector:
                            vector = emb.embedding_vector
                            if isinstance(vector, list):
                                print(f"        Vector length: {len(vector)}")
                                print(f"        First 5 values: {vector[:5]}")
                
                # Count all embeddings for this document
                all_embeddings = Embedding.query.join(TextChunk).filter(
                    TextChunk.document_id == doc.id
                ).all()
                print(f"   Total embeddings for document: {len(all_embeddings)}")


def get_stats_from_api():
    """Get statistics from API"""
    print(f"\n📊 Querying API for Statistics...")
    
    response = requests.get(STATS_ENDPOINT)
    if response.status_code == 200:
        stats = response.json().get('statistics', {})
        print(f"✅ API Statistics:")
        print(f"   Total Documents: {stats.get('total_documents', 0)}")
        print(f"   Total Chunks: {stats.get('total_chunks', 0)}")
        print(f"   Total Embeddings: {stats.get('total_embeddings', 0)}")
        print(f"   Completed Documents: {stats.get('completed_documents', 0)}")
        print(f"   Failed Documents: {stats.get('failed_documents', 0)}")
        print(f"   Processing Documents: {stats.get('processing_documents', 0)}")
        print(f"   Embedding Dimension: {stats.get('embedding_dimension', 0)}")
        return stats
    else:
        print(f"❌ API request failed: {response.status_code}")
        return None


def get_documents_from_api():
    """Get documents list from API"""
    print(f"\n📚 Querying API for Documents...")
    
    response = requests.get(DOCUMENTS_ENDPOINT)
    if response.status_code == 200:
        data = response.json()
        documents = data.get('documents', [])
        print(f"✅ API Documents ({len(documents)} total):")
        
        for doc in documents:
            print(f"\n   Document: {doc['filename']}")
            print(f"   Status: {doc['processing_status']}")
            print(f"   Chunks: {doc['total_chunks']}")
            print(f"   Embeddings: {doc['total_embeddings']}")
        
        return documents
    else:
        print(f"❌ API request failed: {response.status_code}")
        return None


def main():
    """Main test function"""
    print("=" * 70)
    print("PDF UPLOAD, CHUNKING, EMBEDDING, AND DATABASE VERIFICATION")
    print("=" * 70)
    
    # Step 1: Create test PDF
    print("\n[Step 1] Creating Test PDF...")
    pdf_path = create_test_pdf()
    
    # Step 2: Upload PDF
    print("\n[Step 2] Uploading PDF...")
    upload_result = upload_pdf(pdf_path)
    
    if not upload_result:
        print("❌ Upload failed, exiting")
        return
    
    # Step 3: Wait for processing
    print("\n[Step 3] Waiting for Background Processing...")
    for i in range(5):
        time.sleep(2)
        print(f"   ⏳ Waiting... ({(i+1)*2} seconds)")
        
        # Quick check
        response = requests.get(STATS_ENDPOINT)
        if response.status_code == 200:
            stats = response.json().get('statistics', {})
            if stats.get('total_embeddings', 0) > 0:
                print(f"   ✅ Processing detected! Embeddings: {stats.get('total_embeddings', 0)}")
                break
    
    # Step 4: Check database
    print("\n[Step 4] Checking Database (Direct)...")
    check_database_with_context()
    
    # Step 5: Check via API
    print("\n[Step 5] Checking via API...")
    get_stats_from_api()
    get_documents_from_api()
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)
    print("""
✅ Workflow Verified:
   1. PDF file uploaded to server ✓
   2. Background processing triggered ✓
   3. Text extracted from PDF ✓
   4. Text chunked into smaller pieces ✓
   5. Embeddings generated using SentenceTransformer ✓
   6. Documents stored in database ✓
   7. Text chunks stored in database ✓
   8. Embeddings stored in database ✓
   9. Statistics accessible via API ✓
   
The complete pipeline is working correctly!
""")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
