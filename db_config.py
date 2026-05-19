"""
CropPulse Phase 2 - Smart Database Configuration
Automatically uses SQLite for local development, PostgreSQL for production
Perfect for local testing AND cloud deployment!
"""

import os
import sqlite3
import logging
from contextlib import contextmanager
from datetime import datetime

psycopg2 = None
RealDictCursor = None
HAS_PSYCOPG2 = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# ENVIRONMENT DETECTION
# ============================================================================

def _load_psycopg2():
    """Import psycopg2 lazily so module import never fails on cloud startup."""
    global psycopg2, RealDictCursor, HAS_PSYCOPG2

    if HAS_PSYCOPG2:
        return True

    try:
        import psycopg2 as psycopg2_module
        from psycopg2.extras import RealDictCursor as real_dict_cursor

        psycopg2 = psycopg2_module
        RealDictCursor = real_dict_cursor
        HAS_PSYCOPG2 = True
        return True
    except Exception as exc:
        logger.warning(f"psycopg2 unavailable, falling back to SQLite: {exc}")
        return False


def _load_database_url():
    """Resolve database URL from environment or Streamlit secrets when available."""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return database_url

    try:
        import streamlit as st

        secrets = st.secrets
        if 'DATABASE_URL' in secrets:
            return secrets['DATABASE_URL']
    except Exception:
        pass

    return None


def _get_db_settings():
    """Return runtime database settings without doing fragile work at import time."""
    database_url = _load_database_url()
    is_production = database_url is not None
    db_type = 'postgresql' if (database_url and 'postgres' in database_url) else 'sqlite'
    return database_url, is_production, db_type


def log_db_mode():
    """Log the active database mode after the app has finished importing."""
    _, is_production, db_type = _get_db_settings()
    if is_production:
        logger.info(f"🔵 Running in PRODUCTION mode with {db_type}")
    else:
        logger.info("🟢 Running in LOCAL mode with SQLite")

# ============================================================================
# DATABASE CONNECTION - SMART SELECTION
# ============================================================================

@contextmanager
def get_db_connection():
    """
    Smart context manager that uses SQLite locally, PostgreSQL in production.
    Works seamlessly with both environments!
    """
    database_url, _, db_type = _get_db_settings()

    if db_type == 'postgresql' and database_url and _load_psycopg2():
        yield from _get_postgres_connection()
    else:
        yield from _get_sqlite_connection()


def _get_sqlite_connection():
    """SQLite connection for local development."""
    conn = None
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'croppulse_phase2.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        logger.info("✅ SQLite connection successful")
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"SQLite error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()


def _get_postgres_connection():
    """PostgreSQL connection for production (Railway, Heroku, etc)."""
    if not _load_psycopg2():
        raise ImportError("psycopg2 required for PostgreSQL. Install: pip install psycopg2-binary")
    
    conn = None
    try:
        database_url = _load_database_url()
        if not database_url:
            raise ValueError("DATABASE_URL is not configured for PostgreSQL mode")
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(database_url)
        logger.info("✅ PostgreSQL connection successful")
        yield conn
        conn.commit()
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"PostgreSQL error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()


def test_connection():
    """Test database connection."""
    _, _, db_type = _get_db_settings()
    try:
        with get_db_connection() as conn:
            if db_type == 'sqlite':
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
            else:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
        logger.info(f"✅ {db_type.upper()} connection test successful")
        return True
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        return False


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database():
    """Initialize database with proper schema for SQLite or PostgreSQL."""
    _, _, db_type = _get_db_settings()
    if db_type == 'postgresql' and _load_psycopg2():
        _init_postgres_database()
    else:
        _init_sqlite_database()


