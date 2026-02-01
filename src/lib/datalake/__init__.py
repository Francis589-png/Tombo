"""
DataLake library - lightweight dataset storage and retrieval
"""
import json
from typing import Dict, Any, Optional
import os


class DataLake:
    """Minimal data lake storing named datasets on disk as JSONL."""

    def __init__(self, base_path: str = 'datalake'):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, name: str, records: Iterable[Dict[str, Any]]):
        path = os.path.join(self.base_path, f"{name}.jsonl")
        with open(path, 'w', encoding='utf-8') as fh:
            for r in records:
                fh.write(json.dumps(r, separators=(',', ':')) + '\n')
        return path

    def load(self, name: str):
        path = os.path.join(self.base_path, f"{name}.jsonl")
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as fh:
            for line in fh:
                yield json.loads(line)

    def list_datasets(self):
        for f in os.listdir(self.base_path):
            if f.endswith('.jsonl'):
                yield f[:-6]
