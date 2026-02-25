"""
Examples of using and extending the Response Validation system

This file demonstrates various ways to use the validation framework
"""

from pdf_processor.response_validator import (
    ResponseSchema,
    FieldConstraint,
    validate_response,
    validate_response_structure,
    get_validation_errors,
    get_schema,
    SCHEMAS,
    ValidationError
)


# ============================================================================
# EXAMPLE 1: Use validation decorator on endpoint
# ============================================================================

def example_1_decorator():
    """Shows how to add validation to an endpoint"""
    
    from flask import Flask, jsonify, request
    
    app = Flask(__name__)
    
    @app.route('/api/upload', methods=['POST'])
    @validate_response('upload')
    def upload_files():
        """Upload endpoint with automatic response validation"""
        return jsonify({
            'success': True,
            'uploaded': [
                {
                    'name': 'document.pdf',
                    'path': '/uploads/document.pdf',
                    'size': 1024576,
                    'status': 'uploaded - processing embeddings'
                }
            ],
            'errors': [],
            'message': 'Successfully uploaded 1 file. Processing embeddings in background.'
        })


# ============================================================================
# EXAMPLE 2: Manual validation of responses
# ============================================================================

def example_2_manual_validation():
    """Shows how to manually validate responses without decorators"""
    
    response_data = {
        'success': True,
        'uploaded': [{'name': 'doc.pdf'}],
        'errors': [],
        'message': 'Upload successful'
    }
    
    # Method 1: Check if valid (returns bool)
    is_valid = validate_response_structure(response_data, 'upload')
    if is_valid:
        print("✅ Response is valid!")
    else:
        print("❌ Response has validation errors")
    
    # Method 2: Get detailed errors
    errors = get_validation_errors(response_data, 'upload')
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  • {error}")


# ============================================================================
# EXAMPLE 3: Create custom validation schema
# ============================================================================

class CustomReportSchema(ResponseSchema):
    """Custom schema for a report generation endpoint"""
    
    def __init__(self):
        super().__init__()
        
        # Add success field
        self.add_field('success', FieldConstraint(
            required=True,
            data_type=bool,
            allowed_values=[True]
        ))
        
        # Add report ID (required string, max 50 chars)
        self.add_field('report_id', FieldConstraint(
            required=True,
            data_type=str,
            max_length=50
        ))
        
        # Add report title (required string, max 200 chars)
        self.add_field('title', FieldConstraint(
            required=True,
            data_type=str,
            max_length=200
        ))
        
        # Add page count (required, non-negative integer)
        self.add_field('pages', FieldConstraint(
            required=True,
            data_type=int,
            min_value=1
        ))
        
        # Add file size in MB (required, 0-500)
        self.add_field('size_mb', FieldConstraint(
            required=True,
            data_type=float,
            min_value=0.0,
            max_value=500.0
        ))
        
        # Add generation time (optional string)
        self.add_field('generated_at', FieldConstraint(
            required=False,
            data_type=str,
            max_length=100
        ))
        
        # Add report status (required enum)
        self.add_field('status', FieldConstraint(
            required=True,
            data_type=str,
            allowed_values=['draft', 'ready', 'failed']
        ))


def example_3_custom_schema():
    """Demonstrates using a custom schema"""
    
    # Register the schema
    SCHEMAS['custom_report'] = CustomReportSchema()
    
    # Valid report response
    valid_response = {
        'success': True,
        'report_id': 'RPT-001',
        'title': 'Q1 Sales Report',
        'pages': 25,
        'size_mb': 4.5,
        'generated_at': '2024-01-25T14:30:00',
        'status': 'ready'
    }
    
    # Validate
    if validate_response_structure(valid_response, 'custom_report'):
        print("✅ Report response is valid!")
    
    # Invalid response (missing required field)
    invalid_response = {
        'success': True,
        'report_id': 'RPT-002',
        'title': 'Q2 Sales Report',
        # Missing 'pages' and 'size_mb' and 'status'
    }
    
    errors = get_validation_errors(invalid_response, 'custom_report')
    print(f"Found {len(errors)} validation errors:")
    for error in errors:
        print(f"  • {error}")