def _init_sqlite_database():
    """Initialize SQLite schema."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                role TEXT DEFAULT 'farmer',
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Farmer profiles
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS farmer_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                full_name TEXT,
                state TEXT,
                district TEXT,
                village TEXT,
                latitude REAL,
                longitude REAL,
                land_size_acres REAL,
                soil_type TEXT,
                kyc_status TEXT DEFAULT 'pending',
                kyc_document_url TEXT,
                rating REAL DEFAULT 5.0,
                total_deals INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)
            
            # Trader profiles
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS trader_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                business_name TEXT,
                state TEXT,
                district TEXT,
                gst_number TEXT,
                license_number TEXT,
                rating REAL DEFAULT 5.0,
                total_deals INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)
            
            # Crops
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS crops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER NOT NULL,
                crop_name TEXT,
                variety TEXT,
                area_acres REAL,
                sowing_date DATE,
                expected_harvest_date DATE,
                expected_yield_kg REAL,
                soil_health_score REAL,
                fertilizer_used TEXT,
                pesticide_used TEXT,
                status TEXT DEFAULT 'planning',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id)
            )
            """)
            
            # Listings
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop_id INTEGER NOT NULL,
                farmer_id INTEGER NOT NULL,
                quantity_kg REAL,
                quality_grade TEXT,
                price_per_kg REAL,
                available_from DATE,
                available_until DATE,
                status TEXT DEFAULT 'active',
                view_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (crop_id) REFERENCES crops(id),
                FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id)
            )
            """)
            
            # Offers
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id INTEGER NOT NULL,
                trader_id INTEGER NOT NULL,
                price_per_kg REAL,
                quantity_kg REAL,
                status TEXT DEFAULT 'pending',
                pickup_location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (listing_id) REFERENCES listings(id),
                FOREIGN KEY (trader_id) REFERENCES trader_profiles(id)
            )
            """)
            
            # Deals
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS deals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id INTEGER,
                farmer_id INTEGER NOT NULL,
                trader_id INTEGER NOT NULL,
                quantity_kg REAL,
                price_per_kg REAL,
                total_amount REAL,
                payment_status TEXT DEFAULT 'pending',
                deal_status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (listing_id) REFERENCES listings(id),
                FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id),
                FOREIGN KEY (trader_id) REFERENCES trader_profiles(id)
            )
            """)
            
            # Transactions
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deal_id INTEGER NOT NULL,
                amount REAL,
                payment_type TEXT,
                payment_gateway_id TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (deal_id) REFERENCES deals(id)
            )
            """)
            
            logger.info("✅ SQLite database initialized successfully!")
            
    except sqlite3.Error as e:
        logger.error(f"SQLite initialization error: {str(e)}")
        raise


def _init_postgres_database():
    """Initialize PostgreSQL schema."""
    logger.info("PostgreSQL initialization happens automatically on first connection!")
    logger.info("Tables will be created by db_config_postgresql.py in production")


# ============================================================================
# DATABASE HELPERS - SQLite/PostgreSQL Compatible
# ============================================================================

def get_user_by_phone(phone):
    """Get user by phone number."""
    _, _, db_type = _get_db_settings()
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
            user = cursor.fetchone()
            cursor.close()
            if db_type == 'sqlite':
                return dict(user) if user else None
            return user
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        return None


def create_user(phone, name, role):
    """Create new user and return user ID."""
    _, _, db_type = _get_db_settings()
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (phone, name, role) VALUES (?, ?, ?)",
                (phone, name, role)
            )
            
            if db_type == 'sqlite':
                user_id = cursor.lastrowid
            else:
                cursor.execute("SELECT id FROM users WHERE phone = ?", (phone,))
                user_id = cursor.fetchone()[0]
            
            cursor.close()
            logger.info(f"✅ User created with ID: {user_id}")
            return user_id
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return None


def create_farmer_profile(user_id, full_name, state, district, village, land_size_acres, soil_type):
    """Create farmer profile."""
    _, _, db_type = _get_db_settings()
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO farmer_profiles 
                   (user_id, full_name, state, district, village, land_size_acres, soil_type) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (user_id, full_name, state, district, village, land_size_acres, soil_type)
            )
            
            if db_type == 'sqlite':
                profile_id = cursor.lastrowid
            else:
                cursor.execute("SELECT id FROM farmer_profiles WHERE user_id = ?", (user_id,))
                profile_id = cursor.fetchone()[0]
            
            cursor.close()
            logger.info(f"✅ Farmer profile created with ID: {profile_id}")
            return profile_id
    except Exception as e:
        logger.error(f"Error creating farmer profile: {str(e)}")
        return None


def get_farmer_dashboard(user_id):
    """Get farmer dashboard data."""
    _, _, db_type = _get_db_settings()
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get farmer profile
            cursor.execute(
                "SELECT * FROM farmer_profiles WHERE user_id = ?",
                (user_id,)
            )
            profile = cursor.fetchone()
            
            if not profile:
                return None
            
            # Convert to dict if SQLite
            if db_type == 'sqlite':
                profile = dict(profile)
                farmer_id = profile['id']
            else:
                farmer_id = profile['id']
            
            # Get farmer's crops
            cursor.execute(
                "SELECT * FROM crops WHERE farmer_id = ? ORDER BY created_at DESC",
                (farmer_id,)
            )
            crops = cursor.fetchall()
            if db_type == 'sqlite':
                crops = [dict(c) for c in crops]
            
            # Get farmer's listings
            cursor.execute(
                "SELECT * FROM listings WHERE farmer_id = ? ORDER BY created_at DESC LIMIT 10",
                (farmer_id,)
            )
            listings = cursor.fetchall()
            if db_type == 'sqlite':
                listings = [dict(l) for l in listings]
            
            cursor.close()
            return {
                'profile': profile,
                'crops': crops,
                'listings': listings
            }
    except Exception as e:
        logger.error(f"Error fetching farmer dashboard: {str(e)}")
        return None


# Initialize on module load
if __name__ == "__main__":
    _, _, db_type = _get_db_settings()
    logger.info(f"Testing {db_type.upper()} connection...")
    if test_connection():
        logger.info(f"✅ {db_type.upper()} connection successful!")
        init_database()
    else:
        logger.error(f"❌ Failed to connect to {db_type.upper()}")
