from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tenacity import retry, stop_after_attempt, wait_fixed
import time

# Database URL format
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/devsecops"

# Retry logic using tenacity
@retry(stop=stop_after_attempt(10), wait=wait_fixed(3))
def connect_with_retry():
    print("Attempting DB connection...")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Try a test connection
    conn = engine.connect()
    conn.close()
    
    return engine

# Use the retried connection
engine = connect_with_retry()

# Create session and base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()