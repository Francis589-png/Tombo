"""
TOMBO Web Domain - HTTP Client Library

Provides HTTP request/response functionality, URL handling, and REST client utilities.
"""

import urllib.request
import urllib.parse
import json as json_module
import ssl
from typing import Dict, Any, Optional, List


class HTTPResponse:
    """Represents an HTTP response."""
    
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body
        self._json = None
    
    def json(self):
        """Parse response body as JSON."""
        if self._json is None and self.body:
            try:
                self._json = json_module.loads(self.body)
            except:
                self._json = None
        return self._json
    
    def text(self):
        """Get response body as text."""
        if isinstance(self.body, bytes):
            return self.body.decode('utf-8')
        return self.body
    
    def __repr__(self):
        return f"HTTPResponse(status={self.status})"


class HTTPRequest:
    """Represents an HTTP request."""
    
    def __init__(self, url, method='GET', headers=None, body=None, timeout=30):
        self.url = url
        self.method = method
        self.headers = headers or {}
        self.body = body
        self.timeout = timeout
    
    def execute(self):
        """Execute the HTTP request."""
        try:
            # Convert body to bytes if necessary
            if self.body and isinstance(self.body, str):
                body_bytes = self.body.encode('utf-8')
            else:
                body_bytes = self.body
            
            # Create request
            req = urllib.request.Request(
                self.url,
                data=body_bytes,
                headers=self.headers,
                method=self.method
            )
            
            # Execute request
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE  # Allow self-signed certs for dev
            
            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as response:
                status = response.status
                headers = dict(response.headers)
                body = response.read()
            
            return HTTPResponse(status, headers, body)
        
        except Exception as e:
            return HTTPResponse(0, {}, str(e))


def get(url, headers=None, timeout=30):
    """Make a GET request."""
    req = HTTPRequest(url, method='GET', headers=headers or {}, timeout=timeout)
    return req.execute()


def post(url, body=None, headers=None, timeout=30):
    """Make a POST request."""
    if headers is None:
        headers = {}
    if not headers.get('Content-Type'):
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    req = HTTPRequest(url, method='POST', headers=headers, body=body, timeout=timeout)
    return req.execute()


def post_json(url, data, headers=None, timeout=30):
    """Make a POST request with JSON body."""
    if headers is None:
        headers = {}
    headers['Content-Type'] = 'application/json'
    
    body = json_module.dumps(data)
    req = HTTPRequest(url, method='POST', headers=headers, body=body, timeout=timeout)
    return req.execute()


def put(url, body=None, headers=None, timeout=30):
    """Make a PUT request."""
    if headers is None:
        headers = {}
    if not headers.get('Content-Type'):
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    req = HTTPRequest(url, method='PUT', headers=headers, body=body, timeout=timeout)
    return req.execute()


def put_json(url, data, headers=None, timeout=30):
    """Make a PUT request with JSON body."""
    if headers is None:
        headers = {}
    headers['Content-Type'] = 'application/json'
    
    body = json_module.dumps(data)
    req = HTTPRequest(url, method='PUT', headers=headers, body=body, timeout=timeout)
    return req.execute()


def delete(url, headers=None, timeout=30):
    """Make a DELETE request."""
    req = HTTPRequest(url, method='DELETE', headers=headers or {}, timeout=timeout)
    return req.execute()


def patch(url, body=None, headers=None, timeout=30):
    """Make a PATCH request."""
    if headers is None:
        headers = {}
    if not headers.get('Content-Type'):
        headers['Content-Type'] = 'application/json'
    
    req = HTTPRequest(url, method='PATCH', headers=headers, body=body, timeout=timeout)
    return req.execute()


def head(url, headers=None, timeout=30):
    """Make a HEAD request."""
    req = HTTPRequest(url, method='HEAD', headers=headers or {}, timeout=timeout)
    return req.execute()


def options(url, headers=None, timeout=30):
    """Make an OPTIONS request."""
    req = HTTPRequest(url, method='OPTIONS', headers=headers or {}, timeout=timeout)
    return req.execute()


def build_url(base, path='', params=None):
    """Build a complete URL from base, path, and query parameters."""
    url = base.rstrip('/') + '/' + path.lstrip('/') if path else base
    
    if params:
        query_string = urllib.parse.urlencode(params)
        separator = '&' if '?' in url else '?'
        url = url + separator + query_string
    
    return url


def parse_url(url):
    """Parse a URL into components."""
    parsed = urllib.parse.urlparse(url)
    return {
        'scheme': parsed.scheme,
        'host': parsed.hostname,
        'port': parsed.port,
        'path': parsed.path,
        'query': parsed.query,
        'fragment': parsed.fragment,
        'params': dict(urllib.parse.parse_qsl(parsed.query)),
    }


def url_encode(data):
    """URL encode data dictionary."""
    return urllib.parse.urlencode(data)


def url_decode(query_string):
    """URL decode query string to dictionary."""
    return dict(urllib.parse.parse_qsl(query_string))


def register(env):
    """Register HTTP functions in the environment."""
    http_funcs = {
        'get': get,
        'post': post,
        'post_json': post_json,
        'put': put,
        'put_json': put_json,
        'delete': delete,
        'patch': patch,
        'head': head,
        'options': options,
        'build_url': build_url,
        'parse_url': parse_url,
        'url_encode': url_encode,
        'url_decode': url_decode,
    }
    
    for name, func in http_funcs.items():
        env.register_function(name, func, is_builtin=True)
