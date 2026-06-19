from typing import Optional, List, Dict
from app.core.database import (
    read_all,
    read_by_id,
    find_one,
    insert,
    update,
    delete,
    init_table
)
from app.models.user import USER_TABLE, USER_COLUMNS

# Initialize the users table when this file is first imported
# This creates data/users.csv if it doesn't exist yet
# Like CREATE TABLE IF NOT EXISTS in SQL
init_table(USER_TABLE, USER_COLUMNS)


class UserRepository:
    """
    All database operations for the User table.
    
    In MuleSoft terms: this is your Database Connector
    with all your SELECT/INSERT/UPDATE/DELETE operations.
    
    No business logic here — just raw data access.
    Business logic lives in services/ layer.
    """

    def get_all(self) -> List[Dict]:
        """
        Get all users from CSV.
        SQL equivalent: SELECT * FROM users
        """
        return read_all(USER_TABLE)

    def get_by_id(self, user_id: str) -> Optional[Dict]:
        """
        Get one user by ID.
        SQL equivalent: SELECT * FROM users WHERE id = user_id
        """
        return read_by_id(USER_TABLE, user_id)

    def get_by_email(self, email: str) -> Optional[Dict]:
        """
        Get one user by email.
        SQL equivalent: SELECT * FROM users WHERE email = email LIMIT 1
        Used for login — check if email exists
        """
        return find_one(USER_TABLE, "email", email)

    def get_by_role(self, role: str) -> List[Dict]:
        """
        Get all users with a specific role.
        SQL equivalent: SELECT * FROM users WHERE role = role
        Used by admin to list all customers or all admins
        """
        users = read_all(USER_TABLE)
        return [u for u in users if u.get("role") == role]

    def create(self, user_data: Dict) -> Dict:
        """
        Insert a new user into CSV.
        SQL equivalent: INSERT INTO users VALUES (...)
        Returns the created user with auto-generated id and created_at
        """
        return insert(USER_TABLE, user_data)

    def update(self, user_id: str, updated_data: Dict) -> Optional[Dict]:
        """
        Update a user by ID.
        SQL equivalent: UPDATE users SET ... WHERE id = user_id
        Returns updated user or None if not found
        """
        return update(USER_TABLE, user_id, updated_data)

    def delete(self, user_id: str) -> bool:
        """
        Delete a user by ID.
        SQL equivalent: DELETE FROM users WHERE id = user_id
        Returns True if deleted, False if not found
        """
        return delete(USER_TABLE, user_id)

    def email_exists(self, email: str) -> bool:
        """
        Check if an email is already registered.
        SQL equivalent: SELECT COUNT(*) FROM users WHERE email = email
        Used during registration to prevent duplicate accounts
        """
        return self.get_by_email(email) is not None

    def count_all(self) -> int:
        """
        Count total number of users.
        SQL equivalent: SELECT COUNT(*) FROM users
        Used by admin dashboard for stats
        """
        return len(read_all(USER_TABLE))


# Single shared instance — Singleton pattern
# Import this anywhere in the app instead of creating new instances
# Same concept as injecting a @Repository bean in Spring Boot
user_repository = UserRepository()