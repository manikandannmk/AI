# API Response Validation Guide

## Overview

All API endpoint responses are now validated against predefined schemas to ensure consistency, data integrity, and proper error handling.

## Validation Architecture

### Components

1. **ResponseSchema** - Base class for defining response structure
2. **FieldConstraint** - Defines constraints for individual fields
3. **@validate_response()** - Decorator to validate endpoint responses
4. **Validation Registry** - Schema definitions for all endpoints

### Constraint Types

- **Type checking** - Ensures field is correct data type
- **Required fields** - Validates presence of mandatory fields
- **Length constraints** - Min/Max string length validation
- **Numeric ranges** - Min/Max value validation for numbers
- **Allowed values** - Validates field against whitelist
- **Pattern matching** - Regex pattern validation (extensible)

---

## API Response Schemas

### 1. Upload Response (`/api/upload`)

**Schema Name:** `upload`

```python
{
    "success": true,                    # boolean (required)
    "uploaded": [                       # list (required)
        {
            "name": "doc.pdf",          # string
            "path": "/uploads/doc.pdf", # string  
            "size": 1024,               # integer (bytes)
            "status": "uploading"       # string
        }
    ],
    "errors": [],                       # list (required)
    "message": "Successfully uploaded..." # string, max 500 chars
}
```

**Constraints:**
- `success`: Must be `true`
- `uploaded`: Array of file objects
- `errors`: Array of error messages
- `message`: Max 500 characters

**Failure Response:**
```python
{
    "error": "No files provided"  # string, max 500 chars
}
```

---

### 2. Process Response (`/api/process`)

**Schema Name:** `process`

```python
{
    "success": true,            # boolean (required)
    "results": [                # list (required)
        {
            "name": "doc.pdf",
            "type": "success",
            "text": "...",
            "metadata": {},
            "tables_count": 0
        }
    ],
    "count": 1                  # integer, min 0 (required)
}
```

**Constraints:**
- `success`: Must be `true`
- `results`: Array of processing results
- `count`: Non-negative integer

---

### 3. Merge Response (`/api/merge`)

**Schema Name:** `merge`

```python
{
    "success": true,                    # boolean (required)
    "message": "PDFs merged...",        # string, max 500 chars
    "output": "/output/merged_...pdf"  # string, max 1000 chars
}
```

**Constraints:**
- `success`: Must be `true`
- `message`: Max 500 characters
- `output`: File path, max 1000 characters

---

### 4. Split Response (`/api/split`)

**Schema Name:** `split`

```python
{
    "success": true,                # boolean (required)
    "message": "PDF split into...", # string, max 500 chars
    "files": [                      # list (required)
        "/output/split_1.pdf",
        "/output/split_2.pdf"
    ]
}
```

**Constraints:**
- `success`: Must be `true`
- `message`: Max 500 characters
- `files`: Array of file paths

---

### 5. Rotate Response (`/api/rotate`)

**Schema Name:** `rotate`

```python
{
    "success": true,                    # boolean (required)
    "message": "PDF rotated 90...",    # string, max 500 chars
    "output": "/output/rotated_...pdf" # string, max 1000 chars
}
```

**Constraints:**
- `success`: Must be `true`
- `message`: Max 500 characters
- `output`: File path, max 1000 characters

---

### 6. Info Response (`/api/info`)

**Schema Name:** `info`

```python
{
    "success": true,    # boolean (required)
    "info": {           # dict (required)
        "pages": 10,
        "size": "2.5MB",
        "author": "..."
    }
}
```

**Constraints:**
- `success`: Must be `true`
- `info`: Dictionary containing PDF metadata

---

### 7. Documents Response (`/api/documents`)

**Schema Name:** `documents`

```python
{
    "success": true,        # boolean (required)
    "documents": [          # list (required)
        {
            "id": 1,
            "filename": "doc.pdf",
            "uploaded_at": "2024-01-01T00:00:00",
            "processing_status": "completed",
            "chunks_count": 5,
            "embeddings_count": 5
        }
    ],
    "total": 1              # integer, min 0 (required)
}
```

**Constraints:**
- `success`: Must be `true`
- `documents`: Array of document objects
- `total`: Non-negative integer

---

### 8. Single Document Response (`/api/documents/<id>`)

**Schema Name:** `document`

```python
{
    "success": true,        # boolean (required)
    "document": {           # dict (required)
        "id": 1,
        "filename": "doc.pdf",
        "uploaded_at": "...",
        "processing_status": "completed"
    },
    "chunks": [             # list (required)
        {
            "id": 1,
            "text": "...",
            "chunk_index": 0,
            "tokens": 450
        }
    ]
}
```

**Constraints:**
- `success`: Must be `true`
- `document`: Document dictionary
- `chunks`: Array of chunk objects

