"""
CropPulse Phase 2 Database Configuration
PostgreSQL connection and session management
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from contextlib import contextmanager

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/croppulse"
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_DEBUG", "false").lower() == "true",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connection before using
    connect_args={
        "connect_timeout": 10,
        "application_name": "croppulse_api",
    }
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    """
    Dependency for FastAPI to provide database session
    Usage: 
        async def get_user(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """Context manager for manual database usage"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database and create tables"""
    from models import Base
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


async def close_db():
    """Close database connection"""
    engine.dispose()
    print("Database connection closed")


# Health check
def check_db_connection():
    """Verify database connection"""
    try:
        with get_db_context() as db:
            db.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
