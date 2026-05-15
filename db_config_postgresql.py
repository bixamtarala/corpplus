"""
CropPulse Phase 2 - PostgreSQL Database Configuration
Production database connection for Railway/Heroku/Render
Handles user authentication, farmer profiles, crops, listings, trades, etc.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from contextlib import contextmanager
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# DATABASE CONNECTION CONFIGURATION
# ============================================================================

def get_database_url():
    """
    Get PostgreSQL database URL from environment variables.
    Supports:
    - DATABASE_URL (Railway, Heroku standard)
    - POSTGRES_URL (Some platforms)
    - Individual components: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
    """
    # Try standard DATABASE_URL first (Railway, Heroku)
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Ensure it's PostgreSQL (not SQLite)
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    
    # Try POSTGRES_URL
    postgres_url = os.getenv('POSTGRES_URL')
    if postgres_url:
        return postgres_url
    
    # Build from components
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'croppulse')
    
    if password:
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
    else:
        return f"postgresql://{user}@{host}:{port}/{database}"


@contextmanager
def get_db_connection():
    """
    Context manager for PostgreSQL database connections.
    Ensures proper commit/rollback and connection cleanup.
    
    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
    """
    conn = None
    try:
        database_url = get_database_url()
        conn = psycopg2.connect(database_url)
        logger.info("✅ Database connection successful (PostgreSQL)")
        yield conn
        conn.commit()
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()


def test_connection():
    """Test database connection availability."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
        return True
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        return False


# ============================================================================
# DATABASE INITIALIZATION - POSTGRESQL SCHEMA
# ============================================================================

