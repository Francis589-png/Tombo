"""
TOMBO Validation Library - Data validation and schema checking
Validators for types, formats, ranges, and custom rules.
"""

from typing import Dict, List, Any, Callable, Optional, Union


class Validator:
    """Base validator."""
    
    def validate(self, value: Any) -> Tuple[bool, str]:
        """Validate value.
        
        Returns:
            Tuple of (valid, error_message)
        """
        raise NotImplementedError


class RequiredValidator(Validator):
    """Validate required field."""
    
    def validate(self, value: Any) -> tuple:
        """Check if value is not None/empty."""
        if value is None or value == "":
            return False, "Field is required"
        return True, ""


class TypeValidator(Validator):
    """Validate type."""
    
    def __init__(self, expected_type: type):
        """Initialize type validator.
        
        Args:
            expected_type: Expected Python type
        """
        self.expected_type = expected_type
    
    def validate(self, value: Any) -> tuple:
        """Check type."""
        if not isinstance(value, self.expected_type):
            return False, f"Expected {self.expected_type.__name__}"
        return True, ""


class StringValidator(Validator):
    """Validate string format."""
    
    def __init__(self, min_length: int = None, max_length: int = None, 
                 pattern: str = None):
        """Initialize string validator.
        
        Args:
            min_length: Minimum length
            max_length: Maximum length
            pattern: Regex pattern
        """
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern
    
    def validate(self, value: Any) -> tuple:
        """Validate string."""
        if not isinstance(value, str):
            return False, "Must be a string"
        
        if self.min_length and len(value) < self.min_length:
            return False, f"Minimum length is {self.min_length}"
        
        if self.max_length and len(value) > self.max_length:
            return False, f"Maximum length is {self.max_length}"
        
        if self.pattern:
            import re
            if not re.match(self.pattern, value):
                return False, f"Does not match pattern {self.pattern}"
        
        return True, ""


class NumberValidator(Validator):
    """Validate number."""
    
    def __init__(self, min_value: Union[int, float] = None,
                 max_value: Union[int, float] = None):
        """Initialize number validator.
        
        Args:
            min_value: Minimum value
            max_value: Maximum value
        """
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value: Any) -> tuple:
        """Validate number."""
        if not isinstance(value, (int, float)):
            return False, "Must be a number"
        
        if self.min_value is not None and value < self.min_value:
            return False, f"Minimum value is {self.min_value}"
        
        if self.max_value is not None and value > self.max_value:
            return False, f"Maximum value is {self.max_value}"
        
        return True, ""


class EmailValidator(Validator):
    """Validate email address."""
    
    def validate(self, value: Any) -> tuple:
        """Validate email."""
        if not isinstance(value, str):
            return False, "Must be a string"
        
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, value):
            return False, "Invalid email format"
        
        return True, ""


class URLValidator(Validator):
    """Validate URL."""
    
    def validate(self, value: Any) -> tuple:
        """Validate URL."""
        if not isinstance(value, str):
            return False, "Must be a string"
        
        import re
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        
        if not re.match(pattern, value):
            return False, "Invalid URL format"
        
        return True, ""


class EnumValidator(Validator):
    """Validate enum values."""
    
    def __init__(self, allowed: List[Any]):
        """Initialize enum validator.
        
        Args:
            allowed: List of allowed values
        """
        self.allowed = set(allowed)
    
    def validate(self, value: Any) -> tuple:
        """Validate enum."""
        if value not in self.allowed:
            return False, f"Must be one of {self.allowed}"
        
        return True, ""


class ListValidator(Validator):
    """Validate list."""
    
    def __init__(self, item_validator: Validator = None,
                 min_length: int = None, max_length: int = None):
        """Initialize list validator.
        
        Args:
            item_validator: Validator for list items
            min_length: Minimum length
            max_length: Maximum length
        """
        self.item_validator = item_validator
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, value: Any) -> tuple:
        """Validate list."""
        if not isinstance(value, list):
            return False, "Must be a list"
        
        if self.min_length and len(value) < self.min_length:
            return False, f"Minimum length is {self.min_length}"
        
        if self.max_length and len(value) > self.max_length:
            return False, f"Maximum length is {self.max_length}"
        
        if self.item_validator:
            for i, item in enumerate(value):
                valid, error = self.item_validator.validate(item)
                if not valid:
                    return False, f"Item {i}: {error}"
        
        return True, ""


