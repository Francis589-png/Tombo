"""
TOMBO Security Library - Advanced security utilities
Encryption, key management, secure random generation, rate limiting.
"""

import secrets
import hashlib
import hmac
from typing import Dict, Any, Optional, Tuple


class SecureRandom:
    """Cryptographically secure random generation."""
    
    @staticmethod
    def bytes(length: int) -> bytes:
        """Generate random bytes.
        
        Args:
            length: Number of bytes
            
        Returns:
            Random bytes
        """
        return secrets.token_bytes(length)
    
    @staticmethod
    def hex(length: int) -> str:
        """Generate random hex string.
        
        Args:
            length: Number of bytes (returned as 2*length hex chars)
            
        Returns:
            Random hex string
        """
        return secrets.token_hex(length)
    
    @staticmethod
    def urlsafe(length: int) -> str:
        """Generate URL-safe random string.
        
        Args:
            length: String length
            
        Returns:
            Random URL-safe string
        """
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def choice(sequence):
        """Securely choose from sequence.
        
        Args:
            sequence: Sequence to choose from
            
        Returns:
            Random element
        """
        return secrets.choice(sequence)


class AES:
    """AES encryption (simplified)."""
    
    @staticmethod
    def generate_key(length: int = 32) -> bytes:
        """Generate AES key.
        
        Args:
            length: Key length in bytes (16, 24, or 32)
            
        Returns:
            Random key
        """
        return SecureRandom.bytes(length)
    
    @staticmethod
    def generate_iv() -> bytes:
        """Generate initialization vector.
        
        Returns:
            Random IV (16 bytes)
        """
        return SecureRandom.bytes(16)
    
    @staticmethod
    def simple_encrypt(plaintext: str, key: bytes) -> bytes:
        """Simple XOR-based encryption (educational only).
        
        Args:
            plaintext: Text to encrypt
            key: Encryption key
            
        Returns:
            Encrypted data with IV prepended
        """
        import os
        
        iv = SecureRandom.bytes(16)
        ciphertext = b''
        
        plaintext_bytes = plaintext.encode('utf-8')
        
        for i, byte in enumerate(plaintext_bytes):
            key_byte = key[i % len(key)]
            ciphertext += bytes([byte ^ key_byte])
        
        return iv + ciphertext
    
    @staticmethod
    def simple_decrypt(encrypted: bytes, key: bytes) -> str:
        """Simple XOR-based decryption (educational only).
        
        Args:
            encrypted: Encrypted data
            key: Decryption key
            
        Returns:
            Decrypted plaintext
        """
        iv = encrypted[:16]
        ciphertext = encrypted[16:]
        
        plaintext_bytes = b''
        
        for i, byte in enumerate(ciphertext):
            key_byte = key[i % len(key)]
            plaintext_bytes += bytes([byte ^ key_byte])
        
        return plaintext_bytes.decode('utf-8')


class HMAC:
    """HMAC authentication."""
    
    @staticmethod
    def sign(message: str, secret: str, algorithm: str = 'sha256') -> str:
        """Create HMAC signature.
        
        Args:
            message: Message to sign
            secret: Secret key
            algorithm: Hash algorithm
            
        Returns:
            HMAC signature
        """
        h = hmac.new(
            secret.encode(),
            message.encode(),
            getattr(hashlib, algorithm)
        )
        
        return h.hexdigest()
    
    @staticmethod
    def verify(message: str, signature: str, secret: str,
               algorithm: str = 'sha256') -> bool:
        """Verify HMAC signature.
        
        Args:
            message: Original message
            signature: Signature to verify
            secret: Secret key
            algorithm: Hash algorithm
            
        Returns:
            True if signature is valid
        """
        expected = HMAC.sign(message, secret, algorithm)
        return hmac.compare_digest(signature, expected)


class HashingAlgorithm:
    """Secure hashing."""
    
    @staticmethod
    def sha256(data: str) -> str:
        """SHA-256 hash.
        
        Args:
            data: Data to hash
            
        Returns:
            Hex digest
        """
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def sha512(data: str) -> str:
        """SHA-512 hash.
        
        Args:
            data: Data to hash
            
        Returns:
            Hex digest
        """
        return hashlib.sha512(data.encode()).hexdigest()
    
    @staticmethod
    def blake2b(data: str, digest_size: int = 64) -> str:
        """BLAKE2b hash.
        
        Args:
            data: Data to hash
            digest_size: Digest size in bytes
            
        Returns:
            Hex digest
        """
        h = hashlib.blake2b(data.encode(), digest_size=digest_size)
        return h.hexdigest()


class RateLimiter:
    """Rate limiting for security."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        """Initialize rate limiter.
        
        Args:
            max_requests: Max requests per window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed.
        
        Args:
            identifier: Client identifier
            
        Returns:
            True if allowed
        """
        import time
        
        now = time.time()
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Remove old requests outside window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if now - req_time < self.window_seconds
        ]
        
        # Check if limit exceeded
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        
        # Add request
        self.requests[identifier].append(now)
        
        return True
    
    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests.
        
        Args:
            identifier: Client identifier
            
        Returns:
            Remaining requests
        """
        if identifier not in self.requests:
            return self.max_requests
        
        return max(0, self.max_requests - len(self.requests[identifier]))


class InputValidator:
    """Input validation and sanitization."""
    
    @staticmethod
    def sanitize_sql(query: str) -> str:
        """Basic SQL injection prevention.
        
        Args:
            query: SQL query
            
        Returns:
            Sanitized query
        """
        # Replace dangerous characters
        dangerous = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]
        
        for char in dangerous:
            query = query.replace(char, "")
        
        return query
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """XSS prevention via HTML escaping.
        
        Args:
            text: HTML text
            
        Returns:
            Escaped text
        """
        escapes = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }
        
        for char, escaped in escapes.items():
            text = text.replace(char, escaped)
        
        return text
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Prevent directory traversal.
        
        Args:
            filename: File name
            
        Returns:
            Sanitized filename
        """
        import os
        
        # Remove path separators
        filename = os.path.basename(filename)
        
        # Remove dangerous characters
        dangerous = ['..', '/', '\\', '\0', '\n', '\r']
        
        for char in dangerous:
            filename = filename.replace(char, '')
        
        return filename


class CredentialManager:
    """Manage sensitive credentials."""
    
    def __init__(self):
        """Initialize credential manager."""
        self.credentials: Dict[str, str] = {}
    
    def set_credential(self, name: str, value: str):
        """Store credential.
        
        Args:
            name: Credential name
            value: Credential value
        """
        self.credentials[name] = value
    
    def get_credential(self, name: str) -> Optional[str]:
        """Get credential.
        
        Args:
            name: Credential name
            
        Returns:
            Credential value
        """
        return self.credentials.get(name)
    
    def delete_credential(self, name: str):
        """Delete credential.
        
        Args:
            name: Credential name
        """
        if name in self.credentials:
            del self.credentials[name]
    
    def clear_all(self):
        """Clear all credentials."""
        self.credentials.clear()
