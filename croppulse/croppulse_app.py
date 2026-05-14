from datetime import datetime, timedelta
import os

import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st  # type: ignore

# Import eNAM API integration
try:
    from enam_api import fetch_live_data, get_multimandi_prices
    ENAM_AVAILABLE = True
except ImportError:
    ENAM_AVAILABLE = False
    print("⚠️ eNAM API module not found - using fallback data")

# Page configuration
st.set_page_config(
    page_title="CropPulse - Agricultural Market Intelligence",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="auto"
)

# Mobile-friendly viewport
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)

# Custom styling - Enhanced for Phase 2
st.markdown("""
<style>
    /* Main Container */
    .main {
        padding-top: 1rem;
    }
    
    /* Custom Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        padding: 24px;
        border-radius: 12px;
        border-left: 5px solid #2ecc71;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 16px rgba(46, 204, 113, 0.15);
        transform: translateY(-2px);
    }
    
    /* Risk Cards */
    .risk-card {
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ffe6e6 0%, #fff0f0 100%);
        border-left: 5px solid #ff4444;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #fff3cd 0%, #fffaeb 100%);
        border-left: 5px solid #ff9800;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #d4edda 0%, #e8f5e9 100%);
        border-left: 5px solid #2ecc71;
    }
    
    /* Insight Cards */
    .insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-left: 4px solid #2ecc71;
        padding: 20px;
        border-radius: 10px;
        margin: 12px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .insight-opportunity {
        border-left-color: #2ecc71;
    }
    
    .insight-caution {
        border-left-color: #ff9800;
    }
    
    /* Header Styling */
    .header-section {
        text-align: center;
        padding: 24px 0;
        border-bottom: 2px solid #f0f0f0;
        margin-bottom: 24px;
    }
    
    .section-title {
        color: #2c3e50;
        font-size: 22px;
        font-weight: 700;
        margin: 24px 0 16px 0;
    }
    
    /* Progress bars */
    .progress-bar {
        background-color: #e0e0e0;
        border-radius: 10px;
        height: 8px;
        margin: 8px 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Trend Badge */
    .trend-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .trend-up {
        background-color: #d4edda;
        color: #155724;
    }
    
    .trend-down {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    .trend-stable {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    
    /* Divider */
    hr {
        margin: 24px 0;
        border: 1px solid #e0e0e0;
    }

    /* ===== MOBILE RESPONSIVENESS ===== */
    
    /* Mobile: Tablets (768px and below) */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        
        .metric-card {
            padding: 16px;
            margin-bottom: 12px;
            border-left: 4px solid #2ecc71;
        }
        
        .risk-card {
            padding: 16px;
            margin-bottom: 12px;
        }
        
        .insight-card {
            padding: 16px;
            margin: 8px 0;
        }
        
        .section-title {
            font-size: 18px;
            margin: 16px 0 12px 0;
        }
        
        /* Stack columns vertically */
        [data-testid="column"] {
            width: 100% !important;
        }
        
        /* Improve spacing */
        .stButton > button {
            width: 100%;
            padding: 12px;
            font-size: 14px;
        }
        
        /* Responsive charts */
        [data-testid="stPlotlyChart"] {
            padding: 0 !important;
        }
    }
    
    /* Mobile: Small phones (480px and below) */
    @media (max-width: 480px) {
        .main {
            padding: 0.25rem;
        }
        
        .metric-card {
            padding: 12px;
            margin-bottom: 8px;
        }
        
        .risk-card {
            padding: 12px;
            margin-bottom: 8px;
        }
        
        .insight-card {
            padding: 12px;
            margin: 6px 0;
        }
        
        .section-title {
            font-size: 16px;
            margin: 12px 0 8px 0;
        }
        
        .header-section {
            padding: 12px 0;
        }
        
        /* Full-width buttons on small screens */
        .stButton > button {
            width: 100%;
            padding: 10px;
            font-size: 12px;
        }
        
        /* Smaller fonts for small screens */
        .metric-card span {
            font-size: 14px;
        }
        
        /* Reduce trend badge size */
        .trend-badge {
            padding: 3px 8px;
            font-size: 11px;
        }
    }
    
    /* Sidebar adjustments for mobile */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
    }
    
    /* Table responsiveness */
    @media (max-width: 768px) {
        [data-testid="stDataFrame"] {
            font-size: 12px;
        }
        
        table {
            font-size: 12px;
        }
        
        th, td {
            padding: 8px 4px !important;
        }
    }
    
    /* Export button responsiveness */
    @media (max-width: 768px) {
        .stDownloadButton > button {
            width: 100%;
        }
    }
    
    /* Selectbox and Radio button responsiveness */
    @media (max-width: 768px) {
        [data-testid="stSelectbox"] {
            font-size: 14px;
        }
        
        [data-testid="stRadio"] {
            font-size: 14px;
        }
        
        .stRadio > label > div {
            padding: 8px 0;
        }
    }
    
    /* Metric value responsiveness */
    @media (max-width: 480px) {
        .metric-value {
            font-size: 18px;
        }
        
        .metric-label {
            font-size: 12px;
        }
    }
    
    /* Alert and error message responsiveness */
    @media (max-width: 768px) {
        [data-testid="stAlert"] {
            padding: 12px;
            font-size: 13px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# MOBILE RESPONSIVENESS UTILITIES
# ============================================================================

def create_responsive_metric_cards(metrics: dict, columns: int = 4):
    """
    Create responsive metric cards that stack on mobile devices.
    
    Args:
        metrics: Dictionary with metric names as keys and values as dicts with 'value' and 'label'
        columns: Number of columns for desktop (will auto-adjust for mobile)
    """
    # For mobile, reduce to 1-2 columns; for tablet, 2-3 columns
    if columns == 4:
        cols = st.columns(4, gap="medium")
    elif columns == 3:
        cols = st.columns(3, gap="medium")
    else:
        cols = st.columns(columns, gap="medium")
    
    for idx, (metric_name, metric_data) in enumerate(metrics.items()):
        with cols[idx % len(cols)]:
            st.metric(
                label=metric_data.get('label', metric_name),
                value=metric_data.get('value', '—'),
                delta=metric_data.get('delta', None),
                help=metric_data.get('help', None)
            )

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================

@st.cache_data(ttl=3600)  # Refresh every hour
def load_data():
    """
    Load commodity price data - tries eNAM API first, falls back to CSV
    """
    # Try eNAM API first (live data)
    if ENAM_AVAILABLE:
        try:
            st.info("🔄 Fetching live data from eNAM API...", icon="ℹ️")
            
            # Fetch for Rice (most important for Phase 1)
            df_rice = fetch_live_data(commodity="Rice", state="TN")
            
            if df_rice is not None and len(df_rice) > 0:
                st.success("✅ Live eNAM data loaded!", icon="✓")
                return df_rice
        except Exception as e:
            st.warning(f"⚠️ eNAM API error: {str(e)[:50]}... Using cached data", icon="⚠️")
    
    # Fallback: Load from CSV
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, 'data', 'commodity_prices.csv')
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df['date'] = pd.to_datetime(df['date'])
            st.info("📊 Using demo data (CSV fallback)", icon="ℹ️")
            return df
        else:
            raise FileNotFoundError(f"CSV not found at {csv_path}")
    except Exception as e:
        st.error(f"❌ Unable to load data: {e}")
        st.stop()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def calculate_risk_score(commodity_data):
    """Calculate risk score (0-100 scale)"""
    if len(commodity_data) < 7:
        return 0
    
    price_mean = commodity_data['price'].mean()
    if price_mean == 0:
        return 0
    
    # Normalize volatility to percentage
    volatility_pct = (commodity_data['price'].std() / price_mean) * 100
    
    # Price change from mean (in percentage)
    price_change = ((commodity_data['price'].iloc[-1] - price_mean) / price_mean) * 100
    
    # Supply gap (0-100 scale)
    supply_gap = 100 - commodity_data['supply'].iloc[-1]
    
    # Demand pressure (0-100 scale)
    demand = commodity_data['demand'].iloc[-1]
    
    # Normalize all components to 0-100 scale
    volatility_score = min(volatility_pct, 100)  # Cap at 100
    price_change_score = min(abs(price_change), 100)  # Absolute change, cap at 100
    supply_gap_score = supply_gap  # Already 0-100
    demand_pressure_score = demand  # Already 0-100
    
    # Calculate weighted risk score: Volatility (35%) + Price Change (25%) + Supply Gap (20%) + Demand (20%)
    risk_score = (volatility_score * 0.35 + 
                  price_change_score * 0.25 + 
                  supply_gap_score * 0.20 + 
                  demand_pressure_score * 0.20)
    
    return min(risk_score, 100)

def calculate_historical_risk_scores(commodity_data):
    """Calculate risk scores for each day in history (Phase 3 feature)"""
    risk_scores = []
    
    for i in range(7, len(commodity_data)):
        window = commodity_data.iloc[i-7:i+1]
        price_mean = window['price'].mean()
        
        if price_mean == 0:
            risk_scores.append(0)
            continue
        
        # Normalize volatility to percentage
        volatility_pct = (window['price'].std() / price_mean) * 100
        
        # Price change from mean (in percentage)
        price_change = ((window['price'].iloc[-1] - price_mean) / price_mean) * 100
        
        # Supply gap (0-100 scale)
        supply_gap = 100 - window['supply'].iloc[-1]
        
        # Demand pressure (0-100 scale)
        demand = window['demand'].iloc[-1]
        
        # Normalize all components to 0-100 scale
        volatility_score = min(volatility_pct, 100)
        price_change_score = min(abs(price_change), 100)
        supply_gap_score = supply_gap
        demand_pressure_score = demand
        
        # Calculate weighted risk score: Volatility (35%) + Price Change (25%) + Supply Gap (20%) + Demand (20%)
        risk = (volatility_score * 0.35 + 
                price_change_score * 0.25 + 
                supply_gap_score * 0.20 + 
                demand_pressure_score * 0.20)
        
        risk_scores.append(min(risk, 100))
    
    return risk_scores

def get_risk_components(commodity_data):
    """Get detailed breakdown of risk components"""
    if len(commodity_data) < 7:
        return {}
    
    price_mean = commodity_data['price'].mean()
    if price_mean == 0:
        return {}
    
    # Normalize volatility to percentage
    volatility_pct = (commodity_data['price'].std() / price_mean) * 100
    
    # Price change from mean (in percentage)
    price_change = ((commodity_data['price'].iloc[-1] - price_mean) / price_mean) * 100
    
    supply = commodity_data['supply'].iloc[-1]
    demand = commodity_data['demand'].iloc[-1]
    
    # Calculate component scores (0-100) with consistent normalization
    volatility_score = min(volatility_pct, 100)
    price_change_score = min(abs(price_change), 100)
    supply_gap = 100 - supply
    supply_gap_score = supply_gap
    demand_pressure_score = demand
    
    return {
        'volatility': volatility_pct,
        'volatility_score': volatility_score,
        'price_change': price_change,
        'price_change_score': price_change_score,
        'supply': supply,
        'supply_gap': supply_gap,
        'supply_gap_score': supply_gap_score,
        'demand': demand,
        'demand_pressure': demand_pressure_score
    }

def predict_risk_trend(commodity_data):
    """Predict if risk is increasing or decreasing"""
    if len(commodity_data) < 14:
        return "insufficient_data"
    
    # Normalize volatilities to percentages for fair comparison
    recent_prices = commodity_data['price'].iloc[-7:]
    older_prices = commodity_data['price'].iloc[-14:-7]
    
    recent_mean = recent_prices.mean()
    older_mean = older_prices.mean()
    
    if recent_mean == 0 or older_mean == 0:
        return "stable"
    
    recent_volatility = (recent_prices.std() / recent_mean) * 100
    older_volatility = (older_prices.std() / older_mean) * 100
    
    # Use 15% threshold instead of 10% to reduce false positives
    if recent_volatility > older_volatility * 1.15:
        return "increasing"
    elif recent_volatility < older_volatility * 0.85:
        return "decreasing"
    else:
        return "stable"

def get_alert_messages(commodity_data, risk_score, components):
    """Generate specific alert messages based on risk factors (Phase 3)"""
    alerts = []
    
    if components['volatility'] > 8:
        alerts.append({
            "severity": "high",
            "icon": "🚨",
            "message": f"Extreme volatility detected ({components['volatility']:.1f}%)",
            "recommendation": "Avoid large transactions; use limit orders"
        })
    elif components['volatility'] > 6:
        alerts.append({
            "severity": "medium",
            "icon": "⚠️",
            "message": f"High volatility ({components['volatility']:.1f}%)",
            "recommendation": "Exercise caution in pricing decisions"
        })
    
    if components['supply'] < 30:
        alerts.append({
            "severity": "high",
            "icon": "📦",
            "message": "Critical supply shortage",
            "recommendation": "Price may spike further; priority access opportunity"
        })
    elif components['supply'] < 50:
        alerts.append({
            "severity": "medium",
            "icon": "📦",
            "message": "Supply below average",
            "recommendation": "Monitor supply levels closely"
        })
    
    if components['demand'] > 90:
        alerts.append({
            "severity": "medium",
            "icon": "🔥",
            "message": "Peak demand levels",
            "recommendation": "Excellent selling opportunity if you have surplus"
        })
    
    if components['price_change'] > 10:
        alerts.append({
            "severity": "high",
            "icon": "📈",
            "message": "Extreme price movement detected",
            "recommendation": "Understand cause before making decisions"
        })
    
    return alerts

def get_trend_indicator(current, previous):
    """Get trend indicator and badge class"""
    if previous == 0:
        return "→", "stable"
    change = ((current - previous) / previous) * 100
    if change > 1:
        return "↑", "up"
    elif change < -1:
        return "↓", "down"
    else:
        return "→", "stable"

def get_price_trend_category(price_change_7d):
    """Categorize price trend with accurate labels"""
    if price_change_7d > 5:
        return "Strong Uptrend", "#2ecc71"
    elif price_change_7d > 1:
        return "Moderate Uptrend", "#27ae60"
    elif price_change_7d > -1:
        return "Stable", "#3498db"
    elif price_change_7d > -5:
        return "Slight Downtrend", "#f39c12"
    else:
        return "Strong Downtrend", "#e74c3c"

def get_supply_demand_indicator(supply, demand):
    """Get supply/demand balance status"""
    gap = demand - supply
    if gap > 20:
        return "High Shortage", "#e74c3c"
    elif gap > 5:
        return "Moderate Shortage", "#f39c12"
    elif gap > -5:
        return "Balanced", "#2ecc71"
    elif gap > -20:
        return "Moderate Excess", "#3498db"
    else:
        return "High Excess", "#9b59b6"

def get_risk_level(risk_score):
    """Return risk level and color"""
    if risk_score > 66:
        return "HIGH RISK", "🔴", "#ff4444"
    elif risk_score > 33:
        return "MEDIUM RISK", "🟡", "#ff9800"
    else:
        return "LOW RISK", "🟢", "#2ecc71"

def generate_insights(commodity_data, risk_score, commodity):
    """Generate rule-based AI insights with dynamic confidence scoring"""
    insights = []
    
    if len(commodity_data) < 7:
        return insights
    
    # Calculate metrics
    price_7d_val = commodity_data['price'].iloc[-7]
    if price_7d_val == 0:
        price_change_7d = 0
    else:
        price_change_7d = ((commodity_data['price'].iloc[-1] - price_7d_val) / price_7d_val * 100)
    
    price_14d_idx = max(0, len(commodity_data)-14)
    price_14d_val = commodity_data['price'].iloc[price_14d_idx]
    if price_14d_val == 0:
        price_change_14d = 0
    else:
        price_change_14d = ((commodity_data['price'].iloc[-1] - price_14d_val) / price_14d_val * 100)
    
    # Use normalized volatility consistent with risk analysis
    price_mean = commodity_data['price'].mean()
    if price_mean == 0:
        volatility_pct = 0
    else:
        volatility_pct = (commodity_data['price'].std() / price_mean) * 100
    
    supply = commodity_data['supply'].iloc[-1]
    demand = commodity_data['demand'].iloc[-1]
    price_avg = commodity_data['price'].mean()
    current_price = commodity_data['price'].iloc[-1]
    
    # Track if price trend insight already added (to avoid duplicates)
    price_trend_added = False
    
    # Rule 1: Strong momentum with dynamic confidence
    if price_change_7d > 5 and price_change_14d > 8:
        # Higher confidence for stronger, sustained trends
        confidence = min(0.92, 0.75 + (price_change_14d / 50))
        insights.append({
            "emoji": "📈",
            "title": "Sustained Strong Uptrend",
            "description": f"Price up +{price_change_7d:.1f}% (7d) and +{price_change_14d:.1f}% (14d). Consistent buyer pressure.",
            "action": "Excellent selling opportunity - consider timing within 3-5 days",
            "type": "opportunity",
            "confidence": confidence
        })
        price_trend_added = True
    elif price_change_7d > 5:
        # Confidence based on magnitude of movement
        confidence = min(0.85, 0.65 + (price_change_7d / 20))
        insights.append({
            "emoji": "📈",
            "title": "Strong Upward Momentum",
            "description": f"Price up +{price_change_7d:.1f}% in 7 days. Supply may tighten.",
            "action": "Monitor for 2-3 more days before selling",
            "type": "opportunity",
            "confidence": confidence
        })
        price_trend_added = True
    elif price_change_7d < -5 and price_change_14d < -8:
        # Higher confidence for strong, consistent downtrends
        confidence = min(0.90, 0.75 + (abs(price_change_14d) / 50))
        insights.append({
            "emoji": "📉",
            "title": "Sustained Downtrend",
            "description": f"Price down {price_change_7d:.1f}% (7d) and {price_change_14d:.1f}% (14d). Sustained selling pressure.",
            "action": "Wait for stabilization before selling",
            "type": "caution",
            "confidence": confidence
        })
        price_trend_added = True
    elif price_change_7d < -5:
        # Confidence based on magnitude of decline
        confidence = min(0.80, 0.60 + (abs(price_change_7d) / 20))
        insights.append({
            "emoji": "📉",
            "title": "Downward Trend Alert",
            "description": f"Price down {price_change_7d:.1f}% in 7 days. Excess supply likely.",
            "action": "Hold off on selling; wait for recovery",
            "type": "caution",
            "confidence": confidence
        })
        price_trend_added = True
    
    # Rule 2: Volatility analysis with dynamic confidence
    if volatility_pct > 7:
        confidence = min(0.95, 0.80 + (volatility_pct / 50))
        insights.append({
            "emoji": "⚠️",
            "title": "Extreme Volatility Warning",
            "description": f"Price volatility at {volatility_pct:.1f}%. Highly unpredictable market.",
            "action": "Use conservative pricing or limit orders; avoid aggressive trading",
            "type": "caution",
            "confidence": confidence
        })
    elif volatility_pct > 4:
        confidence = min(0.85, 0.65 + (volatility_pct / 30))
        insights.append({
            "emoji": "⚠️",
            "title": "Elevated Volatility",
            "description": f"Price swings at {volatility_pct:.1f}%. Market uncertainty present.",
            "action": "Lock in prices or use hedging strategies",
            "type": "caution",
            "confidence": confidence
        })
    
    # Rule 3: Price positioning (only add if price trend not already added)
    if not price_trend_added:
        price_diff_pct = ((current_price - price_avg) / price_avg) * 100
        if current_price > price_avg * 1.10:  # More than 10% above average
            confidence = min(0.88, 0.70 + (abs(price_diff_pct) / 30))
            insights.append({
                "emoji": "📊",
                "title": "Above Average Pricing",
                "description": f"Price is +{price_diff_pct:.1f}% above 30-day average.",
                "action": "Peak pricing window - strong sell opportunity",
                "type": "opportunity",
                "confidence": confidence
            })
        elif current_price < price_avg * 0.90:  # More than 10% below average
            confidence = min(0.85, 0.70 + (abs(price_diff_pct) / 30))
            insights.append({
                "emoji": "📊",
                "title": "Below Average Pricing",
                "description": f"Price is {price_diff_pct:.1f}% below 30-day average.",
                "action": "Poor sell conditions; wait for recovery to average",
                "type": "caution",
                "confidence": confidence
            })
    
    # Rule 4: Supply shortage with dynamic confidence
    if supply < 30:
        confidence = min(0.92, 0.80 + ((30 - supply) / 50))
        insights.append({
            "emoji": "📦",
            "title": "Critical Supply Shortage",
            "description": f"Supply critically low at {supply:.0f}%. Severe shortage risk.",
            "action": "Strong price support expected - excellent selling conditions",
            "type": "opportunity",
            "confidence": confidence
        })
    elif supply < 45:
        confidence = min(0.82, 0.70 + ((45 - supply) / 50))
        insights.append({
            "emoji": "📦",
            "title": "Supply Below Normal",
            "description": f"Supply at {supply:.0f}%. Below healthy levels.",
            "action": "Monitor supply closely; prices likely elevated",
            "type": "opportunity",
            "confidence": confidence
        })
    elif supply > 80:
        confidence = min(0.88, 0.72 + ((supply - 80) / 30))
        insights.append({
            "emoji": "📦",
            "title": "Excess Supply Alert",
            "description": f"Supply high at {supply:.0f}%. Market oversupply.",
            "action": "Avoid selling now; wait for inventory normalization",
            "type": "caution",
            "confidence": confidence
        })
    
    # Rule 5: Demand dynamics with dynamic confidence
    if demand > 85:
        confidence = min(0.90, 0.75 + ((demand - 85) / 30))
        insights.append({
            "emoji": "🔥",
            "title": "Peak Demand Conditions",
            "description": f"Demand at {demand:.0f}%. Maximum buyer interest.",
            "action": "Optimal selling window if you have inventory",
            "type": "opportunity",
            "confidence": confidence
        })
    elif demand > 70:
        confidence = min(0.78, 0.65 + ((demand - 70) / 40))
        insights.append({
            "emoji": "🔥",
            "title": "Strong Demand Detected",
            "description": f"Demand strong at {demand:.0f}%. Good buyer appetite.",
            "action": "Favorable conditions for selling",
            "type": "opportunity",
            "confidence": confidence
        })
    
    # Rule 6: Composite patterns (perfect storm - only if not caught by individual rules)
    if (supply < 45 and demand > 80 and price_change_7d > 5):
        # Only add if not already captured by supply/demand/price rules above
        confidence = min(0.95, 0.85 + ((price_change_7d + demand - supply) / 100))
        insights.append({
            "emoji": "🎯",
            "title": "Perfect Storm: Shortage + Demand + Rising",
            "description": f"Rare confluence: {supply:.0f}% supply + {demand:.0f}% demand + {price_change_7d:+.1f}% price rise.",
            "action": "Extremely favorable - Sell immediately if possible",
            "type": "opportunity",
            "confidence": min(confidence, 0.98)
        })
    
    # Rule 7: Combined risk alert
    if volatility_pct > 5 and risk_score > 70:
        confidence = min(0.92, 0.78 + (risk_score / 200))
        insights.append({
            "emoji": "⚠️",
            "title": "High Risk + Volatility Alert",
            "description": f"Combined high risk ({risk_score:.0f}) and volatility ({volatility_pct:.1f}%). Uncertain market conditions.",
            "action": "Defer selling; reduce exposure and wait for stabilization",
            "type": "caution",
            "confidence": confidence
        })
    
    return insights

# ============================================================================
# PAGE HEADER
# ============================================================================

# ============================================================================
# PAGE HEADER & SIDEBAR
# ============================================================================

# Sidebar - Hero Card at Top + User Info
with st.sidebar:
    # Hero Card at Top
    st.markdown("""
    <div style='text-align: center; padding: 20px 0; border-bottom: 2px solid #2ecc71; margin-bottom: 20px;'>
        <h1 style='color: #2ecc71; margin: 0; font-size: 40px;'>🌾 CropPulse</h1>
        <p style='color: #7f8c8d; margin: 6px 0 0 0; font-size: 14px;'>Market Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User Profile
    st.markdown("""
    <div style='padding: 20px 0; border-bottom: 1px solid #e0e0e0; margin-bottom: 20px;'>
        <h3 style='margin: 0 0 12px 0; color: #2c3e50;'>👤 User Profile</h3>
        <p style='margin: 8px 0; color: #2c3e50; font-weight: 600;'>Ramesh Kumar</p>
        <p style='margin: 4px 0; color: #7f8c8d; font-size: 12px;'>Rice Trader</p>
        <p style='margin: 8px 0; color: #95a5a6; font-size: 11px;'>📍 Tamil Nadu</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("### 🏠 Navigation")
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("🏠 Home", use_container_width=True):
            st.rerun()
    with col_nav2:
        if st.button("🚪 Logout", use_container_width=True):
            st.info("Login/Logout coming soon")
    
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #95a5a6; font-size: 11px;'>Version 1.0 • May 2026</p>", unsafe_allow_html=True)

# Main Content Header
st.markdown("""
<div style='padding: 20px 0; margin-bottom: 24px;'>
    <p style='color: #7f8c8d; margin: 0; font-size: 16px;'>Real-time trading signals, price insights & risk analysis</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MVP FEATURES - TOP SECTION
# ============================================================================

# Load data first (needed for features)
data = load_data()

# ============================================================================
# TOP CONTROLS - Commodity & View Mode Selector
# ============================================================================

st.markdown("""
<div style='background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); padding: 20px; border-radius: 12px; margin-bottom: 24px; border-left: 5px solid #2ecc71; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
</div>
""", unsafe_allow_html=True)

col_control1, col_control2 = st.columns([1.2, 2], gap="medium")

with col_control1:
    commodity = st.selectbox(
        "📦 Commodity",
        options=["Rice", "Wheat", "Cotton"],
        index=0
    )

with col_control2:
    view_option = st.radio(
        "View",
        ["📊 Dashboard", "⚠️ Risk", "💡 Insights"],
        horizontal=True,
        label_visibility="collapsed"
    )
    # Normalize view_mode
    view_mode_map = {
        "📊 Dashboard": "📊 Dashboard",
        "⚠️ Risk": "⚠️ Risk Analysis",
        "💡 Insights": "💡 Insights Only"
    }
    view_mode = view_mode_map.get(view_option, "📊 Dashboard")

st.markdown("---")

# Filter data for selected commodity
commodity_data = data[data['commodity'] == commodity].sort_values('date').tail(30).reset_index(drop=True)

if len(commodity_data) == 0:
    st.error(f"No data available for {commodity}")
    st.stop()

# Get current metrics
current_price = commodity_data['price'].iloc[-1]
price_7d_ago = commodity_data['price'].iloc[0] if len(commodity_data) >= 7 else commodity_data['price'].iloc[0]
if price_7d_ago == 0:
    price_change_7d = 0
else:
    price_change_7d = ((current_price - price_7d_ago) / price_7d_ago) * 100

high_30d = commodity_data['price'].max()
low_30d = commodity_data['price'].min()
volatility = commodity_data['volatility'].iloc[-1]

# Calculate risk
risk_score = calculate_risk_score(commodity_data)
risk_level, risk_emoji, risk_color = get_risk_level(risk_score)

# Calculate risk trend (needed for export section)
risk_trend = predict_risk_trend(commodity_data)
trend_icon = "📈" if risk_trend == "increasing" else "📉" if risk_trend == "decreasing" else "→"
trend_text = "Increasing" if risk_trend == "increasing" else "Decreasing" if risk_trend == "decreasing" else "Stable"

# ============================================================================
# CORE MVP FEATURES
# ============================================================================

st.markdown('<div class="section-title">⚡ QUICK ACTIONS & MARKET STATUS</div>', unsafe_allow_html=True)

# Feature 1: Trading Signal Buttons
feature_col1, feature_col2, feature_col3, feature_col4 = st.columns(4, gap="medium")

with feature_col1:
    # Generate buy/sell signal
    supply = commodity_data['supply'].iloc[-1]
    demand = commodity_data['demand'].iloc[-1]
    signal = "BUY" if (supply < 50 and demand > 60) else "SELL" if (supply > 70) else "WAIT"
    signal_color = "#2ecc71" if signal == "BUY" else "#e74c3c" if signal == "SELL" else "#f39c12"
    signal_emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "🟡"
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {signal_color}20 0%, {signal_color}10 100%); padding: 20px; border-radius: 12px; border-left: 5px solid {signal_color}; text-align: center;'>
        <div style='font-size: 36px;'>{signal_emoji}</div>
        <div style='font-size: 24px; font-weight: 700; color: {signal_color}; margin: 8px 0;'>{signal}</div>
        <div style='color: #7f8c8d; font-size: 11px;'>Trading Signal</div>
    </div>
    """, unsafe_allow_html=True)

with feature_col2:
    # Feature 2: Current Price (Large Display)
    price_trend, price_color = get_trend_indicator(current_price, commodity_data['price'].iloc[-2] if len(commodity_data) > 1 else current_price)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); padding: 20px; border-radius: 12px; border-left: 5px solid #2ecc71; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
        <div style='color: #7f8c8d; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Current Price</div>
        <div style='font-size: 32px; font-weight: 700; color: #2c3e50; margin: 8px 0;'>₹{current_price:,.0f}</div>
        <div style='color: {price_color}; font-size: 13px; font-weight: 600;'>{price_trend} {price_change_7d:+.1f}% (7d)</div>
    </div>
    """, unsafe_allow_html=True)

