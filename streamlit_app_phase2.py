"""CropPulse Phase 2 - Streamlit-first public app."""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import plotly.express as px
import plotly.graph_objects as go
import os
import hashlib
import secrets
from db_config import (
    get_db_connection, test_connection, init_database
)
import logging

# ============================================================================
# CONFIGURATION & LOGGING
# ============================================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="CropPulse - Agricultural OS",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ADVANCED STYLING (Phase 2 Premium Design)
# ============================================================================

st.markdown("""
<style>
    :root {
        --primary: #2ecc71;
        --secondary: #3498db;
        --danger: #e74c3c;
        --warning: #f39c12;
        --success: #27ae60;
        --dark: #2c3e50;
        --light: #ecf0f1;
    }
    
    .main {
        max-width: 1400px;
        margin: 0 auto;
    }

    .block-container {
        padding-top: 1.25rem;
        padding-bottom: 2rem;
    }

    .top-strip {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        margin-bottom: 20px;
    }

    .brand-lockup {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .brand-mark {
        font-size: 40px;
        line-height: 1;
    }

    .brand-title {
        font-size: 30px;
        font-weight: 800;
        color: #1f2d3d;
        margin: 0;
    }

    .brand-subtitle {
        font-size: 14px;
        color: #5f6c7b;
        margin: 2px 0 0 0;
    }

    .top-badge {
        display: inline-block;
        padding: 8px 14px;
        background: #eef8f1;
        border: 1px solid #cfe8d7;
        border-radius: 999px;
        color: #1d6b3a;
        font-size: 13px;
        font-weight: 600;
    }
    
    /* Landing Page Hero */
    .hero-section {
        background: linear-gradient(135deg, #1f8f4d 0%, #2ecc71 100%);
        color: white;
        padding: 56px 44px;
        border-radius: 24px;
        margin: 24px 0 28px 0;
        box-shadow: 0 10px 40px rgba(46, 204, 113, 0.2);
    }

    .hero-grid {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 28px;
        align-items: center;
    }

    .section-kicker {
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 12px;
        font-weight: 700;
        opacity: 0.85;
        margin-bottom: 14px;
    }
    
    .hero-title {
        font-size: 52px;
        font-weight: 800;
        line-height: 1.05;
        margin: 0 0 18px 0;
    }
    
    .hero-subtitle {
        font-size: 21px;
        font-weight: 400;
        margin: 0 0 18px 0;
        opacity: 0.94;
    }

    .hero-copy {
        font-size: 16px;
        line-height: 1.7;
        opacity: 0.95;
        margin-bottom: 24px;
        max-width: 760px;
    }

    .hero-panel {
        background: rgba(255, 255, 255, 0.14);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 20px;
        padding: 24px;
        backdrop-filter: blur(8px);
    }

    .hero-panel h3 {
        margin: 0 0 14px 0;
        font-size: 20px;
    }

    .hero-panel ul {
        margin: 0;
        padding-left: 18px;
        line-height: 1.8;
    }

    .cta-row {
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
        margin-top: 18px;
    }

    .metric-strip {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin: 10px 0 24px 0;
    }

    .hero-stat {
        background: #ffffff;
        border: 1px solid #e5ece7;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    }

    .hero-stat-value {
        font-size: 28px;
        font-weight: 800;
        color: #1f2d3d;
        margin: 0 0 6px 0;
    }

    .hero-stat-label {
        font-size: 13px;
        color: #607080;
        margin: 0;
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-left: 5px solid #2ecc71;
        padding: 24px;
        border-radius: 12px;
        margin: 16px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(46, 204, 113, 0.15);
    }
    
    /* Dashboard Card */
    .dashboard-card {
        background: white;
        border: 2px solid #ecf0f1;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    
    .dashboard-card:hover {
        border-color: #2ecc71;
        box-shadow: 0 4px 16px rgba(46, 204, 113, 0.1);
    }
    
    /* Button Styles */
    .btn-primary {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
    }
    
    /* Auth Card */
    .auth-card {
        background: white;
        border: 2px solid #ecf0f1;
        border-radius: 12px;
        padding: 40px;
        max-width: 400px;
        margin: 40px auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
    }
    
    .status-success {
        background: #d4edda;
        color: #155724;
    }
    
    .status-pending {
        background: #fff3cd;
        color: #664d03;
    }
    
    .status-active {
        background: #cfe2ff;
        color: #084298;
    }

    @media (max-width: 900px) {
        .hero-grid,
        .metric-strip {
            grid-template-columns: 1fr;
        }

        .top-strip {
            flex-direction: column;
            align-items: flex-start;
        }

        .hero-title {
            font-size: 38px;
        }

        .hero-section {
            padding: 32px 24px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "user" not in st.session_state:
    st.session_state.user = None

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "otp_code" not in st.session_state:
    st.session_state.otp_code = None

if "phone_temp" not in st.session_state:
    st.session_state.phone_temp = None


def go_to_page(page_name):
    """Centralized page switch helper."""
    st.session_state.page = page_name
    st.rerun()


def reset_auth_flow():
    """Clear transient OTP state when leaving auth screens."""
    st.session_state.otp_code = None
    st.session_state.phone_temp = None

# ============================================================================
# DATABASE HELPER FUNCTIONS
# ============================================================================

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_by_phone(phone):
    """Get user from database by phone"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, phone, name, role FROM users WHERE phone = ?",
                (phone,)
            )
            result = cursor.fetchone()
            return result
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        return None

