"""
CropPulse Phase 2 - SQLAlchemy Database Models
Complete schema: Users, Profiles, Crops, Listings, Offers, Deals, Transactions, Prices, Schemes
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

Base = declarative_base()

# ============================================================================
# ENUMS
# ============================================================================

class UserRole(str, enum.Enum):
    FARMER = "farmer"
    TRADER = "trader"
    FPO = "fpo"
    ADMIN = "admin"

class KYCStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"

class CropStatus(str, enum.Enum):
    GROWING = "growing"
    HARVESTED = "harvested"
    SOLD = "sold"

class ListingStatus(str, enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    EXPIRED = "expired"

class OfferStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"

class DealStatus(str, enum.Enum):
    ACTIVE = "active"
    PAYMENT_PENDING = "payment_pending"
    PAYMENT_COMPLETED = "payment_completed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# ============================================================================
# CORE TABLES
# ============================================================================

class User(Base):
    """User account (Farmer, Trader, FPO)"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    phone = Column(String(20), unique=True, nullable=False, index=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.FARMER)
    
    # Auth
    password_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    farmer_profile = relationship("FarmerProfile", back_populates="user", uselist=False)
    trader_profile = relationship("TraderProfile", back_populates="user", uselist=False)
    crops = relationship("Crop", back_populates="user", cascade="all, delete-orphan")
    listings = relationship("Listing", back_populates="user", cascade="all, delete-orphan")
    offers_made = relationship("Offer", foreign_keys="Offer.trader_id", back_populates="trader")
    deals_as_farmer = relationship("Deal", foreign_keys="Deal.farmer_id", back_populates="farmer")
    deals_as_trader = relationship("Deal", foreign_keys="Deal.trader_id", back_populates="trader")
    transactions = relationship("Transaction", back_populates="user")


class FarmerProfile(Base):
    """Farmer-specific profile information"""
    __tablename__ = "farmer_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    
    # Personal Info
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=True)
    
    # Location
    state = Column(String(50), nullable=False, index=True)
    district = Column(String(50), nullable=False)
    village = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Farm Details
    land_size_acres = Column(Float, nullable=False)
    soil_type = Column(String(50))
    irrigation_type = Column(String(50))
    
    # Banking
    bank_account = Column(String(20), nullable=True)
    bank_ifsc = Column(String(15), nullable=True)
    
    # KYC
    kyc_status = Column(Enum(KYCStatus), default=KYCStatus.PENDING)
    kyc_document_url = Column(String(255), nullable=True)
    
    # Reputation
    total_deals = Column(Integer, default=0)
    successful_deals = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="farmer_profile")


class TraderProfile(Base):
    """Trader-specific profile information"""
    __tablename__ = "trader_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    
    # Business Details
    business_name = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    
    # License & Registration
    business_license = Column(String(50), nullable=True)
    gstin = Column(String(15), nullable=True)
    
    # Reputation
    total_deals = Column(Integer, default=0)
    successful_deals = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="trader_profile")


class Crop(Base):
    """Farmer's crop records"""
    __tablename__ = "crops"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Crop Details
    name = Column(String(50), nullable=False, index=True)
    variety = Column(String(50), nullable=False)
    area_acres = Column(Float, nullable=False)
    
    # Dates
    sowing_date = Column(DateTime, nullable=False)
    expected_harvest_date = Column(DateTime, nullable=False)
    actual_harvest_date = Column(DateTime, nullable=True)
    
    # Farming Details
    irrigation_type = Column(String(50))
    fertilizer_used = Column(String(255), nullable=True)
    pesticide_used = Column(String(255), nullable=True)
    
    # Status
    status = Column(Enum(CropStatus), default=CropStatus.GROWING, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="crops")
    listings = relationship("Listing", back_populates="crop")


class Listing(Base):
    """Crop listing for sale (Marketplace)"""
    __tablename__ = "listings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    crop_id = Column(String(36), ForeignKey("crops.id"), nullable=False)
    
    # Listing Details
    quantity_kg = Column(Float, nullable=False)
    quality_grade = Column(String(20), nullable=False)
    price_per_kg = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    
    # Availability
    available_date = Column(DateTime, nullable=False)
    available_until_date = Column(DateTime, nullable=True)
    
    # Status & Tracking
    status = Column(Enum(ListingStatus), default=ListingStatus.ACTIVE, index=True)
    views = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="listings")
    crop = relationship("Crop", back_populates="listings")
    offers = relationship("Offer", back_populates="listing", cascade="all, delete-orphan")


