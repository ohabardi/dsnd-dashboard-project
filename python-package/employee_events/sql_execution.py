import sqlite3
import pandas as pd
from functools import wraps
from pathlib import Path

# Set database path
project_root = Path(__file__).resolve().parents[1]
db_path = project_root / "employee_events.db"

# Decorator to return list-of-tuples (default)
def execute_sql(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        query = func(*args, **kwargs)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query).fetchall()
        return result
    return wrapper

# Decorator to return pandas DataFrame
def execute_sql_df(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        query = func(*args, **kwargs)
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df
    return wrapper
cd python-package