# ============================================================================
# EXAMPLE 4: Using custom schema in Flask endpoint
# ============================================================================

def example_4_custom_endpoint():
    """Shows how to use custom schema in an endpoint"""
    
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    # Register custom schema
    SCHEMAS['custom_report'] = CustomReportSchema()
    
    @app.route('/api/generate-report', methods=['POST'])
    @validate_response('custom_report')
    def generate_report():
        """Generate a report with validation"""
        return jsonify({
            'success': True,
            'report_id': 'RPT-' + '001',
            'title': 'Sales Analysis',
            'pages': 15,
            'size_mb': 2.3,
            'generated_at': '2024-01-25T14:30:00',
            'status': 'ready'
        })


# ============================================================================
# EXAMPLE 5: Validation with error handling
# ============================================================================

def example_5_error_handling():
    """Shows how to handle validation errors"""
    
    response = {
        'success': True,
        'uploaded': [],
        'errors': [],
        # Missing 'message' - this will fail validation
    }
    
    try:
        schema = get_schema('upload')
        if schema:
            schema.validate(response)
            print("✅ Response validated successfully")
    except ValidationError as e:
        print(f"❌ Validation failed: {str(e)}")


# ============================================================================
# EXAMPLE 6: Bulk validation
# ============================================================================

def example_6_bulk_validation():
    """Validate multiple responses"""
    
    responses = [
        {  # Valid search response
            'success': True,
            'query': 'machine learning',
            'results': [
                {'chunk_id': 1, 'text': '...', 'similarity_score': 0.95}
            ],
            'results_count': 1
        },
        {  # Invalid search response (results_count too high)
            'success': True,
            'query': 'AI',
            'results': [],
            'results_count': 150  # Max is 100
        },
        {  # Valid health response
            'status': 'healthy',
            'timestamp': '2024-01-25T14:30:00'
        },
        {  # Invalid health response (bad status)
            'status': 'running',  # Must be 'healthy', 'degraded', or 'unhealthy'
            'timestamp': '2024-01-25T14:30:00'
        }
    ]
    
    schemas = [
        ('search', responses[0]),
        ('search', responses[1]),
        ('health', responses[2]),
        ('health', responses[3])
    ]
    
    print("Bulk Validation Results:\n")
    for i, (schema_name, response_data) in enumerate(schemas, 1):
        is_valid = validate_response_structure(response_data, schema_name)
        status = "✅ PASS" if is_valid else "❌ FAIL"
        print(f"{i}. {schema_name:15} - {status}")
        
        if not is_valid:
            errors = get_validation_errors(response_data, schema_name)
            for error in errors:
                print(f"   └─ {error}")


# ============================================================================
# EXAMPLE 7: Dynamic schema creation
# ============================================================================

def create_api_response_schema(endpoint_name: str, fields: dict) -> ResponseSchema:
    """Factory function to dynamically create schemas"""
    
    schema = ResponseSchema()
    
    for field_name, constraint_dict in fields.items():
        constraint = FieldConstraint(**constraint_dict)
        schema.add_field(field_name, constraint)
    
    return schema


def example_7_dynamic_schema():
    """Create schemas dynamically at runtime"""
    
    # Define a custom schema dynamically
    fields = {
        'success': {
            'required': True,
            'data_type': bool,
            'allowed_values': [True]
        },
        'user_id': {
            'required': True,
            'data_type': int,
            'min_value': 1
        },
        'username': {
            'required': True,
            'data_type': str,
            'max_length': 50
        },
        'email': {
            'required': True,
            'data_type': str,
            'max_length': 100
        }
    }
    
    # Create schema
    user_schema = create_api_response_schema('user', fields)
    SCHEMAS['user'] = user_schema
    
    # Test it
    valid_user = {
        'success': True,
        'user_id': 123,
        'username': 'johndoe',
        'email': 'john@example.com'
    }
    
    is_valid = validate_response_structure(valid_user, 'user')
    print(f"Dynamic schema validation: {'✅ PASS' if is_valid else '❌ FAIL'}")


# ============================================================================
# EXAMPLE 8: Schema composition
# ============================================================================

