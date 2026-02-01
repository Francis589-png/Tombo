"""
TOMBO Filesystem Domain - File operations, formats, and storage
Provides CSV/TSV/JSONL handling, compression, and storage management
"""

# Import Phase 7 filesystem libraries
from tombo.lib.storage import CSVHandler, TSVHandler, JSONLHandler, BinaryHandler, Compressor, FileFormat, StorageManager

# Export main classes
__all__ = [
    'CSVHandler', 'TSVHandler', 'JSONLHandler', 'BinaryHandler', 'Compressor', 'FileFormat', 'StorageManager'
]

# Domain metadata
DOMAIN_NAME = 'filesystem'
DOMAIN_LIBRARIES = ['storage']
DOMAIN_VERSION = '7.0.0'
