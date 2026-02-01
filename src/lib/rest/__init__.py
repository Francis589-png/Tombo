"""
TOMBO REST Library - RESTful API framework with routing and validation
Build REST APIs with decorators, automatic validation, and error handling.
"""

from typing import Dict, Any, Callable, List, Optional


class Route:
    """REST API route."""
    
    def __init__(self, path: str, method: str, handler: Callable):
        """Initialize route.
        
        Args:
            path: URL path pattern
            method: HTTP method (GET, POST, etc.)
            handler: Handler function
        """
        self.path = path
        self.method = method
        self.handler = handler
        self.middleware = []
        self.validators = []
    
    def add_middleware(self, middleware: Callable):
        """Add middleware to route."""
        self.middleware.append(middleware)
        return self
    
    def add_validator(self, validator: Callable):
        """Add request validator."""
        self.validators.append(validator)
        return self
    
    def execute(self, request, response):
        """Execute route handler."""
        # Run validators
        for validator in self.validators:
            result = validator(request)
            if result is not True:
                response.status(400).json({"error": result})
                return response
        
        # Run middleware
        for mw in self.middleware:
            mw(request, response)
        
        # Run handler
        return self.handler(request, response)


class Router:
    """REST API router."""
    
    def __init__(self, base_path: str = ""):
        """Initialize router.
        
        Args:
            base_path: Base path for all routes
        """
        self.base_path = base_path
        self.routes: List[Route] = []
        self.error_handlers = {}
    
    def route(self, path: str, method: str = "GET"):
        """Register a route."""
        def decorator(handler):
            full_path = self.base_path + path
            route = Route(full_path, method, handler)
            self.routes.append(route)
            return route
        return decorator
    
    def get(self, path: str):
        """Register GET route."""
        return self.route(path, "GET")
    
    def post(self, path: str):
        """Register POST route."""
        return self.route(path, "POST")
    
    def put(self, path: str):
        """Register PUT route."""
        return self.route(path, "PUT")
    
    def patch(self, path: str):
        """Register PATCH route."""
        return self.route(path, "PATCH")
    
    def delete(self, path: str):
        """Register DELETE route."""
        return self.route(path, "DELETE")
    
    def handle_error(self, status_code: int):
        """Register error handler."""
        def decorator(handler):
            self.error_handlers[status_code] = handler
            return handler
        return decorator
    
    def match_route(self, method: str, path: str) -> Optional[Route]:
        """Find matching route."""
        for route in self.routes:
            if route.method == method and self._paths_match(route.path, path):
                return route
        return None
    
    def _paths_match(self, pattern: str, path: str) -> bool:
        """Check if path matches pattern."""
        pattern_parts = pattern.split('/')
        path_parts = path.split('/')
        
        if len(pattern_parts) != len(path_parts):
            return False
        
        for p_part, path_part in zip(pattern_parts, path_parts):
            if p_part.startswith(':'):
                continue
            if p_part != path_part:
                return False
        
        return True


class ResourceController:
    """Base resource controller for REST endpoints."""
    
    def __init__(self):
        """Initialize controller."""
        self.router = Router()
    
    def index(self, request, response):
        """List all resources."""
        return response.json([])
    
    def create(self, request, response):
        """Create new resource."""
        return response.status(201).json({})
    
    def show(self, request, response):
        """Show single resource."""
        return response.json({})
    
    def update(self, request, response):
        """Update resource."""
        return response.json({})
    
    def delete(self, request, response):
        """Delete resource."""
        return response.status(204)
    
    def register_routes(self, base_path: str):
        """Register RESTful routes."""
        self.router.get(f"{base_path}")(self.index)
        self.router.post(f"{base_path}")(self.create)
        self.router.get(f"{base_path}/:id")(self.show)
        self.router.put(f"{base_path}/:id")(self.update)
        self.router.delete(f"{base_path}/:id")(self.delete)


class APIResponse:
    """Standardized API response."""
    
    def __init__(self, data=None, error=None, status_code: int = 200):
        """Initialize response.
        
        Args:
            data: Response data
            error: Error message if applicable
            status_code: HTTP status code
        """
        self.data = data
        self.error = error
        self.status_code = status_code
        self.meta = {}
    
    def add_meta(self, key: str, value):
        """Add metadata."""
        self.meta[key] = value
        return self
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        response = {
            'status': self.status_code,
            'success': 200 <= self.status_code < 300
        }
        
        if self.data is not None:
            response['data'] = self.data
        
        if self.error:
            response['error'] = self.error
        
        if self.meta:
            response['meta'] = self.meta
        
        return response


def create_response(data=None, status_code: int = 200) -> APIResponse:
    """Create successful response."""
    return APIResponse(data=data, status_code=status_code)


def create_error(message: str, status_code: int = 400) -> APIResponse:
    """Create error response."""
    return APIResponse(error=message, status_code=status_code)


def validate_request(required_fields: List[str]) -> Callable:
    """Create request validator for required fields."""
    def validator(request):
        data = request.get_json() if hasattr(request, 'get_json') else {}
        for field in required_fields:
            if field not in data:
                return f"Missing required field: {field}"
        return True
    return validator


def validate_types(type_schema: Dict[str, type]) -> Callable:
    """Create validator for field types."""
    def validator(request):
        data = request.get_json() if hasattr(request, 'get_json') else {}
        for field, expected_type in type_schema.items():
            if field in data:
                if not isinstance(data[field], expected_type):
                    return f"Invalid type for {field}: expected {expected_type.__name__}"
        return True
    return validator
