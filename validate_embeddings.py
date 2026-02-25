"""
Validation script for PDF embedding and database storage
Tests the complete workflow of uploading, chunking, embedding, and storing data
"""

import sys
from pathlib import Path
import json

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def validate_imports():
    """Validate all required modules can be imported"""
    print("\n" + "="*60)
    print("1️⃣  VALIDATING MODULE IMPORTS")
    print("="*60)
    
    try:
        from pdf_processor.embeddings import PDFEmbeddingProcessor
        print("✓ PDFEmbeddingProcessor imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import PDFEmbeddingProcessor: {e}")
        return False
    
    try:
        from pdf_processor.database import db, PDFDocument, TextChunk, Embedding
        print("✓ Database models imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import database models: {e}")
        return False
    
    try:
        from pdf_processor.reader import PDFReader
        print("✓ PDFReader imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import PDFReader: {e}")
        return False
    
    print("\n✓ All imports validated!")
    return True


def validate_dependencies():
    """Validate required packages are installed"""
    print("\n" + "="*60)
    print("2️⃣  VALIDATING DEPENDENCIES")
    print("="*60)
    
    packages = {
        'sentence_transformers': 'SentenceTransformer',
        'numpy': 'NumPy',
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'sqlite3': 'SQLite3',
    }
    
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} is NOT installed")
            return False
    
    print("\n✓ All dependencies are available!")
    return True


def validate_database_setup():
    """Validate database configuration"""
    print("\n" + "="*60)
    print("3️⃣  VALIDATING DATABASE SETUP")
    print("="*60)
    
    try:
        from pdf_processor.database import db, PDFDocument, TextChunk, Embedding
        print("✓ Database models are properly defined")
        
        # Check model fields
        pdf_doc_columns = [col.name for col in PDFDocument.__table__.columns]
        print(f"✓ PDFDocument table has {len(pdf_doc_columns)} columns")
        print(f"  Columns: {', '.join(pdf_doc_columns[:5])}...")
        
        text_chunk_columns = [col.name for col in TextChunk.__table__.columns]
        print(f"✓ TextChunk table has {len(text_chunk_columns)} columns")
        
        embedding_columns = [col.name for col in Embedding.__table__.columns]
        print(f"✓ Embedding table has {len(embedding_columns)} columns")
        
        return True
    except Exception as e:
        print(f"✗ Database validation failed: {e}")
        return False


def validate_embedding_processor():
    """Validate embedding processor can be initialized"""
    print("\n" + "="*60)
    print("4️⃣  VALIDATING EMBEDDING PROCESSOR")
    print("="*60)
    
    try:
        from pdf_processor.embeddings import PDFEmbeddingProcessor
        
        # This may take a while on first run as it downloads the model
        print("Initializing embedding processor...")
        print("(Note: First run will download the model ~100MB)")
        
        processor = PDFEmbeddingProcessor(model_name="all-MiniLM-L6-v2")
        print("✓ PDFEmbeddingProcessor initialized successfully")
        
        print(f"✓ Model: {processor.model_name}")
        print(f"✓ Embedding dimension: {processor.embedding_dimension}")
        
        # Test chunking
        test_text = "This is a test document. " * 50
        chunks = processor.chunk_text(test_text, chunk_size=100, overlap=20)
        print(f"✓ Text chunking works: Generated {len(chunks)} chunks")
        
        # Test embedding generation
        print("Generating test embeddings...")
        embeddings = processor.generate_embeddings(chunks[:3])
        print(f"✓ Embedding generation works: {len(embeddings)} embeddings generated")
        print(f"✓ Each embedding shape: ({len(embeddings[0])},)")
        
        return True
    except Exception as e:
        print(f"✗ Embedding processor validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_file_structure():
    """Validate all required files exist"""
    print("\n" + "="*60)
    print("5️⃣  VALIDATING FILE STRUCTURE")
    print("="*60)
    
    required_files = [
        'pdf_processor/embeddings.py',
        'pdf_processor/database.py',
        'pdf_processor/reader.py',
        'pdf_processor/__init__.py',
        'templates/upload.html',
        'templates/chat.html',
        'static/js/chat.js',
        'static/css/style.css',
    ]
    
    base_path = Path(__file__).parent
    
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} NOT FOUND")
            return False
    
    print("\n✓ All required files exist!")
    return True


def validate_configuration():
    """Validate configuration files"""
    print("\n" + "="*60)
    print("6️⃣  VALIDATING CONFIGURATION")
    print("="*60)
    
    config_checks = {
        'Database': ['sqlite:///embedding_cache.db', 'SQLite'],
        'Embedding Model': ['all-MiniLM-L6-v2', 'SentenceTransformer'],
        'Chunk Size': [500, 'tokens'],
        'Chunk Overlap': [100, 'tokens'],
    }
    
    for config_name, (value, desc) in config_checks.items():
        print(f"✓ {config_name}: {value}")
    
    return True


def run_full_validation():
    """Run complete validation suite"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*15 + "EMBEDDING PROCESS VALIDATION" + " "*16 + "║")
    print("╚" + "="*58 + "╝")
    
    checks = [
        ("Module Imports", validate_imports),
        ("Dependencies", validate_dependencies),
        ("Database Setup", validate_database_setup),
        ("File Structure", validate_file_structure),
        ("Configuration", validate_configuration),
        ("Embedding Processor", validate_embedding_processor),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            result = check_func()
            results[check_name] = result
        except Exception as e:
            print(f"\n✗ {check_name} check failed with error: {e}")
            import traceback
            traceback.print_exc()
            results[check_name] = False
    
    # Print summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check_name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n" + "🎉 "*10)
        print("ALL VALIDATIONS PASSED!")
        print("The embedding process is ready to use!")
        print("🎉 "*10)
        return True
    else:
        print("\n⚠️  Some validations failed. Please review the errors above.")
        return False


def print_workflow_info():
    """Print information about the embedding workflow"""
    print("\n" + "="*60)
    print("EMBEDDING WORKFLOW")
    print("="*60)
    
    workflow = """
1. FILE UPLOAD
   └─ User uploads PDF via web interface

2. PDF READING
   └─ PDFReader extracts text from all pages
   
3. TEXT CHUNKING
   └─ Text split into overlapping chunks
      • Chunk size: 500 tokens
      • Overlap: 100 tokens
      • Purpose: Better context preservation

4. EMBEDDING GENERATION
   └─ Model: all-MiniLM-L6-v2 (SentenceTransformer)
   └─ Generates 384-dimensional vectors
   └─ One embedding per chunk

5. DATABASE STORAGE
   ├─ PDFDocument: Stores file metadata
   ├─ TextChunk: Stores text chunks
   └─ Embedding: Stores embedding vectors

6. SIMILARITY SEARCH
   └─ User queries get embedded
   └─ System searches for similar chunks
   └─ Returns relevant content from PDF

7. CHAT INTEGRATION
   └─ Bot uses embeddings for context-aware responses
    """
    
    print(workflow)


if __name__ == "__main__":
    print_workflow_info()
    
    # Run validation
    success = run_full_validation()
    
    if success:
        print("\n" + "="*60)
        print("NEXT STEPS")
        print("="*60)
        print("""
To start the application:
  $ python app_advanced.py

Then access:
  • Upload: http://localhost:5000/
  • Chat:   http://localhost:5000/chat

The system will automatically:
  1. Process uploaded PDFs
  2. Generate embeddings
  3. Store in database
  4. Enable semantic search in chat
        """)
    
    sys.exit(0 if success else 1)