class ErrorResponseSchema(ResponseSchema):
    """Base error schema"""
    def __init__(self):
        super().__init__()
        self.add_field('error', FieldConstraint(
            required=True,
            data_type=str,
            max_length=500
        ))


class DetailedErrorSchema(ErrorResponseSchema):
    """Extended error schema with details"""
    def __init__(self):
        super().__init__()
        self.add_field('error_code', FieldConstraint(
            required=False,
            data_type=str,
            max_length=50
        ))
        self.add_field('timestamp', FieldConstraint(
            required=False,
            data_type=str,
            max_length=100
        ))
        self.add_field('details', FieldConstraint(
            required=False,
            data_type=dict
        ))


def example_8_schema_composition():
    """Shows schema inheritance and composition"""
    
    detailed_error = {
        'error': 'File not found',
        'error_code': 'NOT_FOUND_404',
        'timestamp': '2024-01-25T14:30:00',
        'details': {
            'filename': 'missing.pdf',
            'path': '/uploads/missing.pdf'
        }
    }
    
    schema = DetailedErrorSchema()
    
    try:
        schema.validate(detailed_error)
        print("✅ Detailed error validation passed")
    except ValidationError as e:
        print(f"❌ Validation error: {str(e)}")


# ============================================================================
# EXAMPLE 9: Testing with pytest
# ============================================================================

def example_9_pytest_integration():
    """Example of using validation with pytest"""
    
    # This would be in your test file
    def test_upload_response_valid():
        """Test that valid upload response passes validation"""
        response = {
            'success': True,
            'uploaded': [{'name': 'test.pdf'}],
            'errors': [],
            'message': 'Upload successful'
        }
        
        assert validate_response_structure(response, 'upload'), \
            "Valid response should pass validation"
    
    def test_upload_response_missing_field():
        """Test that missing required field fails validation"""
        response = {
            'success': True,
            'uploaded': [],
            # Missing 'message' and 'errors'
        }
        
        errors = get_validation_errors(response, 'upload')
        assert len(errors) > 0, "Should have validation errors"
        assert any('message' in error for error in errors), \
            "Should complain about missing 'message'"
    
    # Run tests
    test_upload_response_valid()
    test_upload_response_missing_field()
    print("✅ All pytest examples passed")


# ============================================================================
# EXAMPLE 10: Validation middleware
# ============================================================================

def example_10_middleware():
    """Create a Flask middleware for validation"""
    
    from flask import Flask, jsonify, request
    import json
    
    app = Flask(__name__)
    
    # Middleware to log all responses
    @app.after_request
    def validate_response_middleware(response):
        """Middleware to validate all JSON responses"""
        
        if response.content_type == 'application/json':
            try:
                data = json.loads(response.get_data(as_text=True))
                
                # Determine schema from endpoint
                endpoint = request.endpoint
                schema_map = {
                    'upload_files': 'upload',
                    'process_files': 'process',
                    'merge': 'merge',
                    'search_embeddings': 'search',
                    # Add more mappings as needed
                }
                
                schema_name = schema_map.get(endpoint)
                if schema_name:
                    errors = get_validation_errors(data, schema_name)
                    if errors:
                        print(f"⚠️  Response validation warnings for {endpoint}:")
                        for error in errors:
                            print(f"   └─ {error}")
            except:
                pass  # Not JSON or other error
        
        return response


# ============================================================================
# Main - Run all examples
# ============================================================================

if __name__ == '__main__':
    print("Response Validation Examples\n" + "="*50)
    
    print("\n1. Using validation decorator:")
    try:
        example_1_decorator()
        print("   ✅ Decorator example created")
    except:
        print("   ℹ️  (Requires Flask app context)")
    
    print("\n2. Manual validation:")
    example_2_manual_validation()
    
    print("\n3. Custom schema:")
    example_3_custom_schema()
    
    print("\n5. Error handling:")
    example_5_error_handling()
    
    print("\n6. Bulk validation:")
    example_6_bulk_validation()
    
    print("\n7. Dynamic schema:")
    example_7_dynamic_schema()
    
    print("\n8. Schema composition:")
    example_8_schema_composition()
    
    print("\n9. Pytest integration:")
    example_9_pytest_integration()
    
    print("\n" + "="*50)
    print("✅ All examples completed successfully!")
