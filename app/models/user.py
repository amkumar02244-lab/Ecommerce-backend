from dataclasses import dataclass
from typing import Optional

# This defines what a User looks like in our "database" (CSV file)
# Think of this as defining your CSV columns
# Every field here = one column in data/users.csv

# In Java terms this is your User POJO:
# public class User {
#     private String id;
#     private String email;
#     ...
# }

@dataclass
class User:
    # Primary key - auto generated UUID
    # CSV column: id
    id: str

    # Basic user info
    # CSV columns: first_name, last_name, email
    first_name: str
    last_name: str
    email: str

    # Hashed password - we NEVER store plain text passwords
    # CSV column: password
    password: str

    # Role controls what the user can access
    # "customer" = normal user
    # "admin"    = full access
    # CSV column: role
    role: str = "customer"

    # Account status
    # True  = can login
    # False = blocked by admin
    # CSV column: is_active
    is_active: bool = True

    # Email verification
    # True  = email verified
    # False = not verified yet
    # CSV column: is_verified
    is_verified: bool = False

    # Optional fields - not required
    # CSV columns: phone, avatar_url
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

    # Timestamps - auto managed by database layer
    # CSV columns: created_at, updated_at
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# This defines the exact columns our CSV file will have
# Order matters! This is the header row of data/users.csv
USER_COLUMNS = [
    "id",
    "first_name",
    "last_name",
    "email",
    "password",
    "role",
    "is_active",
    "is_verified",
    "phone",
    "avatar_url",
    "created_at",
    "updated_at"
]

# Table name constant
# Used by repository layer to know which CSV file to read/write
USER_TABLE = "users"