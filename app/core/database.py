import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Make sure the data directory exists if using local sqlite
if settings.DATABASE_URL.startswith("sqlite:///"):
    os.makedirs(settings.DATA_DIR, exist_ok=True)

# For SQLite, we need to allow multiple threads to access it
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

# Engine represents the core interface to the database
engine = create_engine(
    settings.DATABASE_URL, connect_args=connect_args
)

# SessionLocal is a class we use to create new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the class that all our ORM models will inherit from
Base = declarative_base()

def get_db():
    """
    Dependency to get a database session for a request.
    Yields the session and ensures it is closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()