class CustomValidator(Validator):
    """Custom validation function."""
    
    def __init__(self, func: Callable[[Any], bool], error_msg: str = None):
        """Initialize custom validator.
        
        Args:
            func: Validation function
            error_msg: Error message
        """
        self.func = func
        self.error_msg = error_msg or "Validation failed"
    
    def validate(self, value: Any) -> tuple:
        """Run custom validation."""
        try:
            if self.func(value):
                return True, ""
            return False, self.error_msg
        except Exception as e:
            return False, str(e)


class Schema:
    """Data validation schema."""
    
    def __init__(self):
        """Initialize schema."""
        self.fields: Dict[str, List[Validator]] = {}
    
    def add_field(self, name: str, *validators: Validator) -> 'Schema':
        """Add field with validators.
        
        Args:
            name: Field name
            validators: Validators for field
            
        Returns:
            Self for chaining
        """
        self.fields[name] = list(validators)
        return self
    
    def validate(self, data: Dict) -> Dict[str, str]:
        """Validate data against schema.
        
        Args:
            data: Data to validate
            
        Returns:
            Dictionary of field errors (empty if valid)
        """
        errors = {}
        
        for field_name, validators in self.fields.items():
            value = data.get(field_name)
            
            for validator in validators:
                valid, error = validator.validate(value)
                
                if not valid:
                    errors[field_name] = error
                    break
        
        return errors
    
    def is_valid(self, data: Dict) -> bool:
        """Check if data is valid."""
        return len(self.validate(data)) == 0


class SchemaBuilder:
    """Build validation schemas."""
    
    def __init__(self):
        """Initialize builder."""
        self.schema = Schema()
    
    def required(self, name: str) -> 'SchemaBuilder':
        """Add required field."""
        self.schema.add_field(name, RequiredValidator())
        return self
    
    def string(self, name: str, min_length: int = None,
               max_length: int = None, pattern: str = None) -> 'SchemaBuilder':
        """Add string field."""
        self.schema.add_field(
            name,
            RequiredValidator(),
            TypeValidator(str),
            StringValidator(min_length, max_length, pattern)
        )
        return self
    
    def number(self, name: str, min_value: Union[int, float] = None,
               max_value: Union[int, float] = None) -> 'SchemaBuilder':
        """Add number field."""
        self.schema.add_field(
            name,
            RequiredValidator(),
            TypeValidator((int, float)),
            NumberValidator(min_value, max_value)
        )
        return self
    
    def email(self, name: str) -> 'SchemaBuilder':
        """Add email field."""
        self.schema.add_field(
            name,
            RequiredValidator(),
            TypeValidator(str),
            EmailValidator()
        )
        return self
    
    def url(self, name: str) -> 'SchemaBuilder':
        """Add URL field."""
        self.schema.add_field(
            name,
            RequiredValidator(),
            TypeValidator(str),
            URLValidator()
        )
        return self
    
    def enum(self, name: str, allowed: List[Any]) -> 'SchemaBuilder':
        """Add enum field."""
        self.schema.add_field(
            name,
            RequiredValidator(),
            EnumValidator(allowed)
        )
        return self
    
    def custom(self, name: str, func: Callable, error_msg: str = None) -> 'SchemaBuilder':
        """Add custom validation field."""
        self.schema.add_field(
            name,
            RequiredValidator(),
            CustomValidator(func, error_msg)
        )
        return self
    
    def optional(self, name: str, validator: Validator) -> 'SchemaBuilder':
        """Add optional field (skips required check)."""
        self.schema.add_field(name, validator)
        return self
    
    def build(self) -> Schema:
        """Build schema."""
        return self.schema


# Utility tuple type for returns
from typing import Tuple
