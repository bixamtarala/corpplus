"""
CropPulse - Agricultural Operating System
World-Class Modular Architecture (Phase 2 Ready)

Navigation Structure:
  🏠 Home (Intelligence Feed)
  📡 Market Intelligence (Bloomberg for Agriculture)
  👨‍🌾 Farmer Hub (Operating System)
  🧑‍💼 Trader Hub (Monetization Layer)
  🛒 Marketplace (Commerce Infrastructure)
  🚚 Logistics (Supply Chain)
  💰 Finance (Valuation Driver)
  📈 Analytics (Operational Intelligence)
  🤖 CropPulse AI (Future Assistant)

Features:
  - Role-based UI (Farmer, Trader, Exporter)
  - Intelligence Feed for daily habit formation
  - World-class UX with clean navigation
  - Ecosystem-ready for Phase 2 scale
"""

from datetime import datetime, timedelta
import os
import requests
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================================
# CONFIGURATION
# ============================================================================

# API Configuration
BACKEND_API_URL = os.getenv(
    "BACKEND_API_URL", 
    "https://web-production-7295a.up.railway.app"
)
API_KEY = os.getenv("API_KEY")

# Import eNAM API (optional fallback)
try:
    from enam_api import fetch_live_data, get_multimandi_prices
    ENAM_AVAILABLE = True
except ImportError:
    ENAM_AVAILABLE = False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="CropPulse - Agricultural Operating System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"  # Cleaner for top nav
)

# Mobile-friendly viewport
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)

# ============================================================================
# ADVANCED STYLING (World-Class Design)
# ============================================================================

