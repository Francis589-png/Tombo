"""
Query library - lightweight query engine for in-memory records
"""
from typing import Iterable, Callable, List, Dict, Any


class Query:
    """Simple query engine: filter, select, sort, limit."""

    def __init__(self, records: Iterable[Dict[str, Any]]):
        self._records = list(records)

    def filter(self, predicate: Callable[[Dict[str, Any]], bool]):
        self._records = [r for r in self._records if predicate(r)]
        return self

    def select(self, fields: List[str]):
        self._records = [{k: r.get(k) for k in fields} for r in self._records]
        return self

    def sort_by(self, key_fn: Callable[[Dict[str, Any]], Any], reverse: bool = False):
        self._records.sort(key=key_fn, reverse=reverse)
        return self

    def limit(self, n: int):
        self._records = self._records[:n]
        return self

    def all(self) -> List[Dict[str, Any]]:
        return self._records