---

### 9. Search Response (`/api/search`)

**Schema Name:** `search`

```python
{
    "success": true,            # boolean (required)
    "query": "search text",     # string, max 500 chars (required)
    "results": [                # list (required)
        {
            "chunk_id": 1,
            "text": "...",
            "similarity_score": 0.95
        }
    ],
    "results_count": 5          # integer, 0-100 (required)
}
```

**Constraints:**
- `success`: Must be `true`
- `query`: Max 500 characters
- `results`: Array of search results
- `results_count`: Integer between 0 and 100

---

### 10. Chunks Response (`/api/chunks/<id>`)

**Schema Name:** `chunks`

```python
{
    "success": true,        # boolean (required)
    "document": {...},      # dict (required)
    "chunks": [...],        # list (required)
    "total": 50,            # integer, min 0 (required)
    "pages": 5,             # integer, min 1 (required)
    "current_page": 1       # integer, min 1 (required)
}
```

**Constraints:**
- `success`: Must be `true`
- `document`: Document dictionary
- `chunks`: Array of chunk objects
- `total`: Non-negative integer
- `pages`: Positive integer (>= 1)
- `current_page`: Positive integer (>= 1)

---

### 11. Embedding Stats Response (`/api/embeddings/stats`)

**Schema Name:** `stats`

```python
{
    "success": true,        # boolean (required)
    "statistics": {         # dict (required)
        "total_documents": 10,
        "total_chunks": 100,
        "total_embeddings": 100,
        "completed_documents": 9,
        "failed_documents": 1,
        "processing_documents": 0,
        "embedding_dimension": 384
    }
}
```

**Constraints:**
- `success`: Must be `true`
- `statistics`: Dictionary with numeric values

---

### 12. Chunk Detail Response (`/api/chunk/<id>`)

**Schema Name:** `chunk`

```python
{
    "success": true,        # boolean (required)
    "chunk": {              # dict (required)
        "id": 1,
        "text": "...",
        "chunk_index": 0,
        "tokens": 450
    },
    "embeddings": [         # list (required)
        {
            "id": 1,
            "vector": [...],
            "created_at": "..."
        }
    ]
}
```

**Constraints:**
- `success`: Must be `true`
- `chunk`: Chunk dictionary
- `embeddings`: Array of embedding objects

---

### 13. Health Response (`/api/health`)

**Schema Name:** `health`

```python
{
    "status": "healthy",              # string, allowed: ["healthy", "degraded", "unhealthy"]
    "timestamp": "2024-01-01T00:00:00"  # string, max 100 chars
}
```

**Constraints:**
- `status`: Must be one of: "healthy", "degraded", "unhealthy"
- `timestamp`: ISO format datetime, max 100 characters

---

### 14. Error Response

**Schema Name:** `error`

```python
{
    "error": "Error message here"  # string, max 500 chars (required)
}
```

**Constraints:**
- `error`: Required, descriptive error message, max 500 characters
- Status code: 400, 404, 500, etc.

---

## Validation Usage

### Automatic Validation

All endpoints with `@validate_response()` decorator automatically validate responses:

```python
@app.route('/api/upload', methods=['POST'])
@validate_response('upload')
def upload_files():
    # ... endpoint code ...
    return jsonify({
        'success': True,
        'uploaded': [...],
        'errors': [],
        'message': '...'
    })
```

### Manual Validation

For custom validation in your code:

```python
from pdf_processor.response_validator import validate_response_structure, get_validation_errors

# Check if valid
if validate_response_structure(data, 'upload'):
    print("Response is valid!")

# Get error details
errors = get_validation_errors(data, 'upload')
for error in errors:
    print(f"Validation error: {error}")
```

### Validation Decorator

Apply validation to any endpoint:

```python
from pdf_processor.response_validator import validate_response

@app.route('/custom/endpoint', methods=['POST'])
@validate_response('upload')  # or any schema name
def custom_endpoint():
    return jsonify(response_data)
```

---

## Field Constraints

### FieldConstraint Parameters

```python
FieldConstraint(
    required=True,              # Field must be present
    data_type=str,              # Field must be this type
    min_length=None,            # Min string length
    max_length=500,             # Max string length
    min_value=None,             # Min numeric value
    max_value=100,              # Max numeric value
    allowed_values=['a', 'b'],  # Whitelist of allowed values
    pattern=None                # Regex pattern (future)
)
```

### Supported Data Types

- `str` - String
- `int` - Integer
- `float` - Floating point
- `bool` - Boolean
- `list` - Array/List
- `dict` - Dictionary/Object

---

## Error Handling

### Validation Exceptions

If validation fails, a `ValidationError` is raised:

```python
from pdf_processor.response_validator import ValidationError

try:
    schema.validate(data)
except ValidationError as e:
    print(f"Validation failed: {str(e)}")
```

