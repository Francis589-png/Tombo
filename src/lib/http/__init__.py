"""
TOMBO HTTP Library - Low-level HTTP handling with request/response objects
Core HTTP functionality for server and client operations.
"""

from typing import Dict, Any, Optional, List
import urllib.parse


class HTTPHeaders:
    """HTTP headers container."""
    
    def __init__(self, headers: Dict = None):
        """Initialize headers."""
        self._headers = {}
        if headers:
            for k, v in headers.items():
                self._headers[k.lower()] = v
    
    def set(self, name: str, value: str):
        """Set header."""
        self._headers[name.lower()] = value
    
    def get(self, name: str, default=None):
        """Get header value."""
        return self._headers.get(name.lower(), default)
    
    def has(self, name: str) -> bool:
        """Check if header exists."""
        return name.lower() in self._headers
    
    def remove(self, name: str):
        """Remove header."""
        self._headers.pop(name.lower(), None)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return self._headers.copy()
    
    def __str__(self) -> str:
        """Convert to HTTP header string."""
        return "\r\n".join([f"{k}: {v}" for k, v in self._headers.items()])


class HTTPMessage:
    """Base HTTP message class."""
    
    def __init__(self):
        """Initialize message."""
        self.headers = HTTPHeaders()
        self.body = b""
    
    def set_header(self, name: str, value: str):
        """Set a header."""
        self.headers.set(name, value)
        return self
    
    def set_body(self, body):
        """Set message body."""
        if isinstance(body, str):
            self.body = body.encode('utf-8')
        else:
            self.body = body
        return self
    
    def get_body_text(self) -> str:
        """Get body as text."""
        if isinstance(self.body, bytes):
            return self.body.decode('utf-8')
        return str(self.body)


class HTTPRequest(HTTPMessage):
    """HTTP Request message."""
    
    def __init__(self, method: str = "GET", path: str = "/", version: str = "1.1"):
        """Initialize request.
        
        Args:
            method: HTTP method
            path: Request path
            version: HTTP version
        """
        super().__init__()
        self.method = method
        self.path = path
        self.version = version
        self.query_params = {}
        self.form_data = {}
    
    def set_query_param(self, name: str, value):
        """Set query parameter."""
        self.query_params[name] = value
        return self
    
    def get_query_param(self, name: str, default=None):
        """Get query parameter."""
        return self.query_params.get(name, default)
    
    def set_form_data(self, name: str, value):
        """Set form data."""
        self.form_data[name] = value
        return self
    
    def get_form_data(self, name: str, default=None):
        """Get form data."""
        return self.form_data.get(name, default)
    
    def to_string(self) -> str:
        """Convert to HTTP request string."""
        query_str = ""
        if self.query_params:
            query_str = "?" + urllib.parse.urlencode(self.query_params)
        
        request_line = f"{self.method} {self.path}{query_str} HTTP/{self.version}\r\n"
        headers = str(self.headers)
        
        if self.body:
            self.headers.set('Content-Length', str(len(self.body)))
        
        request = request_line
        if headers:
            request += headers + "\r\n"
        request += "\r\n"
        
        if self.body:
            request += self.get_body_text()
        
        return request


class HTTPStatus:
    """HTTP status codes."""
    
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503


class HTTPResponse(HTTPMessage):
    """HTTP Response message."""
    
    def __init__(self, status_code: int = 200, reason: str = "OK", version: str = "1.1"):
        """Initialize response.
        
        Args:
            status_code: HTTP status code
            reason: Status reason phrase
            version: HTTP version
        """
        super().__init__()
        self.status_code = status_code
        self.reason = reason
        self.version = version
    
    def is_success(self) -> bool:
        """Check if response is successful (2xx)."""
        return 200 <= self.status_code < 300
    
    def is_redirect(self) -> bool:
        """Check if response is redirect (3xx)."""
        return 300 <= self.status_code < 400
    
    def is_client_error(self) -> bool:
        """Check if response is client error (4xx)."""
        return 400 <= self.status_code < 500
    
    def is_server_error(self) -> bool:
        """Check if response is server error (5xx)."""
        return 500 <= self.status_code < 600
    
    def to_string(self) -> str:
        """Convert to HTTP response string."""
        status_line = f"HTTP/{self.version} {self.status_code} {self.reason}\r\n"
        headers = str(self.headers)
        
        if self.body:
            self.headers.set('Content-Length', str(len(self.body)))
        
        response = status_line
        if headers:
            response += headers + "\r\n"
        response += "\r\n"
        
        if self.body:
            response += self.get_body_text()
        
        return response


def status_text(code: int) -> str:
    """Get status code text."""
    statuses = {
        200: "OK",
        201: "Created",
        204: "No Content",
        301: "Moved Permanently",
        302: "Found",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable"
    }
    return statuses.get(code, "Unknown")


def create_request(method: str = "GET", path: str = "/") -> HTTPRequest:
    """Create HTTP request."""
    return HTTPRequest(method, path)


def create_response(status_code: int = 200) -> HTTPResponse:
    """Create HTTP response."""
    return HTTPResponse(status_code, status_text(status_code))
