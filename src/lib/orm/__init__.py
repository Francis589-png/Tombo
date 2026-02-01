"""
TOMBO ORM Library - Object-relational mapping with models and queries
Define models with automatic database mapping and query builder.
"""

from typing import Dict, List, Any, Optional, Callable


class Field:
    """ORM Field definition."""
    
    def __init__(self, field_type: str = "TEXT", primary_key: bool = False, 
                 nullable: bool = True, default=None):
        """Initialize field.
        
        Args:
            field_type: SQL field type
            primary_key: Is this primary key
            nullable: Is field nullable
            default: Default value
        """
        self.field_type = field_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
        self.name = None
    
    def __call__(self, value):
        """Validate field value."""
        return value


class IntField(Field):
    """Integer field."""
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)


class StringField(Field):
    """String field."""
    def __init__(self, max_length: int = 255, **kwargs):
        super().__init__(f"VARCHAR({max_length})", **kwargs)
        self.max_length = max_length


class TextField(Field):
    """Text field."""
    def __init__(self, **kwargs):
        super().__init__("TEXT", **kwargs)


class FloatField(Field):
    """Float field."""
    def __init__(self, **kwargs):
        super().__init__("REAL", **kwargs)


class BoolField(Field):
    """Boolean field."""
    def __init__(self, **kwargs):
        super().__init__("BOOLEAN", **kwargs)


class DateField(Field):
    """Date field."""
    def __init__(self, **kwargs):
        super().__init__("DATE", **kwargs)


class DateTimeField(Field):
    """DateTime field."""
    def __init__(self, **kwargs):
        super().__init__("DATETIME", **kwargs)


class ModelMeta(type):
    """Metaclass for ORM models."""
    
    def __new__(mcs, name, bases, namespace):
        """Create model class."""
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Collect fields
        cls._fields = {}
        for key, value in namespace.items():
            if isinstance(value, Field):
                value.name = key
                cls._fields[key] = value
        
        return cls


class Model(metaclass=ModelMeta):
    """Base ORM model class."""
    
    _table = None
    _db = None
    _fields: Dict[str, Field] = {}
    
    def __init__(self, **kwargs):
        """Initialize model instance."""
        self._data = {}
        for field_name, field in self._fields.items():
            if field_name in kwargs:
                self._data[field_name] = kwargs[field_name]
            elif field.default is not None:
                self._data[field_name] = field.default
        
        for key, value in kwargs.items():
            if key not in self._fields:
                self._data[key] = value
    
    @classmethod
    def set_db(cls, db):
        """Set database connection."""
        cls._db = db
    
    @classmethod
    def table_name(cls) -> str:
        """Get table name."""
        if cls._table:
            return cls._table
        return cls.__name__.lower() + "s"
    
    @classmethod
    def get_schema(cls) -> Dict[str, str]:
        """Get table schema."""
        schema = {}
        for field_name, field in cls._fields.items():
            col_def = field.field_type
            if field.primary_key:
                col_def += " PRIMARY KEY"
            if not field.nullable:
                col_def += " NOT NULL"
            if field.default is not None:
                col_def += f" DEFAULT {field.default}"
            schema[field_name] = col_def
        return schema
    
    @classmethod
    def create_table(cls):
        """Create table in database."""
        if not cls._db:
            raise RuntimeError("No database set for model")
        
        cls._db.create_table(cls.table_name(), cls.get_schema())
    
    @classmethod
    def all(cls) -> List['Model']:
        """Get all records."""
        if not cls._db:
            return []
        
        rows = cls._db.select(cls.table_name())
        return [cls(**row) for row in rows]
    
    @classmethod
    def find(cls, **where) -> List['Model']:
        """Find records by attributes."""
        if not cls._db:
            return []
        
        rows = cls._db.select(cls.table_name(), where=" AND ".join([f"{k} = ?" for k in where.keys()]),
                             params=tuple(where.values()) if where else None)
        return [cls(**row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id_val) -> Optional['Model']:
        """Find by primary key."""
        results = cls.find(id=id_val)
        return results[0] if results else None
    
    def get(self, field_name: str, default=None):
        """Get field value."""
        return self._data.get(field_name, default)
    
    def set(self, field_name: str, value):
        """Set field value."""
        self._data[field_name] = value
        return self
    
    def save(self) -> 'Model':
        """Save model to database."""
        if not self._db:
            raise RuntimeError("No database set for model")
        
        table = self.table_name()
        
        if 'id' in self._data:
            self._db.update(table, self._data, "id = ?", (self._data['id'],))
        else:
            row_id = self._db.insert(table, self._data)
            self._data['id'] = row_id
        
        return self
    
    def delete(self) -> bool:
        """Delete model from database."""
        if not self._db or 'id' not in self._data:
            return False
        
        self._db.delete(self.table_name(), "id = ?", (self._data['id'],))
        return True
    
    def to_dict(self) -> Dict:
        """Convert model to dictionary."""
        return self._data.copy()


class QueryBuilder:
    """SQL query builder for models."""
    
    def __init__(self, model_class: type):
        """Initialize query builder.
        
        Args:
            model_class: Model class to query
        """
        self.model_class = model_class
        self.db = model_class._db
        self._where_clauses = []
        self._where_params = []
        self._select_cols = ["*"]
        self._order_col = None
        self._order_dir = "ASC"
        self._limit_val = None
        self._offset_val = None
    
    def select(self, *cols):
        """Select specific columns."""
        self._select_cols = list(cols) if cols else ["*"]
        return self
    
    def where(self, column: str, operator: str, value):
        """Add WHERE clause."""
        self._where_clauses.append(f"{column} {operator} ?")
        self._where_params.append(value)
        return self
    
    def where_in(self, column: str, values: List):
        """Add WHERE IN clause."""
        placeholders = ", ".join(["?"] * len(values))
        self._where_clauses.append(f"{column} IN ({placeholders})")
        self._where_params.extend(values)
        return self
    
    def order_by(self, column: str, direction: str = "ASC"):
        """Add ORDER BY."""
        self._order_col = column
        self._order_dir = direction
        return self
    
    def limit(self, limit: int):
        """Add LIMIT."""
        self._limit_val = limit
        return self
    
    def offset(self, offset: int):
        """Add OFFSET."""
        self._offset_val = offset
        return self
    
    def execute(self) -> List[Dict]:
        """Execute query."""
        if not self.db:
            return []
        
        cols = ", ".join(self._select_cols)
        query = f"SELECT {cols} FROM {self.model_class.table_name()}"
        
        if self._where_clauses:
            query += " WHERE " + " AND ".join(self._where_clauses)
        
        if self._order_col:
            query += f" ORDER BY {self._order_col} {self._order_dir}"
        
        if self._limit_val:
            query += f" LIMIT {self._limit_val}"
        
        if self._offset_val:
            query += f" OFFSET {self._offset_val}"
        
        return self.db.fetch_dict(query, tuple(self._where_params))
    
    def get(self) -> List['Model']:
        """Execute and return model instances."""
        rows = self.execute()
        return [self.model_class(**row) for row in rows]


def query(model_class: type) -> QueryBuilder:
    """Create query builder for model."""
    return QueryBuilder(model_class)
