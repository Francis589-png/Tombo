"""
Analytics library - descriptive stats and simple analytics helpers
"""
from typing import Iterable, List, Dict, Any
from statistics import mean, median


def describe(values: Iterable[float]) -> Dict[str, float]:
    vals = list(values)
    return {
        'count': len(vals),
        'mean': mean(vals) if vals else 0.0,
        'median': median(vals) if vals else 0.0,
        'min': min(vals) if vals else 0.0,
        'max': max(vals) if vals else 0.0,
    }


def moving_average(values: Iterable[float], window: int = 3) -> List[float]:
    vals = list(values)
    if window <= 0:
        raise ValueError('window must be > 0')
    out: List[float] = []
    for i in range(len(vals)):
        start = max(0, i - window + 1)
        out.append(mean(vals[start:i+1]))
    return out


def correlation(x: Iterable[float], y: Iterable[float]) -> float:
    x_vals = list(x)
    y_vals = list(y)
    if len(x_vals) != len(y_vals) or len(x_vals) == 0:
        return 0.0
    mx = mean(x_vals)
    my = mean(y_vals)
    num = sum((a - mx) * (b - my) for a, b in zip(x_vals, y_vals))
    denom_x = sum((a - mx) ** 2 for a in x_vals)
    denom_y = sum((b - my) ** 2 for b in y_vals)
    denom = (denom_x * denom_y) ** 0.5
    return num / denom if denom != 0 else 0.0
