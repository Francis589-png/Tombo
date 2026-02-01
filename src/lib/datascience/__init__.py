"""
DataScience Library for TOMBO Language
Professional data manipulation, analysis, and visualization tools
"""

from typing import Any, List, Dict, Tuple, Optional, Union
from collections import defaultdict
import math


class DataFrame:
    """2D tabular data structure for data analysis"""
    
    def __init__(self, data: Optional[Dict[str, List[Any]]] = None):
        """Initialize DataFrame from dict of columns"""
        self.data = data if data else {}
        self.shape = (self._get_rows(), self._get_cols())
    
    def _get_rows(self) -> int:
        """Get number of rows"""
        if not self.data:
            return 0
        return len(next(iter(self.data.values())))
    
    def _get_cols(self) -> int:
        """Get number of columns"""
        return len(self.data)
    
    def add_column(self, name: str, values: List[Any]) -> None:
        """Add a column to DataFrame"""
        if len(values) != self._get_rows() and self._get_rows() > 0:
            raise ValueError("Column length must match DataFrame length")
        self.data[name] = values
        self.shape = (self._get_rows(), self._get_cols())
    
    def remove_column(self, name: str) -> None:
        """Remove a column"""
        if name in self.data:
            del self.data[name]
            self.shape = (self._get_rows(), self._get_cols())
    
    def get_column(self, name: str) -> List[Any]:
        """Get column as list"""
        return self.data.get(name, []).copy()
    
    def get_row(self, index: int) -> Dict[str, Any]:
        """Get row as dict"""
        row = {}
        for col_name, values in self.data.items():
            if index < len(values):
                row[col_name] = values[index]
        return row
    
    def filter(self, condition_func) -> 'DataFrame':
        """Filter rows by condition"""
        indices = []
        for i in range(self._get_rows()):
            if condition_func(self.get_row(i)):
                indices.append(i)
        
        filtered = {}
        for col_name, values in self.data.items():
            filtered[col_name] = [values[i] for i in indices]
        
        return DataFrame(filtered)
    
    def select_columns(self, columns: List[str]) -> 'DataFrame':
        """Select specific columns"""
        selected = {col: self.data[col] for col in columns if col in self.data}
        return DataFrame(selected)
    
    def head(self, n: int = 5) -> 'DataFrame':
        """Get first n rows"""
        result = {}
        for col_name, values in self.data.items():
            result[col_name] = values[:n]
        return DataFrame(result)
    
    def tail(self, n: int = 5) -> 'DataFrame':
        """Get last n rows"""
        result = {}
        for col_name, values in self.data.items():
            result[col_name] = values[-n:] if len(values) >= n else values
        return DataFrame(result)
    
    def describe(self) -> Dict[str, Dict[str, float]]:
        """Get statistical summary"""
        summary = {}
        for col_name, values in self.data.items():
            numeric_vals = [v for v in values if isinstance(v, (int, float))]
            if numeric_vals:
                summary[col_name] = {
                    'count': len(numeric_vals),
                    'mean': sum(numeric_vals) / len(numeric_vals),
                    'min': min(numeric_vals),
                    'max': max(numeric_vals),
                    'std': self._calculate_std(numeric_vals)
                }
        return summary
    
    def _calculate_std(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
    
    def group_by(self, column: str) -> Dict[Any, 'DataFrame']:
        """Group DataFrame by column"""
        groups = defaultdict(lambda: {col: [] for col in self.data})
        
        for i, key_val in enumerate(self.data[column]):
            for col_name, values in self.data.items():
                groups[key_val][col_name].append(values[i])
        
        return {key: DataFrame(data) for key, data in groups.items()}
    
    def sort_by(self, column: str, ascending: bool = True) -> 'DataFrame':
        """Sort DataFrame by column"""
        if column not in self.data:
            return self
        
        values = self.data[column]
        indices = sorted(range(len(values)), 
                        key=lambda i: values[i],
                        reverse=not ascending)
        
        sorted_data = {}
        for col_name, col_values in self.data.items():
            sorted_data[col_name] = [col_values[i] for i in indices]
        
        return DataFrame(sorted_data)
    
    def merge(self, other: 'DataFrame', on: str) -> 'DataFrame':
        """Merge with another DataFrame"""
        merged = {}
        
        # Add columns from self
        for col_name, values in self.data.items():
            merged[col_name] = values.copy()
        
        # Add columns from other
        for col_name, values in other.data.items():
            if col_name != on and col_name not in merged:
                merged[col_name] = values.copy()
        
        return DataFrame(merged)
    
    def unique_values(self, column: str) -> List[Any]:
        """Get unique values in column"""
        return list(set(self.data.get(column, [])))
    
    def value_counts(self, column: str) -> Dict[Any, int]:
        """Count value occurrences"""
        counts = defaultdict(int)
        for val in self.data.get(column, []):
            counts[val] += 1
        return dict(counts)
    
    def to_dict(self) -> Dict[str, List[Any]]:
        """Convert to dictionary"""
        return {col: values.copy() for col, values in self.data.items()}
    
    def __str__(self) -> str:
        """String representation"""
        return f"DataFrame({self._get_rows()} rows, {self._get_cols()} cols)"


class Series:
    """1D labeled data structure"""
    
    def __init__(self, data: List[Any], name: str = "Series"):
        """Initialize Series"""
        self.data = data
        self.name = name
    
    def mean(self) -> float:
        """Calculate mean"""
        numeric = [x for x in self.data if isinstance(x, (int, float))]
        return sum(numeric) / len(numeric) if numeric else 0.0
    
    def median(self) -> float:
        """Calculate median"""
        numeric = sorted([x for x in self.data if isinstance(x, (int, float))])
        if not numeric:
            return 0.0
        n = len(numeric)
        return numeric[n // 2] if n % 2 else (numeric[n // 2 - 1] + numeric[n // 2]) / 2
    
    def std(self) -> float:
        """Calculate standard deviation"""
        numeric = [x for x in self.data if isinstance(x, (int, float))]
        if not numeric:
            return 0.0
        mean = sum(numeric) / len(numeric)
        variance = sum((x - mean) ** 2 for x in numeric) / len(numeric)
        return math.sqrt(variance)
    
    def min(self) -> Any:
        """Get minimum value"""
        numeric = [x for x in self.data if isinstance(x, (int, float))]
        return min(numeric) if numeric else None
    
    def max(self) -> Any:
        """Get maximum value"""
        numeric = [x for x in self.data if isinstance(x, (int, float))]
        return max(numeric) if numeric else None
    
    def unique(self) -> List[Any]:
        """Get unique values"""
        return list(set(self.data))
    
    def value_counts(self) -> Dict[Any, int]:
        """Count value occurrences"""
        counts = defaultdict(int)
        for val in self.data:
            counts[val] += 1
        return dict(counts)


class Visualization:
    """Data visualization tools"""
    
    @staticmethod
    def histogram(values: List[float], bins: int = 10) -> str:
        """Create ASCII histogram"""
        if not values:
            return "No data"
        
        min_val = min(values)
        max_val = max(values)
        bin_width = (max_val - min_val) / bins if max_val > min_val else 1
        
        bin_counts = [0] * bins
        for val in values:
            if val == max_val:
                bin_counts[-1] += 1
            else:
                idx = int((val - min_val) / bin_width)
                if 0 <= idx < bins:
                    bin_counts[idx] += 1
        
        max_count = max(bin_counts)
        height = 20
        
        output = "Histogram\n"
        output += "=" * 50 + "\n"
        
        for h in range(height, 0, -1):
            for count in bin_counts:
                scaled = int((count / max_count * height) if max_count > 0 else 0)
                output += "█" if scaled >= h else " "
            output += "\n"
        
        return output
    
    @staticmethod
    def scatter_plot(x: List[float], y: List[float]) -> str:
        """Create ASCII scatter plot"""
        if len(x) != len(y) or not x:
            return "Invalid data"
        
        width = 50
        height = 20
        
        min_x = min(x)
        max_x = max(x)
        min_y = min(y)
        max_y = max(y)
        
        grid = [['.' for _ in range(width)] for _ in range(height)]
        
        for xi, yi in zip(x, y):
            px = int((xi - min_x) / (max_x - min_x) * (width - 1)) if max_x > min_x else 0
            py = int((yi - min_y) / (max_y - min_y) * (height - 1)) if max_y > min_y else 0
            
            if 0 <= px < width and 0 <= py < height:
                grid[height - 1 - py][px] = '*'
        
        output = "Scatter Plot\n"
        output += "=" * 50 + "\n"
        for row in grid:
            output += ''.join(row) + "\n"
        
        return output
    
    @staticmethod
    def line_plot(values: List[float]) -> str:
        """Create ASCII line plot"""
        if not values:
            return "No data"
        
        height = 15
        width = len(values)
        
        min_val = min(values)
        max_val = max(values)
        
        grid = [['.' for _ in range(width)] for _ in range(height)]
        
        for i, val in enumerate(values):
            if max_val > min_val:
                y = int((val - min_val) / (max_val - min_val) * (height - 1))
            else:
                y = height // 2
            
            if 0 <= y < height:
                grid[height - 1 - y][i] = '*'
        
        output = "Line Plot\n"
        output += "=" * 50 + "\n"
        for row in grid:
            output += ''.join(row) + "\n"
        
        return output


class Statistics:
    """Statistical functions"""
    
    @staticmethod
    def correlation(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation"""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        
        return cov / (std_x * std_y) if std_x > 0 and std_y > 0 else 0.0
    
    @staticmethod
    def covariance(x: List[float], y: List[float]) -> float:
        """Calculate covariance"""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        
        return sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
    
    @staticmethod
    def percentile(data: List[float], p: float) -> float:
        """Calculate percentile"""
        if not data or not (0 <= p <= 100):
            return 0.0
        
        sorted_data = sorted(data)
        idx = (p / 100) * (len(sorted_data) - 1)
        lower = int(idx)
        upper = lower + 1
        
        if upper >= len(sorted_data):
            return sorted_data[-1]
        
        weight = idx - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight
    
    @staticmethod
    def z_score(value: float, mean: float, std: float) -> float:
        """Calculate Z-score"""
        return (value - mean) / std if std > 0 else 0.0


# Public API
__all__ = [
    'DataFrame',
    'Series',
    'Visualization',
    'Statistics'
]