class Offer(Base):
    """Trader's offer on listing"""
    __tablename__ = "offers"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    listing_id = Column(String(36), ForeignKey("listings.id"), nullable=False, index=True)
    trader_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Offer Details
    offered_price_per_kg = Column(Float, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    pickup_location = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
    
    # Status
    status = Column(Enum(OfferStatus), default=OfferStatus.PENDING, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    accepted_at = Column(DateTime, nullable=True)
    
    # Relationships
    listing = relationship("Listing", back_populates="offers")
    trader = relationship("User", foreign_keys=[trader_id], back_populates="offers_made")


class Deal(Base):
    """Completed deal (Offer Accepted)"""
    __tablename__ = "deals"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    listing_id = Column(String(36), ForeignKey("listings.id"), nullable=False)
    farmer_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    trader_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Deal Details
    quantity_kg = Column(Float, nullable=False)
    price_per_kg = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    # Status
    status = Column(Enum(DealStatus), default=DealStatus.ACTIVE, index=True)
    
    # Payment
    payment_id = Column(String(100), nullable=True)
    payment_method = Column(String(50), nullable=True)
    payment_status = Column(String(50), default="pending")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    payment_completed_at = Column(DateTime, nullable=True)
    delivery_completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    farmer = relationship("User", foreign_keys=[farmer_id], back_populates="deals_as_farmer")
    trader = relationship("User", foreign_keys=[trader_id], back_populates="deals_as_trader")


class Transaction(Base):
    """Payment transaction record"""
    __tablename__ = "transactions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    deal_id = Column(String(36), ForeignKey("deals.id"), nullable=True)
    
    # Transaction Details
    amount = Column(Float, nullable=False)
    type = Column(String(20), nullable=False)
    status = Column(String(50), default="pending")
    
    # External References
    payment_gateway_id = Column(String(100), nullable=True)
    reference_number = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="transactions")


class MarketPrice(Base):
    """Live market prices (from eNAM API)"""
    __tablename__ = "market_prices"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Crop & Location
    crop_name = Column(String(50), nullable=False, index=True)
    mandi_name = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=False, index=True)
    
    # Price Data
    price_per_kg = Column(Float, nullable=False)
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
    volume_traded_kg = Column(Float, nullable=True)
    
    # Timestamp
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)


class GovernmentScheme(Base):
    """Government schemes database"""
    __tablename__ = "government_schemes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Scheme Details
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    ministry = Column(String(100), nullable=False)
    
    # Eligibility
    target_states = Column(JSON)
    crop_types = Column(JSON)
    farmer_size_min_acres = Column(Float, nullable=True)
    farmer_size_max_acres = Column(Float, nullable=True)
    
    # Benefits
    subsidy_amount = Column(Float, nullable=True)
    loan_amount = Column(Float, nullable=True)
    other_benefits = Column(Text, nullable=True)
    
    # Application
    application_deadline = Column(DateTime, nullable=True)
    application_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AlertLog(Base):
    """Alert sent to users"""
    __tablename__ = "alert_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Alert Details
    type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Delivery
    sent_via = Column(String(50))
    status = Column(String(50), default="sent")
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    delivered_at = Column(DateTime, nullable=True)
    district = Column(String(50))
    village = Column(String(100), nullable=False)
    
    # Verification
    kyc_verified = Column(Boolean, default=False)
    kyc_document_id = Column(String(20))  # Aadhaar or PAN
    kyc_verified_at = Column(DateTime)
    
    # Profile
    email = Column(String(100), unique=True, nullable=True)
    device_id = Column(String(50))  # Mobile device ID for push notifications
    language_preference = Column(String(10), default='en')  # en, ta, ka, te, etc.
    
    # Reputation (Phase 2)
    rating = Column(Float, default=5.0)  # 1-5 star rating
    total_trades = Column(Integer, default=0)
    completed_trades = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    orders = relationship("Order", foreign_keys="Order.user_id")
    signals = relationship("TradingSignal", foreign_keys="TradingSignal.user_id")
    trades = relationship("Trade")


class AuthToken(Base):
    """JWT authentication tokens"""
    __tablename__ = "auth_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)


# ============================================================================
# MARKETPLACE
# ============================================================================

