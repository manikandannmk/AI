"""
Response validation module for API endpoints.
Defines constraints and validation schemas for all API responses.
"""

from typing import Dict, List, Any, Optional, Union, Type
from functools import wraps
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when response validation fails"""
    pass


@dataclass
class FieldConstraint:
    """Defines constraints for a response field"""
    required: bool = True
    data_type: Type = str
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    allowed_values: Optional[List[Any]] = None
    pattern: Optional[str] = None
    
    def validate(self, value: Any, field_name: str) -> None:
        """Validate a field value against constraints"""
        # Check type
        if not isinstance(value, self.data_type):
            raise ValidationError(
                f"Field '{field_name}' must be of type {self.data_type.__name__}, "
                f"got {type(value).__name__}"
            )
        
        # Check string length
        if isinstance(value, str):
            if self.min_length is not None and len(value) < self.min_length:
                raise ValidationError(
                    f"Field '{field_name}' must have minimum length {self.min_length}"
                )
            if self.max_length is not None and len(value) > self.max_length:
                raise ValidationError(
                    f"Field '{field_name}' exceeds maximum length {self.max_length}"
                )
        
        # Check numeric ranges
        if isinstance(value, (int, float)):
            if self.min_value is not None and value < self.min_value:
                raise ValidationError(
                    f"Field '{field_name}' must be >= {self.min_value}"
                )
            if self.max_value is not None and value > self.max_value:
                raise ValidationError(
                    f"Field '{field_name}' must be <= {self.max_value}"
                )
        
        # Check allowed values
        if self.allowed_values is not None and value not in self.allowed_values:
            raise ValidationError(
                f"Field '{field_name}' must be one of {self.allowed_values}"
            )


@dataclass
class ResponseSchema:
    """Base schema for API responses"""
    fields: Dict[str, FieldConstraint] = field(default_factory=dict)
    
    def add_field(self, name: str, constraint: FieldConstraint) -> None:
        """Add a field constraint"""
        self.fields[name] = constraint
    
    def validate(self, data: Dict[str, Any]) -> None:
        """Validate response data against schema"""
        if not isinstance(data, dict):
            raise ValidationError("Response must be a dictionary")
        
        # Check required fields
        for field_name, constraint in self.fields.items():
            if constraint.required and field_name not in data:
                raise ValidationError(f"Required field '{field_name}' is missing")
        
        # Validate each field
        for field_name, value in data.items():
            if field_name in self.fields:
                self.fields[field_name].validate(value, field_name)


# === RESPONSE SCHEMAS ===

class SuccessResponseSchema(ResponseSchema):
    """Schema for successful responses"""
    def __init__(self):
        super().__init__()
        self.add_field('success', FieldConstraint(
            required=True,
            data_type=bool,
            allowed_values=[True]
        ))
        self.add_field('message', FieldConstraint(
            required=False,
            data_type=str,
            max_length=500
        ))


class ErrorResponseSchema(ResponseSchema):
    """Schema for error responses"""
    def __init__(self):
        super().__init__()
        self.add_field('error', FieldConstraint(
            required=True,
            data_type=str,
            max_length=500
        ))


class UploadResponseSchema(SuccessResponseSchema):
    """Schema for /api/upload responses"""
    def __init__(self):
        super().__init__()
        self.add_field('uploaded', FieldConstraint(
            required=True,
            data_type=list
        ))
        self.add_field('errors', FieldConstraint(
            required=True,
            data_type=list
        ))
        self.add_field('message', FieldConstraint(
            required=True,
            data_type=str,
            max_length=500
        ))


class ProcessResponseSchema(SuccessResponseSchema):
    """Schema for /api/process responses"""
    def __init__(self):
        super().__init__()
        self.add_field('results', FieldConstraint(
            required=True,
            data_type=list
        ))
        self.add_field('count', FieldConstraint(
            required=True,
            data_type=int,
            min_value=0
        ))


class MergeResponseSchema(SuccessResponseSchema):
    """Schema for /api/merge responses"""
    def __init__(self):
        super().__init__()
        self.add_field('message', FieldConstraint(
            required=True,
            data_type=str,
            max_length=500
        ))
        self.add_field('output', FieldConstraint(
            required=True,
            data_type=str,
            max_length=1000
        ))


class SplitResponseSchema(SuccessResponseSchema):
    """Schema for /api/split responses"""
    def __init__(self):
        super().__init__()
        self.add_field('message', FieldConstraint(
            required=True,
            data_type=str,
            max_length=500
        ))
        self.add_field('files', FieldConstraint(
            required=True,
            data_type=list
        ))


class RotateResponseSchema(SuccessResponseSchema):
    """Schema for /api/rotate responses"""
    def __init__(self):
        super().__init__()
        self.add_field('message', FieldConstraint(
            required=True,
            data_type=str,
            max_length=500
        ))
        self.add_field('output', FieldConstraint(
            required=True,
            data_type=str,
            max_length=1000
        ))


class InfoResponseSchema(SuccessResponseSchema):
    """Schema for /api/info responses"""
    def __init__(self):
        super().__init__()
        self.add_field('info', FieldConstraint(
            required=True,
            data_type=dict
        ))


class DocumentsResponseSchema(SuccessResponseSchema):
    """Schema for /api/documents responses"""
    def __init__(self):
        super().__init__()
        self.add_field('documents', FieldConstraint(
            required=True,
            data_type=list
        ))
        self.add_field('total', FieldConstraint(
            required=True,
            data_type=int,
            min_value=0
        ))


class SingleDocumentResponseSchema(SuccessResponseSchema):
    """Schema for /api/documents/<id> responses"""
    def __init__(self):
        super().__init__()
        self.add_field('document', FieldConstraint(
            required=True,
            data_type=dict
        ))
        self.add_field('chunks', FieldConstraint(
            required=True,
            data_type=list
        ))


class SearchResponseSchema(SuccessResponseSchema):
    """Schema for /api/search responses"""
    def __init__(self):
        super().__init__()
        self.add_field('query', FieldConstraint(
            required=True,
            data_type=str,
            max_length=500
        ))
        self.add_field('results', FieldConstraint(
            required=True,
            data_type=list
        ))
        self.add_field('results_count', FieldConstraint(
            required=True,
            data_type=int,
            min_value=0,
            max_value=100
        ))


class ChunksResponseSchema(SuccessResponseSchema):
    """Schema for /api/chunks/<id> responses"""
    def __init__(self):
        super().__init__()
        self.add_field('document', FieldConstraint(
            required=True,
            data_type=dict
        ))
        self.add_field('chunks', FieldConstraint(
            required=True,
            data_type=list
        ))
        self.add_field('total', FieldConstraint(
            required=True,
            data_type=int,
            min_value=0
        ))
        self.add_field('pages', FieldConstraint(
            required=True,
            data_type=int,
            min_value=1
        ))
        self.add_field('current_page', FieldConstraint(
            required=True,
            data_type=int,
            min_value=1
        ))


class EmbeddingStatsResponseSchema(SuccessResponseSchema):
    """Schema for /api/embeddings/stats responses"""
    def __init__(self):
        super().__init__()
        self.add_field('statistics', FieldConstraint(
            required=True,
            data_type=dict
        ))


class ChunkDetailResponseSchema(SuccessResponseSchema):
    """Schema for /api/chunk/<id> responses"""
    def __init__(self):
        super().__init__()
        self.add_field('chunk', FieldConstraint(
            required=True,
            data_type=dict
        ))
        self.add_field('embeddings', FieldConstraint(
            required=True,
            data_type=list
        ))


class HealthResponseSchema(ResponseSchema):
    """Schema for /api/health responses"""
    def __init__(self):
        super().__init__()
        self.add_field('status', FieldConstraint(
            required=True,
            data_type=str,
            allowed_values=['healthy', 'degraded', 'unhealthy']
        ))
        self.add_field('timestamp', FieldConstraint(
            required=True,
            data_type=str,
            max_length=100
        ))


# === SCHEMA REGISTRY ===

SCHEMAS: Dict[str, ResponseSchema] = {
    'upload': UploadResponseSchema(),
    'process': ProcessResponseSchema(),
    'merge': MergeResponseSchema(),
    'split': SplitResponseSchema(),
    'rotate': RotateResponseSchema(),
    'info': InfoResponseSchema(),
    'documents': DocumentsResponseSchema(),
    'document': SingleDocumentResponseSchema(),
    'search': SearchResponseSchema(),
    'chunks': ChunksResponseSchema(),
    'chunk': ChunkDetailResponseSchema(),
    'stats': EmbeddingStatsResponseSchema(),
    'health': HealthResponseSchema(),
    'error': ErrorResponseSchema(),
    'success': SuccessResponseSchema(),
}


def validate_response(schema_name: str):
    """
    Decorator to validate API responses against defined schemas
    
    Args:
        schema_name: Name of the schema to validate against
    
    Returns:
        Decorator function
    
    Raises:
        ValidationError: If response doesn't match schema
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Extract JSON data from Flask response (result is tuple of (data, status_code) or just data)
            if isinstance(result, tuple):
                response_data, status_code = result[0], result[1] if len(result) > 1 else 200
            else:
                response_data, status_code = result, 200
            
            # Only validate successful responses (2xx status codes) and JSON dictionaries
            if 200 <= status_code < 300 and isinstance(response_data, dict):
                schema = SCHEMAS.get(schema_name)
                if schema:
                    try:
                        schema.validate(response_data)
                        logger.debug(f"Response validation passed for {schema_name}")
                    except ValidationError as e:
                        logger.error(f"Response validation failed for {schema_name}: {str(e)}")
                        raise
            
            return result
        
        return wrapper
    return decorator


