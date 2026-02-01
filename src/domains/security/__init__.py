"""
TOMBO Security Domain - Advanced security, encryption, and credential management
Provides secure hashing, encryption, rate limiting, and credential management
"""

# Import Phase 7 security libraries
from tombo.lib.security import AES, HMAC, HashingAlgorithm, RateLimiter, InputValidator, CredentialManager, SecureRandom

# Export main classes
__all__ = [
    'AES', 'HMAC', 'HashingAlgorithm', 'RateLimiter', 'InputValidator', 'CredentialManager', 'SecureRandom'
]

# Domain metadata
DOMAIN_NAME = 'security'
DOMAIN_LIBRARIES = ['security']
DOMAIN_VERSION = '7.0.0'