class Order(Base):
    """Marketplace orders (buy/sell)"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Order details
    commodity = Column(String(50), nullable=False, index=True)
    order_type = Column(String(10), nullable=False)  # buy or sell
    quantity = Column(Float, nullable=False)  # in kg
    quantity_unit = Column(String(10), default='kg')
    
    # Pricing
    price_per_unit = Column(Float, nullable=False)
    total_value = Column(Float, nullable=False)
    currency = Column(String(3), default='INR')
    
    # Status
    status = Column(String(20), default='open', index=True)  # open, matched, completed, cancelled
    matched_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Location
    state = Column(String(50), nullable=False, index=True)
    mandi = Column(String(100), nullable=False)  # Market location
    
    # Quality
    quality_grade = Column(String(10))  # A, B, C, etc.
    moisture_content = Column(Float)  # % moisture
    impurity_level = Column(Float)  # % impurities
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime)  # Order expiry
    matched_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    matched_user = relationship("User", foreign_keys=[matched_user_id])


class Trade(Base):
    """Completed trade transactions"""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    seller_order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    buyer_order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Trade details
    commodity = Column(String(50), nullable=False)
    quantity = Column(Float, nullable=False)
    agreed_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    # Status
    status = Column(String(20), default='pending')  # pending, confirmed, shipped, delivered, completed
    
    # Negotiation
    initial_seller_price = Column(Float)
    initial_buyer_price = Column(Float)
    negotiation_rounds = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime)
    
    # Relationships
    seller = relationship("User", foreign_keys=[seller_id])
    buyer = relationship("User", foreign_keys=[buyer_id])


# ============================================================================
# PRICES & MARKET DATA
# ============================================================================

class CommodityPrice(Base):
    """Commodity price history"""
    __tablename__ = "commodity_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Commodity info
    commodity = Column(String(50), nullable=False, index=True)
    ticker = Column(String(10))  # RICE, WHEAT, etc.
    
    # Market info
    mandi = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=False, index=True)
    
    # Price data
    price = Column(Float, nullable=False)
    high_price = Column(Float)
    low_price = Column(Float)
    open_price = Column(Float)
    close_price = Column(Float)
    
    # Volume
    volume = Column(Float)  # Trading volume in units
    volume_unit = Column(String(10), default='quintal')
    
    # Technical
    volatility = Column(Float)  # % volatility
    supply = Column(Float)
    demand = Column(Float)
    
    # Metadata
    source = Column(String(20))  # 'enam', 'manual', 'scrape'
    timestamp = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class PriceForecast(Base):
    """AI price forecasts"""
    __tablename__ = "price_forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    commodity = Column(String(50), nullable=False, index=True)
    mandi = Column(String(100), nullable=False)
    
    # Forecast
    forecast_date = Column(DateTime, nullable=False, index=True)
    forecasted_price = Column(Float, nullable=False)
    confidence = Column(Float)  # 0-1 confidence interval
    
    # Model info
    model_type = Column(String(20))  # 'arima', 'prophet', 'lstm'
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================================================
# TRADING SIGNALS (AI ALERTS)
# ============================================================================

class TradingSignal(Base):
    """AI-generated trading signals"""
    __tablename__ = "trading_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Signal details
    commodity = Column(String(50), nullable=False, index=True)
    signal_type = Column(String(10), nullable=False)  # buy or sell
    confidence = Column(Float, nullable=False)  # 0-100
    
    # Reasoning
    reason = Column(Text)  # Why the signal was generated
    price_target = Column(Float)
    
    # Signals components
    volatility_signal = Column(Float)  # Weight in decision
    trend_signal = Column(Float)
    supply_demand_signal = Column(Float)
    weather_signal = Column(Float)  # Weather impact
    
    # Status
    acknowledged = Column(Boolean, default=False)
    acted_upon = Column(Boolean, default=False)  # User took action
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime)  # Signal validity period


# ============================================================================
# FARMER OS
# ============================================================================

class CropPlan(Base):
    """Farmer crop cultivation plans"""
    __tablename__ = "crop_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Crop info
    commodity = Column(String(50), nullable=False)
    variety = Column(String(100))  # Basmati, Sona Masoori, etc.
    area_hectares = Column(Float, nullable=False)
    
    # Dates
    sowing_date = Column(DateTime)
    expected_harvest_date = Column(DateTime)
    actual_harvest_date = Column(DateTime)
    
    # Estimate
    expected_yield_kg = Column(Float)
    estimated_cost = Column(Float)
    estimated_revenue = Column(Float)
    
    # Status
    status = Column(String(20), default='planning')  # planning, active, completed
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CropAlert(Base):
    """Alerts for crop health, disease, best time to sell"""
    __tablename__ = "crop_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_plan_id = Column(Integer, ForeignKey("crop_plans.id"), nullable=False)
    farmer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Alert info
    alert_type = Column(String(50))  # disease, weather, best_time_to_sell
    severity = Column(String(10))  # critical, high, medium, low
    message = Column(Text)
    
    # Recommendation
    recommendation = Column(Text)
    action_items = Column(Text)  # JSON
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    acknowledged_at = Column(DateTime)


# ============================================================================
# NOTIFICATIONS
# ============================================================================

class Notification(Base):
    """Push/SMS notifications"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Notification content
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(20))  # signal, order, trade, alert
    
    # Delivery
    delivery_method = Column(String(20))  # push, sms, whatsapp
    sent_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime)
    
    # Metadata
    related_id = Column(Integer)  # ID of related signal, order, etc.
    action_url = Column(String(500))  # Deep link


# ============================================================================
# ANALYTICS & AUDIT
# ============================================================================

class UserActivity(Base):
    """Audit trail for user actions"""
    __tablename__ = "user_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Action
    action = Column(String(50), nullable=False)  # login, order_created, trade_completed
    resource_type = Column(String(20))  # order, signal, trade
    resource_id = Column(Integer)
    
    # Details
    details = Column(Text)  # JSON for extra metadata
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


# ============================================================================
# INDEXES for Performance
# ============================================================================
# These are automatically created by SQLAlchemy for columns with index=True
# Additional composite indexes can be created with:
# Index('idx_user_commodity', User.id, CommodityPrice.commodity)
