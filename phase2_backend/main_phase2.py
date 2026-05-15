"""
CropPulse Phase 2 Backend - FastAPI Main Application
Complete API for Farmer Dashboard + Marketplace + AI Intelligence
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import os
import logging
import secrets
import hashlib
import json

# Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

# Security
from jose import JWTError, jwt
from passlib.context import CryptContext
from slowapi import Limiter
from slowapi.util import get_remote_address

# External APIs
import httpx
import redis.asyncio as redis

# Environment
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

# App Info
APP_NAME = "CropPulse Phase 2 API"
APP_VERSION = "2.0.0"
API_PREFIX = "/api/v2"

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/croppulse_phase2"
)

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# External APIs
ENAM_API_URL = "https://enam.gov.in/api"  # eNAM API
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "your-key")

# Razorpay
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")

# Rate Limiting
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

# ============================================================================
# DATABASE SETUP
# ============================================================================

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# SECURITY
# ============================================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(authorization: Optional[str] = Header(None)):
    """Validate JWT token and return user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "phone": payload.get("phone")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ============================================================================
# PYDANTIC MODELS (Request/Response)
# ============================================================================

class UserRole(str, Enum):
    FARMER = "farmer"
    TRADER = "trader"
    FPO = "fpo"
    ADMIN = "admin"

# Auth Models
class PhoneOTPRequest(BaseModel):
    phone: str = Field(..., regex=r"^\+91[0-9]{10}$", description="Phone with +91 prefix")

class OTPVerifyRequest(BaseModel):
    phone: str
    otp: str = Field(..., min_length=6, max_length=6)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    phone: str

# Farmer Profile Models
class FarmerProfileRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    state: str  # Tamil Nadu, Punjab, etc.
    district: str
    village: str
    land_size_acres: float = Field(..., gt=0)
    soil_type: str  # Clay, Sandy, Loamy
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    bank_account: Optional[str] = None

class FarmerProfileResponse(FarmerProfileRequest):
    phone: str
    user_id: str
    created_at: datetime
    kyc_status: str = "pending"  # pending, verified, rejected

# Crop Models
class CropRequest(BaseModel):
    name: str  # Rice, Wheat, Cotton
    variety: str  # Basmati, IR64
    area_acres: float = Field(..., gt=0)
    sowing_date: str  # YYYY-MM-DD
    expected_harvest_date: str  # YYYY-MM-DD
    irrigation_type: str  # Rainfed, Irrigated
    fertilizer_used: Optional[str] = None
    pesticide_used: Optional[str] = None

class CropResponse(CropRequest):
    crop_id: str
    user_id: str
    created_at: datetime
    status: str = "growing"  # growing, harvested, sold

# Marketplace Models
class ListingRequest(BaseModel):
    crop_id: str
    quantity_kg: float = Field(..., gt=0)
    quality_grade: str  # Premium, A, B
    price_per_kg: float = Field(..., gt=0)
    description: Optional[str] = None
    available_date: str  # YYYY-MM-DD

class ListingResponse(ListingRequest):
    listing_id: str
    user_id: str
    created_at: datetime
    status: str = "active"  # active, sold, expired
    views: int = 0

class OfferRequest(BaseModel):
    listing_id: str
    offered_price_per_kg: float = Field(..., gt=0)
    quantity_kg: float = Field(..., gt=0)
    pickup_location: str
    message: Optional[str] = None

class OfferResponse(OfferRequest):
    offer_id: str
    created_at: datetime
    status: str = "pending"  # pending, accepted, rejected, expired

# Deal Models
class DealResponse(BaseModel):
    deal_id: str
    listing_id: str
    farmer_id: str
    trader_id: str
    quantity_kg: float
    total_amount: float
    status: str  # active, payment_pending, completed
    created_at: datetime
    payment_id: Optional[str] = None

# AI Models
class CropRecommendationRequest(BaseModel):
    state: str
    soil_type: str
    rainfall_mm: int
    season: str  # Kharif, Rabi, Summer

class CropRecommendationResponse(BaseModel):
    crops: List[Dict[str, Any]]  # [{"name": "Rice", "profit_potential": 85, "water_needed": 1200}]

class DiseaseCheckRequest(BaseModel):
    crop_id: str
    symptoms: List[str]  # ["yellow_leaves", "wilting"]

class DiseaseCheckResponse(BaseModel):
    disease: str
    confidence: float  # 0-1
    treatment: List[str]
    prevention: List[str]

class PriceInsightRequest(BaseModel):
    crop: str
    quantity_kg: float
    state: str

