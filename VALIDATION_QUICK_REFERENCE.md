# Response Validation Quick Reference

## Field Constraint Types

| Constraint | Type | Example | Purpose |
|-----------|------|---------|---------|
| `required` | bool | `True` | Field must be present |
| `data_type` | Type | `str, int, bool, list, dict` | Type checking |
| `min_length` | int | `10` | Min string length |
| `max_length` | int | `500` | Max string length |
| `min_value` | number | `0` | Min numeric value |
| `max_value` | number | `100` | Max numeric value |
| `allowed_values` | list | `['high', 'medium', 'low']` | Enum validation |

## Schema Validation Summary

### ✅ Upload Response (`/api/upload`)
```
success (bool)          ✓ Required ✓ = true
uploaded (list)         ✓ Required
errors (list)           ✓ Required
message (str 0-500)     ✓ Required
```

### ✅ Process Response (`/api/process`)
```
success (bool)          ✓ Required ✓ = true
results (list)          ✓ Required
count (int ≥0)          ✓ Required
```

### ✅ Merge Response (`/api/merge`)
```
success (bool)          ✓ Required ✓ = true
message (str 0-500)     ✓ Required
output (str 0-1000)     ✓ Required
```

### ✅ Split Response (`/api/split`)
```
success (bool)          ✓ Required ✓ = true
message (str 0-500)     ✓ Required
files (list)            ✓ Required
```

### ✅ Rotate Response (`/api/rotate`)
```
success (bool)          ✓ Required ✓ = true
message (str 0-500)     ✓ Required
output (str 0-1000)     ✓ Required
```

### ✅ Info Response (`/api/info`)
```
success (bool)          ✓ Required ✓ = true
info (dict)             ✓ Required
```

### ✅ Documents Response (`/api/documents`)
```
success (bool)          ✓ Required ✓ = true
documents (list)        ✓ Required
total (int ≥0)          ✓ Required
```

### ✅ Document Response (`/api/documents/<id>`)
```
success (bool)          ✓ Required ✓ = true
document (dict)         ✓ Required
chunks (list)           ✓ Required
```

### ✅ Search Response (`/api/search`)
```
success (bool)          ✓ Required ✓ = true
query (str 0-500)       ✓ Required
results (list)          ✓ Required
results_count (0-100)   ✓ Required
```

### ✅ Chunks Response (`/api/chunks/<id>`)
```
success (bool)          ✓ Required ✓ = true
document (dict)         ✓ Required
chunks (list)           ✓ Required
total (int ≥0)          ✓ Required
pages (int ≥1)          ✓ Required
current_page (int ≥1)   ✓ Required
```

### ✅ Chunk Response (`/api/chunk/<id>`)
```
success (bool)          ✓ Required ✓ = true
chunk (dict)            ✓ Required
embeddings (list)       ✓ Required
```

### ✅ Stats Response (`/api/embeddings/stats`)
```
success (bool)          ✓ Required ✓ = true
statistics (dict)       ✓ Required
```

### ✅ Health Response (`/api/health`)
```
status (enum)           ✓ Required ✓ in ['healthy', 'degraded', 'unhealthy']
timestamp (str 0-100)   ✓ Required
```

### ❌ Error Response (all errors)
```
error (str 0-500)       ✓ Required
```

## Common Validation Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Required field 'X' is missing | Field not in response | Add field to response |
| Field 'X' must be of type Y | Wrong data type | Convert to correct type |
| Field 'X' exceeds maximum length Z | String too long | Truncate to max_length |
| Field 'X' must be >= Y | Value below minimum | Ensure value ≥ min |
| Field 'X' must be <= Y | Value above maximum | Ensure value ≤ max |
| Field 'X' must be one of Y | Invalid enum value | Use allowed value |

## Usage Patterns

### Pattern 1: Use Validation in Endpoint
```python
from pdf_processor.response_validator import validate_response

@app.route('/api/upload', methods=['POST'])
@validate_response('upload')
def upload_files():
    return jsonify({
        'success': True,
        'uploaded': [...],
        'errors': [],
        'message': '...'
    })
```

### Pattern 2: Manual Validation
```python
from pdf_processor.response_validator import validate_response_structure

if validate_response_structure(data, 'upload'):
    # Response is valid
    pass
```

### Pattern 3: Get Errors
```python
from pdf_processor.response_validator import get_validation_errors

errors = get_validation_errors(data, 'upload')
if errors:
    for error in errors:
        print(f"Error: {error}")
```

### Pattern 4: List All Schemas
```python
from pdf_processor.response_validator import list_all_schemas

schemas = list_all_schemas()
print(schemas)
# ['upload', 'process', 'merge', 'split', 'rotate', 'info', 'documents', ...]
```

## Validation Flow

```
Request to API Endpoint
         ↓
    Endpoint Processing
         ↓
    Generate Response
         ↓
  Validation Decorator
         ↓
    Validate Against Schema
         ↓
  ┌─────────────┬──────────────┐
  ↓             ↓
✅ Valid     ❌ Invalid
  ↓             ↓
Return      Log Error
Response    & Return
```

## Testing

### Run All Tests
```bash
python test_response_validation.py
```

### Result
```
✅ All 20 tests passed
  • 10 valid responses
  • 10 invalid responses (caught correctly)
```

## Decorators Applied

- ✅ POST `/api/upload` - `@validate_response('upload')`
- ✅ POST `/api/process` - `@validate_response('process')`
- ✅ POST `/api/merge` - `@validate_response('merge')`
- ✅ POST `/api/split` - `@validate_response('split')`
- ✅ POST `/api/rotate` - `@validate_response('rotate')`
- ✅ POST `/api/info` - `@validate_response('info')`
- ✅ GET `/api/documents` - `@validate_response('documents')`
- ✅ GET `/api/documents/<id>` - `@validate_response('document')`
- ✅ POST `/api/search` - `@validate_response('search')`
- ✅ GET `/api/chunks/<id>` - `@validate_response('chunks')`
- ✅ GET `/api/chunk/<id>` - `@validate_response('chunk')`
- ✅ GET `/api/embeddings/stats` - `@validate_response('stats')`
- ✅ GET `/api/health` - `@validate_response('health')`

## Field Types Quick Map

| Type | Python | JSON | Example |
|------|--------|------|---------|
| String | `str` | string | `"hello"` |
| Integer | `int` | number | `123` |
| Boolean | `bool` | boolean | `true` |
| Float | `float` | number | `3.14` |
| List | `list` | array | `[1, 2, 3]` |
| Dict | `dict` | object | `{"a": 1}` |

## Constraint Ranges

| Constraint | Min | Max | Type |
|-----------|-----|-----|------|
| message length | 0 | 500 | string |
| output path | 0 | 1000 | string |
| query length | 0 | 500 | string |
| results_count | 0 | 100 | integer |
| timestamp length | 0 | 100 | string |
| count field | 0 | ∞ | non-negative int |
| page numbers | 1 | ∞ | positive int |

## Key Points

✓ All responses validated automatically
✓ Validation occurs before response sent
✓ Invalid responses logged with details
✓ Non-blocking - errors don't break flow
✓ Decorators on 13 main endpoints
✓ Extensible - easy to add schemas
✓ Tested - 20/20 test cases pass
✓ Documented - complete guide available

---

**For detailed documentation**: See `RESPONSE_VALIDATION_GUIDE.md`
**For test examples**: See `test_response_validation.py`
**For implementation details**: See `pdf_processor/response_validator.py`
