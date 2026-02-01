"""
TOMBO Storage Library - File format handling and compression
Support for various formats: CSV, TSV, Parquet-like, with compression.
"""

import gzip
import struct
from typing import Dict, List, Any, Optional


class CSVHandler:
    """CSV file handling."""
    
    @staticmethod
    def read(filename: str, delimiter: str = ',') -> List[Dict]:
        """Read CSV file.
        
        Args:
            filename: File path
            delimiter: Field delimiter
            
        Returns:
            List of row dictionaries
        """
        rows = []
        
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            if not lines:
                return rows
            
            # Parse header
            headers = [h.strip() for h in lines[0].split(delimiter)]
            
            # Parse rows
            for line in lines[1:]:
                if line.strip():
                    values = [v.strip() for v in line.split(delimiter)]
                    row = {headers[i]: values[i] if i < len(values) else None
                           for i in range(len(headers))}
                    rows.append(row)
        
        return rows
    
    @staticmethod
    def write(filename: str, data: List[Dict], delimiter: str = ','):
        """Write CSV file.
        
        Args:
            filename: File path
            data: List of row dictionaries
            delimiter: Field delimiter
        """
        if not data:
            return
        
        headers = list(data[0].keys())
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Write header
            f.write(delimiter.join(headers) + '\n')
            
            # Write rows
            for row in data:
                values = [str(row.get(h, '')) for h in headers]
                f.write(delimiter.join(values) + '\n')


class TSVHandler:
    """TSV file handling."""
    
    @staticmethod
    def read(filename: str) -> List[Dict]:
        """Read TSV file."""
        return CSVHandler.read(filename, delimiter='\t')
    
    @staticmethod
    def write(filename: str, data: List[Dict]):
        """Write TSV file."""
        CSVHandler.write(filename, data, delimiter='\t')


class JSONLHandler:
    """JSONL (JSON Lines) file handling."""
    
    @staticmethod
    def read(filename: str) -> List[Dict]:
        """Read JSONL file.
        
        Args:
            filename: File path
            
        Returns:
            List of JSON objects
        """
        import json
        
        rows = []
        
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        row = json.loads(line)
                        rows.append(row)
                    except json.JSONDecodeError:
                        pass
        
        return rows
    
    @staticmethod
    def write(filename: str, data: List[Dict]):
        """Write JSONL file.
        
        Args:
            filename: File path
            data: List of objects
        """
        import json
        
        with open(filename, 'w', encoding='utf-8') as f:
            for row in data:
                f.write(json.dumps(row) + '\n')


class BinaryHandler:
    """Binary data handling."""
    
    @staticmethod
    def pack_numbers(numbers: List[float]) -> bytes:
        """Pack numbers as binary.
        
        Args:
            numbers: List of floats
            
        Returns:
            Binary data
        """
        # Pack as IEEE 754 doubles
        data = b''
        for num in numbers:
            data += struct.pack('d', num)
        return data
    
    @staticmethod
    def unpack_numbers(data: bytes) -> List[float]:
        """Unpack binary to numbers.
        
        Args:
            data: Binary data
            
        Returns:
            List of floats
        """
        numbers = []
        for i in range(0, len(data), 8):
            num = struct.unpack('d', data[i:i+8])[0]
            numbers.append(num)
        return numbers


class Compressor:
    """Data compression utilities."""
    
    @staticmethod
    def gzip_compress(data: bytes, level: int = 9) -> bytes:
        """Compress data with gzip.
        
        Args:
            data: Data to compress
            level: Compression level (1-9)
            
        Returns:
            Compressed data
        """
        return gzip.compress(data, compresslevel=level)
    
    @staticmethod
    def gzip_decompress(data: bytes) -> bytes:
        """Decompress gzip data.
        
        Args:
            data: Compressed data
            
        Returns:
            Decompressed data
        """
        return gzip.decompress(data)
    
    @staticmethod
    def simple_compress(data: bytes) -> bytes:
        """Simple run-length compression.
        
        Args:
            data: Data to compress
            
        Returns:
            Compressed data
        """
        if not data:
            return b''
        
        compressed = b''
        current_byte = data[0]
        count = 1
        
        for byte in data[1:]:
            if byte == current_byte and count < 255:
                count += 1
            else:
                compressed += bytes([count, current_byte])
                current_byte = byte
                count = 1
        
        compressed += bytes([count, current_byte])
        
        return compressed
    
    @staticmethod
    def simple_decompress(data: bytes) -> bytes:
        """Simple run-length decompression.
        
        Args:
            data: Compressed data
            
        Returns:
            Decompressed data
        """
        decompressed = b''
        
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                count = data[i]
                byte = data[i + 1]
                decompressed += bytes([byte] * count)
        
        return decompressed