def create_user(phone, name, role="farmer"):
    """Create new user in database"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (phone, name, role) VALUES (?, ?, ?)",
                (phone, name, role)
            )
            user_id = cursor.lastrowid
            conn.commit()
            
            # Create farmer profile if role is farmer
            if role == "farmer":
                cursor.execute(
                    "INSERT INTO farmer_profiles (user_id, full_name) VALUES (?, ?)",
                    (user_id, name)
                )
                conn.commit()
            
            return user_id
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return None

def generate_otp():
    """Generate random 6-digit OTP"""
    return ''.join([str(np.random.randint(0, 10)) for _ in range(6)])

def get_farmer_dashboard(user_id):
    """Get farmer's dashboard data"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get farmer profile
            cursor.execute(
                """SELECT id, full_name, state, district, village, land_size_acres, 
                          kyc_status, rating, total_deals FROM farmer_profiles 
                   WHERE user_id = ?""",
                (user_id,)
            )
            profile = cursor.fetchone()
            
            # Get active crops
            if profile:
                cursor.execute(
                    """SELECT id, crop_name, area_acres, status FROM crops 
                       WHERE farmer_id = ? AND status IN ('growing', 'ready_harvest')""",
                    (profile[0],)
                )
                crops = cursor.fetchall()
            else:
                crops = []
            
            # Get active listings
            cursor.execute(
                """SELECT id, quantity_kg, quality_grade, price_per_kg, status, created_at 
                   FROM listings WHERE farmer_id = ? AND status = 'active' 
                   ORDER BY created_at DESC LIMIT 5""",
                (user_id,)
            )
            listings = cursor.fetchall()
            
            return {
                "profile": profile,
                "crops": crops,
                "listings": listings
            }
    except Exception as e:
        logger.error(f"Error fetching dashboard: {e}")
        return {"profile": None, "crops": [], "listings": []}

# ============================================================================
# PAGE COMPONENTS
# ============================================================================