def init_database():
    """
    Initialize PostgreSQL database with all required tables.
    Called once on application startup.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # ===== USERS TABLE (Authentication) =====
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                phone VARCHAR(20) UNIQUE NOT NULL,
                password_hash VARCHAR(255),
                role VARCHAR(50) NOT NULL DEFAULT 'farmer',
                name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            logger.info("✅ users table initialized")
            
            # ===== FARMER PROFILES TABLE =====
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS farmer_profiles (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL UNIQUE,
                full_name VARCHAR(255),
                state VARCHAR(100),
                district VARCHAR(100),
                village VARCHAR(100),
                latitude FLOAT,
                longitude FLOAT,
                land_size_acres FLOAT,
                soil_type VARCHAR(100),
                kyc_status VARCHAR(50) DEFAULT 'pending',
                kyc_document_url VARCHAR(500),
                rating FLOAT DEFAULT 5.0,
                total_deals INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """)
            logger.info("✅ farmer_profiles table initialized")
            
            # ===== TRADER PROFILES TABLE =====
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS trader_profiles (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL UNIQUE,
                business_name VARCHAR(255),
                state VARCHAR(100),
                district VARCHAR(100),
                gst_number VARCHAR(50),
                license_number VARCHAR(100),
                rating FLOAT DEFAULT 5.0,
                total_deals INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """)
            logger.info("✅ trader_profiles table initialized")
            
            # ===== CROPS TABLE (Farm Inventory) =====
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS crops (
                id SERIAL PRIMARY KEY,
                farmer_id INTEGER NOT NULL,
                crop_name VARCHAR(100),
                variety VARCHAR(100),
                area_acres FLOAT,
                sowing_date DATE,
                expected_harvest_date DATE,
                expected_yield_kg FLOAT,
                soil_health_score FLOAT,
                fertilizer_used VARCHAR(255),
                pesticide_used VARCHAR(255),
                status VARCHAR(50) DEFAULT 'planning',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id) ON DELETE CASCADE
            )
            """)
            logger.info("✅ crops table initialized")
            
            # ===== LISTINGS TABLE (Marketplace Items) =====
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id SERIAL PRIMARY KEY,
                crop_id INTEGER NOT NULL,
                farmer_id INTEGER NOT NULL,
                quantity_kg FLOAT,
                quality_grade VARCHAR(50),
                price_per_kg FLOAT,
                available_from DATE,
                available_until DATE,
                status VARCHAR(50) DEFAULT 'active',
                view_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE,
                FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id) ON DELETE CASCADE
            )
            """)
            logger.info("✅ listings table initialized")
            
            # ===== OFFERS TABLE (Trader Bids) =====
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                id SERIAL PRIMARY KEY,
                listing_id INTEGER NOT NULL,
                trader_id INTEGER NOT NULL,
                price_per_kg FLOAT,
                quantity_kg FLOAT,
                status VARCHAR(50) DEFAULT 'pending',
                pickup_location VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE CASCADE,
                FOREIGN KEY (trader_id) REFERENCES trader_profiles(id) ON DELETE CASCADE
            )
            """)
            logger.info("✅ offers table initialized")
            
            # ===== DEALS TABLE (Completed Transactions) =====
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS deals (
                id SERIAL PRIMARY KEY,
                listing_id INTEGER,
                farmer_id INTEGER NOT NULL,
                trader_id INTEGER NOT NULL,
                quantity_kg FLOAT,
                price_per_kg FLOAT,
                total_amount FLOAT,
                payment_status VARCHAR(50) DEFAULT 'pending',
                deal_status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (listing_id) REFERENCES listings(id),
                FOREIGN KEY (farmer_id) REFERENCES farmer_profiles(id) ON DELETE CASCADE,
                FOREIGN KEY (trader_id) REFERENCES trader_profiles(id) ON DELETE CASCADE
            )
            """)
            logger.info("✅ deals table initialized")
            
            # ===== TRANSACTIONS TABLE (Payment Records) =====
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                deal_id INTEGER NOT NULL,
                amount FLOAT,
                payment_type VARCHAR(50),
                payment_gateway_id VARCHAR(255),
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (deal_id) REFERENCES deals(id) ON DELETE CASCADE
            )
            """)
            logger.info("✅ transactions table initialized")
            
            # ===== CREATE INDEXES FOR PERFORMANCE =====
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_listings_status ON listings(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_listings_farmer_id ON listings(farmer_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_offers_trader_id ON offers(trader_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_deals_farmer_id ON deals(farmer_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_deals_trader_id ON deals(trader_id)")
            
            logger.info("✅ Database indexes created")
            logger.info("✅ All PostgreSQL tables initialized successfully!")
            
    except psycopg2.Error as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during initialization: {str(e)}")
        raise


# ============================================================================
# DATABASE QUERY HELPERS (PostgreSQL SYNTAX)
# ============================================================================

def get_user_by_phone(phone):
    """Get user by phone number."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT * FROM users WHERE phone = %s",
                (phone,)
            )
            user = cursor.fetchone()
            cursor.close()
            return user
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        return None


def create_user(phone, name, role):
    """Create new user and return user ID."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO users (phone, name, role) 
                   VALUES (%s, %s, %s) 
                   RETURNING id""",
                (phone, name, role)
            )
            user_id = cursor.fetchone()[0]
            cursor.close()
            logger.info(f"✅ User created with ID: {user_id}")
            return user_id
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return None


def create_farmer_profile(user_id, full_name, state, district, village, land_size_acres, soil_type):
    """Create farmer profile."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO farmer_profiles 
                   (user_id, full_name, state, district, village, land_size_acres, soil_type) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s) 
                   RETURNING id""",
                (user_id, full_name, state, district, village, land_size_acres, soil_type)
            )
            profile_id = cursor.fetchone()[0]
            cursor.close()
            logger.info(f"✅ Farmer profile created with ID: {profile_id}")
            return profile_id
    except Exception as e:
        logger.error(f"Error creating farmer profile: {str(e)}")
        return None


def get_farmer_dashboard(user_id):
    """Get complete farmer dashboard data."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get farmer profile
            cursor.execute(
                "SELECT * FROM farmer_profiles WHERE user_id = %s",
                (user_id,)
            )
            profile = cursor.fetchone()
            
            # Get farmer's crops
            cursor.execute(
                "SELECT * FROM crops WHERE farmer_id = %s ORDER BY created_at DESC",
                (profile['id'] if profile else None,)
            )
            crops = cursor.fetchall()
            
            # Get farmer's listings
            cursor.execute(
                "SELECT * FROM listings WHERE farmer_id = %s ORDER BY created_at DESC LIMIT 10",
                (profile['id'] if profile else None,)
            )
            listings = cursor.fetchall()
            
            cursor.close()
            return {
                'profile': profile,
                'crops': crops,
                'listings': listings
            }
    except Exception as e:
        logger.error(f"Error fetching farmer dashboard: {str(e)}")
        return None


# Initialize database on module import (if running as main)
if __name__ == "__main__":
    logger.info("Testing PostgreSQL connection and initializing database...")
    if test_connection():
        logger.info("✅ PostgreSQL connection successful!")
        init_database()
    else:
        logger.error("❌ Failed to connect to PostgreSQL")
