"""
CropPulse Phase 2 Database Models
SQLAlchemy ORM models for PostgreSQL
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class UserType(enum.Enum):
    """User type enumeration"""
    FARMER = "farmer"
    TRADER = "trader"
    GOVERNMENT = "government"


class OrderStatus(enum.Enum):
    """Order status enumeration"""
    OPEN = "open"
    MATCHED = "matched"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SignalType(enum.Enum):
    """Trading signal type"""
    BUY = "buy"
    SELL = "sell"


# ============================================================================
# USERS & AUTHENTICATION
# ============================================================================

class User(Base):
    """User profile table"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15), unique=True, index=True, nullable=False)  # Primary ID
    name = Column(String(100), nullable=False)
    user_type = Column(String(20), nullable=False)  # farmer, trader, government
    
    # Location
    state = Column(String(50), nullable=False)
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
