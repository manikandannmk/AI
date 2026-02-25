#!/usr/bin/env python3
"""
Test script for API response validation

This script demonstrates how to validate API responses against defined schemas
and provides examples of valid and invalid responses.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from pdf_processor.response_validator import (
    validate_response_structure,
    get_validation_errors,
    get_schema,
    list_all_schemas,
    ValidationError
)


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_schema(schema_name: str, test_data: dict, description: str = ""):
    """Test a single schema"""
    print(f"Testing: {description or schema_name}")
    print(f"Schema: {schema_name}")
    print(f"Data: {test_data}")
    
    errors = get_validation_errors(test_data, schema_name)
    if errors:
        print("❌ FAILED - Validation Errors:")
        for error in errors:
            print(f"  • {error}")
    else:
        print("✅ PASSED - Response is valid")
    
    print()


def main():
    """Run validation tests"""
    
    print_section("API Response Validation Test Suite")
    
    # Show available schemas
    print("Available Schemas:")
    schemas = list_all_schemas()
    for i, schema_name in enumerate(schemas, 1):
        print(f"  {i:2d}. {schema_name}")
    
    # Test 1: Valid Upload Response
    print_section("Test 1: Valid Upload Response")
    test_schema('upload', {
        'success': True,
        'uploaded': [
            {
                'name': 'document.pdf',
                'path': '/uploads/document.pdf',
                'size': 2048576,
                'status': 'uploaded - processing embeddings'
            }
        ],
        'errors': [],
        'message': 'Successfully uploaded 1 of 1 files. Processing embeddings in background.'
    }, "Valid upload response with one file")
    
    # Test 2: Invalid Upload Response (missing field)
    print_section("Test 2: Invalid Upload Response (Missing Field)")
    test_schema('upload', {
        'success': True,
        'uploaded': [],
        'errors': ['File too large']
        # Missing 'message' field
    }, "Upload response missing required 'message' field")
    
    # Test 3: Invalid Upload Response (wrong type)
    print_section("Test 3: Invalid Upload Response (Wrong Type)")
    test_schema('upload', {
        'success': True,
        'uploaded': 'not a list',  # Should be list
        'errors': [],
        'message': 'Upload failed'
    }, "Upload response with 'uploaded' as string instead of list")
    
    # Test 4: Valid Process Response
    print_section("Test 4: Valid Process Response")
    test_schema('process', {
        'success': True,
        'results': [
            {
                'name': 'doc1.pdf',
                'type': 'success',
                'text': 'Extracted PDF text...',
                'metadata': {'pages': 10, 'author': 'John Doe'}
            }
        ],
        'count': 1
    }, "Valid process response with one file")
    
    # Test 5: Invalid Process Response (negative count)
    print_section("Test 5: Invalid Process Response (Negative Count)")
    test_schema('process', {
        'success': True,
        'results': [],
        'count': -1  # Should be >= 0
    }, "Process response with negative count")
    
    # Test 6: Valid Merge Response
    print_section("Test 6: Valid Merge Response")
    test_schema('merge', {
        'success': True,
        'message': 'PDFs merged successfully',
        'output': '/output/merged_20240101_120000.pdf'
    }, "Valid merge response")
    
    # Test 7: Invalid Merge Response (message too long)
    print_section("Test 7: Invalid Merge Response (Message Too Long)")
    test_schema('merge', {
        'success': True,
        'message': 'A' * 501,  # Exceeds max 500 chars
        'output': '/output/merged.pdf'
    }, "Merge response with message exceeding 500 characters")
    
    # Test 8: Valid Search Response
    print_section("Test 8: Valid Search Response")
    test_schema('search', {
        'success': True,
        'query': 'What is machine learning?',
        'results': [
            {
                'chunk_id': 1,
                'text': 'Machine learning is a subset of AI...',
                'similarity_score': 0.92
            },
            {
                'chunk_id': 5,
                'text': 'Deep learning is a branch of ML...',
                'similarity_score': 0.87
            }
        ],
        'results_count': 2
    }, "Valid search response with 2 results")
    
    # Test 9: Invalid Search Response (results_count too high)
    print_section("Test 9: Invalid Search Response (results_count Too High)")
    test_schema('search', {
        'success': True,
        'query': 'test query',
        'results': [],
        'results_count': 150  # Should be 0-100
    }, "Search response with results_count exceeding max 100")
    
    # Test 10: Valid Chunks Response
    print_section("Test 10: Valid Chunks Response (Pagination)")
    test_schema('chunks', {
        'success': True,
        'document': {
            'id': 1,
            'filename': 'book.pdf',
            'processing_status': 'completed',
            'chunks_count': 50
        },
        'chunks': [
            {'id': 1, 'text': '...', 'chunk_index': 0},
            {'id': 2, 'text': '...', 'chunk_index': 1}
        ],
        'total': 50,
        'pages': 5,
        'current_page': 1
    }, "Valid chunks response with pagination")
    
    # Test 11: Invalid Chunks Response (current_page too high)
    print_section("Test 11: Invalid Chunks Response (Invalid Pagination)")
    test_schema('chunks', {
        'success': True,
        'document': {'id': 1},
        'chunks': [],
        'total': 100,
        'pages': 10,
        'current_page': 0  # Should be >= 1
    }, "Chunks response with current_page = 0 (must be >= 1)")
    
    # Test 12: Valid Health Response
    print_section("Test 12: Valid Health Response")
    test_schema('health', {
        'status': 'healthy',
        'timestamp': '2024-01-15T14:30:45'
    }, "Valid health check response")
    
    # Test 13: Invalid Health Response (invalid status)
    print_section("Test 13: Invalid Health Response (Invalid Status)")
    test_schema('health', {
        'status': 'running',  # Should be 'healthy', 'degraded', or 'unhealthy'
        'timestamp': '2024-01-15T14:30:45'
    }, "Health response with invalid status value")
    
    # Test 14: Valid Error Response
    print_section("Test 14: Valid Error Response")
    test_schema('error', {
        'error': 'File not found: document.pdf'
    }, "Valid error response")
    
    # Test 15: Invalid Error Response (error too long)
    print_section("Test 15: Invalid Error Response (Message Too Long)")
    test_schema('error', {
        'error': 'A' * 501  # Exceeds max 500 chars
    }, "Error response with message exceeding 500 characters")
    
    # Test 16: Valid Documents List Response
    print_section("Test 16: Valid Documents List Response")
    test_schema('documents', {
        'success': True,
        'documents': [
            {
                'id': 1,
                'filename': 'report.pdf',
                'uploaded_at': '2024-01-15T10:00:00',
                'processing_status': 'completed',
                'chunks_count': 25,
                'embeddings_count': 25
            },
            {
                'id': 2,
                'filename': 'guide.pdf',
                'uploaded_at': '2024-01-15T11:00:00',
                'processing_status': 'processing',
                'chunks_count': 0,
                'embeddings_count': 0
            }
        ],
        'total': 2
    }, "Valid documents list with 2 documents")
    
    # Test 17: Valid Single Document Response
    print_section("Test 17: Valid Single Document Response")
    test_schema('document', {
        'success': True,
        'document': {
            'id': 1,
            'filename': 'document.pdf',
            'uploaded_at': '2024-01-15T10:00:00',
            'processing_status': 'completed'
        },
        'chunks': [
            {'id': 1, 'text': 'First chunk...', 'chunk_index': 0, 'tokens': 250},
            {'id': 2, 'text': 'Second chunk...', 'chunk_index': 1, 'tokens': 300}
        ]
    }, "Valid single document with chunks")
    
    # Test 18: Valid Embedding Stats Response
    print_section("Test 18: Valid Embedding Stats Response")
    test_schema('stats', {
        'success': True,
        'statistics': {
            'total_documents': 5,
            'total_chunks': 125,
            'total_embeddings': 125,
            'completed_documents': 4,
            'failed_documents': 1,
            'processing_documents': 0,
            'embedding_dimension': 384
        }
    }, "Valid embedding statistics response")
    
    # Test 19: Valid Split Response
    print_section("Test 19: Valid Split Response")
    test_schema('split', {
        'success': True,
        'message': 'PDF split into 5 files',
        'files': [
            '/output/split_20240115_140000/page_1.pdf',
            '/output/split_20240115_140000/page_2.pdf',
            '/output/split_20240115_140000/page_3.pdf',
            '/output/split_20240115_140000/page_4.pdf',
            '/output/split_20240115_140000/page_5.pdf'
        ]
    }, "Valid split response with 5 files")
    
    # Test 20: Valid Rotate Response
    print_section("Test 20: Valid Rotate Response")
    test_schema('rotate', {
        'success': True,
        'message': 'PDF rotated 90 degrees',
        'output': '/output/rotated_90_20240115_140000.pdf'
    }, "Valid rotate response")
    
    # Summary
    print_section("Test Suite Summary")
    print("""
✅ Test suite completed!

Key takeaways:
  1. All responses must conform to their schema
  2. Required fields must always be present
  3. Field types must match exactly
  4. String lengths have maximum limits
  5. Numeric values have minimum/maximum ranges
  6. Enums (allowed_values) restrict to specific values
  7. Use validation during development to catch errors early
  
For more information, see RESPONSE_VALIDATION_GUIDE.md
    """)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error running tests: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