class FileFormat:
    """Detect and handle file formats."""
    
    FORMATS = {
        '.csv': CSVHandler,
        '.tsv': TSVHandler,
        '.jsonl': JSONLHandler,
        '.json': 'json',  # Use json module
        '.gz': 'gzip'
    }
    
    @staticmethod
    def get_format(filename: str):
        """Get handler for file format.
        
        Args:
            filename: File path
            
        Returns:
            Handler class or module
        """
        import os
        
        ext = os.path.splitext(filename)[1].lower()
        return FileFormat.FORMATS.get(ext)
    
    @staticmethod
    def read(filename: str) -> Any:
        """Read file with auto-detection.
        
        Args:
            filename: File path
            
        Returns:
            Parsed data
        """
        handler = FileFormat.get_format(filename)
        
        if handler == 'json':
            import json
            with open(filename, 'r') as f:
                return json.load(f)
        elif handler == 'gzip':
            with gzip.open(filename, 'rb') as f:
                return f.read()
        elif hasattr(handler, 'read'):
            return handler.read(filename)
        
        raise ValueError(f"Unknown file format: {filename}")
    
    @staticmethod
    def write(filename: str, data: Any):
        """Write file with auto-detection.
        
        Args:
            filename: File path
            data: Data to write
        """
        handler = FileFormat.get_format(filename)
        
        if handler == 'json':
            import json
            with open(filename, 'w') as f:
                json.dump(data, f)
        elif handler == 'gzip':
            with gzip.open(filename, 'wb') as f:
                f.write(data if isinstance(data, bytes) else str(data).encode())
        elif hasattr(handler, 'write'):
            handler.write(filename, data)
        else:
            raise ValueError(f"Unknown file format: {filename}")


class StorageManager:
    """Manage data storage and retrieval."""
    
    def __init__(self, base_path: str = "."):
        """Initialize storage manager.
        
        Args:
            base_path: Base directory for files
        """
        self.base_path = base_path
        self.cache: Dict[str, Any] = {}
    
    def save(self, name: str, data: Any, format: str = 'json', 
             compress: bool = False):
        """Save data.
        
        Args:
            name: File name (without extension)
            data: Data to save
            format: File format (csv, json, etc)
            compress: Whether to compress
        """
        import os
        
        filename = os.path.join(self.base_path, f"{name}.{format}")
        
        FileFormat.write(filename, data)
        
        if compress:
            with open(filename, 'rb') as f:
                compressed = Compressor.gzip_compress(f.read())
            
            with open(f"{filename}.gz", 'wb') as f:
                f.write(compressed)
        
        self.cache[name] = data
    
    def load(self, name: str, format: str = 'json') -> Any:
        """Load data.
        
        Args:
            name: File name
            format: File format
            
        Returns:
            Loaded data
        """
        import os
        
        if name in self.cache:
            return self.cache[name]
        
        filename = os.path.join(self.base_path, f"{name}.{format}")
        
        if os.path.exists(filename):
            data = FileFormat.read(filename)
            self.cache[name] = data
            return data
        
        return None
    
    def delete(self, name: str, format: str = 'json'):
        """Delete file.
        
        Args:
            name: File name
            format: File format
        """
        import os
        
        filename = os.path.join(self.base_path, f"{name}.{format}")
        
        if os.path.exists(filename):
            os.remove(filename)
        
        if name in self.cache:
            del self.cache[name]
    
    def list_files(self) -> List[str]:
        """List all files."""
        import os
        
        files = []
        
        if os.path.exists(self.base_path):
            files = os.listdir(self.base_path)
        
        return files