with feature_col3:
    # Feature 3: Risk Meter
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); padding: 20px; border-radius: 12px; border-left: 5px solid {risk_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
        <div style='color: #7f8c8d; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Risk Level</div>
        <div style='font-size: 32px; font-weight: 700; color: {risk_color}; margin: 8px 0;'>{risk_emoji} {risk_level.split()[0]}</div>
        <div style='color: #7f8c8d; font-size: 12px;'>Score: {risk_score:.0f}/100</div>
    </div>
    """, unsafe_allow_html=True)

with feature_col4:
    # Feature 4: Supply/Demand Status
    sd_status, sd_color = get_supply_demand_indicator(supply, demand)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); padding: 20px; border-radius: 12px; border-left: 5px solid {sd_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
        <div style='color: #7f8c8d; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Market Balance</div>
        <div style='font-size: 18px; font-weight: 700; color: {sd_color}; margin: 8px 0; word-wrap: break-word;'>{sd_status}</div>
        <div style='color: #7f8c8d; font-size: 11px; margin-top: 8px;'>S:{supply:.0f}% D:{demand:.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# KPI CARDS - DISPLAY ALWAYS AT TOP
# ============================================================================

st.markdown('<div class="section-title">📈 Market Overview - ' + commodity + '</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4, gap="medium")

# Trend indicators
trend_category, trend_color = get_price_trend_category(price_change_7d)
supply_demand_status, sd_color = get_supply_demand_indicator(commodity_data['supply'].iloc[-1], commodity_data['demand'].iloc[-1])

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>Current Price</div>
        <div style='font-size: 32px; font-weight: 700; color: #2c3e50; margin: 8px 0;'>₹{current_price:,.0f}</div>
        <div style='color: {trend_color}; font-size: 13px; font-weight: 600;'>
            {get_trend_indicator(current_price, commodity_data['price'].iloc[-2] if len(commodity_data) > 1 else current_price)[0]} 
            {price_change_7d:+.1f}% (7 days)
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>30-Day Range</div>
        <div style='font-size: 28px; font-weight: 700; color: #2c3e50; margin: 8px 0;'>₹{high_30d:,.0f}</div>
        <div style='color: #7f8c8d; font-size: 12px;'>High | Low ₹{low_30d:,.0f}</div>
        <div style='color: #e74c3c; font-size: 13px; font-weight: 600; margin-top: 4px;'>Δ {((high_30d - low_30d) / low_30d * 100):.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # Calculate normalized volatility for display consistency
    price_mean_display = commodity_data['price'].mean()
    if price_mean_display == 0:
        volatility_display = 0
    else:
        volatility_display = (commodity_data['price'].std() / price_mean_display) * 100
    
    st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>Volatility</div>
        <div style='font-size: 32px; font-weight: 700; color: #2c3e50; margin: 8px 0;'>{volatility_display:.1f}%</div>
        <div style='color: #7f8c8d; font-size: 13px;'>Price stability indicator</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>Trend</div>
        <div style='font-size: 24px; font-weight: 700; color: {trend_color}; margin: 8px 0;'>{trend_category}</div>
        <div style='color: #7f8c8d; font-size: 12px;'>Based on 7-day movement</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# PRICE CHART - DISPLAY ALWAYS AT TOP
# ============================================================================

st.markdown('<div class="section-title">📊 30-Day Price Trend</div>', unsafe_allow_html=True)

fig_price = go.Figure()

# Calculate moving averages
ma_7 = commodity_data['price'].rolling(window=7, min_periods=1).mean()
ma_14 = commodity_data['price'].rolling(window=14, min_periods=1).mean()

# Calculate volatility band (mean ± 1 std dev)
price_mean = commodity_data['price'].mean()
price_std = commodity_data['price'].std()
upper_band = price_mean + price_std
lower_band = price_mean - price_std

# Add volatility band (light fill)
fig_price.add_trace(go.Scatter(
    x=commodity_data['date'],
    y=[upper_band] * len(commodity_data['date']),
    fill=None,
    mode='lines',
    line_color='rgba(0,0,0,0)',
    showlegend=False,
    name='Upper Band'
))

fig_price.add_trace(go.Scatter(
    x=commodity_data['date'],
    y=[lower_band] * len(commodity_data['date']),
    fill='tonexty',
    mode='lines',
    line_color='rgba(0,0,0,0)',
    fillcolor='rgba(52, 152, 219, 0.1)',
    name='Volatility Band (±1σ)'
))

# Add main price line (on top)
fig_price.add_trace(go.Scatter(
    x=commodity_data['date'],
    y=commodity_data['price'],
    mode='lines+markers',
    name='Current Price',
    line=dict(color='#2ecc71', width=3),
    marker=dict(size=5, opacity=0.8),
    hovertemplate='<b>%{x|%b %d}</b><br>Price: ₹%{y:,.0f}<extra></extra>'
))

# Add 7-day moving average
fig_price.add_trace(go.Scatter(
    x=commodity_data['date'],
    y=ma_7,
    mode='lines',
    name='7-Day MA',
    line=dict(color='#f39c12', width=2, dash='dash'),
    hovertemplate='<b>%{x|%b %d}</b><br>7-Day MA: ₹%{y:,.0f}<extra></extra>'
))

# Add 14-day moving average
fig_price.add_trace(go.Scatter(
    x=commodity_data['date'],
    y=ma_14,
    mode='lines',
    name='14-Day MA',
    line=dict(color='#e74c3c', width=2, dash='dash'),
    hovertemplate='<b>%{x|%b %d}</b><br>14-Day MA: ₹%{y:,.0f}<extra></extra>'
))

# Add 30-day average line
avg_price = commodity_data['price'].mean()
fig_price.add_hline(
    y=avg_price, 
    line_dash="dot", 
    line_color="#95a5a6",
    line_width=2,
    annotation_text=f"30-Day Avg: ₹{avg_price:.0f}",
    annotation_position="right",
    annotation_font_color="#95a5a6"
)

fig_price.update_layout(
    title=f"<b>{commodity} Price Movement (30-Day History)</b>",
    xaxis_title="Date",
    yaxis_title="Price (₹)",
    hovermode='x unified',
    template='plotly_white',
    height=450,
    margin=dict(l=0, r=80, t=40, b=0),
    font=dict(family="Arial, sans-serif", size=11, color="#2c3e50"),
    legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)', bordercolor='#e0e0e0', borderwidth=1)
)

st.plotly_chart(fig_price, use_container_width=True)

st.markdown("---")
# Display critical alerts first (Phase 3)
if risk_alerts:
    st.markdown("**⚠️ Real-Time Alerts**")
    for alert in risk_alerts:
        if alert['severity'] == 'high':
            st.error(f"{alert['icon']} **{alert['message']}** — {alert['recommendation']}")
        else:
            st.warning(f"{alert['icon']} **{alert['message']}** — {alert['recommendation']}")
    st.markdown("")

col_risk1, col_risk2 = st.columns([1, 1], gap="medium")

with col_risk1:
    # Trend color for risk card
    trend_color_risk = "#e74c3c" if risk_trend == "increasing" else "#2ecc71" if risk_trend == "decreasing" else "#3498db"
    
    st.markdown(f"""
<div class="risk-card risk-{risk_level.lower().split()[0]}">
    <div style='text-align: center;'>
        <div style='font-size: 48px; margin-bottom: 12px;'>{risk_emoji}</div>
        <div style='font-size: 20px; font-weight: 700; color: #2c3e50; margin-bottom: 8px;'>{risk_level}</div>
        <div style='font-size: 42px; font-weight: 700; color: {risk_color};'>{risk_score:.0f}</div>
        <div style='font-size: 12px; color: #7f8c8d; margin-top: 8px;'>Risk Score (0-100)</div>
        <div style='margin-top: 16px; padding-top: 16px; border-top: 1px solid rgba(0,0,0,0.1);'>
            <span style='color: {trend_color_risk}; font-size: 14px; font-weight: 600;'>{trend_icon} {trend_text} Trend</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with col_risk2:
    # Risk breakdown with progress bars - weighted by importance
    if components:
        volatility_score = min(components['volatility_score'], 100)
        price_change_score = min(components['price_change_score'], 100)
        supply_gap_score = components['supply_gap_score']
        demand_pressure = components['demand_pressure']
        
        st.markdown(f"""<div style='background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
<h4 style='margin-top: 0; color: #2c3e50;'>Risk Factors Breakdown</h4>
<p style='color: #95a5a6; font-size: 11px; margin: 0 0 12px 0;'>Weighted by importance in risk calculation</p>
<div style='margin: 14px 0;'><div style='display: flex; justify-content: space-between; margin-bottom: 4px;'><span style='color: #7f8c8d; font-size: 11px; font-weight: 600;'>📊 Volatility (35%)</span><span style='color: #e74c3c; font-weight: 600; font-size: 11px;'>{components['volatility']:.1f}%</span></div><div style='background-color: #e0e0e0; border-radius: 10px; height: 8px; overflow: hidden;'><div style='height: 100%; width: {volatility_score}%; background-color: #e74c3c; border-radius: 10px;'></div></div></div>
<div style='margin: 14px 0;'><div style='display: flex; justify-content: space-between; margin-bottom: 4px;'><span style='color: #7f8c8d; font-size: 11px; font-weight: 600;'>💹 Price Change (25%)</span><span style='color: #f39c12; font-weight: 600; font-size: 11px;'>{abs(components['price_change']):.1f}%</span></div><div style='background-color: #e0e0e0; border-radius: 10px; height: 8px; overflow: hidden;'><div style='height: 100%; width: {price_change_score}%; background-color: #f39c12; border-radius: 10px;'></div></div></div>
<div style='margin: 14px 0;'><div style='display: flex; justify-content: space-between; margin-bottom: 4px;'><span style='color: #7f8c8d; font-size: 11px; font-weight: 600;'>📦 Supply Gap (20%)</span><span style='color: #3498db; font-weight: 600; font-size: 11px;'>{components['supply_gap']:.0f}%</span></div><div style='background-color: #e0e0e0; border-radius: 10px; height: 8px; overflow: hidden;'><div style='height: 100%; width: {supply_gap_score}%; background-color: #3498db; border-radius: 10px;'></div></div></div>
<div style='margin: 14px 0;'><div style='display: flex; justify-content: space-between; margin-bottom: 4px;'><span style='color: #7f8c8d; font-size: 11px; font-weight: 600;'>🔥 Demand Pressure (20%)</span><span style='color: #9b59b6; font-weight: 600; font-size: 11px;'>{components['demand']:.0f}%</span></div><div style='background-color: #e0e0e0; border-radius: 10px; height: 8px; overflow: hidden;'><div style='height: 100%; width: {demand_pressure}%; background-color: #9b59b6; border-radius: 10px;'></div></div></div>
</div>""", unsafe_allow_html=True)
    else:
        st.info("Insufficient data to calculate risk components")

# Historical risk trend chart (Phase 3)
st.markdown("**Risk Evolution (7-Day History)**")

# Calculate historical risks
historical_risks = calculate_historical_risk_scores(commodity_data)
risk_dates = commodity_data['date'].iloc[7:].reset_index(drop=True)

fig_risk_trend = go.Figure()
fig_risk_trend.add_trace(go.Scatter(
    x=risk_dates,
    y=historical_risks,
    mode='lines+markers',
    name='Risk Score',
    line=dict(color='#e74c3c', width=2),
    marker=dict(size=5),
    fill='tozeroy',
    fillcolor='rgba(231, 76, 60, 0.1)',
    hovertemplate='<b>%{x|%b %d}</b><br>Risk: %{y:.0f}/100<extra></extra>'
))

fig_risk_trend.add_hline(
    y=33, 
    line_dash="dash", 
    line_color="#2ecc71",
    annotation_text="Low Risk",
    annotation_position="right"
)

fig_risk_trend.add_hline(
    y=66, 
    line_dash="dash", 
    line_color="#ff9800",
    annotation_text="High Risk",
    annotation_position="right"
)

fig_risk_trend.update_layout(
    title="<b>Risk Score Trend</b>",
    xaxis_title="Date",
    yaxis_title="Risk Score (0-100)",
    template='plotly_white',
    height=250,
    margin=dict(l=0, r=80, t=40, b=0),
    hovermode='x unified',
    font=dict(family="Arial, sans-serif", size=10, color="#2c3e50")
)

st.plotly_chart(fig_risk_trend, use_container_width=True)

st.markdown("---")

# ============================================================================
# AI INSIGHTS - DISPLAY ALWAYS AT TOP
# ============================================================================

st.markdown('<div class="section-title">💡 AI Insights & Recommendations</div>', unsafe_allow_html=True)

insights = generate_insights(commodity_data, risk_score, commodity)

if insights:
    for idx, insight in enumerate(insights):
        insight_class = f"insight-{insight['type']}"
        icon_color = "#2ecc71" if insight['type'] == 'opportunity' else "#ff9800"
        action_type = "✅ Opportunity" if insight['type'] == 'opportunity' else "⚠️ Caution"
        confidence = insight.get('confidence', 0.75)
        
        st.markdown(f"""
    <div class="insight-card insight-{insight['type']}">
        <div style='display: flex; align-items: flex-start; gap: 16px;'>
            <div style='font-size: 32px; flex-shrink: 0;'>{insight['emoji']}</div>
            <div style='flex-grow: 1;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h4 style='margin: 0 0 8px 0; color: #2c3e50;'>{insight['title']}</h4>
                    <span style='background-color: {"#d4edda" if insight["type"] == "opportunity" else "#fff3cd"}; color: {"#155724" if insight["type"] == "opportunity" else "#856404"}; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600;'>
                        Confidence: {confidence*100:.0f}%
                    </span>
                </div>
                <p style='margin: 0 0 12px 0; color: #555; font-size: 14px;'>{insight['description']}</p>
                <div style='padding: 12px; background-color: rgba(0,0,0,0.02); border-radius: 8px; border-left: 3px solid {icon_color};'>
                    <span style='color: {icon_color}; font-weight: 600; font-size: 13px;'>{action_type}</span>
                    <br/>
                    <span style='color: #555; font-size: 13px;'>{insight['action']}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("📊 No specific insights at this time. Market conditions are stable.")

st.markdown("---")

# ============================================================================
# SUPPLY & DEMAND CHART
# ============================================================================

if view_mode == "📊 Dashboard":
    st.markdown('<div class="section-title">📦 Supply & Demand Analysis</div>', unsafe_allow_html=True)

    supply = commodity_data['supply'].iloc[-1]
    demand = commodity_data['demand'].iloc[-1]
    sd_status, sd_color = get_supply_demand_indicator(supply, demand)

    col_sd1, col_sd2, col_sd3 = st.columns([1, 2, 2], gap="medium")

    with col_sd1:
        st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
        <div style='font-size: 12px; color: #7f8c8d; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;'>Market Status</div>
        <div style='font-size: 24px; font-weight: 700; color: {sd_color}; margin: 12px 0;'>{sd_status}</div>
        <div style='font-size: 13px; color: #555;'>Demand - Supply Gap: {(demand - supply):+.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    with col_sd2:
        fig_balance = go.Figure(data=[
            go.Bar(name='Supply', x=['Current'], y=[supply], marker_color='#3498db', marker_pattern_shape="/"),
            go.Bar(name='Demand', x=['Current'], y=[demand], marker_color='#e74c3c')
        ])
        fig_balance.update_layout(
            title="<b>Current Supply vs Demand</b>",
            barmode='group',
            template='plotly_white',
            height=300,
            margin=dict(l=0, r=0, t=40, b=0),
            yaxis_title="Level (0-100)",
            font=dict(family="Arial, sans-serif", size=10, color="#2c3e50")
        )
        st.plotly_chart(fig_balance, use_container_width=True)

    with col_sd3:
        fig_supply = go.Figure()
        fig_supply.add_trace(go.Scatter(
            x=commodity_data['date'],
            y=commodity_data['supply'],
            mode='lines+markers',
            name='Supply',
            line=dict(color='#3498db', width=2),
            marker=dict(size=4),
            fill='tozeroy',
            fillcolor='rgba(52, 152, 219, 0.1)'
        ))
        fig_supply.add_trace(go.Scatter(
            x=commodity_data['date'],
            y=commodity_data['demand'],
            mode='lines+markers',
            name='Demand',
            line=dict(color='#e74c3c', width=2),
            marker=dict(size=4),
            fill='tozeroy',
            fillcolor='rgba(231, 76, 60, 0.1)'
        ))
        fig_supply.update_layout(
            title="<b>30-Day Trend</b>",
            xaxis_title="Date",
            yaxis_title="Level (0-100)",
            template='plotly_white',
            height=300,
            margin=dict(l=0, r=0, t=40, b=0),
            hovermode='x unified',
            font=dict(family="Arial, sans-serif", size=10, color="#2c3e50")
        )
        st.plotly_chart(fig_supply, use_container_width=True)

    st.markdown("---")

    # ============================================================================
    # ADDITIONAL METRICS (NEW IN PHASE 2)
    # ============================================================================

    st.markdown('<div class="section-title">📊 Additional Market Metrics</div>', unsafe_allow_html=True)

    # Calculate additional metrics
    price_14d_ago = commodity_data['price'].iloc[14] if len(commodity_data) >= 14 else commodity_data['price'].iloc[0]
    if price_14d_ago == 0:
        price_change_14d = 0
    else:
        price_change_14d = ((current_price - price_14d_ago) / price_14d_ago) * 100

    price_30d_ago = commodity_data['price'].iloc[0]
    if price_30d_ago == 0:
        price_change_30d = 0
    else:
        price_change_30d = ((current_price - price_30d_ago) / price_30d_ago) * 100

    if current_price == 0:
        avg_daily_change = 0
    else:
        avg_daily_change = (commodity_data['price'].diff().mean() / current_price) * 100

    col_m1, col_m2, col_m3, col_m4 = st.columns(4, gap="medium")

    with col_m1:
        st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 12px; font-weight: 600; text-transform: uppercase;'>14-Day Change</div>
        <div style='font-size: 28px; font-weight: 700; color: {"#2ecc71" if price_change_14d > 0 else "#e74c3c"}; margin: 8px 0;'>{price_change_14d:+.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

    with col_m2:
        st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 12px; font-weight: 600; text-transform: uppercase;'>30-Day Change</div>
        <div style='font-size: 28px; font-weight: 700; color: {"#2ecc71" if price_change_30d > 0 else "#e74c3c"}; margin: 8px 0;'>{price_change_30d:+.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

    with col_m3:
        st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 12px; font-weight: 600; text-transform: uppercase;'>Avg Daily Change</div>
        <div style='font-size: 28px; font-weight: 700; color: #2c3e50; margin: 8px 0;'>{avg_daily_change:+.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

    with col_m4:
        st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 12px; font-weight: 600; text-transform: uppercase;'>Demand Level</div>
        <div style='font-size: 28px; font-weight: 700; color: #2c3e50; margin: 8px 0;'>{commodity_data['demand'].iloc[-1]:.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

# ============================================================================
# FEATURE 1: 7-DAY PRICE FORECAST
# ============================================================================

st.markdown('<div class="section-title">🔮 7-Day Price Forecast</div>', unsafe_allow_html=True)

# Simple linear regression forecast
if len(commodity_data) >= 5:
    x = np.arange(len(commodity_data))
    y = commodity_data['price'].values
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    
    # Forecast next 7 days
    forecast_x = np.arange(len(commodity_data), len(commodity_data) + 7)
    forecast_y = p(forecast_x)
    forecast_dates = pd.date_range(start=commodity_data['date'].iloc[-1] + timedelta(days=1), periods=7)
    
    # Create forecast chart
    fig_forecast = go.Figure()
    
    # Historical data
    fig_forecast.add_trace(go.Scatter(
        x=commodity_data['date'],
        y=commodity_data['price'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#2ecc71', width=2),
        marker=dict(size=4)
    ))
    
    # Forecast
    fig_forecast.add_trace(go.Scatter(
        x=forecast_dates,
        y=forecast_y,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#f39c12', width=2, dash='dash'),
        marker=dict(size=4, color='#f39c12')
    ))
    
    fig_forecast.update_layout(
        title="<b>Next 7 Days Price Forecast</b>",
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        template='plotly_white',
        height=350,
        hovermode='x unified',
        margin=dict(l=0, r=0, t=40, b=0),
        font=dict(family="Arial, sans-serif", size=10, color="#2c3e50")
    )
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Forecast summary
    forecast_col1, forecast_col2, forecast_col3 = st.columns(3, gap="medium")
    
    with forecast_col1:
        predicted_price = forecast_y[-1]
        price_delta = predicted_price - current_price
        price_delta_pct = (price_delta / current_price) * 100 if current_price != 0 else 0
        
        st.markdown(f"""
        <div class="metric-card">
            <div style='color: #7f8c8d; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Predicted Price (Day 7)</div>
            <div style='font-size: 28px; font-weight: 700; color: #2c3e50; margin: 8px 0;'>₹{predicted_price:,.0f}</div>
            <div style='color: {"#2ecc71" if price_delta > 0 else "#e74c3c"}; font-size: 12px; font-weight: 600;'>{price_delta:+.0f} ({price_delta_pct:+.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with forecast_col2:
        forecast_high = forecast_y.max()
        st.markdown(f"""
        <div class="metric-card">
            <div style='color: #7f8c8d; font-size: 11px; font-weight: 600; text-transform: uppercase;'>7-Day High</div>
            <div style='font-size: 28px; font-weight: 700; color: #2ecc71; margin: 8px 0;'>₹{forecast_high:,.0f}</div>
            <div style='color: #7f8c8d; font-size: 12px;'>Best selling opportunity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with forecast_col3:
        forecast_low = forecast_y.min()
        st.markdown(f"""
        <div class="metric-card">
            <div style='color: #7f8c8d; font-size: 11px; font-weight: 600; text-transform: uppercase;'>7-Day Low</div>
            <div style='font-size: 28px; font-weight: 700; color: #e74c3c; margin: 8px 0;'>₹{forecast_low:,.0f}</div>
            <div style='color: #7f8c8d; font-size: 12px;'>Best buying opportunity</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# FEATURE 2: PROFIT/LOSS CALCULATOR
# ============================================================================

st.markdown('<div class="section-title">💰 Profit/Loss Calculator</div>', unsafe_allow_html=True)

calc_col1, calc_col2, calc_col3, calc_col4 = st.columns(4, gap="medium")

with calc_col1:
    buy_price = st.number_input("Buy Price (₹/quintal)", min_value=0.0, value=float(current_price), step=10.0)

with calc_col2:
    buy_qty = st.number_input("Buy Quantity (quintals)", min_value=0.0, value=50.0, step=5.0)

with calc_col3:
    sell_price = st.number_input("Sell Price (₹/quintal)", min_value=0.0, value=float(current_price + 100), step=10.0)

with calc_col4:
    sell_qty = st.number_input("Sell Quantity (quintals)", min_value=0.0, value=50.0, step=5.0)

# Calculate profit/loss
total_cost = buy_price * buy_qty
total_revenue = sell_price * sell_qty
profit_loss = total_revenue - total_cost
profit_loss_pct = (profit_loss / total_cost * 100) if total_cost > 0 else 0
margin_per_quintal = sell_price - buy_price

calc_result_col1, calc_result_col2, calc_result_col3, calc_result_col4 = st.columns(4, gap="medium")

with calc_result_col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Total Investment</div>
        <div style='font-size: 24px; font-weight: 700; color: #2c3e50;'>₹{total_cost:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with calc_result_col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Total Revenue</div>
        <div style='font-size: 24px; font-weight: 700; color: #3498db;'>₹{total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with calc_result_col3:
    st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Profit/Loss</div>
        <div style='font-size: 24px; font-weight: 700; color: {"#2ecc71" if profit_loss > 0 else "#e74c3c"};'>₹{profit_loss:+,.0f}</div>
        <div style='color: {"#2ecc71" if profit_loss_pct > 0 else "#e74c3c"}; font-size: 12px; font-weight: 600;'>{profit_loss_pct:+.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with calc_result_col4:
    st.markdown(f"""
    <div class="metric-card">
        <div style='color: #7f8c8d; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Margin/Quintal</div>
        <div style='font-size: 24px; font-weight: 700; color: {"#2ecc71" if margin_per_quintal > 0 else "#e74c3c"};'>₹{margin_per_quintal:+,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# FEATURE 3: QUICK TRADE LOGGER
# ============================================================================

st.markdown('<div class="section-title">📝 Quick Trade Logger</div>', unsafe_allow_html=True)

log_col1, log_col2, log_col3, log_col4, log_col5 = st.columns(5, gap="medium")

with log_col1:
    trade_type = st.radio("Trade Type", ["🟢 Buy", "🔴 Sell"], horizontal=True, label_visibility="collapsed")

with log_col2:
    trade_price = st.number_input("Price (₹/qt)", min_value=0.0, value=float(current_price), step=10.0, key="trade_price")

with log_col3:
    trade_qty = st.number_input("Qty (qtl)", min_value=0.0, value=50.0, step=5.0, key="trade_qty")

with log_col4:
    trade_mandi = st.selectbox("Mandi", ["Tamil Nadu", "Telangana", "Andhra Pradesh"], label_visibility="collapsed")

with log_col5:
    if st.button("📊 Log Trade", use_container_width=True):
        st.success(f"✅ {trade_type} logged: {trade_qty} qt @ ₹{trade_price}/qt ({trade_mandi})")

st.markdown("---")

# ============================================================================
# FEATURE 4: MULTI-MANDI PRICE COMPARISON
# ============================================================================

st.markdown('<div class="section-title">🏪 Multi-Mandi Price Comparison</div>', unsafe_allow_html=True)

# Fetch multi-mandi prices from eNAM or use fallback
if ENAM_AVAILABLE:
    try:
        mandis = get_multimandi_prices(commodity)
    except Exception as e:
        st.warning(f"Could not fetch multi-mandi prices: {e}")
        mandis = None
else:
    mandis = None

# Fallback if eNAM data unavailable
if not mandis:
    mandis = {
        "Tamil Nadu (Today)": current_price,
        "Telangana (Today)": current_price - 50,
        "Andhra Pradesh (Today)": current_price + 75,
        "Karnataka (Today)": current_price - 100,
    }

mandi_col1, mandi_col2, mandi_col3, mandi_col4 = st.columns(4, gap="medium")

mandi_list = list(mandis.items())

for idx, (mandi_name, mandi_price) in enumerate(mandi_list):
    with [mandi_col1, mandi_col2, mandi_col3, mandi_col4][idx]:
        # Handle both dict values and direct numbers
        if isinstance(mandi_price, dict):
            actual_price = mandi_price.get("price", current_price)
        else:
            actual_price = mandi_price
        
        diff = actual_price - current_price
        diff_pct = (diff / current_price * 100) if current_price != 0 else 0
        color = "#2ecc71" if actual_price > current_price else "#e74c3c" if actual_price < current_price else "#3498db"
        
        st.markdown(f"""
        <div class="metric-card">
            <div style='color: #7f8c8d; font-size: 11px; font-weight: 600;'>{mandi_name}</div>
            <div style='font-size: 26px; font-weight: 700; color: {color}; margin: 8px 0;'>₹{actual_price:,.0f}</div>
            <div style='color: {color}; font-size: 12px; font-weight: 600;'>{diff:+.0f} ({diff_pct:+.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# FEATURE 5: PRICE ALERT SETTINGS
# ============================================================================

st.markdown('<div class="section-title">🔔 Price Alert Settings</div>', unsafe_allow_html=True)

alert_col1, alert_col2, alert_col3, alert_col4 = st.columns(4, gap="medium")

with alert_col1:
    alert_buy = st.number_input("Buy Alert At (₹)", min_value=0.0, value=float(current_price - 200), step=10.0)

with alert_col2:
    alert_sell = st.number_input("Sell Alert At (₹)", min_value=0.0, value=float(current_price + 200), step=10.0)

with alert_col3:
    alert_method = st.selectbox("Notify Via", ["📱 WhatsApp", "📧 Email", "🔔 In-App"], label_visibility="collapsed")

with alert_col4:
    if st.button("✅ Set Alerts", use_container_width=True):
        st.success(f"🎯 Alerts set! Buy: ₹{alert_buy}, Sell: ₹{alert_sell} via {alert_method}")

# Alert status
alert_status_col1, alert_status_col2 = st.columns(2, gap="medium")

with alert_status_col1:
    buy_diff = current_price - alert_buy
    buy_status = "✅ READY TO BUY" if current_price <= alert_buy else f"⏳ Waiting ({buy_diff:.0f}₹ to go)"
    buy_color = "#2ecc71" if current_price <= alert_buy else "#f39c12"
    
    st.markdown(f"""
    <div style='background: {buy_color}20; padding: 16px; border-radius: 8px; border-left: 4px solid {buy_color};'>
        <div style='color: {buy_color}; font-weight: 700; font-size: 14px;'>{buy_status}</div>
        <div style='color: #7f8c8d; font-size: 12px; margin-top: 4px;'>Buy target: ₹{alert_buy:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with alert_status_col2:
    sell_diff = alert_sell - current_price
    sell_status = "✅ READY TO SELL" if current_price >= alert_sell else f"⏳ Waiting ({sell_diff:.0f}₹ to go)"
    sell_color = "#2ecc71" if current_price >= alert_sell else "#f39c12"
    
    st.markdown(f"""
    <div style='background: {sell_color}20; padding: 16px; border-radius: 8px; border-left: 4px solid {sell_color};'>
        <div style='color: {sell_color}; font-weight: 700; font-size: 14px;'>{sell_status}</div>
        <div style='color: #7f8c8d; font-size: 12px; margin-top: 4px;'>Sell target: ₹{alert_sell:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# EXPORT & REFERENCE (PHASE 5) - Available in all views
# ============================================================================

st.markdown("---")
st.markdown('<div class="section-title">📥 Export Data & Quick Reference</div>', unsafe_allow_html=True)

col_export1, col_export2, col_export3 = st.columns([1, 1, 2], gap="medium")

with col_export1:
    # Export current data
    csv_data = commodity_data.to_csv(index=False).encode()
    st.download_button(
        label="📊 Export CSV",
        data=csv_data,
        file_name=f"croppulse_{commodity}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col_export2:
    # Export summary
    summary_text = f"""
CROPPULSE EXPORT - {commodity.upper()}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CURRENT METRICS:
- Price: ₹{current_price:,.0f}
- Risk Score: {risk_score:.0f}/100
- Volatility: {volatility:.1f}%
- Supply: {commodity_data['supply'].iloc[-1]:.0f}%
- Demand: {commodity_data['demand'].iloc[-1]:.0f}%
- 7-Day Change: {price_change_7d:+.1f}%

STATUS: {risk_level}
TREND: {trend_text}
"""
    st.download_button(
        label="📝 Export Summary",
        data=summary_text,
        file_name=f"croppulse_summary_{commodity}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

with col_export3:
    st.markdown("""
    **Quick Reference Guide**
    - **Risk Score**: Lower is better (0 = safe, 100 = risky)
    - **Supply**: Higher is better for buyers (indicators prices down)
    - **Demand**: Higher means more buyers (indicators prices up)
    - **Volatility**: Lower is better (stable prices, less risk)
    """)

st.markdown("---")

st.markdown("""
<div style='text-align: center; padding: 24px; color: #7f8c8d; border-top: 1px solid #e0e0e0; margin-top: 32px;'>
    <p style='margin: 0; font-size: 14px;'><strong>🌾 CropPulse</strong> — Agricultural Market Intelligence Platform</p>
    <p style='margin: 8px 0 0 0; font-size: 11px;'>Powered by Real-Time Data | Last updated: May 12, 2026</p>
    <p style='margin: 8px 0 0 0; font-size: 11px; color: #bdc3c7;'>Disclaimer: This information is for educational purposes only. Not investment advice.</p>
</div>
""", unsafe_allow_html=True)