### Error Messages

Validation errors include helpful details:

```
Field 'count' must be >= 0
Field 'message' exceeds maximum length 500
Required field 'success' is missing
Field 'status' must be of type bool, got str
Field 'level' must be one of ['high', 'medium', 'low']
```

---

## Testing Responses

### Using the Validation Tester

Create a test script to validate responses:

```python
from pdf_processor.response_validator import get_validation_errors

# Test upload response
response = {
    'success': True,
    'uploaded': [{'name': 'doc.pdf'}],
    'errors': [],
    'message': 'Uploaded 1 file'
}

errors = get_validation_errors(response, 'upload')
if errors:
    print("Validation failed:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Response is valid!")
```

### Available Helper Functions

```python
from pdf_processor.response_validator import (
    validate_response_structure,    # Returns bool
    get_validation_errors,          # Returns list of errors
    get_schema,                     # Returns schema object
    list_all_schemas               # Returns list of schema names
)

# Check if valid
is_valid = validate_response_structure(data, 'upload')

# Get all available schemas
all_schemas = list_all_schemas()
print(all_schemas)
# Output: ['upload', 'process', 'merge', 'split', 'rotate', 'info', ...]
```

---

## Common Validation Patterns

### Pattern 1: Required Status Field

All success responses must have:
```python
'success': True  # boolean, required
```

### Pattern 2: Error Responses

All error responses must have:
```python
'error': 'Error description'  # string, required, max 500 chars
```

### Pattern 3: Lists in Responses

Arrays should be:
- Present (even if empty)
- Contain valid objects
- Not exceed reasonable limits

### Pattern 4: File Paths

File paths:
- String type
- Max 1000 characters
- Should be absolute or relative to app root

### Pattern 5: Timestamps

Timestamps:
- ISO 8601 format
- String type
- Max 100 characters

---

## Adding New Schemas

To add validation for new endpoints:

```python
from pdf_processor.response_validator import ResponseSchema, FieldConstraint, SCHEMAS

# Create schema
class CustomResponseSchema(ResponseSchema):
    def __init__(self):
        super().__init__()
        self.add_field('success', FieldConstraint(
            required=True,
            data_type=bool,
            allowed_values=[True]
        ))
        self.add_field('custom_field', FieldConstraint(
            required=True,
            data_type=str,
            max_length=200
        ))

# Register schema
SCHEMAS['custom'] = CustomResponseSchema()

# Use in endpoints
@app.route('/custom', methods=['POST'])
@validate_response('custom')
def custom_endpoint():
    return jsonify({
        'success': True,
        'custom_field': 'value'
    })
```

---

## Performance Considerations

- Validation occurs only on successful (2xx) responses
- Minimal overhead - field checks are O(n) where n = number of fields
- Logging at INFO/DEBUG level only
- Non-blocking - validation doesn't interrupt response flow

---

## Best Practices

1. **Always use decorators** - Apply `@validate_response()` to all endpoints
2. **Be specific with constraints** - Set realistic min/max values
3. **Document changes** - Update this guide when adding schemas
4. **Test responses** - Use validation during development
5. **Monitor logs** - Check for validation warnings
6. **Version schemas** - Keep backward compatibility in mind

---

## Troubleshooting

### "Required field 'X' is missing"
- Ensure endpoint returns the field
- Check field name spelling

### "Field 'X' must be of type Y"
- Convert value to correct type before returning
- Use `str()`, `int()`, `bool()` as needed

### "Field 'X' exceeds maximum length Z"
- Truncate string to max length
- Use substring: `value[:max_length]`

### "Validation not triggering"
- Ensure `@validate_response()` decorator is present
- Check schema name matches endpoint requirements
- Verify response returns 2xx status code

---

## Full Schema Reference

| Schema Name | Endpoint | Primary Fields |
|---|---|---|
| upload | /api/upload | success, uploaded, errors, message |
| process | /api/process | success, results, count |
| merge | /api/merge | success, message, output |
| split | /api/split | success, message, files |
| rotate | /api/rotate | success, message, output |
| info | /api/info | success, info |
| documents | /api/documents | success, documents, total |
| document | /api/documents/<id> | success, document, chunks |
| search | /api/search | success, query, results, results_count |
| chunks | /api/chunks/<id> | success, document, chunks, total, pages, current_page |
| chunk | /api/chunk/<id> | success, chunk, embeddings |
| stats | /api/embeddings/stats | success, statistics |
| health | /api/health | status, timestamp |
| error | (all errors) | error |

---

## Questions & Support

For validation-related questions or to request new schemas:
1. Check this guide's examples
2. Review response_validator.py source code
3. Run validation tests with get_validation_errors()
4. Check application logs for validation messages
