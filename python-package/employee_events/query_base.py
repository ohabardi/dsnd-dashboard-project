import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'employee_events.db'

class QueryBase:
    def __init__(self):
        self.name = ""

    def names(self):
        """Return list of table names in the database"""
        with sqlite3.connect(DB_PATH) as conn:
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            df = pd.read_sql(query, conn)
        return df

    def event_counts(self, id):
        """Returns count of positive and negative events for a given ID"""
        self.name = 'employee_events'
        query = f"""
            SELECT event_date,
                   SUM(positive_events) as total_positive,
                   SUM(negative_events) as total_negative
            FROM {self.name}
            WHERE employee_id = ?
            GROUP BY event_date
            ORDER BY event_date;
        """
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql(query, conn, params=(id,))
        return df

    def notes(self, id):
        """Returns notes and note_date for a given ID"""
        self.name = 'notes'
        query = f"""
            SELECT note_date, note
            FROM {self.name}
            WHERE employee_id = ?
            ORDER BY note_date;
        """
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql(query, conn, params=(id,))
        return df