class PriceInsightResponse(BaseModel):
    recommended_price: float
    market_trend: str  # "rising", "stable", "falling"
    nearby_prices: Dict[str, float]  # {"mandi1": 2500, "mandi2": 2400}
    best_selling_time: str

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Phase 2 API for Farmer Dashboard + Marketplace + AI Intelligence"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# HEALTH & INFO
# ============================================================================

@app.get("/health")
@limiter.limit("100/minute")
async def health_check():
    """API health check"""
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/info")
async def app_info():
    """API information"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "api_prefix": API_PREFIX,
        "docs": "/docs",
        "endpoints": {
            "auth": f"{API_PREFIX}/auth",
            "farmer": f"{API_PREFIX}/farmer",
            "marketplace": f"{API_PREFIX}/marketplace",
            "intelligence": f"{API_PREFIX}/intelligence"
        }
    }

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post(f"{API_PREFIX}/auth/request-otp")
@limiter.limit("5/minute")
async def request_otp(request: PhoneOTPRequest):
    """Request OTP for phone number"""
    # In production: Send OTP via Twilio SMS
    # For now: Return mock OTP
    otp = "123456"  # Mock OTP
    
    # Store in Redis (10 min expiry)
    # await redis_client.setex(f"otp:{request.phone}", 600, otp)
    
    return {
        "message": "OTP sent to phone",
        "phone": request.phone,
        "expires_in_seconds": 600
    }

@app.post(f"{API_PREFIX}/auth/verify-otp", response_model=TokenResponse)
@limiter.limit("10/minute")
async def verify_otp(request: OTPVerifyRequest):
    """Verify OTP and return JWT token"""
    # In production: Check OTP from Redis
    # For now: Accept any 6-digit OTP
    
    if len(request.otp) != 6 or not request.otp.isdigit():
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Generate token
    access_token = create_access_token(
        data={"sub": "user_id_here", "phone": request.phone}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": "user_id_here",
        "phone": request.phone
    }

# ============================================================================
# FARMER PROFILE ENDPOINTS
# ============================================================================

@app.post(f"{API_PREFIX}/farmer/profile", response_model=FarmerProfileResponse)
async def create_farmer_profile(
    profile: FarmerProfileRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create farmer profile"""
    # TODO: Save to database
    return {
        **profile.dict(),
        "phone": current_user["phone"],
        "user_id": current_user["user_id"],
        "created_at": datetime.utcnow(),
        "kyc_status": "pending"
    }

@app.get(f"{API_PREFIX}/farmer/profile", response_model=FarmerProfileResponse)
async def get_farmer_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get farmer's profile"""
    # TODO: Fetch from database
    return {
        "name": "Sample Farmer",
        "phone": current_user["phone"],
        "user_id": current_user["user_id"],
        "state": "Tamil Nadu",
        "district": "Tiruppur",
        "village": "Sample Village",
        "land_size_acres": 2.5,
        "soil_type": "Loamy",
        "latitude": 11.4064,
        "longitude": 77.3506,
        "kyc_status": "pending",
        "created_at": datetime.utcnow()
    }

