"""
Tombo Crypto Library - Cryptographic Functions
"""
import hashlib
import hmac
import secrets

def tombo_md5(data):
    """MD5 hash."""
    return hashlib.md5(str(data).encode()).hexdigest()

def tombo_sha1(data):
    """SHA1 hash."""
    return hashlib.sha1(str(data).encode()).hexdigest()

def tombo_sha256(data):
    """SHA256 hash."""
    return hashlib.sha256(str(data).encode()).hexdigest()

def tombo_sha512(data):
    """SHA512 hash."""
    return hashlib.sha512(str(data).encode()).hexdigest()

def tombo_sha3_256(data):
    """SHA3-256 hash."""
    return hashlib.sha3_256(str(data).encode()).hexdigest()

def tombo_sha3_512(data):
    """SHA3-512 hash."""
    return hashlib.sha3_512(str(data).encode()).hexdigest()

def tombo_blake2(data):
    """BLAKE2 hash."""
    return hashlib.blake2b(str(data).encode()).hexdigest()

def tombo_hmac_sha256(data, key):
    """HMAC-SHA256."""
    return hmac.new(str(key).encode(), str(data).encode(), hashlib.sha256).hexdigest()

def tombo_hmac_sha512(data, key):
    """HMAC-SHA512."""
    return hmac.new(str(key).encode(), str(data).encode(), hashlib.sha512).hexdigest()

def tombo_generate_key(length=32):
    """Generate random key."""
    return secrets.token_hex(int(length) // 2)

def tombo_generate_token(length=32):
    """Generate random token."""
    return secrets.token_hex(int(length) // 2)

def tombo_secure_random(n=32):
    """Generate n random bytes."""
    return secrets.token_bytes(int(n)).hex()

def tombo_hash_password(password, algorithm='sha256'):
    """Hash a password."""
    algo = str(algorithm).lower()
    if algo == 'sha256':
        return tombo_sha256(password)
    elif algo == 'sha512':
        return tombo_sha512(password)
    elif algo == 'blake2':
        return tombo_blake2(password)
    else:
        return tombo_sha256(password)

def tombo_verify_hash(data, hash_value, algorithm='sha256'):
    """Verify a hash."""
    return tombo_hash_password(data, algorithm) == hash_value

def register(env):
    """Register crypto library functions."""
    functions = {
        'md5': tombo_md5,
        'sha1': tombo_sha1,
        'sha256': tombo_sha256,
        'sha512': tombo_sha512,
        'sha3_256': tombo_sha3_256,
        'sha3_512': tombo_sha3_512,
        'blake2': tombo_blake2,
        'hmac_sha256': tombo_hmac_sha256,
        'hmac_sha512': tombo_hmac_sha512,
        'generate_key': tombo_generate_key,
        'generate_token': tombo_generate_token,
        'secure_random': tombo_secure_random,
        'hash_password': tombo_hash_password,
        'verify_hash': tombo_verify_hash,
    }
    for name, func in functions.items():
        env.set(name, func)
