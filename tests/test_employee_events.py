import pytest
from pathlib import Path

# Using pathlib create a project_root
# variable set to the absolute path
# for the root of this project
project_root = Path(__file__).resolve().parents[1]

# apply the pytest fixture decorator
# to a `db_path` function
@pytest.fixture
def db_path():
    # Using the `project_root` variable
    # return a pathlib object for the `employee_events.db` file
    return project_root / "python-package" / "employee_events" / "employee_events.db"

# Define a function called `test_db_exists`
# to verify the database file exists
def test_db_exists(db_path):
    # using the pathlib `.is_file` method
    assert db_path.is_file(), f"Database file does not exist at: {db_path}"

@pytest.fixture
def db_conn(db_path):
    from sqlite3 import connect
    return connect(db_path)

@pytest.fixture
def table_names(db_conn):
    name_tuples = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    return [x[0] for x in name_tuples]

# Define test for employee table
def test_employee_table_exists(table_names):
    assert "employee" in table_names, "Missing 'employee' table"

# Define test for team table
def test_team_table_exists(table_names):
    assert "team" in table_names, "Missing 'team' table"

# Define test for employee_events table
def test_employee_events_table_exists(table_names):
    assert "employee_events" in table_names, "Missing 'employee_events' table"

def test_db_exists(db_path):
    assert db_path.is_file(), f"Database file does not exist at: {db_path}"

def test_employee_table_exists(table_names):
    assert "employee" in table_names, "Missing 'employee' table"

def test_team_table_exists(table_names):
    assert "team" in table_names, "Missing 'team' table"

def test_employee_events_table_exists(table_names):
    assert "employee_events" in table_names, "Missing 'employee_events' table"