@app.get(f"{API_PREFIX}/farmer/dashboard")
async def get_farmer_dashboard(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get farmer dashboard (main landing)"""
    return {
        "user": {
            "name": "Sample Farmer",
            "phone": current_user["phone"],
            "kyc_status": "pending"
        },
        "weather": {
            "temperature": 32,
            "condition": "Sunny",
            "humidity": 65,
            "rainfall_forecast": "Light rain in 2 days"
        },
        "crops": {
            "total": 2,
            "active": 2,
            "data": [
                {"name": "Rice", "variety": "IR64", "area": 2.5, "status": "growing"}
            ]
        },
        "market_prices": {
            "Rice": 2500,
            "Wheat": 2200,
            "Cotton": 5800
        },
        "active_listings": 1,
        "active_offers": 2,
        "active_deals": 0,
        "wallet_balance": 5000
    }

# ============================================================================
# CROP MANAGEMENT ENDPOINTS
# ============================================================================

@app.post(f"{API_PREFIX}/farmer/crops", response_model=CropResponse)
async def add_crop(
    crop: CropRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add crop for farmer"""
    # TODO: Save to database
    return {
        **crop.dict(),
        "crop_id": "crop_123",
        "user_id": current_user["user_id"],
        "created_at": datetime.utcnow(),
        "status": "growing"
    }

@app.get(f"{API_PREFIX}/farmer/crops")
async def get_farmer_crops(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all farmer's crops"""
    # TODO: Fetch from database
    return {
        "crops": [
            {
                "crop_id": "crop_1",
                "name": "Rice",
                "variety": "IR64",
                "area_acres": 2.5,
                "status": "growing",
                "sowing_date": "2024-06-01",
                "expected_harvest_date": "2024-09-15"
            }
        ],
        "total": 1
    }

# ============================================================================
# MARKETPLACE ENDPOINTS
# ============================================================================

@app.post(f"{API_PREFIX}/marketplace/listings", response_model=ListingResponse)
async def create_listing(
    listing: ListingRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create crop listing (farmer selling)"""
    # TODO: Save to database
    return {
        **listing.dict(),
        "listing_id": "listing_123",
        "user_id": current_user["user_id"],
        "created_at": datetime.utcnow(),
        "status": "active",
        "views": 0
    }

@app.get(f"{API_PREFIX}/marketplace/search")
@limiter.limit("30/minute")
async def search_listings(
    crop: str,
    state: Optional[str] = None,
    quality: Optional[str] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Search marketplace listings (trader view)"""
    # TODO: Query database with filters
    return {
        "search": {
            "crop": crop,
            "state": state,
            "quality": quality
        },
        "results": [
            {
                "listing_id": "listing_1",
                "crop": "Rice",
                "farmer_name": "Sample Farmer",
                "quantity_kg": 1000,
                "quality_grade": "A",
                "price_per_kg": 2400,
                "available_date": "2024-09-20",
                "location": {"state": "Tamil Nadu", "district": "Tiruppur"}
            }
        ],
        "total": 1
    }

@app.post(f"{API_PREFIX}/marketplace/offers", response_model=OfferResponse)
@limiter.limit("30/minute")
async def make_offer(
    offer: OfferRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Trader makes offer on listing"""
    # TODO: Save to database and send SMS to farmer
    return {
        **offer.dict(),
        "offer_id": "offer_123",
        "created_at": datetime.utcnow(),
        "status": "pending"
    }

@app.post(f"{API_PREFIX}/marketplace/deals")
async def accept_offer(
    offer_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Farmer accepts offer → Creates deal"""
    # TODO: Update database and initiate payment
    return {
        "deal_id": "deal_123",
        "status": "payment_pending",
        "message": "Payment link sent to your phone"
    }

# ============================================================================
# INTELLIGENCE ENDPOINTS (AI)
# ============================================================================

@app.post(f"{API_PREFIX}/intelligence/crop-recommendation")
async def recommend_crops(
    request: CropRecommendationRequest,
    db: Session = Depends(get_db)
):
    """AI: Recommend crops based on conditions"""
    # TODO: Call ML model or rule engine
    return {
        "recommendations": {
            "state": request.state,
            "season": request.season
        },
        "crops": [
            {
                "name": "Rice",
                "profit_potential": 85,
                "water_needed_mm": 1200,
                "days_to_harvest": 120,
                "market_demand": "high"
            },
            {
                "name": "Sugarcane",
                "profit_potential": 92,
                "water_needed_mm": 2000,
                "days_to_harvest": 365,
                "market_demand": "medium"
            }
        ]
    }

@app.post(f"{API_PREFIX}/intelligence/disease-check")
async def check_disease(
    request: DiseaseCheckRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI: Predict disease from symptoms"""
    # TODO: Call ML model
    return {
        "crop_id": request.crop_id,
        "disease": "Blast",
        "confidence": 0.87,
        "treatment": [
            "Spray Tricyclazole fungicide",
            "Remove infected plants",
            "Improve drainage"
        ],
        "prevention": [
            "Use disease-resistant varieties",
            "Maintain proper spacing",
            "Avoid excess nitrogen"
        ]
    }

@app.post(f"{API_PREFIX}/intelligence/price-insight")
async def get_price_insight(
    request: PriceInsightRequest
):
    """AI: Suggest best selling price"""
    # TODO: Call price prediction model
    return {
        "crop": request.crop,
        "recommended_price": 2500,
        "market_trend": "rising",
        "nearby_prices": {
            "Mandi A": 2450,
            "Mandi B": 2500,
            "Mandi C": 2550
        },
        "best_selling_time": "Next 3-5 days (before monsoon)",
        "analysis": "Prices rising due to low supply"
    }

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# ============================================================================
# STARTUP EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logging.info("Starting CropPulse Phase 2 API")
    # Connect to Redis
    # Create database tables if not exist

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logging.info("Shutting down CropPulse Phase 2 API")

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
