"""
TOMBO Database Domain - SQL Lite Library

Provides SQLite database operations, queries, and basic ORM functionality.
"""

import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


class Database:
    """SQLite database connection wrapper."""
    
    def __init__(self, path=':memory:'):
        self.path = path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Open database connection."""
        try:
            self.connection = sqlite3.connect(str(self.path))
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def execute(self, sql, params=None):
        """Execute SQL query."""
        if not self.connection:
            self.connect()
        
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return True
        except Exception as e:
            print(f"Error executing SQL: {e}")
            return False
    
    def fetch_one(self, sql, params=None):
        """Execute query and fetch one row."""
        if self.execute(sql, params):
            row = self.cursor.fetchone()
            if row:
                return dict(row)
            return None
        return None
    
    def fetch_all(self, sql, params=None):
        """Execute query and fetch all rows."""
        if self.execute(sql, params):
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        return []
    
    def insert(self, table, data):
        """Insert a row into table."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        if self.execute(sql, list(data.values())):
            self.connection.commit()
            return self.cursor.lastrowid
        return None
    
    def update(self, table, data, where):
        """Update rows in table."""
        set_clause = ', '.join(f"{k}=?" for k in data.keys())
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        
        params = list(data.values())
        if self.execute(sql, params):
            self.connection.commit()
            return self.cursor.rowcount
        return 0
    
    def delete(self, table, where):
        """Delete rows from table."""
        sql = f"DELETE FROM {table} WHERE {where}"
        
        if self.execute(sql):
            self.connection.commit()
            return self.cursor.rowcount
        return 0
    
    def create_table(self, table, columns):
        """Create a table.
        
        columns: dict of {name: 'type [constraints]'}
        Example: {'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT NOT NULL'}
        """
        col_defs = ', '.join(f"{k} {v}" for k, v in columns.items())
        sql = f"CREATE TABLE IF NOT EXISTS {table} ({col_defs})"
        
        return self.execute(sql)
    
    def drop_table(self, table):
        """Drop a table."""
        sql = f"DROP TABLE IF EXISTS {table}"
        return self.execute(sql)
    
    def table_exists(self, table):
        """Check if table exists."""
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.fetch_one(sql, [table])
        return result is not None
    
    def list_tables(self):
        """List all tables in database."""
        sql = "SELECT name FROM sqlite_master WHERE type='table'"
        rows = self.fetch_all(sql)
        return [row['name'] for row in rows]
    
    def count(self, table, where=None):
        """Count rows in table."""
        sql = f"SELECT COUNT(*) as count FROM {table}"
        if where:
            sql += f" WHERE {where}"
        result = self.fetch_one(sql)
        return result['count'] if result else 0


def open_database(path=':memory:'):
    """Open a database connection."""
    db = Database(path)
    db.connect()
    return db


def close_database(db):
    """Close a database connection."""
    if db:
        db.close()


def create_in_memory_db():
    """Create an in-memory SQLite database."""
    return open_database(':memory:')


def create_file_db(path):
    """Create or open a file-based SQLite database."""
    return open_database(path)


def execute_query(db, sql, params=None):
    """Execute a query and return results."""
    return db.fetch_all(sql, params)


def execute_single(db, sql, params=None):
    """Execute a query and return first row."""
    return db.fetch_one(sql, params)


def execute_update(db, sql, params=None):
    """Execute an update/insert/delete and return affected rows."""
    db.execute(sql, params)
    if db.connection:
        db.connection.commit()
        return db.cursor.rowcount
    return 0


def create_table_from_schema(db, table_name, schema):
    """Create table from schema dictionary."""
    return db.create_table(table_name, schema)


def insert_row(db, table, data):
    """Insert a row and return ID."""
    return db.insert(table, data)


def insert_many(db, table, rows):
    """Insert multiple rows."""
    ids = []
    for row in rows:
        row_id = db.insert(table, row)
        if row_id:
            ids.append(row_id)
    return ids


def update_rows(db, table, data, where):
    """Update rows matching condition."""
    return db.update(table, data, where)


def delete_rows(db, table, where):
    """Delete rows matching condition."""
    return db.delete(table, where)


def query_builder(table):
    """Create a simple query builder."""
    return QueryBuilder(table)


class QueryBuilder:
    """Simple SQL query builder."""
    
    def __init__(self, table):
        self.table = table
        self.columns = ['*']
        self.where_clauses = []
        self.order_by = None
        self.limit_val = None
        self.offset_val = None
    
    def select(self, *columns):
        """Specify columns to select."""
        self.columns = list(columns) if columns else ['*']
        return self
    
    def where(self, condition):
        """Add WHERE clause."""
        self.where_clauses.append(condition)
        return self
    
    def order_by(self, column, direction='ASC'):
        """Add ORDER BY clause."""
        self.order_by = f"{column} {direction}"
        return self
    
    def limit(self, n):
        """Add LIMIT clause."""
        self.limit_val = n
        return self
    
    def offset(self, n):
        """Add OFFSET clause."""
        self.offset_val = n
        return self
    
    def build(self):
        """Build the SQL query."""
        columns = ', '.join(self.columns)
        sql = f"SELECT {columns} FROM {self.table}"
        
        if self.where_clauses:
            sql += " WHERE " + " AND ".join(self.where_clauses)
        
        if self.order_by:
            sql += f" ORDER BY {self.order_by}"
        
        if self.limit_val is not None:
            sql += f" LIMIT {self.limit_val}"
        
        if self.offset_val is not None:
            sql += f" OFFSET {self.offset_val}"
        
        return sql


def register(env):
    """Register database functions in the environment."""
    db_funcs = {
        'open_database': open_database,
        'close_database': close_database,
        'create_in_memory_db': create_in_memory_db,
        'create_file_db': create_file_db,
        'execute_query': execute_query,
        'execute_single': execute_single,
        'execute_update': execute_update,
        'insert_row': insert_row,
        'insert_many': insert_many,
        'update_rows': update_rows,
        'delete_rows': delete_rows,
        'query_builder': query_builder,
    }
    
    for name, func in db_funcs.items():
        env.register_function(name, func, is_builtin=True)
