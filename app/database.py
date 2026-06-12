from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Determine database URL based on environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Default for local Docker Compose
    DATABASE_URL = "postgresql://postgres:postgres@db:5432/students_db"

# For GitHub Actions CI, DATABASE_URL will be set to localhost

# SQLite specific settings
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()"# Database connection module" 