def validate_all_responses(func):
    """
    Auto-detect schema based on response success/error
    Validates automatically based on presence of 'success' or 'error' field
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        
        # Extract JSON data
        if isinstance(result, tuple):
            response_data, status_code = result[0], result[1] if len(result) > 1 else 200
        else:
            response_data, status_code = result, 200
        
        # Determine schema based on response structure
        if isinstance(response_data, dict):
            if 'success' in response_data and response_data.get('success'):
                schema = SCHEMAS.get('success')
            elif 'error' in response_data:
                schema = SCHEMAS.get('error')
            else:
                return result  # Unknown schema, skip validation
            
            try:
                schema.validate(response_data)
                logger.debug(f"Response validation passed for {func.__name__}")
            except ValidationError as e:
                logger.error(f"Response validation failed for {func.__name__}: {str(e)}")
                # Don't raise, just log to avoid breaking functionality
        
        return result
    
    return wrapper


# === UTILITY FUNCTIONS ===

def get_schema(name: str) -> Optional[ResponseSchema]:
    """Get a schema by name"""
    return SCHEMAS.get(name)


def list_all_schemas() -> List[str]:
    """Get list of all available schemas"""
    return list(SCHEMAS.keys())


def validate_response_structure(data: Dict[str, Any], schema_name: str) -> bool:
    """
    Validate response structure without raising exceptions
    
    Args:
        data: Response data to validate
        schema_name: Name of the schema
    
    Returns:
        True if valid, False otherwise
    """
    schema = SCHEMAS.get(schema_name)
    if not schema:
        return False
    
    try:
        schema.validate(data)
        return True
    except ValidationError:
        return False


def get_validation_errors(data: Dict[str, Any], schema_name: str) -> List[str]:
    """
    Get list of validation errors without raising
    
    Args:
        data: Response data to validate
        schema_name: Name of the schema
    
    Returns:
        List of validation error messages
    """
    errors = []
    schema = SCHEMAS.get(schema_name)
    if not schema:
        errors.append(f"Schema '{schema_name}' not found")
        return errors
    
    # Check required fields
    for field_name, constraint in schema.fields.items():
        if constraint.required and field_name not in data:
            errors.append(f"Required field '{field_name}' is missing")
    
    # Check field types and constraints
    for field_name, value in data.items():
        if field_name in schema.fields:
            try:
                schema.fields[field_name].validate(value, field_name)
            except ValidationError as e:
                errors.append(str(e))
    
    return errors
