"""
MapReduce library - simple in-memory MapReduce utilities
"""
from typing import Callable, Iterable, List, Tuple, Dict, Any


class MapReduce:
    """Lightweight MapReduce-style processing for lists of data."""

    @staticmethod
    def map(records: Iterable[Any], map_fn: Callable[[Any], Iterable[Tuple[Any, Any]]]) -> List[Tuple[Any, Any]]:
        out = []
        for r in records:
            for kv in map_fn(r):
                out.append(kv)
        return out

    @staticmethod
    def shuffle(pairs: Iterable[Tuple[Any, Any]]) -> Dict[Any, List[Any]]:
        grouped: Dict[Any, List[Any]] = {}
        for k, v in pairs:
            grouped.setdefault(k, []).append(v)
        return grouped

    @staticmethod
    def reduce(grouped: Dict[Any, List[Any]], reduce_fn: Callable[[Any, List[Any]], Tuple[Any, Any]]) -> List[Tuple[Any, Any]]:
        results = []
        for k, values in grouped.items():
            results.append(reduce_fn(k, values))
        return results

    @staticmethod
    def execute(records: Iterable[Any], map_fn: Callable[[Any], Iterable[Tuple[Any, Any]]], reduce_fn: Callable[[Any, List[Any]], Tuple[Any, Any]]) -> List[Tuple[Any, Any]]:
        pairs = MapReduce.map(records, map_fn)
        grouped = MapReduce.shuffle(pairs)
        return MapReduce.reduce(grouped, reduce_fn)