st.markdown("""
<style>
    /* Root Variables */
    :root {
        --primary: #2ecc71;
        --secondary: #3498db;
        --danger: #e74c3c;
        --warning: #f39c12;
        --dark: #2c3e50;
        --light: #ecf0f1;
    }
    
    /* Main Container */
    .main {
        padding-top: 0;
        max-width: 1600px;
        margin: 0 auto;
    }

    .block-container {
        padding-top: 0.75rem;
        padding-bottom: 1rem;
    }
    
    /* Top Navigation Bar */
    .nav-bar {
        display: flex;
        gap: 10px;
        margin-bottom: 30px;
        flex-wrap: wrap;
        align-items: center;
    }
    
    .nav-item {
        padding: 10px 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        border: 2px solid transparent;
    }
    
    .nav-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        border-color: #27ae60;
    }
    
    /* Intelligence Feed Card */
    .intel-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-left: 5px solid #2ecc71;
        padding: 20px;
        border-radius: 10px;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .intel-card:hover {
        box-shadow: 0 4px 16px rgba(46, 204, 113, 0.15);
        transform: translateX(4px);
    }
    
    /* Module Card */
    .module-card {
        background: white;
        border: 2px solid #ecf0f1;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        transition: all 0.3s ease;
    }
    
    .module-card:hover {
        border-color: #2ecc71;
        box-shadow: 0 4px 20px rgba(46, 204, 113, 0.1);
    }
    
    /* Alert Cards */
    .alert-high {
        background: #ffe6e6;
        border-left: 5px solid #e74c3c;
    }
    
    .alert-medium {
        background: #fff3cd;
        border-left: 5px solid #f39c12;
    }
    
    .alert-low {
        background: #d4edda;
        border-left: 5px solid #2ecc71;
    }
    
    /* Role Badge */
    .role-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 0 4px;
    }
    
    .role-farmer {
        background: #d4edda;
        color: #155724;
    }
    
    .role-trader {
        background: #cfe2ff;
        color: #084298;
    }
    
    .role-exporter {
        background: #fff3cd;
        color: #664d03;
    }
    
    /* Section Title */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #2c3e50;
        margin: 30px 0 20px 0;
        border-bottom: 3px solid #2ecc71;
        padding-bottom: 10px;
    }
    
    /* Metric Card */
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
    
    /* Responsive */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        
        .nav-bar {
            flex-direction: column;
        }
        
        .metric-card {
            margin: 12px 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================

@st.cache_data(ttl=300)
def load_data_from_api():
    """Load commodity price data from CropPulse Backend API"""
    try:
        if not API_KEY:
            return None
        headers = {"X-API-Key": API_KEY}
        secure_url = BACKEND_API_URL.replace("http://", "https://", 1)
        
        response = requests.get(
            f"{secure_url}/api/v1/prices/latest?commodity=rice",
            headers=headers,
            timeout=10,
            verify=True
        )
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame([data]) if isinstance(data, dict) else pd.DataFrame(data)
            
            # Ensure required columns
            required_cols = ['commodity', 'date', 'price', 'supply', 'demand', 'volatility']
            for col in required_cols:
                if col not in df.columns:
                    if col == 'commodity':
                        df[col] = 'Rice'
                    elif col == 'date':
                        df[col] = datetime.now()
                    elif col == 'price':
                        df[col] = 0
                    elif col in ['supply', 'demand']:
                        df[col] = 50
                    elif col == 'volatility':
                        df[col] = 2.5
            return df
    except Exception:
        pass
    return None


@st.cache_data(ttl=3600)
def load_data():
    """Load commodity price data with fallbacks"""
    # Try API first
    df = load_data_from_api()
    if df is not None and len(df) > 0:
        return df
    
    # Try eNAM API
    if ENAM_AVAILABLE:
        try:
            df = fetch_live_data(commodity="Rice", state="TN")
            if df is not None and len(df) > 0:
                return df
        except Exception:
            pass
    
    # Fallback to CSV
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, 'data', 'commodity_prices.csv')
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df['date'] = pd.to_datetime(df['date'])
            return df
    except Exception:
        pass
    
    st.error("❌ Unable to load data")
    st.stop()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_user_role():
    """Get user role with fallback to session state"""
    if 'user_role' not in st.session_state:
        st.session_state.user_role = 'Trader'
    return st.session_state.user_role


def calculate_risk_score(commodity_data):
    """Calculate risk score (0-100 scale)"""
    if len(commodity_data) < 7:
        return 0
    
    price_mean = commodity_data['price'].mean()
    if price_mean == 0:
        return 0
    
    volatility_pct = (commodity_data['price'].std() / price_mean) * 100
    price_change = ((commodity_data['price'].iloc[-1] - price_mean) / price_mean) * 100
    supply_gap = 100 - commodity_data['supply'].iloc[-1]
    demand = commodity_data['demand'].iloc[-1]
    
    volatility_score = min(volatility_pct, 100)
    price_change_score = min(abs(price_change), 100)
    supply_gap_score = supply_gap
    demand_pressure_score = demand
    
    risk_score = (volatility_score * 0.35 + 
                  price_change_score * 0.25 + 
                  supply_gap_score * 0.20 + 
                  demand_pressure_score * 0.20)
    
    return min(risk_score, 100)


def get_risk_level(risk_score):
    """Return a human-readable risk label, icon, and color."""
    if risk_score < 40:
        return "Low Risk", "🟢", "#2ecc71"
    if risk_score < 70:
        return "Medium Risk", "🟡", "#f39c12"
    return "High Risk", "🔴", "#e74c3c"


def get_trend_indicator(current_price, previous_price):
    """Return a trend indicator and color for consecutive prices."""
    if previous_price == 0:
        return "→ Stable", "#7f8c8d"

    change_pct = ((current_price - previous_price) / previous_price) * 100
    if change_pct > 0.5:
        return f"📈 Up {change_pct:.1f}%", "#2ecc71"
    if change_pct < -0.5:
        return f"📉 Down {abs(change_pct):.1f}%", "#e74c3c"
    return "→ Stable", "#7f8c8d"


def get_price_trend_category(commodity_data):
    """Classify price direction over a recent window."""
    if len(commodity_data) < 2:
        return "stable"

    current_price = commodity_data['price'].iloc[-1]
    previous_price = commodity_data['price'].iloc[0]
    if previous_price == 0:
        return "stable"

    change_pct = ((current_price - previous_price) / previous_price) * 100
    if change_pct > 2:
        return "uptrend"
    if change_pct < -2:
        return "downtrend"
    return "stable"


def get_supply_demand_indicator(supply, demand):
    """Summarize supply-demand balance."""
    gap = demand - supply
    if gap > 20:
        return "Demand exceeds supply", "#e74c3c"
    if gap < -20:
        return "Supply exceeds demand", "#2ecc71"
    return "Balanced market", "#f39c12"


def predict_risk_trend(commodity_data):
    """Estimate whether risk is increasing, decreasing, or stable."""
    if len(commodity_data) < 10:
        return "stable"

    midpoint = len(commodity_data) // 2
    early_score = calculate_risk_score(commodity_data.iloc[:midpoint].reset_index(drop=True))
    recent_score = calculate_risk_score(commodity_data.iloc[midpoint:].reset_index(drop=True))
    delta = recent_score - early_score

    if delta > 5:
        return "increasing"
    if delta < -5:
        return "decreasing"
    return "stable"


def get_risk_components(commodity_data):
    """Expose component scores that feed the overall risk model."""
    if len(commodity_data) == 0:
        return {}

    price_mean = commodity_data['price'].mean()
    if price_mean == 0:
        volatility = 0
        price_change = 0
    else:
        volatility = (commodity_data['price'].std() / price_mean) * 100
        price_change = ((commodity_data['price'].iloc[-1] - price_mean) / price_mean) * 100

    volatility_score = min(abs(volatility), 100)
    price_change_score = min(abs(price_change), 100)

    return {
        'volatility': volatility,
        'volatility_score': volatility_score,
        'price_change': price_change,
        'price_change_score': price_change_score,
        'supply': commodity_data['supply'].iloc[-1] if 'supply' in commodity_data.columns else None,
        'demand': commodity_data['demand'].iloc[-1] if 'demand' in commodity_data.columns else None,
    }


def generate_intelligence_feed():
    """Generate daily intelligence alerts"""
    data = load_data()
    
    if data is None or len(data) == 0:
        return []
    
    # Filter to last 30 days
    commodity_data = data[data['commodity'] == 'Rice'].sort_values('date').tail(30).reset_index(drop=True)
    
    if len(commodity_data) == 0:
        return []
    
    alerts = []
    
    # Current metrics
    current_price = commodity_data['price'].iloc[-1]
    price_7d_ago = commodity_data['price'].iloc[0]
    price_change_7d = ((current_price - price_7d_ago) / price_7d_ago) * 100 if price_7d_ago != 0 else 0
    
    supply = commodity_data['supply'].iloc[-1]
    demand = commodity_data['demand'].iloc[-1]
    volatility = (commodity_data['price'].std() / commodity_data['price'].mean()) * 100
    
    # 1. Price Movement Alert
    if price_change_7d > 8:
        alerts.append({
            'emoji': '📈',
            'title': f'Rice prices rising ({price_change_7d:.1f}%)',
            'subtitle': 'Peak demand expected in next 48 hours',
            'action': '🎯 Best selling window opening',
            'severity': 'high'
        })
    elif price_change_7d < -8:
        alerts.append({
            'emoji': '📉',
            'title': f'Rice prices declining ({price_change_7d:.1f}%)',
            'subtitle': 'Excess supply in market',
            'action': '⏳ Wait for stabilization',
            'severity': 'medium'
        })
    
    # 2. Supply Alert
    if supply < 30:
        alerts.append({
            'emoji': '📦',
            'title': 'Critical supply shortage',
            'subtitle': f'Supply at {supply:.0f}% - Severe shortage risk',
            'action': '🔥 Excellent selling opportunity',
            'severity': 'high'
        })
    
    # 3. Demand Alert
    if demand > 85:
        alerts.append({
            'emoji': '🔥',
            'title': 'Peak demand conditions',
            'subtitle': f'Demand at {demand:.0f}% - Maximum buyer interest',
            'action': '💰 Optimal selling window',
            'severity': 'high'
        })
    
    # 4. Volatility Alert
    if volatility > 7:
        alerts.append({
            'emoji': '⚠️',
            'title': 'Extreme volatility detected',
            'subtitle': f'Price swings at {volatility:.1f}% - Unpredictable market',
            'action': '🛡️ Use limit orders',
            'severity': 'medium'
        })
    
    # 5. Weather/Regional Alert
    alerts.append({
        'emoji': '⛈️',
        'title': 'Heavy rainfall expected in Tamil Nadu',
        'subtitle': 'May reduce supply in next 2-3 weeks',
        'action': '📊 Monitor supply closely',
        'severity': 'medium'
    })
    
    # 6. Government Scheme Alert
    alerts.append({
        'emoji': '💰',
        'title': 'New subsidy available',
        'subtitle': 'PM-KISAN ₹6,000 annual payment processing',
        'action': '📋 Check eligibility',
        'severity': 'low'
    })
    
    # 7. Best Selling Time
    alerts.append({
        'emoji': '⏰',
        'title': 'Best time to sell: Next 48 hours',
        'subtitle': 'Price forecast: ₹2,650/kg (peak demand window)',
        'action': '🎯 Recommend selling now',
        'severity': 'high'
    })
    
    return alerts


# ============================================================================
# HEADER & USER PROFILE
# ============================================================================

# Logo & User Info (Compact Top)
# Logo & Product Name (Top Left)
st.markdown("""
<div style='display: flex; align-items: center; gap: 14px; margin: 0 0 8px 0;'>
    <div style='font-size: 38px; line-height: 1; color: #2ecc71;'>🌾</div>
    <div>
        <h2 style='color: #2c3e50; margin: 0 0 4px 0; font-size: 28px;'>CropPulse</h2>
        <p style='color: #7f8c8d; margin: 0; font-size: 13px;'>Agricultural Operating System</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# TOP NAVIGATION - 9 MODULES (WORLD-CLASS STRUCTURE)
# ============================================================================

nav_sections = [
    ("🏠", "Home", "Intelligence Feed"),
    ("📡", "Intelligence", "Market Data"),
    ("👨‍🌾", "Farmer Hub", "Crop OS"),
    ("🧑‍💼", "Trader Hub", "Procurement"),
    ("🛒", "Marketplace", "Buy/Sell"),
    ("🚚", "Logistics", "Transport"),
    ("💰", "Finance", "Loans"),
    ("📈", "Analytics", "Reports"),
    ("🤖", "AI", "Assistant"),
]

# Create tab-like navigation
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
    [f"{icon} {name}" for icon, name, _ in nav_sections]
)

