"""
TOMBO Auth Library - Authentication and authorization framework
JWT tokens, password hashing, role-based access control, session management.
"""

import hashlib
import hmac
import json
import time
from typing import Dict, Any, Optional, List, Callable


class PasswordHasher:
    """Password hashing with salt."""
    
    def __init__(self, algorithm: str = "sha256", iterations: int = 100000):
        """Initialize hasher.
        
        Args:
            algorithm: Hashing algorithm (sha256, sha512)
            iterations: Number of iterations for key derivation
        """
        self.algorithm = algorithm
        self.iterations = iterations
    
    def hash(self, password: str, salt: str = None) -> Dict:
        """Hash password with salt.
        
        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)
            
        Returns:
            Dict with hash, salt, algorithm, iterations
        """
        import os
        import binascii
        
        if not salt:
            salt = binascii.hexlify(os.urandom(32)).decode()
        
        pwd_hash = hashlib.pbkdf2_hmac(
            self.algorithm,
            password.encode(),
            salt.encode(),
            self.iterations
        )
        
        return {
            "hash": pwd_hash.hex(),
            "salt": salt,
            "algorithm": self.algorithm,
            "iterations": self.iterations
        }
    
    def verify(self, password: str, hash_data: Dict) -> bool:
        """Verify password against hash.
        
        Args:
            password: Password to verify
            hash_data: Hash data from hash()
            
        Returns:
            True if password matches
        """
        new_hash = self.hash(password, hash_data["salt"])
        return hmac.compare_digest(new_hash["hash"], hash_data["hash"])


class JWTToken:
    """JWT token encoder/decoder."""
    
    def __init__(self, secret: str, algorithm: str = "HS256"):
        """Initialize JWT handler.
        
        Args:
            secret: Secret key for signing
            algorithm: Algorithm (HS256, HS512)
        """
        self.secret = secret
        self.algorithm = algorithm
    
    def encode(self, payload: Dict, ttl: int = 3600) -> str:
        """Encode JWT token.
        
        Args:
            payload: Token payload
            ttl: Time to live in seconds
            
        Returns:
            JWT token string
        """
        import base64
        
        # Add expiration
        payload["exp"] = time.time() + ttl
        payload["iat"] = time.time()
        
        # Encode header
        header = {"alg": self.algorithm, "typ": "JWT"}
        header_b64 = base64.b64encode(json.dumps(header).encode()).decode().rstrip("=")
        
        # Encode payload
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        
        # Create signature
        message = f"{header_b64}.{payload_b64}"
        signature = hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
        signature_b64 = base64.b64encode(signature).decode().rstrip("=")
        
        return f"{message}.{signature_b64}"
    
    def decode(self, token: str) -> Optional[Dict]:
        """Decode and verify JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Payload dict or None if invalid
        """
        import base64
        
        try:
            header_b64, payload_b64, signature_b64 = token.split(".")
            
            # Verify signature
            message = f"{header_b64}.{payload_b64}"
            signature = hmac.new(
                self.secret.encode(),
                message.encode(),
                hashlib.sha256
            ).digest()
            
            expected_sig = base64.b64encode(signature).decode().rstrip("=")
            if not hmac.compare_digest(signature_b64, expected_sig):
                return None
            
            # Decode payload
            padding = "=" * (4 - len(payload_b64) % 4)
            payload_json = base64.b64decode(payload_b64 + padding).decode()
            payload = json.loads(payload_json)
            
            # Check expiration
            if "exp" in payload and payload["exp"] < time.time():
                return None
            
            return payload
        except Exception:
            return None


class Role:
    """Role definition with permissions."""
    
    def __init__(self, name: str, permissions: List[str] = None):
        """Initialize role.
        
        Args:
            name: Role name
            permissions: List of permission names
        """
        self.name = name
        self.permissions = set(permissions or [])
    
    def grant(self, permission: str):
        """Grant permission."""
        self.permissions.add(permission)
        return self
    
    def revoke(self, permission: str):
        """Revoke permission."""
        self.permissions.discard(permission)
        return self
    
    def has_permission(self, permission: str) -> bool:
        """Check if role has permission."""
        return permission in self.permissions


class User:
    """User with roles and permissions."""
    
    def __init__(self, username: str, email: str, password_hash: Dict = None):
        """Initialize user.
        
        Args:
            username: Username
            email: Email address
            password_hash: Password hash from PasswordHasher
        """
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.roles: List[Role] = []
        self.metadata: Dict = {}
        self.created_at = time.time()
        self.last_login = None
    
    def add_role(self, role: Role):
        """Add role to user."""
        self.roles.append(role)
        return self
    
    def remove_role(self, role: Role):
        """Remove role from user."""
        self.roles = [r for r in self.roles if r.name != role.name]
        return self
    
    def has_role(self, role_name: str) -> bool:
        """Check if user has role."""
        return any(r.name == role_name for r in self.roles)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has permission (via any role)."""
        return any(role.has_permission(permission) for role in self.roles)
    
    def get_permissions(self) -> set:
        """Get all user permissions."""
        perms = set()
        for role in self.roles:
            perms.update(role.permissions)
        return perms
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary."""
        return {
            "username": self.username,
            "email": self.email,
            "roles": [r.name for r in self.roles],
            "permissions": list(self.get_permissions()),
            "created_at": self.created_at,
            "last_login": self.last_login
        }


class AuthManager:
    """Authentication and authorization manager."""
    
    def __init__(self, jwt_secret: str):
        """Initialize auth manager.
        
        Args:
            jwt_secret: Secret key for JWT tokens
        """
        self.jwt = JWTToken(jwt_secret)
        self.hasher = PasswordHasher()
        self.users: Dict[str, User] = {}
        self.roles: Dict[str, Role] = {}
    
    def create_role(self, name: str, permissions: List[str] = None) -> Role:
        """Create role."""
        role = Role(name, permissions)
        self.roles[name] = role
        return role
    
    def register_user(self, username: str, email: str, password: str) -> User:
        """Register new user.
        
        Args:
            username: Username
            email: Email address
            password: Password (will be hashed)
            
        Returns:
            User instance
        """
        password_hash = self.hasher.hash(password)
        user = User(username, email, password_hash)
        self.users[username] = user
        return user
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return JWT token.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            JWT token or None
        """
        if username not in self.users:
            return None
        
        user = self.users[username]
        if not self.hasher.verify(password, user.password_hash):
            return None
        
        user.last_login = time.time()
        
        payload = {
            "username": username,
            "roles": [r.name for r in user.roles],
            "permissions": list(user.get_permissions())
        }
        
        return self.jwt.encode(payload)
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            Payload or None if invalid
        """
        return self.jwt.decode(token)
    
    def authorize(self, token: str, required_permission: str) -> bool:
        """Check if token has required permission.
        
        Args:
            token: JWT token
            required_permission: Permission to check
            
        Returns:
            True if authorized
        """
        payload = self.jwt.decode(token)
        if not payload:
            return False
        
        return required_permission in payload.get("permissions", [])


def require_permission(permission: str):
    """Decorator for permission-based access control."""
    def decorator(func: Callable) -> Callable:
        def wrapper(self, token: str, *args, **kwargs):
            manager = getattr(self, 'auth_manager', None)
            if not manager or not manager.authorize(token, permission):
                raise PermissionError(f"Permission '{permission}' required")
            return func(self, token, *args, **kwargs)
        return wrapper
    return decorator
