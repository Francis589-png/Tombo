"""
Aggregations library - common aggregation functions and group-bys
"""
from typing import Iterable, Callable, List, Dict, Any
import math


def sum_values(values: Iterable[float]) -> float:
    return sum(values)


def mean(values: Iterable[float]) -> float:
    vals = list(values)
    return sum(vals) / len(vals) if vals else 0.0


def median(values: Iterable[float]) -> float:
    vals = sorted(values)
    n = len(vals)
    if n == 0:
        return 0.0
    mid = n // 2
    if n % 2 == 1:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2.0


def variance(values: Iterable[float], sample: bool = False) -> float:
    vals = list(values)
    n = len(vals)
    if n == 0:
        return 0.0
    m = mean(vals)
    ss = sum((x - m) ** 2 for x in vals)
    return ss / (n - 1 if sample and n > 1 else n)


def stddev(values: Iterable[float], sample: bool = False) -> float:
    return math.sqrt(variance(values, sample))


def group_by(records: Iterable[Dict[str, Any]], key_fn: Callable[[Dict[str, Any]], Any]) -> Dict[Any, List[Dict[str, Any]]]:
    groups: Dict[Any, List[Dict[str, Any]]] = {}
    for r in records:
        k = key_fn(r)
        groups.setdefault(k, []).append(r)
    return groups
