"""
Tombo Web Domain - Web Development and HTTP
Provides HTTP client/server, WebSocket, routing, and templating
"""

class Request:
    def __init__(self, method='GET', path='/', headers=None, body=''):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body

class Response:
    def __init__(self, body='', status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {'Content-Type': 'text/plain'}

class Router:
    def __init__(self):
        self.routes = {}
        self.middlewares = []
    
    def add(self, path, handler, methods=None):
        if methods is None:
            methods = ['GET']
        if path not in self.routes:
            self.routes[path] = {}
        for method in methods:
            self.routes[path][method] = handler
        return self
    
    def match(self, path, method='GET'):
        if path in self.routes:
            return self.routes[path].get(method)
        return None
    
    def use(self, middleware):
        self.middlewares.append(middleware)
        return self
    
    def routes_list(self):
        result = []
        for path, methods in self.routes.items():
            for method in methods:
                result.append({'path': path, 'method': method})
        return result

class Server:
    def __init__(self, port=8000):
        self.port = port
        self.router = Router()
        self.middleware = []
        self.handlers = {}
    
    def start(self):
        return f"Server listening on port {self.port}"
    
    def route(self, path, handler, methods=None):
        self.router.add(path, handler, methods)
        return self
    
    def get(self, path, handler):
        self.router.add(path, handler, ['GET'])
        return self
    
    def post(self, path, handler):
        self.router.add(path, handler, ['POST'])
        return self
    
    def put(self, path, handler):
        self.router.add(path, handler, ['PUT'])
        return self
    
    def delete(self, path, handler):
        self.router.add(path, handler, ['DELETE'])
        return self
    
    def use(self, middleware):
        self.middleware.append(middleware)
        return self

class WebSocket:
    def __init__(self, url):
        self.url = url
        self.connected = True
        self.data = []
    
    def send(self, message):
        self.data.append(message)
        return True
    
    def receive(self):
        if self.data:
            return self.data.pop(0)
        return None
    
    def close(self):
        self.connected = False
        return True

# HTTP Client Methods
def tombo_get(url, headers=None, params=None):
    """Make GET request."""
    if headers is None:
        headers = {}
    return {'method': 'GET', 'url': url, 'status': 200, 'data': {}}

def tombo_post(url, data=None, headers=None):
    """Make POST request."""
    if headers is None:
        headers = {}
    return {'method': 'POST', 'url': url, 'status': 201, 'data': data or {}}

def tombo_put(url, data=None, headers=None):
    """Make PUT request."""
    if headers is None:
        headers = {}
    return {'method': 'PUT', 'url': url, 'status': 200, 'data': data or {}}

def tombo_delete(url, headers=None):
    """Make DELETE request."""
    if headers is None:
        headers = {}
    return {'method': 'DELETE', 'url': url, 'status': 204, 'data': {}}

def tombo_patch(url, data=None, headers=None):
    """Make PATCH request."""
    if headers is None:
        headers = {}
    return {'method': 'PATCH', 'url': url, 'status': 200, 'data': data or {}}

def tombo_head(url, headers=None):
    """Make HEAD request."""
    if headers is None:
        headers = {}
    return {'method': 'HEAD', 'url': url, 'status': 200, 'data': {}}

def tombo_options(url, headers=None):
    """Make OPTIONS request."""
    if headers is None:
        headers = {}
    return {'method': 'OPTIONS', 'url': url, 'status': 200, 'allow': ['GET', 'POST', 'PUT', 'DELETE']}

# WebSocket
def tombo_websocket_connect(url):
    """Connect to WebSocket server."""
    return WebSocket(url)

# JSON Response Helpers
def tombo_json_response(data, status=200):
    """Create JSON response."""
    try:
        import json
        body = json.dumps(data)
    except:
        body = str(data)
    headers = {'Content-Type': 'application/json'}
    return Response(body, status, headers)

def tombo_html_response(html, status=200):
    """Create HTML response."""
    headers = {'Content-Type': 'text/html'}
    return Response(html, status, headers)

def tombo_text_response(text, status=200):
    """Create text response."""
    headers = {'Content-Type': 'text/plain'}
    return Response(text, status, headers)

# Template Engine
def tombo_render(template_str, context=None):
    """Render template with context."""
    if context is None:
        context = {}
    result = str(template_str)
    for key, value in context.items():
        result = result.replace('{{' + key + '}}', str(value))
    return result

def tombo_template(name):
    """Load and return template."""
    return {'name': name, 'render': lambda ctx: f"Rendered {name}"}

# URL & Encoding
def tombo_urlencode(data):
    """URL encode data."""
    try:
        from urllib.parse import urlencode
        return urlencode(data)
    except:
        return str(data)

def tombo_urldecode(encoded):
    """URL decode string."""
    try:
        from urllib.parse import parse_qs
        return parse_qs(encoded)
    except:
        return {}

def tombo_parse_url(url):
    """Parse URL into components."""
    parts = url.split('?')
    path = parts[0]
    query = parts[1] if len(parts) > 1 else ''
    return {'path': path, 'query': query, 'full': url}

def tombo_build_url(base, path, query=None):
    """Build URL from components."""
    url = base + path
    if query:
        url += '?' + tombo_urlencode(query)
    return url

# Middleware
def tombo_cors_middleware(origins=None):
    """Create CORS middleware."""
    if origins is None:
        origins = ['*']
    return {'type': 'cors', 'origins': origins}

def tombo_auth_middleware(secret=None):
    """Create authentication middleware."""
    return {'type': 'auth', 'secret': secret or 'default'}

def tombo_logging_middleware():
    """Create logging middleware."""
    return {'type': 'logging'}

def tombo_rate_limit_middleware(limit=100, window=60):
    """Create rate limiting middleware."""
    return {'type': 'rate_limit', 'limit': limit, 'window': window}

# Session Management
class Session:
    def __init__(self, session_id=''):
        self.id = session_id
        self.data = {}
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def set(self, key, value):
        self.data[key] = value
        return True
    
    def delete(self, key):
        if key in self.data:
            del self.data[key]
        return True
    
    def clear(self):
        self.data = {}
        return True

def tombo_session_create(session_id=''):
    """Create new session."""
    import time
    sid = session_id or f"session_{int(time.time())}"
    return Session(sid)

def tombo_session_get(session_id):
    """Retrieve session by ID."""
    return Session(session_id)

# Cookie Management
def tombo_cookie_set(name, value, maxage=3600, path='/'):
    """Set cookie."""
    return {'name': name, 'value': value, 'maxage': maxage, 'path': path}

def tombo_cookie_get(cookies, name):
    """Get cookie value."""
    if isinstance(cookies, dict):
        return cookies.get(name)
    return None

def tombo_cookie_delete(name):
    """Delete cookie."""
    return {'name': name, 'maxage': 0}

# Content Negotiation
def tombo_accept_header(accept_string):
    """Parse Accept header."""
    types = accept_string.split(',')
    return [t.strip().split(';')[0] for t in types]

def tombo_content_type(extension):
    """Get content type for extension."""
    types = {
        'json': 'application/json',
        'html': 'text/html',
        'txt': 'text/plain',
        'xml': 'application/xml',
        'js': 'application/javascript',
        'css': 'text/css',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'gif': 'image/gif',
    }
    return types.get(extension, 'application/octet-stream')

def register(env):
    """Register web domain."""
    env.set('Server', Server)
    env.set('Router', Router)
    env.set('Request', Request)
    env.set('Response', Response)
    env.set('WebSocket', WebSocket)
    env.set('Session', Session)
    
    functions = {
        'get': tombo_get,
        'post': tombo_post,
        'put': tombo_put,
        'delete': tombo_delete,
        'patch': tombo_patch,
        'head': tombo_head,
        'options': tombo_options,
        'websocket_connect': tombo_websocket_connect,
        'json_response': tombo_json_response,
        'html_response': tombo_html_response,
        'text_response': tombo_text_response,
        'render': tombo_render,
        'template': tombo_template,
        'urlencode': tombo_urlencode,
        'urldecode': tombo_urldecode,
        'parse_url': tombo_parse_url,
        'build_url': tombo_build_url,
        'cors_middleware': tombo_cors_middleware,
        'auth_middleware': tombo_auth_middleware,
        'logging_middleware': tombo_logging_middleware,
        'rate_limit_middleware': tombo_rate_limit_middleware,
        'session_create': tombo_session_create,
        'session_get': tombo_session_get,
        'cookie_set': tombo_cookie_set,
        'cookie_get': tombo_cookie_get,
        'cookie_delete': tombo_cookie_delete,
        'accept_header': tombo_accept_header,
        'content_type': tombo_content_type,
    }
    for name, func in functions.items():
        env.set(name, func)

provides = ['web']
