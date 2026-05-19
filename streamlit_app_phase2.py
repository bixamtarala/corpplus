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

    /* Landing Page */
    .landing-nav {
        display: grid;
        grid-template-columns: auto 1fr auto;
        align-items: center;
        gap: 28px;
        background: #ffffff;
        border: 1px solid #edf3f7;
        border-radius: 0;
        padding: 20px 34px;
        margin: 0 0 10px 0;
        box-shadow: 0 8px 20px rgba(31, 45, 61, 0.04);
    }

    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .nav-mark {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        color: white;
        background: linear-gradient(135deg, #1b98d2 0%, #67c658 100%);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.28);
    }

    .nav-wordmark {
        display: inline-flex;
        align-items: baseline;
        gap: 2px;
        font-size: 24px;
        font-weight: 800;
        line-height: 1;
        margin: 0;
    }

    .nav-wordmark-primary {
        color: #1490d2;
    }

    .nav-wordmark-secondary {
        color: #1f3151;
    }

    .nav-subtitle {
        font-size: 10px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #6f8498;
        margin: 3px 0 0 0;
    }

    .nav-menu {
        display: flex;
        justify-content: center;
        gap: 38px;
        flex-wrap: wrap;
    }

    .nav-menu a {
        color: #182635;
        text-decoration: none;
        font-size: 15px;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        white-space: nowrap;
    }

    .nav-menu-caret {
        font-size: 11px;
        color: #182635;
    }

    .nav-actions {
        display: flex;
        gap: 12px;
        justify-content: flex-end;
        flex-wrap: nowrap;
        align-items: center;
    }

    .nav-chip {
        color: #17324d;
        border-radius: 999px;
        padding: 11px 20px;
        font-size: 14px;
        font-weight: 700;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 122px;
        border: 1px solid #d6e4ee;
        background: #ffffff;
        box-shadow: 0 8px 20px rgba(31, 45, 61, 0.05);
    }

    .nav-chip.primary {
        background: #7acb57;
        border-color: #7acb57;
        color: white;
        min-width: 64px;
        width: 64px;
        height: 64px;
        padding: 0;
        font-size: 24px;
        box-shadow: 0 10px 24px rgba(122, 203, 87, 0.26);
    }

    .nav-chip.secondary {
        min-width: 116px;
        height: 64px;
        padding: 0 18px;
        font-size: 16px;
        font-weight: 800;
        gap: 10px;
        border-color: #edf1f5;
        box-shadow: 0 10px 24px rgba(31, 45, 61, 0.06);
    }

    .hero-section {
        background: linear-gradient(180deg, #ffffff 0%, #f4fbff 100%);
        border: 1px solid #e1eef5;
        border-radius: 34px;
        padding: 28px;
        margin: 0 0 26px 0;
        box-shadow: 0 22px 48px rgba(20, 52, 84, 0.08);
    }

    .hero-grid {
        display: grid;
        grid-template-columns: 1.05fr 1fr;
        gap: 34px;
        align-items: center;
    }

    .section-kicker {
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 12px;
        font-weight: 800;
        color: #1b8d59;
        margin-bottom: 14px;
    }
    
    .hero-title {
        font-size: 64px;
        font-weight: 800;
        line-height: 1.02;
        color: #193259;
        margin: 0 0 18px 0;
        max-width: 620px;
    }
    
    .hero-subtitle {
        font-size: 20px;
        font-weight: 500;
        line-height: 1.6;
        margin: 0 0 18px 0;
        color: #51657d;
        max-width: 600px;
    }

    .hero-copy {
        font-size: 17px;
        line-height: 1.7;
        color: #61768d;
        margin: 0 0 20px 0;
        max-width: 620px;
    }

    .hero-tags {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 12px;
    }

    .hero-tag {
        background: #eaf4ff;
        color: #325a8a;
        border-radius: 999px;
        padding: 10px 16px;
        font-size: 13px;
        font-weight: 700;
    }

    .hero-visual {
        position: relative;
        background: linear-gradient(180deg, #16233a 0%, #1d2d49 100%);
        border-radius: 24px;
        padding: 18px;
        min-height: 360px;
        box-shadow: 0 20px 50px rgba(10, 18, 34, 0.22);
        overflow: hidden;
    }

    .hero-visual::after {
        content: "";
        position: absolute;
        inset: auto -80px -120px auto;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(46,204,113,0.45) 0%, rgba(46,204,113,0) 70%);
    }

    .visual-top {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #8fa1bb;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .visual-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
    }

    .dot-red { background: #ff5f57; }
    .dot-yellow { background: #febc2e; }
    .dot-green { background: #28c840; }

    .visual-chart {
        background: linear-gradient(180deg, #284a79 0%, #233d63 100%);
        border: 1px solid rgba(140, 182, 235, 0.18);
        border-radius: 20px;
        padding: 20px;
        height: 140px;
        position: relative;
        overflow: hidden;
        margin-bottom: 16px;
    }

    .visual-chart::before {
        content: "";
        position: absolute;
        inset: 20px 18px 18px 18px;
        border-radius: 14px;
        background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0));
    }

    .chart-line {
        position: absolute;
        left: 16px;
        right: 16px;
        top: 24px;
        height: 4px;
        border-radius: 999px;
        background: linear-gradient(90deg, #7aa3d5 0%, #2ed0a1 45%, #8bb8f5 100%);
    }

    .chart-area {
        position: absolute;
        left: 18px;
        right: 18px;
        bottom: 18px;
        height: 68px;
        background: linear-gradient(180deg, rgba(46, 204, 113, 0.15), rgba(46, 204, 113, 0.04));
        clip-path: polygon(0% 85%, 14% 83%, 28% 80%, 42% 88%, 58% 60%, 74% 70%, 88% 38%, 100% 24%, 100% 100%, 0% 100%);
        border-radius: 12px;
    }

    .visual-grid {
        display: grid;
        grid-template-columns: 1.1fr 0.9fr;
        gap: 14px;
    }

    .visual-card,
    .floating-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 16px;
        color: white;
        position: relative;
        z-index: 1;
    }

    .visual-label {
        font-size: 14px;
        color: #9db2ce;
        margin-bottom: 8px;
    }

    .visual-value {
        font-size: 34px;
        font-weight: 800;
        line-height: 1.1;
        margin: 0 0 6px 0;
    }

    .visual-note {
        font-size: 13px;
        color: #b8cae2;
        margin: 0;
    }

    .floating-card {
        position: absolute;
        right: -18px;
        top: 160px;
        width: 190px;
        background: linear-gradient(180deg, #2fa84a 0%, #2c9c46 100%);
        box-shadow: 0 16px 30px rgba(25, 64, 25, 0.25);
    }

    .floating-card.secondary {
        top: 264px;
        right: -8px;
        background: white;
        color: #1f2d3d;
    }

    .floating-card.secondary .visual-label,
    .floating-card.secondary .visual-note {
        color: #5f7286;
    }

    .action-bar {
        margin: 18px 0 34px 0;
    }

    .section-shell {
        background: linear-gradient(180deg, #ffffff 0%, #f7fbff 100%);
        border: 1px solid #e2edf5;
        border-radius: 32px;
        padding: 34px;
        margin: 0 0 26px 0;
        box-shadow: 0 18px 44px rgba(20, 52, 84, 0.06);
    }

    .section-header {
        text-align: center;
        margin-bottom: 28px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #1c365c;
        margin: 0 0 10px 0;
    }

    .section-description {
        font-size: 18px;
        line-height: 1.7;
        color: #72859b;
        max-width: 860px;
        margin: 0 auto;
    }

    .card-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 24px;
    }

    .mini-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 18px;
        margin-bottom: 22px;
    }

    .workflow-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 24px;
    }

    .section-card,
    .workflow-card,
    .detail-card,
    .mini-card {
        background: white;
        border: 1px solid #dfeaf3;
        border-radius: 26px;
        padding: 28px;
        box-shadow: 0 14px 34px rgba(20, 52, 84, 0.06);
    }

    .section-card {
        min-height: 250px;
        display: flex;
        flex-direction: column;
    }

    .icon-badge {
        width: 56px;
        height: 56px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        background: linear-gradient(180deg, #eaf4ff 0%, #d8ebff 100%);
        margin-bottom: 16px;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        width: fit-content;
        border-radius: 999px;
        background: #eaf4ff;
        color: #40658f;
        padding: 8px 14px;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .section-card h3,
    .workflow-card h3,
    .detail-card h3,
    .mini-card h3 {
        font-size: 20px;
        color: #17324d;
        margin: 0 0 12px 0;
    }

    .section-card p,
    .workflow-card p,
    .detail-card p,
    .mini-card p {
        color: #5f7286;
        line-height: 1.75;
        font-size: 16px;
        margin: 0;
    }

    .section-card ul,
    .workflow-card ul,
    .detail-card ul {
        padding-left: 22px;
        margin: 16px 0 0 0;
        color: #4d6176;
        line-height: 1.85;
    }

    .workflow-card {
        border-top: 6px solid #44b2e8;
    }

    .workflow-card.alt {
        border-top-color: #d9a73a;
    }

    .feedback-card {
        background: white;
        border: 1px solid #dfeaf3;
        border-radius: 28px;
        padding: 26px;
        box-shadow: 0 14px 34px rgba(20, 52, 84, 0.06);
    }

    .feedback-row {
        display: grid;
        grid-template-columns: 1.4fr 0.8fr;
        gap: 22px;
        align-items: center;
    }

    .demo-shell {
        background: linear-gradient(135deg, #173d70 0%, #3387df 100%);
        border-radius: 32px;
        padding: 38px 34px;
        color: white;
        box-shadow: 0 20px 46px rgba(23, 61, 112, 0.24);
        margin-top: 8px;
    }

    .demo-title {
        font-size: 22px;
        font-weight: 800;
        margin: 0 0 12px 0;
        text-align: center;
    }

    .demo-copy {
        font-size: 17px;
        line-height: 1.75;
        max-width: 780px;
        margin: 0 auto 18px auto;
        text-align: center;
        color: rgba(255,255,255,0.86);
    }

    .demo-pills {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
    }

    .demo-pill {
        background: rgba(255,255,255,0.14);
        border-radius: 999px;
        padding: 10px 16px;
        font-size: 14px;
        font-weight: 700;
    }

    .landing-footer {
        text-align: center;
        color: #6a7f95;
        font-size: 14px;
        margin-top: 20px;
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
        .landing-nav,
        .hero-grid,
        .card-grid,
        .mini-grid,
        .workflow-grid,
        .feedback-row,
        .visual-grid {
            grid-template-columns: 1fr;
        }

        .landing-nav,
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

        .nav-menu,
        .nav-actions {
            justify-content: flex-start;
        }

        .nav-chip.primary {
            width: auto;
            min-width: 122px;
            height: auto;
            padding: 11px 20px;
            font-size: 14px;
        }

        .nav-chip.secondary {
            height: auto;
            padding: 11px 20px;
        }

        .floating-card,
        .floating-card.secondary {
            position: static;
            width: auto;
            margin-top: 14px;
        }

        .section-shell,
        .feedback-card,
        .demo-shell {
            padding: 24px;
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


def enter_demo_mode():
    """Open the dashboard in lightweight demo mode."""
    reset_auth_flow()
    st.session_state.user = -1
    st.session_state.user_role = "farmer"
    st.session_state.page = "dashboard"
    st.rerun()

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
    landing_action = st.query_params.get("action")
    if landing_action == "login":
        st.query_params.clear()
        reset_auth_flow()
        go_to_page("login")
    if landing_action == "register":
        st.query_params.clear()
        reset_auth_flow()
        go_to_page("register")
    if landing_action == "demo":
        st.query_params.clear()
        enter_demo_mode()

    st.markdown("""
    <div class="landing-nav">
        <div class="nav-brand">
            <div class="nav-mark">🌾</div>
            <div>
                <p class="nav-wordmark"><span class="nav-wordmark-primary">Crop</span><span class="nav-wordmark-secondary">Pulse</span></p>
                <p class="nav-subtitle">Agricultural intelligence</p>
            </div>
        </div>
        <div class="nav-menu">
            <a href="#features">Products <span class="nav-menu-caret">&#9662;</span></a>
            <a href="#workflows">Industry <span class="nav-menu-caret">&#9662;</span></a>
            <a href="#trust">Solutions <span class="nav-menu-caret">&#9662;</span></a>
            <a href="#demo">Crop Knowledge Grid</a>
            <a href="#demo">Resources <span class="nav-menu-caret">&#9662;</span></a>
            <a href="#demo">Company <span class="nav-menu-caret">&#9662;</span></a>
        </div>
        <div class="nav-actions">
            <a class="nav-chip primary" href="?action=demo">&#8981;</a>
            <a class="nav-chip secondary" href="?action=login">&#127760; <span>Login</span> <span class="nav-menu-caret">&#9662;</span></a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-section">
        <div class="hero-grid">
            <div>
                <div class="section-kicker">Agricultural intelligence and market coordination</div>
                <div class="hero-title">Know when to sell. Find supply faster. Coordinate every farm move.</div>
                <div class="hero-subtitle">CropPulse brings price visibility, crop planning, marketplace activity, and deal coordination into one clean operating surface.</div>
                <p class="hero-copy">
                    Built for farmers, traders, and agricultural teams that need faster decisions, fewer calls, clearer market signals, and stronger execution across the value chain.
                </p>
                <div class="hero-tags">
                    <span class="hero-tag">Best time to sell</span>
                    <span class="hero-tag">Verified trader access</span>
                    <span class="hero-tag">Crop and listing management</span>
                </div>
            </div>
            <div class="hero-visual">
                <div class="visual-top">
                    <span class="visual-dot dot-red"></span>
                    <span class="visual-dot dot-yellow"></span>
                    <span class="visual-dot dot-green"></span>
                    <span>LIVE MARKET WORKSPACE</span>
                </div>
                <div class="visual-chart">
                    <div class="chart-line"></div>
                    <div class="chart-area"></div>
                </div>
                <div class="visual-grid">
                    <div class="visual-card">
                        <div class="visual-label">Best selling window</div>
                        <p class="visual-value">48 hrs</p>
                        <p class="visual-note">Demand is strongest for premium rice in nearby districts.</p>
                    </div>
                    <div class="visual-card">
                        <div class="visual-label">Buyer activity</div>
                        <p class="visual-value">High</p>
                        <p class="visual-note">More verified traders are actively searching today.</p>
                    </div>
                </div>
                <div class="floating-card">
                    <div class="visual-label">Signal confidence</div>
                    <p class="visual-value">Active</p>
                    <p class="visual-note">Price momentum and buying interest are aligned.</p>
                </div>
                <div class="floating-card secondary">
                    <div class="visual-label">Watchlist priority</div>
                    <p class="visual-value" style="font-size: 24px; color: #17324d;">Rice buyers</p>
                    <p class="visual-note">Shortlist refreshed with stronger district demand.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div id="features" class="section-shell">
        <div class="section-header">
            <p class="section-title">Platform features</p>
            <p class="section-description">Everything needed for daily agricultural decisions, from crop planning and pricing visibility to marketplace action and deal follow-through.</p>
        </div>
        <div class="card-grid">
            <div class="section-card">
                <div class="icon-badge">📈</div>
                <h3>Price intelligence</h3>
                <p>Track market movement, demand spikes, and high-value selling windows without relying on scattered updates.</p>
                <div class="pill">Live market visibility</div>
            </div>
            <div class="section-card">
                <div class="icon-badge">🌱</div>
                <h3>Crop planning</h3>
                <p>Manage crop details, field timelines, and harvest readiness in one place so operational decisions stay current.</p>
                <div class="pill">Farmer workflow</div>
            </div>
            <div class="section-card">
                <div class="icon-badge">🛒</div>
                <h3>Marketplace coordination</h3>
                <p>Create listings, receive offers, compare buyers, and keep negotiations moving inside a shared workflow.</p>
                <div class="pill">Listing to deal flow</div>
            </div>
            <div class="section-card">
                <div class="icon-badge">📍</div>
                <h3>Trader sourcing</h3>
                <p>Help traders discover supply faster through verified listings, location context, and crop availability visibility.</p>
                <div class="pill">Verified network</div>
            </div>
            <div class="section-card">
                <div class="icon-badge">🤝</div>
                <h3>Deal management</h3>
                <p>Keep active deals visible from first offer to final coordination so follow-up and payment steps do not get lost.</p>
                <div class="pill">Execution support</div>
            </div>
            <div class="section-card">
                <div class="icon-badge">🌦️</div>
                <h3>Weather and scheme alerts</h3>
                <p>Surface field-relevant weather events, subsidy programs, and action-ready updates that affect real decisions.</p>
                <div class="pill">Action-ready alerts</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div id="workflows" class="section-shell">
        <div class="section-header">
            <p class="section-title">Built for both sides of the market</p>
            <p class="section-description">CropPulse supports farmer action, trader sourcing, and agri-team coordination without forcing everyone into the same workflow.</p>
        </div>
        <div class="workflow-grid">
            <div class="workflow-card">
                <div class="pill">👨‍🌾 Simplified farmer view</div>
                <h3>Farmer workflow</h3>
                <p>Designed for producers who need clear next steps, cleaner market visibility, and an easier path from crop readiness to buyer connection.</p>
                <ul>
                    <li>Best-time-to-sell guidance</li>
                    <li>Crop and harvest planning</li>
                    <li>Simple listing and offer flow</li>
                    <li>Clear alerts and next actions</li>
                </ul>
            </div>
            <div class="workflow-card alt">
                <div class="pill">🧑‍💼 Trader and agri team desk</div>
                <h3>Buyer and coordination workflow</h3>
                <p>Designed for professionals who need stronger sourcing visibility, easier supply discovery, and a structured way to track ongoing opportunities.</p>
                <ul>
                    <li>Verified supply discovery</li>
                    <li>Regional demand and price context</li>
                    <li>Deal follow-up and coordination</li>
                    <li>Faster buyer shortlisting</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div id="trust" class="section-shell">
        <div class="section-header">
            <p class="section-title">Trusted and structured for real agricultural operations</p>
            <p class="section-description">The landing experience should feel credible. These are the pillars that make CropPulse useful for serious field, market, and operational use.</p>
        </div>
        <div class="card-grid">
            <div class="section-card">
                <div class="icon-badge">✅</div>
                <h3>Verified participants</h3>
                <p>Profiles, listings, and interactions are built around trust so buyers and sellers can work with stronger confidence.</p>
            </div>
            <div class="section-card">
                <div class="icon-badge">🔐</div>
                <h3>Protected access</h3>
                <p>Authentication and account flows are structured to support reliable access for production users and future scaling.</p>
            </div>
            <div class="section-card">
                <div class="icon-badge">📋</div>
                <h3>Decision records</h3>
                <p>Listings, crop entries, offers, and market signals stay visible in one system instead of disappearing across calls and chats.</p>
            </div>
            <div class="section-card">
                <div class="icon-badge">🛡️</div>
                <h3>Privacy aware</h3>
                <p>Farmer and marketplace data should be easy to use operationally without exposing more than the workflow actually needs.</p>
            </div>
            <div class="section-card">
                <div class="icon-badge">📡</div>
                <h3>Field-relevant intelligence</h3>
                <p>Weather, schemes, demand, and pricing signals are placed inside the workflow so users can act instead of just reading updates.</p>
            </div>
            <div class="section-card">
                <div class="icon-badge">⚙️</div>
                <h3>Operational focus</h3>
                <p>The product is organized around daily action: monitor, list, negotiate, coordinate, and decide faster with less friction.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-shell">
        <div class="section-header">
            <p class="section-title">Why choose CropPulse?</p>
            <p class="section-description">The landing page in your screenshots is strong because it layers proof, workflows, trust, and calls to action. CropPulse now follows that same structure with agriculture-specific value.</p>
        </div>
        <div class="mini-grid">
            <div class="mini-card">
                <h3>Action-first</h3>
                <p>Decision support is tied to pricing, crops, and live marketplace movement.</p>
            </div>
            <div class="mini-card">
                <h3>Market-aware</h3>
                <p>Context is built around buyers, supply, timing, and negotiation readiness.</p>
            </div>
            <div class="mini-card">
                <h3>Operationally useful</h3>
                <p>The homepage leads directly into real workflows instead of static marketing copy.</p>
            </div>
        </div>
        <div class="card-grid">
            <div class="detail-card">
                <div class="pill">Better selling signals</div>
                <h3>Know what to do next</h3>
                <p>Move beyond generic price tables with signals that help farmers and teams understand when the market is strong and why timing matters.</p>
                <ul>
                    <li>Explainable market confidence</li>
                    <li>Cleaner next-step guidance</li>
                    <li>Less noise, more usable clarity</li>
                </ul>
            </div>
            <div class="detail-card">
                <div class="pill">Stronger negotiation discipline</div>
                <h3>Avoid weak deals</h3>
                <p>See opportunities in context with demand, location, crop readiness, and supply signals before making a pricing move.</p>
                <ul>
                    <li>Buyer and supply awareness</li>
                    <li>District-level market context</li>
                    <li>Smarter offer comparison</li>
                </ul>
            </div>
            <div class="detail-card">
                <div class="pill">Faster coordination</div>
                <h3>Move opportunities sooner</h3>
                <p>Compress scattered communication into one cleaner loop so listings, offers, and follow-up actions stay aligned.</p>
                <ul>
                    <li>Quicker marketplace response</li>
                    <li>Less manual follow-up overhead</li>
                    <li>More time spent closing deals</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-shell">
        <div class="section-header">
            <p class="section-title">Help shape CropPulse</p>
            <p class="section-description">A strong landing page should not end with static testimonials. It should show how users can respond, give feedback, and move directly into the product.</p>
        </div>
        <div class="feedback-card">
            <div class="feedback-row">
                <div>
                    <div class="pill">Feedback channel</div>
                    <h3 style="margin-top: 0;">Tell us what should improve next</h3>
                    <p>Use this channel to share where the workflow feels strong, where clarity is missing, and which farmer, trader, or intelligence tools you want improved next.</p>
                </div>
                <div>
                    <div class="pill">Product improvement</div>
                    <p style="margin-bottom: 16px;">Email the team at <strong>support@croppulse.ai</strong> or continue directly into the live product flow below.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div id="demo" class="demo-shell">
        <div class="pill" style="margin: 0 auto 16px auto; background: rgba(255,255,255,0.14); color: white;">Step into the live product flow</div>
        <p class="demo-title">Explore the interactive CropPulse demo</p>
        <p class="demo-copy">See how CropPulse turns crop data, market prices, buyer activity, and field alerts into clearer agricultural decisions without leaving the homepage experience.</p>
        <div class="demo-pills">
            <span class="demo-pill">No signup required for demo</span>
            <span class="demo-pill">Fast dashboard access</span>
            <span class="demo-pill">Built for farmers and traders</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    demo_left, demo_center, demo_right = st.columns([1.2, 1.4, 1.2])
    with demo_center:
        st.markdown("### Continue into the live demo")
        st.caption("Add your email if you want it carried into future follow-up, or continue directly to explore the product workflow.")
        st.text_input("Work email", placeholder="your@email.com", key="landing_demo_email")
        demo_action1, demo_action2 = st.columns(2)
        with demo_action1:
            if st.button("Continue to demo", key="landing_demo_continue", use_container_width=True):
                enter_demo_mode()
        with demo_action2:
            if st.button("Create account", key="landing_demo_register", use_container_width=True):
                reset_auth_flow()
                go_to_page("register")

    st.markdown('<p class="landing-footer">©2026 CropPulse. Agricultural intelligence, marketplace visibility, and operational coordination in one platform.</p>', unsafe_allow_html=True)

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

            if st.session_state.user == -1:
                st.info("You are viewing CropPulse in demo mode. Create an account to save crops, listings, and deals.")

                demo_col1, demo_col2, demo_col3 = st.columns(3)

                with demo_col1:
                    st.markdown("""
                    <div class="dashboard-card">
                        <h4>📈 Best Time to Sell</h4>
                        <p style="font-size: 28px; color: #27ae60;">Next 48 hours</p>
                        <p>Buyer demand is strongest for premium rice.</p>
                    </div>
                    """, unsafe_allow_html=True)

                with demo_col2:
                    st.markdown("""
                    <div class="dashboard-card">
                        <h4>🛒 Active Buyer Interest</h4>
                        <p style="font-size: 28px; color: #3498db;">12 traders</p>
                        <p>Verified buyers are watching nearby supply.</p>
                    </div>
                    """, unsafe_allow_html=True)

                with demo_col3:
                    st.markdown("""
                    <div class="dashboard-card">
                        <h4>🌦️ Weather Watch</h4>
                        <p style="font-size: 28px; color: #f39c12;">Rain alert</p>
                        <p>Prepare harvest logistics in the next 3 days.</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("""
                <div class="dashboard-card">
                    <h4>Demo overview</h4>
                    <p>Use the tabs above to explore crop management, marketplace listings, intelligence alerts, and deal tracking in the current Streamlit flow.</p>
                </div>
                """, unsafe_allow_html=True)
            
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
