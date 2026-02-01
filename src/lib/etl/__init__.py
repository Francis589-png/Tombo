"""
TOMBO Data ETL Library - Extract, transform, load for data processing
Data pipelines, transformations, aggregations, and joins.
"""

from typing import Dict, List, Any, Callable, Optional, Union


class DataFrame:
    """Simple in-memory data frame."""
    
    def __init__(self, data: Dict[str, List] = None, rows: List[Dict] = None):
        """Initialize DataFrame.
        
        Args:
            data: Dictionary of column_name: [values]
            rows: List of row dictionaries
        """
        if data:
            self.columns = list(data.keys())
            self.data = data
            self.rows_count = len(list(data.values())[0]) if data else 0
        elif rows:
            if not rows:
                self.columns = []
                self.data = {}
                self.rows_count = 0
            else:
                self.columns = list(rows[0].keys())
                self.data = {col: [] for col in self.columns}
                
                for row in rows:
                    for col in self.columns:
                        self.data[col].append(row.get(col))
                
                self.rows_count = len(rows)
        else:
            self.columns = []
            self.data = {}
            self.rows_count = 0
    
    def shape(self) -> tuple:
        """Get shape (rows, columns)."""
        return (self.rows_count, len(self.columns))
    
    def head(self, n: int = 5) -> List[Dict]:
        """Get first n rows."""
        rows = []
        for i in range(min(n, self.rows_count)):
            row = {col: self.data[col][i] for col in self.columns}
            rows.append(row)
        return rows
    
    def tail(self, n: int = 5) -> List[Dict]:
        """Get last n rows."""
        start = max(0, self.rows_count - n)
        rows = []
        for i in range(start, self.rows_count):
            row = {col: self.data[col][i] for col in self.columns}
            rows.append(row)
        return rows
    
    def select(self, columns: List[str]) -> 'DataFrame':
        """Select specific columns."""
        new_data = {col: self.data[col] for col in columns if col in self.data}
        return DataFrame(data=new_data)
    
    def filter(self, condition: Callable[[Dict], bool]) -> 'DataFrame':
        """Filter rows by condition."""
        new_rows = []
        for i in range(self.rows_count):
            row = {col: self.data[col][i] for col in self.columns}
            if condition(row):
                new_rows.append(row)
        return DataFrame(rows=new_rows)
    
    def map(self, transform: Callable[[Dict], Dict]) -> 'DataFrame':
        """Apply transformation to each row."""
        new_rows = []
        for i in range(self.rows_count):
            row = {col: self.data[col][i] for col in self.columns}
            new_rows.append(transform(row))
        return DataFrame(rows=new_rows)
    
    def sort_by(self, column: str, ascending: bool = True) -> 'DataFrame':
        """Sort by column."""
        indices = list(range(self.rows_count))
        indices.sort(
            key=lambda i: self.data[column][i],
            reverse=not ascending
        )
        
        new_data = {}
        for col in self.columns:
            new_data[col] = [self.data[col][i] for i in indices]
        
        return DataFrame(data=new_data)
    
    def group_by(self, column: str) -> Dict[Any, 'DataFrame']:
        """Group by column value."""
        groups = {}
        
        for i in range(self.rows_count):
            key = self.data[column][i]
            if key not in groups:
                groups[key] = {col: [] for col in self.columns}
            
            for col in self.columns:
                groups[key][col].append(self.data[col][i])
        
        return {
            key: DataFrame(data=data)
            for key, data in groups.items()
        }
    
    def aggregate(self, column: str, func: str) -> Any:
        """Aggregate column with function.
        
        Args:
            column: Column to aggregate
            func: Function name (sum, mean, min, max, count)
            
        Returns:
            Aggregation result
        """
        values = self.data[column]
        
        if func == "sum":
            return sum(v for v in values if isinstance(v, (int, float)))
        elif func == "mean":
            numeric = [v for v in values if isinstance(v, (int, float))]
            return sum(numeric) / len(numeric) if numeric else 0
        elif func == "min":
            numeric = [v for v in values if isinstance(v, (int, float))]
            return min(numeric) if numeric else None
        elif func == "max":
            numeric = [v for v in values if isinstance(v, (int, float))]
            return max(numeric) if numeric else None
        elif func == "count":
            return len([v for v in values if v is not None])
        else:
            raise ValueError(f"Unknown aggregation: {func}")
    
    def join(self, other: 'DataFrame', on: str, how: str = "inner") -> 'DataFrame':
        """Join with another DataFrame.
        
        Args:
            other: Other DataFrame
            on: Column name to join on
            how: Join type (inner, left, right, outer)
            
        Returns:
            Joined DataFrame
        """
        result_rows = []
        
        for i in range(self.rows_count):
            self_key = self.data[on][i]
            
            for j in range(other.rows_count):
                other_key = other.data[on][j]
                
                if self_key == other_key:
                    # Inner join - rows match
                    row = {}
                    for col in self.columns:
                        row[col] = self.data[col][i]
                    
                    for col in other.columns:
                        if col != on:
                            row[f"{col}_other"] = other.data[col][j]
                    
                    result_rows.append(row)
        
        return DataFrame(rows=result_rows)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary format."""
        return {
            "columns": self.columns,
            "data": self.data,
            "shape": self.shape()
        }
    
    def to_list(self) -> List[Dict]:
        """Convert to list of row dictionaries."""
        rows = []
        for i in range(self.rows_count):
            row = {col: self.data[col][i] for col in self.columns}
            rows.append(row)
        return rows


class ETLPipeline:
    """ETL pipeline for data processing."""
    
    def __init__(self, data: Union[Dict, List[Dict]]):
        """Initialize pipeline.
        
        Args:
            data: Input data (dict or list of dicts)
        """
        if isinstance(data, dict):
            self.dataframe = DataFrame(data=data)
        else:
            self.dataframe = DataFrame(rows=data)
    
    def extract(self, source_data: Union[Dict, List[Dict]]) -> 'ETLPipeline':
        """Extract data from source."""
        if isinstance(source_data, dict):
            self.dataframe = DataFrame(data=source_data)
        else:
            self.dataframe = DataFrame(rows=source_data)
        return self
    
    def select_columns(self, columns: List[str]) -> 'ETLPipeline':
        """Select specific columns."""
        self.dataframe = self.dataframe.select(columns)
        return self
    
    def filter_rows(self, condition: Callable[[Dict], bool]) -> 'ETLPipeline':
        """Filter rows."""
        self.dataframe = self.dataframe.filter(condition)
        return self
    
    def transform(self, func: Callable[[Dict], Dict]) -> 'ETLPipeline':
        """Transform rows."""
        self.dataframe = self.dataframe.map(func)
        return self
    
    def add_column(self, name: str, values: List) -> 'ETLPipeline':
        """Add new column."""
        if len(values) != self.dataframe.rows_count:
            raise ValueError("Values length must match DataFrame rows")
        
        self.dataframe.columns.append(name)
        self.dataframe.data[name] = values
        
        return self
    
    def drop_column(self, column: str) -> 'ETLPipeline':
        """Drop column."""
        if column in self.dataframe.data:
            del self.dataframe.data[column]
            self.dataframe.columns.remove(column)
        return self
    
    def sort(self, column: str, ascending: bool = True) -> 'ETLPipeline':
        """Sort by column."""
        self.dataframe = self.dataframe.sort_by(column, ascending)
        return self
    
    def load(self) -> DataFrame:
        """Load and return processed data."""
        return self.dataframe
    
    def to_dict(self) -> Dict:
        """Export as dictionary."""
        return self.dataframe.to_dict()
    
    def to_list(self) -> List[Dict]:
        """Export as list of dicts."""
        return self.dataframe.to_list()


class DataValidator:
    """Validate data quality."""
    
    @classmethod
    def check_missing(cls, dataframe: DataFrame) -> Dict[str, int]:
        """Check for missing values.
        
        Args:
            dataframe: DataFrame to check
            
        Returns:
            Column names and missing count
        """
        missing = {}
        for col in dataframe.columns:
            count = sum(1 for v in dataframe.data[col] if v is None)
            if count > 0:
                missing[col] = count
        return missing
    
    @classmethod
    def check_duplicates(cls, dataframe: DataFrame) -> int:
        """Check for duplicate rows.
        
        Args:
            dataframe: DataFrame to check
            
        Returns:
            Number of duplicate rows
        """
        rows_set = set()
        duplicates = 0
        
        for i in range(dataframe.rows_count):
            row_tuple = tuple(
                dataframe.data[col][i]
                for col in dataframe.columns
            )
            
            if row_tuple in rows_set:
                duplicates += 1
            else:
                rows_set.add(row_tuple)
        
        return duplicates
    
    @classmethod
    def check_schema(cls, dataframe: DataFrame, schema: Dict) -> Dict[str, str]:
        """Validate data types.
        
        Args:
            dataframe: DataFrame to check
            schema: Expected column types
            
        Returns:
            Validation errors
        """
        errors = {}
        
        for col, expected_type in schema.items():
            if col not in dataframe.columns:
                errors[col] = "Column missing"
                continue
            
            for val in dataframe.data[col]:
                if val is not None:
                    actual_type = type(val).__name__
                    if actual_type != expected_type:
                        errors[col] = f"Expected {expected_type}, got {actual_type}"
                        break
        
        return errors