def page_landing():
    """Public landing page for the Streamlit deployment."""
    st.markdown("""
    <div class="top-strip">
        <div class="brand-lockup">
            <div class="brand-mark">🌾</div>
            <div>
                <h1 class="brand-title">CropPulse</h1>
                <p class="brand-subtitle">Agricultural Operating System</p>
            </div>
        </div>
        <div class="top-badge">Streamlit-first public app</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-section">
        <div class="hero-grid">
            <div>
                <div class="section-kicker">Agricultural intelligence and market coordination</div>
                <div class="hero-title">One public entry point for farmers, traders, and agri teams.</div>
                <div class="hero-subtitle">Landing page, onboarding, and working dashboards in a single Streamlit app.</div>
                <p class="hero-copy">
                    CropPulse helps farmers get market visibility, helps traders find supply faster, and gives agricultural teams
                    a single operating surface for crop intelligence, listings, and deal coordination.
                </p>
            </div>
            <div class="hero-panel">
                <h3>What you can do here</h3>
                <ul>
                    <li>Register farmers and traders from the same public app</li>
                    <li>Use one-host Streamlit deployment for landing, auth, and dashboard</li>
                    <li>Connect directly to SQLite locally or Railway PostgreSQL in production</li>
                    <li>Run without the FastAPI service in the active user path</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-strip">
        <div class="hero-stat">
            <p class="hero-stat-value">500+</p>
            <p class="hero-stat-label">Traders validated in Phase 1</p>
        </div>
        <div class="hero-stat">
            <p class="hero-stat-value">1 app</p>
            <p class="hero-stat-label">Landing, auth, and dashboard together</p>
        </div>
        <div class="hero-stat">
            <p class="hero-stat-value">2 DB modes</p>
            <p class="hero-stat-label">SQLite local, PostgreSQL in production</p>
        </div>
        <div class="hero-stat">
            <p class="hero-stat-value">0 API</p>
            <p class="hero-stat-label">Required in the active Streamlit path</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📍 Farmer Dashboard</h3>
            <p>
            Manage crops, track prices, find the best time to sell, and connect directly
            with buyers using one public app.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🛒 Smart Marketplace</h3>
            <p>
            Create listings, receive offers, negotiate prices, and coordinate deals
            without leaving the Streamlit flow.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>💡 Intelligence Feed</h3>
            <p>
            Daily weather forecasts, price trends, scheme visibility, and action-ready
            market guidance for field users.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Call to Action
    c1, c2, c3 = st.columns([1.2, 1.2, 1])
    with c1:
        if st.button("👨‍🌾 Create farmer account", use_container_width=True):
            reset_auth_flow()
            go_to_page("register")
    with c2:
        if st.button("🔐 Sign in to CropPulse", use_container_width=True):
            reset_auth_flow()
            go_to_page("login")
    with c3:
        st.caption("Deploy this file directly on Streamlit Cloud.")

    # Phase Info
    st.markdown("""
    ### Public deployment notes
    
    **This Streamlit app is the recommended public entrypoint:**
    - Landing page, onboarding, and dashboard live in one app
    - No FastAPI service is required in the active user journey
    - Database auto-initializes on first run
    - Ready for Streamlit Cloud with Railway PostgreSQL or local SQLite
    
    **Recommended deployment:** Streamlit Cloud for the app, PostgreSQL only for data.
    
    ---
    *©2026 CropPulse. Making agriculture smarter, fairer, and more profitable.*
    """)

def page_register():
    """Farmer Registration"""
    st.markdown("## 👨‍🌾 Create Farmer Account")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        
        # Step 1: Phone Registration
        st.subheader("Step 1: Phone Number")
        phone = st.text_input("📱 Phone Number (10 digits)", placeholder="9876543210")
        
        if st.button("Send OTP", use_container_width=True):
            if phone and len(phone) == 10 and phone.isdigit():
                # Check if user exists
                existing_user = get_user_by_phone(phone)
                if existing_user:
                    st.error("❌ This phone is already registered. Please login instead.")
                else:
                    # Generate and show OTP
                    otp = generate_otp()
                    st.session_state.otp_code = otp
                    st.session_state.phone_temp = phone
                    st.success(f"✅ OTP sent! (Demo: {otp})")
                    st.info("This Streamlit-only build shows a demo OTP on screen instead of using an API service.")
            else:
                st.error("❌ Please enter a valid 10-digit phone number")
        
        # Step 2: OTP Verification
        if st.session_state.otp_code:
            st.subheader("Step 2: Verify OTP")
            otp_input = st.text_input("🔐 Enter OTP", placeholder="123456")
            
            if otp_input and otp_input == st.session_state.otp_code:
                st.success("✅ OTP Verified!")
                
                # Step 3: Farmer Details
                st.subheader("Step 3: Your Details")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    name = st.text_input("Full Name", placeholder="John Farmer")
                
                with col_b:
                    state = st.selectbox("State", [
                        "Tamil Nadu", "Andhra Pradesh", "Karnataka", 
                        "Maharashtra", "Telangana", "Uttar Pradesh"
                    ])
                
                col_c, col_d = st.columns(2)
                with col_c:
                    district = st.text_input("District", placeholder="Madurai")
                
                with col_d:
                    village = st.text_input("Village", placeholder="Village Name")
                
                land_size = st.number_input("Land Size (acres)", min_value=0.5, value=1.0)
                soil_type = st.selectbox("Soil Type", [
                    "Black Soil", "Red Soil", "Alluvial", "Laterite", "Clay"
                ])
                
                if st.button("✅ Register Now", use_container_width=True):
                    if name and district and village:
                        user_id = create_user(st.session_state.phone_temp, name, "farmer")
                        if user_id:
                            # Update farmer profile
                            try:
                                with get_db_connection() as conn:
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        """UPDATE farmer_profiles 
                                           SET state = ?, district = ?, village = ?, 
                                               land_size_acres = ?, soil_type = ? 
                                           WHERE user_id = ?""",
                                        (state, district, village, land_size, soil_type, user_id)
                                    )
                                    conn.commit()
                            except Exception as e:
                                logger.error(f"Error updating profile: {e}")
                            
                            st.session_state.user = user_id
                            st.session_state.user_role = "farmer"
                            st.session_state.page = "dashboard"
                            st.success("✅ Registration successful!")
                            st.rerun()
                    else:
                        st.error("❌ Please fill all fields")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("← Back to Landing"):
            reset_auth_flow()
            go_to_page("landing")

def page_login():
    """Login Page"""
    st.markdown("## 🔐 Sign In")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        
        phone = st.text_input("📱 Phone Number", placeholder="9876543210")
        
        if st.button("Send OTP", use_container_width=True):
            if phone and len(phone) == 10:
                user = get_user_by_phone(phone)
                if user:
                    otp = generate_otp()
                    st.session_state.otp_code = otp
                    st.session_state.phone_temp = phone
                    st.success(f"✅ OTP sent! (Demo: {otp})")
                else:
                    st.error("❌ User not found. Please register first.")
        
        if st.session_state.otp_code:
            otp_input = st.text_input("🔐 Enter OTP")
            
            if otp_input and otp_input == st.session_state.otp_code:
                user = get_user_by_phone(st.session_state.phone_temp)
                st.session_state.user = user[0]
                st.session_state.user_role = user[3]
                st.session_state.page = "dashboard"
                st.success("✅ Login successful!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("← Back to Landing"):
            reset_auth_flow()
            go_to_page("landing")

def page_dashboard():
    """Main Dashboard for Farmers/Traders"""
    # Top Navigation
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        st.markdown("### 🌾 CropPulse Dashboard")
    
    with col4:
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.session_state.page = "landing"
            st.rerun()
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", "🌱 Crops", "🛒 Marketplace", "📡 Intelligence", "💰 Deals"
    ])
    
    with tab1:
        st.subheader("Your Dashboard")
        
        if st.session_state.user_role == "farmer":
            dashboard_data = get_farmer_dashboard(st.session_state.user)
            
            if dashboard_data["profile"]:
                profile = dashboard_data["profile"]
                
                # Profile Card
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4>👨 {profile[1]}</h4>
                        <p>📍 {profile[3]}, {profile[2]}</p>
                        <p>🌾 {profile[5]} acres</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4>⭐ Rating</h4>
                        <p style="font-size: 28px; color: #f39c12;">{profile[7]:.1f}</p>
                        <p>{profile[8]} deals completed</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    kyc_color = "🟢" if profile[6] == 'verified' else "🟡"
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4>📋 KYC Status</h4>
                        <p>{kyc_color} {profile[6].capitalize()}</p>
                        <p>Verified farmers get priority</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Active Crops
                if dashboard_data["crops"]:
                    st.subheader("🌱 Your Active Crops")
                    for crop in dashboard_data["crops"]:
                        st.markdown(f"""
                        <div class="dashboard-card">
                            <b>{crop[1]}</b> • {crop[2]} acres • Status: {crop[3]}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Recent Listings
                if dashboard_data["listings"]:
                    st.subheader("🛒 Your Recent Listings")
                    for listing in dashboard_data["listings"]:
                        st.markdown(f"""
                        <div class="dashboard-card">
                            📦 {listing[1]} kg • Grade: {listing[2]} • ₹{listing[3]}/kg
                            <br><span class="status-badge status-active">{listing[4]}</span>
                        </div>
                        """, unsafe_allow_html=True)
        
        else:  # Trader
            st.info("🧑‍💼 Trader Dashboard - View available listings and make offers")
    
    with tab2:
        st.subheader("🌱 Manage Your Crops")
        
        with st.form("crop_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                crop_name = st.selectbox("Crop", [
                    "Rice", "Wheat", "Corn", "Cotton", "Sugarcane", "Soybean"
                ])
                variety = st.text_input("Variety", placeholder="Sona Masuri")
            
            with col2:
                area = st.number_input("Area (acres)", min_value=0.1, value=1.0)
                soil_type = st.selectbox("Soil Type", [
                    "Black Soil", "Red Soil", "Alluvial", "Laterite"
                ])
            
            sowing_date = st.date_input("Sowing Date")
            harvest_date = st.date_input("Expected Harvest")
            
            if st.form_submit_button("✅ Add Crop"):
                st.success("✅ Crop added to your farm!")
    
    with tab3:
        st.subheader("🛒 Marketplace")
        st.info("📋 Create listings to connect with traders and get best prices")
        
        with st.form("listing_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                crop = st.selectbox("Select Crop", ["Rice", "Wheat", "Corn"])
                quantity = st.number_input("Quantity (kg)", min_value=100.0, value=1000.0)
            
            with col2:
                quality = st.selectbox("Quality Grade", ["A", "B", "C"])
                price = st.number_input("Price per kg (₹)", min_value=10.0, value=2000.0)
            
            available_from = st.date_input("Available From")
            available_until = st.date_input("Available Until")
            
            if st.form_submit_button("📤 Create Listing"):
                st.success("✅ Listing created! Traders can now see and make offers.")
    
    with tab4:
        st.subheader("📡 Market Intelligence Feed")
        
        # Weather Alert
        col1, col2 = st.columns([0.5, 2])
        with col1:
            st.markdown("🌦️")
        with col2:
            st.markdown("""
            **Heavy rainfall expected in Tamil Nadu**
            
            May 15-20: 60-80% rain expected. Reduce supply in next 2-3 weeks.
            """)
        
        st.divider()
        
        # Price Alert
        col1, col2 = st.columns([0.5, 2])
        with col1:
            st.markdown("📈")
        with col2:
            st.markdown("""
            **Best Time to Sell: Next 48 Hours**
            
            Price forecast: ₹2,650/kg (peak demand window). 
            Traders are actively buying premium rice.
            """)
        
        st.divider()
        
        # Scheme Alert
        col1, col2 = st.columns([0.5, 2])
        with col1:
            st.markdown("💰")
        with col2:
            st.markdown("""
            **PM-KISAN Subsidy Available**
            
            ₹6,000 annual payment now open for registration.
            Check your eligibility - takes 5 minutes.
            """)
    
    with tab5:
        st.subheader("💰 Your Active Deals")
        st.info("Track your ongoing transactions with traders")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Deals", 2)
        with col2:
            st.metric("Pending Payment", "₹45,000")
        with col3:
            st.metric("Completed This Month", 5)

# ============================================================================
# MAIN APP ROUTER
# ============================================================================

def main():
    """Main app router"""
    # Initialize schema before serving any page.
    init_database()

    if not test_connection():
        st.error("❌ Database connection failed. Please check your database configuration.")
        st.info("Use local SQLite for development or set DATABASE_URL for Streamlit Cloud production.")
        return
    
    # Route to appropriate page
    if st.session_state.page == "landing":
        page_landing()
    elif st.session_state.page == "register":
        page_register()
    elif st.session_state.page == "login":
        page_login()
    elif st.session_state.page == "dashboard" and st.session_state.user:
        page_dashboard()
    else:
        st.session_state.page = "landing"
        st.rerun()

if __name__ == "__main__":
    main()