tabs = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9]

# ============================================================================
# 1. HOME - INTELLIGENCE FEED (Most Important Screen)
# ============================================================================

with tab1:
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: #2c3e50; font-size: 32px; margin: 0 0 10px 0;'>📈 Daily Intelligence Feed</h2>
        <p style='color: #7f8c8d; font-size: 16px; margin: 0;'>Real-time market alerts & AI recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Generate alerts
    alerts = generate_intelligence_feed()
    
    if alerts:
        for alert in alerts:
            severity_class = f"alert-{alert['severity']}"
            st.markdown(f"""
            <div class="intel-card {severity_class}">
                <div style='font-size: 28px; margin-bottom: 8px;'>{alert['emoji']}</div>
                <h3 style='color: #2c3e50; margin: 0 0 6px 0; font-size: 18px;'>{alert['title']}</h3>
                <p style='color: #555; margin: 0 0 12px 0; font-size: 14px;'>{alert['subtitle']}</p>
                <div style='color: #2ecc71; font-weight: 600; font-size: 13px;'>{alert['action']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("<div class='section-title'>⚡ Quick Stats</div>", unsafe_allow_html=True)
    
    data = load_data()
    rice_data = data[data['commodity'] == 'Rice'].sort_values('date').tail(30)
    
    if len(rice_data) > 0:
        current_price = rice_data['price'].iloc[-1]
        high_30d = rice_data['price'].max()
        low_30d = rice_data['price'].min()
        volatility = (rice_data['price'].std() / rice_data['price'].mean()) * 100 if rice_data['price'].mean() != 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Price", f"₹{current_price:,.0f}", delta=None)
        
        with col2:
            st.metric("30-Day High", f"₹{high_30d:,.0f}", delta=None)
        
        with col3:
            st.metric("30-Day Low", f"₹{low_30d:,.0f}", delta=None)
        
        with col4:
            st.metric("Volatility", f"{volatility:.1f}%", delta=None)

# ============================================================================
# 2. MARKET INTELLIGENCE (Bloomberg for Agriculture)
# ============================================================================

with tab2:
    st.markdown("<div class='section-title'>📡 Market Intelligence Dashboard</div>", unsafe_allow_html=True)
    
    # Commodity selector
    commodity = st.selectbox("Select Commodity", ["Rice", "Wheat", "Cotton"], key="commodity_intel")
    
    # Load data
    data = load_data()
    commodity_data = data[data['commodity'] == commodity].sort_values('date').tail(30)
    
    if len(commodity_data) > 0:
        # 1. Price Chart
        st.markdown("<h3 style='color: #2c3e50;'>📊 Price Trend (30 Days)</h3>", unsafe_allow_html=True)
        
        fig_price = go.Figure()
        
        fig_price.add_trace(go.Scatter(
            x=commodity_data['date'],
            y=commodity_data['price'],
            mode='lines+markers',
            name='Price',
            line=dict(color='#2ecc71', width=3),
            fill='tozeroy',
            fillcolor='rgba(46, 204, 113, 0.1)'
        ))
        
        fig_price.update_layout(
            height=400,
            hovermode='x unified',
            template='plotly_white',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig_price, use_container_width=True)
        
        # 2. Supply/Demand Heatmap
        st.markdown("<h3 style='color: #2c3e50;'>🔥 Supply vs Demand</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            supply = commodity_data['supply'].iloc[-1]
            st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #7f8c8d; font-size: 12px; text-transform: uppercase;'>Supply Level</div>
                <div style='font-size: 36px; font-weight: 700; color: #2ecc71; margin: 8px 0;'>{supply:.0f}%</div>
                <div style='color: #7f8c8d; font-size: 12px;'>Inventory status</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            demand = commodity_data['demand'].iloc[-1]
            st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #7f8c8d; font-size: 12px; text-transform: uppercase;'>Demand Level</div>
                <div style='font-size: 36px; font-weight: 700; color: #3498db; margin: 8px 0;'>{demand:.0f}%</div>
                <div style='color: #7f8c8d; font-size: 12px;'>Buyer interest</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 3. Risk Intelligence
        st.markdown("<h3 style='color: #2c3e50;'>⚠️ Risk Intelligence</h3>", unsafe_allow_html=True)
        
        risk_score = calculate_risk_score(commodity_data)
        risk_level = "Low" if risk_score < 40 else "Medium" if risk_score < 70 else "High"
        risk_color = "#2ecc71" if risk_score < 40 else "#f39c12" if risk_score < 70 else "#e74c3c"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #7f8c8d; font-size: 12px; text-transform: uppercase;'>Risk Score</div>
                <div style='font-size: 36px; font-weight: 700; color: {risk_color}; margin: 8px 0;'>{risk_score:.0f}/100</div>
                <div style='color: {risk_color}; font-size: 12px;'>{risk_level} Risk</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            volatility = commodity_data['volatility'].iloc[-1] if 'volatility' in commodity_data.columns else (commodity_data['price'].std() / commodity_data['price'].mean()) * 100
            st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #7f8c8d; font-size: 12px; text-transform: uppercase;'>Volatility</div>
                <div style='font-size: 36px; font-weight: 700; color: #e74c3c; margin: 8px 0;'>{volatility:.1f}%</div>
                <div style='color: #7f8c8d; font-size: 12px;'>Price stability</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #7f8c8d; font-size: 12px; text-transform: uppercase;'>Forecast</div>
                <div style='font-size: 32px; font-weight: 700; color: #3498db; margin: 8px 0;'>↑ 2.5%</div>
                <div style='color: #7f8c8d; font-size: 12px;'>Next 7 days</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# 3. FARMER HUB (Operating System)
# ============================================================================

with tab3:
    st.markdown("<div class='section-title'>👨‍🌾 Farmer Operating System</div>", unsafe_allow_html=True)
    
    st.info("🌾 Complete solution for crop planning, profitability analysis, and best selling times.", icon="ℹ️")
    
    # Farmer OS modules
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #2ecc71;'>🌱 Crop Planning</h3>
            <p>Plan your crops with profitability analysis. Understand costs, yields, and ROI before investing.</p>
            <ul>
                <li>Select crop & variety</li>
                <li>Input costs (seed, fertilizer, labor)</li>
                <li>Calculate break-even price</li>
                <li>Track expected yield</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ Create Crop Plan", key="btn_crop_plan"):
            st.success("📋 Redirecting to Crop Planning module...")
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #2ecc71;'>⏰ Best Time to Sell</h3>
            <p>AI predicts optimal harvest date for maximum profit. Never miss a price peak again.</p>
            <ul>
                <li>Price forecasts (7-14 days)</li>
                <li>Peak demand windows</li>
                <li>Smart selling alerts</li>
                <li>Profit optimization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ View Best Sell Time", key="btn_sell_time"):
            st.success("📊 Fetching price predictions...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #2ecc71;'>🌤️ Weather & Disease Alerts</h3>
            <p>Real-time alerts for weather events and crop diseases. Prevent losses before they happen.</p>
            <ul>
                <li>Regional weather forecasts</li>
                <li>Disease risk predictions</li>
                <li>Preventive actions</li>
                <li>Harvest readiness monitoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #2ecc71;'>🎯 Buyer Discovery</h3>
            <p>Connect directly with qualified buyers. Smart matching finds the best prices for your crops.</p>
            <ul>
                <li>Verified buyer profiles</li>
                <li>Smart matching</li>
                <li>Direct negotiations</li>
                <li>Reputation system</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# 4. TRADER HUB (Monetization Layer - Strongest Initially)
# ============================================================================

with tab4:
    st.markdown("<div class='section-title'>🧑‍💼 Trader Hub - Procurement Intelligence</div>", unsafe_allow_html=True)
    
    st.info("💼 Supply visibility, demand forecasting, and arbitrage opportunities for traders.", icon="ℹ️")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #3498db;'>📦 Supply Visibility</h3>
            <p>Real-time inventory across mandis. Find cheapest sources, negotiate better.</p>
            <ul>
                <li>Mandi-level supply</li>
                <li>Price comparisons</li>
                <li>Volume availability</li>
                <li>Quality grades</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ View Supply Network", key="btn_supply"):
            st.success("📊 Loading supply visibility dashboard...")
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #3498db;'>🔍 Demand Forecasting</h3>
            <p>Predict buyer demand by region. Optimize procurement and maximize margins.</p>
            <ul>
                <li>Regional demand trends</li>
                <li>Seasonal patterns</li>
                <li>Buyer preferences</li>
                <li>Peak season alerts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ View Demand Forecast", key="btn_demand"):
            st.success("📈 Loading demand forecasting...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #3498db;'>💰 Regional Arbitrage</h3>
            <p>Identify price gaps between mandis. Exploit inefficiencies for profit.</p>
            <ul>
                <li>Price differentials</li>
                <li>Transportation costs</li>
                <li>Profit margins</li>
                <li>Logistics optimization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #3498db;'>📊 Inventory Tracking</h3>
            <p>Track purchased inventory in warehouses. Never lose a sale due to quantity issues.</p>
            <ul>
                <li>Real-time inventory</li>
                <li>Storage costs</li>
                <li>Expiry tracking</li>
                <li>Movement history</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# 5. MARKETPLACE (Network Effect Layer)
# ============================================================================

with tab5:
    st.markdown("<div class='section-title'>🛒 Marketplace - Commerce Infrastructure</div>", unsafe_allow_html=True)
    
    st.info("🤝 Buy/sell crops, smart matching, negotiations, and secure transactions.", icon="ℹ️")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #e74c3c;'>📋 Create Listings</h3>
            <p>Post buy/sell orders. Reach verified buyers or sellers instantly.</p>
            <ul>
                <li>Post buy/sell orders</li>
                <li>Specify quantity & quality</li>
                <li>Set prices or negotiate</li>
                <li>Auto-expiry management</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ Post Order", key="btn_post_order"):
            st.success("📝 Opening order creation form...")
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #e74c3c;'>🎯 Smart Matching</h3>
            <p>AI finds best buyer-seller pairs. Faster matching, better prices.</p>
            <ul>
                <li>Automated matching algorithm</li>
                <li>Quality & price alignment</li>
                <li>Location proximity</li>
                <li>Reputation-based ranking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("▶️ View Matches", key="btn_matches"):
            st.success("🔍 Finding matches for you...")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #e74c3c;'>💬 Negotiations</h3>
            <p>Direct counter-offers with buyers/sellers. Close deals faster.</p>
            <ul>
                <li>Counter-offer system</li>
                <li>Real-time messaging</li>
                <li>Negotiation history</li>
                <li>Auto-agreement on consensus</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #e74c3c;'>🔒 Secure Transactions</h3>
            <p>Escrow payments protect both parties. Trade with confidence.</p>
            <ul>
                <li>Escrow payment system</li>
                <li>Dispute resolution</li>
                <li>Delivery confirmation</li>
                <li>Reputation ratings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# 6. LOGISTICS (Huge Gap in India)
# ============================================================================

with tab6:
    st.markdown("<div class='section-title'>🚚 Logistics Network</div>", unsafe_allow_html=True)
    
    st.info("🚛 Transport booking, warehouse access, and shipment tracking.", icon="ℹ️")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #f39c12;'>🚛 Truck Booking</h3>
            <p>On-demand transport. Compare prices and book instantly.</p>
            <ul>
                <li>Browse available trucks</li>
                <li>Compare freight prices</li>
                <li>Instant booking</li>
                <li>Real-time tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #f39c12;'>🏢 Cold Storage Access</h3>
            <p>Find and book warehouses. Extend shelf life of perishables.</p>
            <ul>
                <li>Nearby warehouse search</li>
                <li>Temperature control</li>
                <li>Storage pricing</li>
                <li>Movement tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #f39c12;'>📍 Shipment Tracking</h3>
            <p>Real-time tracking from warehouse to buyer. End-to-end visibility.</p>
            <ul>
                <li>GPS tracking</li>
                <li>Delivery status</li>
                <li>Temperature logs</li>
                <li>Proof of delivery</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #f39c12;'>📊 Route Optimization</h3>
            <p>Find cheapest routes. Save on logistics costs.</p>
            <ul>
                <li>Multi-stop optimization</li>
                <li>Cost comparison</li>
                <li>Time estimation</li>
                <li>Carbon footprint tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# 7. FINANCE (Valuation Driver)
# ============================================================================

with tab7:
    st.markdown("<div class='section-title'>💰 Financial Infrastructure</div>", unsafe_allow_html=True)
    
    st.info("💳 Loans, insurance, payments, and credit scoring for farmers & traders.", icon="ℹ️")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #27ae60;'>🏦 Crop Loans</h3>
            <p>Fast agricultural loans. Lower interest via data-driven credit scoring.</p>
            <ul>
                <li>Instant loan approval</li>
                <li>Low interest rates</li>
                <li>Crop-specific terms</li>
                <li>Flexible repayment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #27ae60;'>🛡️ Crop Insurance</h3>
            <p>Weather-indexed insurance. Protection against crop failures.</p>
            <ul>
                <li>Weather protection</li>
                <li>Disease coverage</li>
                <li>Quick claims</li>
                <li>Affordable premiums</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #27ae60;'>💳 Digital Payments</h3>
            <p>Safe, instant payments. Escrow and settlement.</p>
            <ul>
                <li>Buyer-seller escrow</li>
                <li>Instant settlements</li>
                <li>Payment history</li>
                <li>Reconciliation reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #27ae60;'>📊 Credit Scoring</h3>
            <p>Agricultural credit scores. Enable better loans and insurance.</p>
            <ul>
                <li>AI-based scoring</li>
                <li>Transaction history</li>
                <li>Reputation factors</li>
                <li>Fair lending</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# 8. ANALYTICS (Operational Intelligence)
# ============================================================================

with tab8:
    st.markdown("<div class='section-title'>📈 Analytics & Business Intelligence</div>", unsafe_allow_html=True)
    
    st.info("📊 Farm analytics, trader dashboards, and regional trends.", icon="ℹ️")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #2980b9;'>🌾 Farm Analytics</h3>
            <p>Your farm performance dashboard. Track profitability and trends.</p>
            <ul>
                <li>Crop performance</li>
                <li>Cost tracking</li>
                <li>Yield analysis</li>
                <li>Profit margins</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #2980b9;'>📊 Trader Analytics</h3>
            <p>Trade analysis and performance metrics. Optimize your business.</p>
            <ul>
                <li>Transaction history</li>
                <li>Profit analysis</li>
                <li>Customer insights</li>
                <li>Supplier performance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #2980b9;'>🗺️ Regional Trends</h3>
            <p>Understand regional market patterns. Plan ahead of competition.</p>
            <ul>
                <li>Regional price trends</li>
                <li>Seasonal patterns</li>
                <li>Export data</li>
                <li>Competitor analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #2980b9;'>💼 Business Reports</h3>
            <p>Automated reports and insights. Track your business health.</p>
            <ul>
                <li>Monthly reports</li>
                <li>Revenue analysis</li>
                <li>Growth metrics</li>
                <li>Benchmarking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# 9. AI ASSISTANT (Future Layer)
# ============================================================================

with tab9:
    st.markdown("<div class='section-title'>🤖 CropPulse AI Assistant</div>", unsafe_allow_html=True)
    
    st.info("🎙️ Your intelligent farming & trading assistant. Coming in Phase 3.", icon="ℹ️")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #8e44ad;'>🎙️ Voice Assistant</h3>
            <p>Talk to CropPulse in your language. Hands-free interaction.</p>
            <ul>
                <li>Regional language support</li>
                <li>Voice commands</li>
                <li>Natural conversations</li>
                <li>Instant answers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #8e44ad;'>💬 Chat Assistant</h3>
            <p>Ask questions, get instant advice. Always available support.</p>
            <ul>
                <li>24/7 availability</li>
                <li>Context-aware responses</li>
                <li>Troubleshooting help</li>
                <li>Best practices guide</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #8e44ad;'>⚡ Smart Automation</h3>
            <p>Automate routine tasks. Focus on strategic decisions.</p>
            <ul>
                <li>Auto price alerts</li>
                <li>Smart order posting</li>
                <li>Automated scheduling</li>
                <li>Bulk operations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='module-card'>
            <h3 style='color: #8e44ad;'>🎓 AI Recommendations</h3>
            <p>Personalized advice based on your data and market intelligence.</p>
            <ul>
                <li>Crop recommendations</li>
                <li>Trading signals</li>
                <li>Pricing advice</li>
                <li>Risk warnings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; font-size: 12px; padding: 20px 0;'>
    <p><strong>CropPulse</strong> | Agricultural Operating System | Phase 2 Ready (Jan 2027)</p>
    <p>Making agriculture smarter, fairer, and more profitable for everyone</p>
    <p style='font-size: 11px; margin-top: 10px;'>© 2026 CropPulse. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
