import csv
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from app.core.config import settings

# This is our core CSV database engine
# Every "table" = one CSV file inside the data/ folder
# Example: users table = data/users.csv

def get_table_path(table_name: str) -> str:
    """
    Get the full file path for a table's CSV file.
    Example: get_table_path("users") → "data/users.csv"
    In SQL terms: this is like knowing which table to query
    """
    return os.path.join(settings.DATA_DIR, f"{table_name}.csv")


def init_table(table_name: str, columns: List[str]) -> None:
    """
    Create a CSV file with headers if it doesn't already exist.
    This is like CREATE TABLE IF NOT EXISTS in SQL.

    table_name = "users"
    columns    = ["id", "name", "email", "password", "role", "created_at"]
    """
    path = get_table_path(table_name)

    # Only create the file if it doesn't exist yet
    # We don't want to overwrite existing data
    if not os.path.exists(path):
        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()  # Write the column names as first row
        print(f"[DB] Table created: {table_name}.csv with columns {columns}")
    else:
        print(f"[DB] Table already exists: {table_name}.csv")


def read_all(table_name: str) -> List[Dict]:
    """
    Read all rows from a CSV table and return as a list of dictionaries.
    This is like: SELECT * FROM table_name

    Returns:
    [
        {"id": "1", "name": "John", "email": "john@example.com"},
        {"id": "2", "name": "Jane", "email": "jane@example.com"},
    ]
    """
    path = get_table_path(table_name)

    # If file doesn't exist, return empty list (no records)
    if not os.path.exists(path):
        return []

    with open(path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)  # Convert to list so we can use it freely


def read_by_id(table_name: str, record_id: str) -> Optional[Dict]:
    """
    Find one row by its ID.
    This is like: SELECT * FROM table_name WHERE id = record_id

    Returns the row as a dict, or None if not found.
    """
    rows = read_all(table_name)
    for row in rows:
        if row.get("id") == record_id:
            return row
    return None  # Not found


def find_one(table_name: str, field: str, value: str) -> Optional[Dict]:
    """
    Find one row by any field, not just ID.
    This is like: SELECT * FROM table_name WHERE field = value LIMIT 1

    Example: find_one("users", "email", "john@example.com")
    """
    rows = read_all(table_name)
    for row in rows:
        if row.get(field) == value:
            return row
    return None


def find_many(table_name: str, field: str, value: str) -> List[Dict]:
    """
    Find all rows matching a field/value.
    This is like: SELECT * FROM table_name WHERE field = value

    Example: find_many("orders", "user_id", "abc-123")
    """
    rows = read_all(table_name)
    return [row for row in rows if row.get(field) == value]


def insert(table_name: str, data: Dict) -> Dict:
    """
    Insert a new row into the CSV table.
    This is like: INSERT INTO table_name VALUES (...)

    Automatically adds:
    - id          → unique UUID (like a database auto-generated primary key)
    - created_at  → current timestamp
    """
    path = get_table_path(table_name)

    # Auto-generate ID and timestamp if not provided
    if "id" not in data or not data["id"]:
        data["id"] = str(uuid.uuid4())  # e.g. "f47ac10b-58cc-4372-a567-0e02b2c3d479"

    if "created_at" not in data or not data["created_at"]:
        data["created_at"] = datetime.utcnow().isoformat()

    # Read existing rows to get the column headers
    existing_rows = read_all(table_name)

    # Get columns from the file header
    with open(path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames  # Get header columns

    # Append the new row
    with open(path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writerow(data)

    return data  # Return the inserted record (with id and created_at)


def update(table_name: str, record_id: str, updated_data: Dict) -> Optional[Dict]:
    """
    Update a row by ID.
    This is like: UPDATE table_name SET field=value WHERE id = record_id

    Reads all rows, updates the matching one, rewrites the whole file.
    (CSV doesn't support in-place edits like a real database)
    """
    path = get_table_path(table_name)
    rows = read_all(table_name)
    updated_row = None

    for i, row in enumerate(rows):
        if row.get("id") == record_id:
            rows[i].update(updated_data)        # Merge new data into existing row
            rows[i]["updated_at"] = datetime.utcnow().isoformat()  # Track update time
            updated_row = rows[i]
            break

    if updated_row is None:
        return None  # Record not found

    # Rewrite the entire file with updated data
    # This is the CSV limitation - no partial updates
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    return updated_row


def delete(table_name: str, record_id: str) -> bool:
    """
    Delete a row by ID.
    This is like: DELETE FROM table_name WHERE id = record_id

    Returns True if deleted, False if not found.
    """
    path = get_table_path(table_name)
    rows = read_all(table_name)

    # Keep all rows EXCEPT the one we want to delete
    filtered_rows = [row for row in rows if row.get("id") != record_id]

    if len(filtered_rows) == len(rows):
        return False  # Nothing was removed = record not found

    # Rewrite file without the deleted row
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(filtered_rows)

    return True


def generate_id() -> str:
    """
    Generate a unique UUID string.
    Use this whenever you need a new unique ID anywhere in the app.
    Like a database sequence or auto-increment, but universally unique.
    """
    return str(uuid.uuid4())