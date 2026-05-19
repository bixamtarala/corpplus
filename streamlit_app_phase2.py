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
from urllib.parse import urlencode
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
    .landing-header-shell {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(8px);
        box-shadow: 0 10px 22px rgba(31, 45, 61, 0.06);
    }

    .landing-header-spacer {
        height: 132px;
    }

    .promo-bar {
        background: linear-gradient(90deg, #0a2f1f 0%, #0f3c29 100%);
        color: rgba(255, 255, 255, 0.92);
        text-align: center;
        font-size: 14px;
        font-weight: 600;
        padding: 10px 24px;
        margin: 0;
    }

    .landing-header-shell a,
    .hero-section a,
    .section-shell a,
    .demo-shell a,
    .landing-footer a,
    .landing-header-shell a:hover,
    .hero-section a:hover,
    .section-shell a:hover,
    .demo-shell a:hover,
    .landing-footer a:hover,
    .landing-header-shell a:focus,
    .hero-section a:focus,
    .section-shell a:focus,
    .demo-shell a:focus,
    .landing-footer a:focus,
    .landing-header-shell a:visited,
    .hero-section a:visited,
    .section-shell a:visited,
    .demo-shell a:visited,
    .landing-footer a:visited {
        text-decoration: none !important;
    }

    .promo-bar a {
        color: #ffffff;
        font-weight: 800;
    }

    .landing-nav {
        display: grid;
        grid-template-columns: auto minmax(0, 1fr) auto;
        align-items: center;
        gap: 20px;
        background: #ffffff;
        border: 1px solid #edf3f7;
        border-radius: 0;
        padding: 20px 28px;
        margin: 0 0 10px 0;
        box-shadow: 0 8px 20px rgba(31, 45, 61, 0.04);
    }

    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: max-content;
    }

    .nav-brand-copy {
        display: flex;
        align-items: center;
    }

    .nav-mark {
        width: 50px;
        height: 50px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
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

    .nav-menu {
        display: flex;
        justify-content: center;
        gap: 26px;
        flex-wrap: nowrap;
        min-width: 0;
        position: relative;
        overflow: visible;
    }

    .nav-item {
        position: relative;
        display: flex;
        align-items: center;
    }

    .nav-item::after {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        top: 100%;
        height: 14px;
    }

    .nav-link {
        color: #182635;
        font-size: 13px;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        white-space: nowrap;
        cursor: default;
    }

    .nav-item.active .nav-link {
        color: #1f8f4d;
        font-weight: 700;
    }

    .nav-menu-caret {
        font-size: 11px;
        color: #182635;
    }

    .nav-item.active .nav-menu-caret {
        color: #1f8f4d;
    }

    .nav-dropdown {
        position: absolute;
        top: calc(100% + 8px);
        left: 50%;
        transform: translateX(-50%) translateY(10px);
        min-width: 300px;
        background: #ffffff;
        border: 1px solid #e8eff4;
        box-shadow: 0 18px 36px rgba(31, 45, 61, 0.1);
        border-radius: 20px;
        padding: 22px;
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transition: opacity 0.18s ease, transform 0.18s ease, visibility 0.18s ease;
        z-index: 1005;
    }

    .nav-dropdown.mega {
        width: 760px;
        max-width: min(760px, 78vw);
    }

    .nav-dropdown.compact {
        width: 360px;
        max-width: min(360px, 78vw);
    }

    .nav-item:hover .nav-dropdown,
    .nav-item:focus-within .nav-dropdown {
        opacity: 1;
        visibility: visible;
        pointer-events: auto;
        transform: translateX(-50%) translateY(0);
    }

    .dropdown-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 18px 20px;
    }

    .dropdown-list {
        display: grid;
        gap: 14px;
    }

    .dropdown-item {
        display: flex;
        gap: 12px;
        align-items: flex-start;
        text-decoration: none;
        padding: 8px;
        border-radius: 14px;
    }

    .dropdown-item:hover {
        background: #f6fbf8;
    }

    .dropdown-icon {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #edf8f1;
        color: #1f8f4d;
        font-size: 22px;
        flex: 0 0 auto;
    }

    .dropdown-item h4 {
        font-size: 16px;
        color: #1b2c3a;
        margin: 0 0 5px 0;
        font-weight: 700;
    }

    .dropdown-item p {
        margin: 0;
        font-size: 13px;
        line-height: 1.45;
        color: #556979;
    }

    .nav-actions {
        display: flex;
        gap: 10px;
        justify-content: flex-end;
        flex-wrap: nowrap;
        align-items: center;
        min-width: max-content;
    }

    .language-toggle {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px;
        border-radius: 999px;
        background: #f5f8fb;
        border: 1px solid #e2eaf0;
    }

    .language-pill {
        text-decoration: none !important;
        color: #36506a;
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        line-height: 1;
    }

    .language-pill.active {
        background: #1f8f4d;
        color: white;
    }

    .nav-chip {
        color: #17324d;
        border-radius: 999px;
        padding: 11px 20px;
        font-size: 14px;
        font-weight: 700;
        text-decoration: none !important;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 122px;
        border: 1px solid #d6e4ee;
        background: #ffffff;
        box-shadow: 0 8px 20px rgba(31, 45, 61, 0.05);
    }

    .nav-chip:hover,
    .nav-chip:focus,
    .nav-chip:active,
    .nav-chip:visited,
    .nav-chip span {
        text-decoration: none !important;
    }

    .nav-chip.primary {
        background: #7acb57;
        border-color: #7acb57;
        color: white;
        min-width: 56px;
        width: 56px;
        height: 56px;
        padding: 0;
        font-size: 20px;
        box-shadow: 0 10px 24px rgba(122, 203, 87, 0.26);
    }

    .nav-chip.secondary {
        min-width: 108px;
        height: 56px;
        padding: 0 16px;
        font-size: 14px;
        font-weight: 800;
        gap: 8px;
        border-color: #edf1f5;
        box-shadow: 0 10px 24px rgba(31, 45, 61, 0.06);
    }

    .hero-section {
        background: linear-gradient(180deg, #ffffff 0%, #f4fbff 100%);
        border: 1px solid #e1eef5;
        border-radius: 34px;
        padding: 24px;
        margin: 0 0 26px 0;
        box-shadow: 0 22px 48px rgba(20, 52, 84, 0.08);
    }

    .hero-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 18px;
        align-items: flex-start;
        max-width: 1040px;
        margin: 0 auto;
    }

    .section-kicker {
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 11px;
        font-weight: 800;
        color: #1b8d59;
        margin-bottom: 12px;
    }
    
    .hero-title {
        font-size: 48px;
        font-weight: 800;
        line-height: 1.08;
        color: #193259;
        margin: 0 0 14px 0;
        max-width: none;
    }
    
    .hero-subtitle {
        font-size: 18px;
        font-weight: 500;
        line-height: 1.55;
        margin: 0 0 14px 0;
        color: #51657d;
        max-width: none;
    }

    .hero-copy {
        font-size: 15px;
        line-height: 1.65;
        color: #61768d;
        margin: 0 0 18px 0;
        max-width: none;
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
        padding: 8px 14px;
        font-size: 12px;
        font-weight: 700;
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
        .visual-grid,
        .dropdown-grid {
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

        .nav-menu {
            flex-wrap: wrap;
        }

        .nav-dropdown,
        .nav-dropdown.mega,
        .nav-dropdown.compact {
            position: static;
            width: 100%;
            max-width: 100%;
            min-width: 0;
            margin-top: 12px;
            transform: none;
            opacity: 1;
            visibility: visible;
            pointer-events: auto;
            display: none;
        }

        .nav-item:hover .nav-dropdown,
        .nav-item:focus-within .nav-dropdown {
            display: block;
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

        .promo-bar {
            margin-left: -2rem;
            margin-right: -2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            font-size: 12px;
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

if "language" not in st.session_state:
    st.session_state.language = "en"

if "landing_panel" not in st.session_state:
    st.session_state.landing_panel = None


TRANSLATIONS = {
    "en": {
        "lang_en": "EN",
        "lang_te": "తెలుగు",
        "language_label": "Language",
        "language_english": "English",
        "language_telugu": "Telugu",
        "promo_bar": "Turn farm data into ROI.",
        "invite_link": "Invite CropPulse",
        "promo_suffix": "to your AI and digital transformation workflow.",
        "nav_products": "Products",
        "nav_industry": "Industry",
        "nav_solutions": "Solutions",
        "nav_crop_knowledge": "Crop Intelligence",
        "nav_resources": "Resources",
        "nav_company": "Company",
        "nav_user": "User",
        "nav_language": "Language",
        "login": "Login",
        "price_intelligence": "Price Intelligence",
        "price_intelligence_desc": "Daily market signals, price visibility, and selling windows.",
        "farmer_os": "Farmer OS",
        "farmer_os_desc": "Crop tracking, harvest planning, and farmer workflows.",
        "marketplace": "Marketplace",
        "marketplace_desc": "Listings, offers, negotiations, and deal coordination.",
        "crop_rice_desc": "Price signals, demand trends, and trading visibility for rice markets.",
        "crop_wheat_desc": "Crop and market intelligence for wheat production and selling windows.",
        "crop_corn_desc": "Planning and buyer visibility for corn supply and harvest movement.",
        "crop_cotton_desc": "Field updates and market context for cotton growers and buyers.",
        "crop_sugarcane_desc": "Operational and pricing support for sugarcane farmers and trade flows.",
        "crop_soybean_desc": "Supply tracking and market awareness for soybean production and sales.",
        "food_retail": "Food Retail",
        "food_retail_desc": "Intelligent sourcing for a smarter, more sustainable food retail future.",
        "cpg_fmcg": "CPG/FMCG",
        "cpg_fmcg_desc": "AI support for supply leaders managing food production and procurement.",
        "seed_manufacturing": "Seed Manufacturing",
        "seed_manufacturing_desc": "Field intelligence, forecasting, and scale-ready seed operations.",
        "governments": "Governments",
        "governments_desc": "Traceable agricultural visibility for public-sector coordination and programs.",
        "food_processing": "Food Processing",
        "food_processing_desc": "Digitized farm operations and end-to-end processing traceability.",
        "agri_teams": "Agri Teams",
        "agri_teams_desc": "Shared workflow for sourcing, monitoring, and coordination teams.",
        "verified_network": "Verified Network",
        "verified_network_desc": "Profiles and participant trust for cleaner buyer-seller interactions.",
        "protected_access": "Protected Access",
        "protected_access_desc": "Reliable access, account flows, and future-ready authentication.",
        "operational_focus": "Operational Focus",
        "operational_focus_desc": "Built for monitoring, listing, negotiating, and deciding faster.",
        "crop_signals": "Crop Signals",
        "crop_signals_desc": "Weather, readiness, and market context across crop cycles.",
        "decision_guidance": "Decision Guidance",
        "decision_guidance_desc": "Use intelligence layers to improve timing and action quality.",
        "guides": "Guides",
        "guides_desc": "Product walkthroughs and onboarding help for new users.",
        "case_examples": "Case Examples",
        "case_examples_desc": "See how teams use pricing, crop, and marketplace workflows.",
        "about_croppulse": "About CropPulse",
        "about_croppulse_desc": "Why we are building agricultural intelligence and coordination tools.",
        "contact": "Contact",
        "contact_desc": "Reach the team for product access, demos, and partnerships.",
        "user_farmer": "Farmer",
        "user_farmer_desc": "Crop planning, selling guidance, and farm workflow tools for producers.",
        "user_traders": "Traders",
        "user_traders_desc": "Supply discovery, buyer visibility, and faster deal coordination for traders.",
        "user_fpo": "FPO",
        "user_fpo_desc": "Aggregation, coordination, and member support tools for farmer producer organizations.",
        "language_english_desc": "Switch the landing page and app into English.",
        "language_telugu_desc": "Switch the landing page and app into Telugu.",
        "section_kicker": "Agricultural intelligence and market coordination",
        "hero_title": "Know when to sell. Find supply faster. Coordinate every farm move.",
        "hero_subtitle": "CropPulse brings price visibility, crop planning, marketplace activity, and deal coordination into one clean operating surface.",
        "hero_copy": "Built for farmers, traders, and agricultural teams that need faster decisions, fewer calls, clearer market signals, and stronger execution across the value chain.",
        "tag_sell": "Best time to sell",
        "tag_trader": "Verified trader access",
        "tag_listing": "Crop and listing management",
        "live_market_workspace": "LIVE MARKET WORKSPACE",
        "best_selling_window": "Best selling window",
        "demand_desc": "Demand is strongest for premium rice in nearby districts.",
        "buyer_activity": "Buyer activity",
        "high": "High",
        "buyer_activity_desc": "More verified traders are actively searching today.",
        "signal_confidence": "Signal confidence",
        "active": "Active",
        "signal_confidence_desc": "Price momentum and buying interest are aligned.",
        "watchlist_priority": "Watchlist priority",
        "rice_buyers": "Rice buyers",
        "watchlist_priority_desc": "Shortlist refreshed with stronger district demand.",
        "platform_features": "Platform features",
        "platform_features_desc": "Everything needed for daily agricultural decisions, from crop planning and pricing visibility to marketplace action and deal follow-through.",
        "feature_price_title": "Price intelligence",
        "feature_price_desc": "Track market movement, demand spikes, and high-value selling windows without relying on scattered updates.",
        "pill_live_market": "Live market visibility",
        "feature_crop_title": "Crop planning",
        "feature_crop_desc": "Manage crop details, field timelines, and harvest readiness in one place so operational decisions stay current.",
        "pill_farmer_workflow": "Farmer workflow",
        "feature_market_title": "Marketplace coordination",
        "feature_market_desc": "Create listings, receive offers, compare buyers, and keep negotiations moving inside a shared workflow.",
        "pill_listing_flow": "Listing to deal flow",
        "feature_trader_title": "Trader sourcing",
        "feature_trader_desc": "Help traders discover supply faster through verified listings, location context, and crop availability visibility.",
        "pill_verified_network": "Verified network",
        "feature_deal_title": "Deal management",
        "feature_deal_desc": "Keep active deals visible from first offer to final coordination so follow-up and payment steps do not get lost.",
        "pill_execution_support": "Execution support",
        "feature_weather_title": "Weather and scheme alerts",
        "feature_weather_desc": "Surface field-relevant weather events, subsidy programs, and action-ready updates that affect real decisions.",
        "pill_action_ready": "Action-ready alerts",
        "workflows_title": "Built for both sides of the market",
        "workflows_desc": "CropPulse supports farmer action, trader sourcing, and agri-team coordination without forcing everyone into the same workflow.",
        "farmer_view": "👨‍🌾 Simplified farmer view",
        "farmer_workflow": "Farmer workflow",
        "farmer_workflow_desc": "Designed for producers who need clear next steps, cleaner market visibility, and an easier path from crop readiness to buyer connection.",
        "farmer_b1": "Best-time-to-sell guidance",
        "farmer_b2": "Crop and harvest planning",
        "farmer_b3": "Simple listing and offer flow",
        "farmer_b4": "Clear alerts and next actions",
        "trader_desk": "🧑‍💼 Trader and agri team desk",
        "buyer_workflow": "Buyer and coordination workflow",
        "buyer_workflow_desc": "Designed for professionals who need stronger sourcing visibility, easier supply discovery, and a structured way to track ongoing opportunities.",
        "buyer_b1": "Verified supply discovery",
        "buyer_b2": "Regional demand and price context",
        "buyer_b3": "Deal follow-up and coordination",
        "buyer_b4": "Faster buyer shortlisting",
        "trust_title": "Trusted and structured for real agricultural operations",
        "trust_desc": "The landing experience should feel credible. These are the pillars that make CropPulse useful for serious field, market, and operational use.",
        "trust_card_1": "Verified participants",
        "trust_card_1_desc": "Profiles, listings, and interactions are built around trust so buyers and sellers can work with stronger confidence.",
        "trust_card_2": "Protected access",
        "trust_card_2_desc": "Authentication and account flows are structured to support reliable access for production users and future scaling.",
        "trust_card_3": "Decision records",
        "trust_card_3_desc": "Listings, crop entries, offers, and market signals stay visible in one system instead of disappearing across calls and chats.",
        "trust_card_4": "Privacy aware",
        "trust_card_4_desc": "Farmer and marketplace data should be easy to use operationally without exposing more than the workflow actually needs.",
        "trust_card_5": "Field-relevant intelligence",
        "trust_card_5_desc": "Weather, schemes, demand, and pricing signals are placed inside the workflow so users can act instead of just reading updates.",
        "trust_card_6": "Operational focus",
        "trust_card_6_desc": "The product is organized around daily action: monitor, list, negotiate, coordinate, and decide faster with less friction.",
        "why_title": "Why choose CropPulse?",
        "why_desc": "The landing page in your screenshots is strong because it layers proof, workflows, trust, and calls to action. CropPulse now follows that same structure with agriculture-specific value.",
        "mini_1": "Action-first",
        "mini_1_desc": "Decision support is tied to pricing, crops, and live marketplace movement.",
        "mini_2": "Market-aware",
        "mini_2_desc": "Context is built around buyers, supply, timing, and negotiation readiness.",
        "mini_3": "Operationally useful",
        "mini_3_desc": "The homepage leads directly into real workflows instead of static marketing copy.",
        "detail_pill_1": "Better selling signals",
        "detail_title_1": "Know what to do next",
        "detail_desc_1": "Move beyond generic price tables with signals that help farmers and teams understand when the market is strong and why timing matters.",
        "detail_1_b1": "Explainable market confidence",
        "detail_1_b2": "Cleaner next-step guidance",
        "detail_1_b3": "Less noise, more usable clarity",
        "detail_pill_2": "Stronger negotiation discipline",
        "detail_title_2": "Avoid weak deals",
        "detail_desc_2": "See opportunities in context with demand, location, crop readiness, and supply signals before making a pricing move.",
        "detail_2_b1": "Buyer and supply awareness",
        "detail_2_b2": "District-level market context",
        "detail_2_b3": "Smarter offer comparison",
        "detail_pill_3": "Faster coordination",
        "detail_title_3": "Move opportunities sooner",
        "detail_desc_3": "Compress scattered communication into one cleaner loop so listings, offers, and follow-up actions stay aligned.",
        "detail_3_b1": "Quicker marketplace response",
        "detail_3_b2": "Less manual follow-up overhead",
        "detail_3_b3": "More time spent closing deals",
        "help_title": "Help shape CropPulse",
        "help_desc": "A strong landing page should not end with static testimonials. It should show how users can respond, give feedback, and move directly into the product.",
        "feedback_channel": "Feedback channel",
        "feedback_title": "Tell us what should improve next",
        "feedback_desc": "Use this channel to share where the workflow feels strong, where clarity is missing, and which farmer, trader, or intelligence tools you want improved next.",
        "product_improvement": "Product improvement",
        "product_improvement_desc": "Email the team at support@croppulse.ai or continue directly into the live product flow below.",
        "demo_pill": "Step into the live product flow",
        "demo_title": "Explore the interactive CropPulse demo",
        "demo_desc": "See how CropPulse turns crop data, market prices, buyer activity, and field alerts into clearer agricultural decisions without leaving the homepage experience.",
        "demo_p1": "No signup required for demo",
        "demo_p2": "Fast dashboard access",
        "demo_p3": "Built for farmers and traders",
        "continue_demo": "Continue into the live demo",
        "continue_demo_desc": "Add your email if you want it carried into future follow-up, or continue directly to explore the product workflow.",
        "work_email": "Work email",
        "continue_to_demo": "Continue to demo",
        "create_account": "Create account",
        "landing_footer": "©2026 CropPulse. Agricultural intelligence, marketplace visibility, and operational coordination in one platform.",
        "register_title": "👨‍🌾 Create Farmer Account",
        "step_1_phone": "Step 1: Phone Number",
        "phone_number_10": "📱 Phone Number (10 digits)",
        "send_otp": "Send OTP",
        "phone_registered": "❌ This phone is already registered. Please login instead.",
        "otp_sent_demo": "✅ OTP sent! (Demo: {otp})",
        "otp_demo_info": "This Streamlit-only build shows a demo OTP on screen instead of using an API service.",
        "valid_phone_error": "❌ Please enter a valid 10-digit phone number",
        "step_2_verify": "Step 2: Verify OTP",
        "enter_otp": "🔐 Enter OTP",
        "otp_verified": "✅ OTP Verified!",
        "step_3_details": "Step 3: Your Details",
        "full_name": "Full Name",
        "placeholder_name": "John Farmer",
        "state": "State",
        "district": "District",
        "placeholder_district": "Madurai",
        "village": "Village",
        "placeholder_village": "Village Name",
        "land_size": "Land Size (acres)",
        "soil_type": "Soil Type",
        "register_now": "✅ Register Now",
        "registration_success": "✅ Registration successful!",
        "fill_all_fields": "❌ Please fill all fields",
        "back_to_landing": "← Back to Landing",
        "sign_in": "## 🔐 Sign In",
        "phone_number": "📱 Phone Number",
        "user_not_found": "❌ User not found. Please register first.",
        "login_success": "✅ Login successful!",
        "dashboard_title": "### 🌾 CropPulse",
        "logout": "🚪 Logout",
        "tab_dashboard": "📊 Dashboard",
        "tab_crops": "🌱 Crops",
        "tab_marketplace": "🛒 Marketplace",
        "tab_intelligence": "📡 Intelligence",
        "tab_deals": "💰 Deals",
        "your_dashboard": "Your Dashboard",
        "demo_mode_info": "You are viewing CropPulse in demo mode. Create an account to save crops, listings, and deals.",
        "best_time_to_sell": "📈 Best Time to Sell",
        "next_48_hours": "Next 48 hours",
        "buyer_demand_strong": "Buyer demand is strongest for premium rice.",
        "active_buyer_interest": "🛒 Active Buyer Interest",
        "verified_buyers_watching": "Verified buyers are watching nearby supply.",
        "weather_watch": "🌦️ Weather Watch",
        "rain_alert": "Rain alert",
        "prepare_harvest": "Prepare harvest logistics in the next 3 days.",
        "demo_overview": "Demo overview",
        "demo_overview_desc": "Use the tabs above to explore crop management, marketplace listings, intelligence alerts, and deal tracking in the current Streamlit flow.",
        "rating": "⭐ Rating",
        "deals_completed": "{count} deals completed",
        "kyc_status": "📋 KYC Status",
        "verified_priority": "Verified farmers get priority",
        "your_active_crops": "🌱 Your Active Crops",
        "your_recent_listings": "🛒 Your Recent Listings",
        "trader_dashboard_info": "🧑‍💼 Trader Dashboard - View available listings and make offers",
        "manage_crops": "🌱 Manage Your Crops",
        "crop": "Crop",
        "variety": "Variety",
        "placeholder_variety": "Sona Masuri",
        "area": "Area (acres)",
        "sowing_date": "Sowing Date",
        "expected_harvest": "Expected Harvest",
        "add_crop": "✅ Add Crop",
        "crop_added": "✅ Crop added to your farm!",
        "marketplace_title": "🛒 Marketplace",
        "marketplace_info": "📋 Create listings to connect with traders and get best prices",
        "select_crop": "Select Crop",
        "quantity": "Quantity (kg)",
        "quality_grade": "Quality Grade",
        "price_per_kg": "Price per kg (₹)",
        "available_from": "Available From",
        "available_until": "Available Until",
        "create_listing": "📤 Create Listing",
        "listing_created": "✅ Listing created! Traders can now see and make offers.",
        "intelligence_feed": "📡 Market Intelligence Feed",
        "rainfall_alert_title": "**Heavy rainfall expected in Tamil Nadu**",
        "rainfall_alert_body": "May 15-20: 60-80% rain expected. Reduce supply in next 2-3 weeks.",
        "sell_time_title": "**Best Time to Sell: Next 48 Hours**",
        "sell_time_body": "Price forecast: ₹2,650/kg (peak demand window). Traders are actively buying premium rice.",
        "scheme_alert_title": "**PM-KISAN Subsidy Available**",
        "scheme_alert_body": "₹6,000 annual payment now open for registration. Check your eligibility - takes 5 minutes.",
        "active_deals_title": "💰 Your Active Deals",
        "active_deals_info": "Track your ongoing transactions with traders",
        "active_deals": "Active Deals",
        "pending_payment": "Pending Payment",
        "completed_this_month": "Completed This Month",
        "location_value": "📍 {district}, {state}",
        "land_acres": "🌾 {acres} acres",
        "status_label": "Status",
        "grade_label": "Grade",
        "quantity_kg_value": "{quantity} kg",
        "price_per_kg_value": "₹{price}/kg",
        "traders_count": "{count} traders",
        "status_growing": "Growing",
        "status_ready_harvest": "Ready for harvest",
        "status_active_label": "Active",
        "status_verified": "Verified",
        "status_pending": "Pending",
        "db_connection_failed": "❌ Database connection failed. Please check your database configuration.",
        "db_connection_info": "Use local SQLite for development or set DATABASE_URL for Streamlit Cloud production.",
        "state_tn": "Tamil Nadu",
        "state_ap": "Andhra Pradesh",
        "state_ka": "Karnataka",
        "state_mh": "Maharashtra",
        "state_tg": "Telangana",
        "state_up": "Uttar Pradesh",
        "soil_black": "Black Soil",
        "soil_red": "Red Soil",
        "soil_alluvial": "Alluvial",
        "soil_laterite": "Laterite",
        "soil_clay": "Clay",
        "crop_rice": "Rice",
        "crop_wheat": "Wheat",
        "crop_corn": "Corn",
        "crop_cotton": "Cotton",
        "crop_sugarcane": "Sugarcane",
        "crop_soybean": "Soybean",
    },
    "te": {
        "lang_en": "EN",
        "lang_te": "తెలుగు",
        "language_label": "భాష",
        "language_english": "ఇంగ్లీష్",
        "language_telugu": "తెలుగు",
        "promo_bar": "వ్యవసాయ డేటాను ROIగా మార్చండి.",
        "invite_link": "CropPulse ను ఆహ్వానించండి",
        "promo_suffix": "మీ AI మరియు డిజిటల్ ట్రాన్స్‌ఫార్మేషన్ వర్క్‌ఫ్లోకు.",
        "nav_products": "ఉత్పత్తులు",
        "nav_industry": "పరిశ్రమ",
        "nav_solutions": "పరిష్కారాలు",
        "nav_crop_knowledge": "పంట ఇంటెలిజెన్స్",
        "nav_resources": "వనరులు",
        "nav_company": "సంస్థ",
        "nav_user": "వినియోగదారులు",
        "nav_language": "భాష",
        "login": "లాగిన్",
        "price_intelligence": "ధరల ఇంటెలిజెన్స్",
        "price_intelligence_desc": "రోజువారీ మార్కెట్ సంకేతాలు, ధరల విజిబిలిటీ, అమ్మకానికి సరైన సమయ సూచనలు.",
        "farmer_os": "రైతు OS",
        "farmer_os_desc": "పంట ట్రాకింగ్, కోత ప్రణాళిక, రైతు వర్క్‌ఫ్లోలు.",
        "marketplace": "మార్కెట్‌ప్లేస్",
        "marketplace_desc": "లిస్టింగ్స్, ఆఫర్లు, చర్చలు, డీల్ సమన్వయం.",
        "crop_rice_desc": "బియ్యం మార్కెట్లకు ధరల సంకేతాలు, డిమాండ్ ధోరణులు, ట్రేడింగ్ విజిబిలిటీ.",
        "crop_wheat_desc": "గోధుమ ఉత్పత్తి మరియు అమ్మకాల సమయాల కోసం పంట మరియు మార్కెట్ ఇంటెలిజెన్స్.",
        "crop_corn_desc": "మొక్కజొన్న సరఫరా మరియు కోత కదలికలకు ప్రణాళిక మరియు కొనుగోలుదారుల విజిబిలిటీ.",
        "crop_cotton_desc": "పత్తి రైతులు మరియు కొనుగోలుదారుల కోసం ఫీల్డ్ అప్డేట్స్ మరియు మార్కెట్ సందర్భం.",
        "crop_sugarcane_desc": "చెరకు రైతులు మరియు ట్రేడ్ ఫ్లోలకు ఆపరేషనల్ మరియు ధరల మద్దతు.",
        "crop_soybean_desc": "సోయాబీన్ ఉత్పత్తి మరియు అమ్మకాల కోసం సరఫరా ట్రాకింగ్ మరియు మార్కెట్ అవగాహన.",
        "food_retail": "ఫుడ్ రిటైల్",
        "food_retail_desc": "తెలివైన సోర్సింగ్‌తో మరింత స్థిరమైన ఫుడ్ రిటైల్ భవిష్యత్తు.",
        "cpg_fmcg": "CPG/FMCG",
        "cpg_fmcg_desc": "ఆహార ఉత్పత్తి మరియు కొనుగోలు నిర్వహణకు AI మద్దతు.",
        "seed_manufacturing": "సీడ్ మాన్యుఫ్యాక్చరింగ్",
        "seed_manufacturing_desc": "ఫీల్డ్ ఇంటెలిజెన్స్, అంచనాలు, విస్తరణకు సిద్ధమైన సీడ్ ఆపరేషన్లు.",
        "governments": "ప్రభుత్వాలు",
        "governments_desc": "ప్రభుత్వ సమన్వయం కోసం ట్రేసబుల్ వ్యవసాయ విజిబిలిటీ.",
        "food_processing": "ఫుడ్ ప్రాసెసింగ్",
        "food_processing_desc": "డిజిటైజ్డ్ ఫార్మ్ ఆపరేషన్లు మరియు ఎండ్-టు-ఎండ్ ట్రేసబిలిటీ.",
        "agri_teams": "వ్యవసాయ బృందాలు",
        "agri_teams_desc": "సోర్సింగ్, మానిటరింగ్, సమన్వయం కోసం పంచుకునే వర్క్‌ఫ్లో.",
        "verified_network": "ధృవీకరించిన నెట్‌వర్క్",
        "verified_network_desc": "శుభ్రమైన కొనుగోలుదారు-అమ్మకందారు పరస్పర చర్యలకు ప్రొఫైళ్లు మరియు నమ్మకం.",
        "protected_access": "రక్షిత ప్రాప్తి",
        "protected_access_desc": "నమ్మదగిన ప్రాప్తి, ఖాతా ప్రవాహాలు, భవిష్యత్ సిద్ధమైన ధృవీకరణ.",
        "operational_focus": "ఆపరేషనల్ ఫోకస్",
        "operational_focus_desc": "మానిటరింగ్, లిస్టింగ్, చర్చలు, వేగవంతమైన నిర్ణయాల కోసం నిర్మితం.",
        "crop_signals": "పంట సంకేతాలు",
        "crop_signals_desc": "వాతావరణం, సిద్ధత, మార్కెట్ సందర్భం పంట చక్రాలంతటా.",
        "decision_guidance": "నిర్ణయ మార్గదర్శకం",
        "decision_guidance_desc": "సరైన సమయం మరియు చర్య నాణ్యత మెరుగుపరచడానికి ఇంటెలిజెన్స్ లేయర్లు ఉపయోగించండి.",
        "guides": "మార్గదర్శకాలు",
        "guides_desc": "కొత్త వినియోగదారుల కోసం ఉత్పత్తి వాక్‌త్రూ మరియు ఆన్‌బోర్డింగ్ సహాయం.",
        "case_examples": "ఉదాహరణలు",
        "case_examples_desc": "ధరలు, పంట, మార్కెట్‌ప్లేస్ వర్క్‌ఫ్లోలను బృందాలు ఎలా ఉపయోగిస్తున్నాయో చూడండి.",
        "about_croppulse": "CropPulse గురించి",
        "about_croppulse_desc": "వ్యవసాయ ఇంటెలిజెన్స్ మరియు సమన్వయ సాధనాలను ఎందుకు నిర్మిస్తున్నామో.",
        "contact": "సంప్రదించండి",
        "contact_desc": "ఉత్పత్తి ప్రాప్తి, డెమోలు, భాగస్వామ్యాల కోసం బృందాన్ని సంప్రదించండి.",
        "user_farmer": "రైతులు",
        "user_farmer_desc": "రైతుల కోసం పంట ప్రణాళిక, అమ్మకాల మార్గదర్శకం, ఫార్మ్ వర్క్‌ఫ్లో సాధనాలు.",
        "user_traders": "వ్యాపారులు",
        "user_traders_desc": "వ్యాపారుల కోసం సరఫరా గుర్తింపు, కొనుగోలుదారు విజిబిలిటీ, వేగవంతమైన డీల్ సమన్వయం.",
        "user_fpo": "FPO",
        "user_fpo_desc": "రైతు ఉత్పత్తిదారుల సంస్థల కోసం ఏకీకరణ, సమన్వయం, సభ్యుల మద్దతు సాధనాలు.",
        "language_english_desc": "ల్యాండింగ్ పేజీ మరియు యాప్‌ను ఇంగ్లీష్‌లో చూపించండి.",
        "language_telugu_desc": "ల్యాండింగ్ పేజీ మరియు యాప్‌ను తెలుగులో చూపించండి.",
        "section_kicker": "వ్యవసాయ ఇంటెలిజెన్స్ మరియు మార్కెట్ సమన్వయం",
        "hero_title": "ఎప్పుడు అమ్మాలో తెలుసుకోండి. సరఫరాను వేగంగా కనుగొనండి. ప్రతి వ్యవసాయ నిర్ణయాన్ని సమన్వయం చేయండి.",
        "hero_subtitle": "CropPulse ధరల విజిబిలిటీ, పంట ప్రణాళిక, మార్కెట్‌ప్లేస్ కార్యకలాపాలు, డీల్ సమన్వయాన్ని ఒకే ప్లాట్‌ఫార్మ్‌లో అందిస్తుంది.",
        "hero_copy": "త్వరిత నిర్ణయాలు, తక్కువ కాల్స్, స్పష్టమైన మార్కెట్ సంకేతాలు, బలమైన అమలు అవసరమైన రైతులు, వ్యాపారులు, వ్యవసాయ బృందాల కోసం నిర్మించబడింది.",
        "tag_sell": "అమ్మకానికి సరైన సమయం",
        "tag_trader": "ధృవీకరించిన వ్యాపారి ప్రాప్తి",
        "tag_listing": "పంట మరియు లిస్టింగ్ నిర్వహణ",
        "live_market_workspace": "ప్రత్యక్ష మార్కెట్ వర్క్‌స్పేస్",
        "best_selling_window": "అమ్మకానికి ఉత్తమ సమయం",
        "demand_desc": "సమీప జిల్లాల్లో ప్రీమియం బియ్యం డిమాండ్ ఎక్కువగా ఉంది.",
        "buyer_activity": "కొనుగోలుదారు కార్యకలాపం",
        "high": "ఎక్కువ",
        "buyer_activity_desc": "ఈరోజు మరిన్ని ధృవీకరించిన వ్యాపారులు శోధిస్తున్నారు.",
        "signal_confidence": "సంకేత విశ్వసనీయత",
        "active": "సక్రియం",
        "signal_confidence_desc": "ధరల మొమెంటం మరియు కొనుగోలు ఆసక్తి సరిపోతున్నాయి.",
        "watchlist_priority": "ప్రాధాన్య వాచ్‌లిస్ట్",
        "rice_buyers": "బియ్యం కొనుగోలుదారులు",
        "watchlist_priority_desc": "బలమైన జిల్లా డిమాండ్‌తో షార్ట్‌లిస్ట్ నవీకరించబడింది.",
        "platform_features": "ప్లాట్‌ఫార్మ్ లక్షణాలు",
        "platform_features_desc": "పంట ప్రణాళిక, ధరల విజిబిలిటీ, మార్కెట్‌ప్లేస్ చర్య, డీల్ ఫాలో-థ్రూ వరకు రోజువారీ వ్యవసాయ నిర్ణయాలకు అవసరమైన ప్రతిదీ.",
        "feature_price_title": "ధరల ఇంటెలిజెన్స్",
        "feature_price_desc": "చెల్లాచెదురైన అప్డేట్స్‌పై ఆధారపడకుండా మార్కెట్ కదలికలు, డిమాండ్ స్పైక్స్, అధిక విలువ అమ్మక సమయాలను ట్రాక్ చేయండి.",
        "pill_live_market": "ప్రత్యక్ష మార్కెట్ విజిబిలిటీ",
        "feature_crop_title": "పంట ప్రణాళిక",
        "feature_crop_desc": "పంట వివరాలు, ఫీల్డ్ టైమ్‌లైన్లు, కోత సిద్ధతను ఒకేచోట నిర్వహించండి.",
        "pill_farmer_workflow": "రైతు వర్క్‌ఫ్లో",
        "feature_market_title": "మార్కెట్‌ప్లేస్ సమన్వయం",
        "feature_market_desc": "లిస్టింగ్స్ సృష్టించండి, ఆఫర్లు పొందండి, కొనుగోలుదారులను పోల్చండి, చర్చలను కొనసాగించండి.",
        "pill_listing_flow": "లిస్టింగ్ నుండి డీల్ వరకు",
        "feature_trader_title": "వ్యాపారి సోర్సింగ్",
        "feature_trader_desc": "ధృవీకరించిన లిస్టింగ్స్, స్థానం సందర్భం, పంట లభ్యత ద్వారా వ్యాపారులు సరఫరాను వేగంగా కనుగొనడంలో సహాయపడండి.",
        "pill_verified_network": "ధృవీకరించిన నెట్‌వర్క్",
        "feature_deal_title": "డీల్ నిర్వహణ",
        "feature_deal_desc": "మొదటి ఆఫర్ నుండి తుది సమన్వయం వరకు డీల్‌లను స్పష్టంగా కనిపించేలా ఉంచండి.",
        "pill_execution_support": "అమలు మద్దతు",
        "feature_weather_title": "వాతావరణం మరియు పథకాల హెచ్చరికలు",
        "feature_weather_desc": "ఫీల్డ్‌కు సంబంధించిన వాతావరణ సంఘటనలు, సబ్సిడీ పథకాలు, చర్యకు సిద్ధమైన అప్డేట్స్‌ను చూపించండి.",
        "pill_action_ready": "చర్యకు సిద్ధమైన హెచ్చరికలు",
        "workflows_title": "మార్కెట్ యొక్క రెండు వైపులకూ రూపొందించబడింది",
        "workflows_desc": "CropPulse రైతు చర్య, వ్యాపారి సోర్సింగ్, వ్యవసాయ బృంద సమన్వయాన్ని ఒకే వర్క్‌ఫ్లోలో బలవంతం చేయకుండా మద్దతు ఇస్తుంది.",
        "farmer_view": "👨‍🌾 సరళీకరించిన రైతు దృశ్యం",
        "farmer_workflow": "రైతు వర్క్‌ఫ్లో",
        "farmer_workflow_desc": "స్పష్టమైన తదుపరి చర్యలు, మంచి మార్కెట్ విజిబిలిటీ, పంట సిద్ధత నుండి కొనుగోలుదారుల కనెక్షన్ వరకు సులభ మార్గం కోరుకునే రైతుల కోసం.",
        "farmer_b1": "అమ్మకానికి సరైన సమయ మార్గదర్శకం",
        "farmer_b2": "పంట మరియు కోత ప్రణాళిక",
        "farmer_b3": "సరళమైన లిస్టింగ్ మరియు ఆఫర్ ప్రవాహం",
        "farmer_b4": "స్పష్టమైన హెచ్చరికలు మరియు తదుపరి చర్యలు",
        "trader_desk": "🧑‍💼 వ్యాపారి మరియు వ్యవసాయ బృంద డెస్క్",
        "buyer_workflow": "కొనుగోలుదారు మరియు సమన్వయ వర్క్‌ఫ్లో",
        "buyer_workflow_desc": "బలమైన సోర్సింగ్ విజిబిలిటీ, సరళమైన సరఫరా శోధన, కొనసాగుతున్న అవకాశాల ట్రాకింగ్ అవసరమైన వృత్తిపరుల కోసం.",
        "buyer_b1": "ధృవీకరించిన సరఫరా శోధన",
        "buyer_b2": "ప్రాంతీయ డిమాండ్ మరియు ధరల సందర్భం",
        "buyer_b3": "డీల్ ఫాలో-అప్ మరియు సమన్వయం",
        "buyer_b4": "త్వరిత కొనుగోలుదారు షార్ట్‌లిస్టింగ్",
        "trust_title": "నిజమైన వ్యవసాయ కార్యకలాపాల కోసం నమ్మదగిన మరియు నిర్మితమైనది",
        "trust_desc": "ల్యాండింగ్ అనుభవం విశ్వసనీయంగా ఉండాలి. CropPulse ను ఫీల్డ్, మార్కెట్, ఆపరేషనల్ వినియోగానికి ఉపయోగకరంగా చేసే స్థంభాలు ఇవి.",
        "trust_card_1": "ధృవీకరించిన పాల్గొనేవారు",
        "trust_card_1_desc": "కొనుగోలుదారులు మరియు అమ్మకందారులు మరింత నమ్మకంతో పనిచేయడానికి ప్రొఫైల్స్, లిస్టింగ్స్, పరస్పర చర్యలు నమ్మకంపై నిర్మించబడ్డాయి.",
        "trust_card_2": "రక్షిత ప్రాప్తి",
        "trust_card_2_desc": "ధృవీకరణ మరియు ఖాతా ప్రవాహాలు ఉత్పత్తి వినియోగదారుల కోసం నమ్మదగిన ప్రాప్తిని మద్దతు ఇస్తాయి.",
        "trust_card_3": "నిర్ణయ రికార్డులు",
        "trust_card_3_desc": "లిస్టింగ్స్, పంట ఎంట్రీలు, ఆఫర్లు, మార్కెట్ సంకేతాలు కాల్స్ మరియు చాట్స్‌లో మాయమవకుండా ఒకేచోట కనిపిస్తాయి.",
        "trust_card_4": "గోప్యతపై దృష్టి",
        "trust_card_4_desc": "రైతు మరియు మార్కెట్‌ప్లేస్ డేటా అవసరమైనంత వరకు మాత్రమే బహిర్గతమవుతుంది.",
        "trust_card_5": "ఫీల్డ్‌కు సంబంధించిన ఇంటెలిజెన్స్",
        "trust_card_5_desc": "వాతావరణం, పథకాలు, డిమాండ్, ధరల సంకేతాలు వర్క్‌ఫ్లోలో ఉంచబడతాయి.",
        "trust_card_6": "ఆపరేషనల్ ఫోకస్",
        "trust_card_6_desc": "ఉత్పత్తి రోజువారీ చర్య కోసం రూపొందించబడింది: మానిటర్ చేయండి, లిస్ట్ చేయండి, చర్చించండి, సమన్వయం చేయండి, వేగంగా నిర్ణయించండి.",
        "why_title": "ఎందుకు CropPulse?",
        "why_desc": "మీ స్క్రీన్‌షాట్‌లలోని ల్యాండింగ్ పేజీ బలం దాని నిర్మాణంలో ఉంది. CropPulse ఇప్పుడు అదే నిర్మాణాన్ని వ్యవసాయ విలువలతో అనుసరిస్తోంది.",
        "mini_1": "చర్య-మొదటి",
        "mini_1_desc": "నిర్ణయ మద్దతు ధరలు, పంటలు, ప్రత్యక్ష మార్కెట్ కదలికలకు అనుసంధానించబడింది.",
        "mini_2": "మార్కెట్ అవగాహన",
        "mini_2_desc": "సందర్భం కొనుగోలుదారులు, సరఫరా, సమయం, చర్చ సిద్ధత చుట్టూ నిర్మించబడింది.",
        "mini_3": "ఆపరేషనల్‌గా ఉపయోగకరం",
        "mini_3_desc": "హోమ్‌పేజ్ స్థిర మార్కెటింగ్ కాపీ కంటే నిజమైన వర్క్‌ఫ్లోలకు నడిపిస్తుంది.",
        "detail_pill_1": "మంచి అమ్మక సంకేతాలు",
        "detail_title_1": "తదుపరి ఏమి చేయాలో తెలుసుకోండి",
        "detail_desc_1": "మార్కెట్ బలంగా ఉన్నప్పుడు రైతులు మరియు బృందాలు అర్థం చేసుకోవడానికి సహాయపడే సంకేతాలు పొందండి.",
        "detail_1_b1": "వివరణాత్మక మార్కెట్ విశ్వసనీయత",
        "detail_1_b2": "స్పష్టమైన తదుపరి మార్గదర్శకం",
        "detail_1_b3": "తక్కువ శబ్దం, ఎక్కువ స్పష్టత",
        "detail_pill_2": "బలమైన చర్చ క్రమశిక్షణ",
        "detail_title_2": "బలహీన డీల్‌లను నివారించండి",
        "detail_desc_2": "ధర నిర్ణయం తీసుకునే ముందు డిమాండ్, స్థానం, పంట సిద్ధత, సరఫరా సంకేతాలను పరిశీలించండి.",
        "detail_2_b1": "కొనుగోలుదారు మరియు సరఫరా అవగాహన",
        "detail_2_b2": "జిల్లా స్థాయి మార్కెట్ సందర్భం",
        "detail_2_b3": "మంచి ఆఫర్ పోలిక",
        "detail_pill_3": "త్వరిత సమన్వయం",
        "detail_title_3": "అవకాశాలను త్వరగా ముందుకు తీసుకెళ్లండి",
        "detail_desc_3": "చెల్లాచెదురైన కమ్యూనికేషన్‌ను ఒక శుభ్రమైన లూప్‌గా మార్చండి.",
        "detail_3_b1": "త్వరిత మార్కెట్ ప్రతిస్పందన",
        "detail_3_b2": "తక్కువ మాన్యువల్ ఫాలో-అప్",
        "detail_3_b3": "డీల్ ముగింపుపై ఎక్కువ సమయం",
        "help_title": "CropPulse ను మెరుగుపరచడంలో సహాయపడండి",
        "help_desc": "బలమైన ల్యాండింగ్ పేజీ స్టాటిక్ టెస్టిమోనియల్స్‌తో ముగియకూడదు. వినియోగదారులు ఎలా స్పందించవచ్చో చూపాలి.",
        "feedback_channel": "ఫీడ్‌బ్యాక్ ఛానల్",
        "feedback_title": "తదుపరి ఏమి మెరుగుపరచాలో మాకు చెప్పండి",
        "feedback_desc": "వర్క్‌ఫ్లో ఎక్కడ బలంగా ఉందో, ఎక్కడ స్పష్టత అవసరమో, ఏ రైతు/వ్యాపారి/ఇంటెలిజెన్స్ సాధనాలు మెరుగుపరచాలని అనుకుంటున్నారో చెప్పండి.",
        "product_improvement": "ఉత్పత్తి మెరుగుదల",
        "product_improvement_desc": "support@croppulse.ai కు ఈమెయిల్ చేయండి లేదా క్రింది ప్రత్యక్ష ఉత్పత్తి ప్రవాహంలో కొనసాగండి.",
        "demo_pill": "ప్రత్యక్ష ఉత్పత్తి ప్రవాహంలోకి అడుగు పెట్టండి",
        "demo_title": "ఇంటరాక్టివ్ CropPulse డెమోను అన్వేషించండి",
        "demo_desc": "హోమ్‌పేజ్ వదిలి వెళ్లకుండా CropPulse పంట డేటా, మార్కెట్ ధరలు, కొనుగోలుదారు కార్యకలాపం, ఫీల్డ్ హెచ్చరికలను స్పష్టమైన వ్యవసాయ నిర్ణయాలుగా ఎలా మారుస్తుందో చూడండి.",
        "demo_p1": "డెమో కోసం సైన్‌అప్ అవసరం లేదు",
        "demo_p2": "త్వరిత డ్యాష్‌బోర్డ్ ప్రాప్తి",
        "demo_p3": "రైతులు మరియు వ్యాపారుల కోసం నిర్మితమైనది",
        "continue_demo": "ప్రత్యక్ష డెమోలో కొనసాగండి",
        "continue_demo_desc": "మీ ఇమెయిల్‌ను జోడించండి లేదా నేరుగా ఉత్పత్తి వర్క్‌ఫ్లోను అన్వేషించండి.",
        "work_email": "పని ఇమెయిల్",
        "continue_to_demo": "డెమోలో కొనసాగండి",
        "create_account": "ఖాతా సృష్టించండి",
        "landing_footer": "©2026 CropPulse. వ్యవసాయ ఇంటెలిజెన్స్, మార్కెట్‌ప్లేస్ విజిబిలిటీ, ఆపరేషనల్ సమన్వయం ఒకే ప్లాట్‌ఫార్మ్‌లో.",
        "register_title": "👨‍🌾 రైతు ఖాతా సృష్టించండి",
        "step_1_phone": "దశ 1: ఫోన్ నంబర్",
        "phone_number_10": "📱 ఫోన్ నంబర్ (10 అంకెలు)",
        "send_otp": "OTP పంపండి",
        "phone_registered": "❌ ఈ ఫోన్ ఇప్పటికే నమోదు అయింది. దయచేసి లాగిన్ చేయండి.",
        "otp_sent_demo": "✅ OTP పంపబడింది! (డెమో: {otp})",
        "otp_demo_info": "ఈ Streamlit-only build API సేవకు బదులుగా డెమో OTP ను స్క్రీన్‌పై చూపిస్తుంది.",
        "valid_phone_error": "❌ సరైన 10 అంకెల ఫోన్ నంబర్ నమోదు చేయండి",
        "step_2_verify": "దశ 2: OTP ధృవీకరించండి",
        "enter_otp": "🔐 OTP నమోదు చేయండి",
        "otp_verified": "✅ OTP ధృవీకరించబడింది!",
        "step_3_details": "దశ 3: మీ వివరాలు",
        "full_name": "పూర్తి పేరు",
        "placeholder_name": "రామయ్య రైతు",
        "state": "రాష్ట్రం",
        "district": "జిల్లా",
        "placeholder_district": "మదురై",
        "village": "గ్రామం",
        "placeholder_village": "గ్రామ పేరు",
        "land_size": "భూమి పరిమాణం (ఎకరాలు)",
        "soil_type": "మట్టి రకం",
        "register_now": "✅ ఇప్పుడే నమోదు చేయండి",
        "registration_success": "✅ నమోదు విజయవంతం!",
        "fill_all_fields": "❌ అన్ని ఫీల్డ్‌లు నింపండి",
        "back_to_landing": "← హోమ్‌కు తిరిగి",
        "sign_in": "## 🔐 సైన్ ఇన్",
        "phone_number": "📱 ఫోన్ నంబర్",
        "user_not_found": "❌ వినియోగదారు కనబడలేదు. ముందుగా నమోదు చేయండి.",
        "login_success": "✅ లాగిన్ విజయవంతం!",
        "dashboard_title": "### 🌾 CropPulse",
        "logout": "🚪 లాగ్ అవుట్",
        "tab_dashboard": "📊 డ్యాష్‌బోర్డ్",
        "tab_crops": "🌱 పంటలు",
        "tab_marketplace": "🛒 మార్కెట్‌ప్లేస్",
        "tab_intelligence": "📡 ఇంటెలిజెన్స్",
        "tab_deals": "💰 డీల్‌లు",
        "your_dashboard": "మీ డ్యాష్‌బోర్డ్",
        "demo_mode_info": "మీరు CropPulse ను డెమో మోడ్‌లో చూస్తున్నారు. పంటలు, లిస్టింగ్స్, డీల్‌లను సేవ్ చేయడానికి ఖాతా సృష్టించండి.",
        "best_time_to_sell": "📈 అమ్మకానికి ఉత్తమ సమయం",
        "next_48_hours": "తదుపరి 48 గంటలు",
        "buyer_demand_strong": "ప్రీమియం బియ్యం కోసం కొనుగోలుదారుల డిమాండ్ బలంగా ఉంది.",
        "active_buyer_interest": "🛒 సక్రియ కొనుగోలుదారుల ఆసక్తి",
        "verified_buyers_watching": "ధృవీకరించిన కొనుగోలుదారులు సమీప సరఫరాను గమనిస్తున్నారు.",
        "weather_watch": "🌦️ వాతావరణ గమనిక",
        "rain_alert": "వర్ష హెచ్చరిక",
        "prepare_harvest": "తదుపరి 3 రోజుల్లో కోత లాజిస్టిక్స్ సిద్ధం చేయండి.",
        "demo_overview": "డెమో అవలోకనం",
        "demo_overview_desc": "పైన ఉన్న ట్యాబ్‌ల ద్వారా పంట నిర్వహణ, మార్కెట్‌ప్లేస్ లిస్టింగ్స్, ఇంటెలిజెన్స్ హెచ్చరికలు, డీల్ ట్రాకింగ్‌ను అన్వేషించండి.",
        "rating": "⭐ రేటింగ్",
        "deals_completed": "{count} డీల్‌లు పూర్తయ్యాయి",
        "kyc_status": "📋 KYC స్థితి",
        "verified_priority": "ధృవీకరించిన రైతులకు ప్రాధాన్యం ఉంటుంది",
        "your_active_crops": "🌱 మీ సక్రియ పంటలు",
        "your_recent_listings": "🛒 మీ తాజా లిస్టింగ్స్",
        "trader_dashboard_info": "🧑‍💼 వ్యాపారి డ్యాష్‌బోర్డ్ - లిస్టింగ్స్ చూడండి మరియు ఆఫర్లు ఇవ్వండి",
        "manage_crops": "🌱 మీ పంటలను నిర్వహించండి",
        "crop": "పంట",
        "variety": "వెరైటీ",
        "placeholder_variety": "సోనా మసూరి",
        "area": "విస్తీర్ణం (ఎకరాలు)",
        "sowing_date": "విత్తిన తేదీ",
        "expected_harvest": "అంచనా కోత తేదీ",
        "add_crop": "✅ పంట జోడించండి",
        "crop_added": "✅ పంట మీ ఫార్మ్‌కి జోడించబడింది!",
        "marketplace_title": "🛒 మార్కెట్‌ప్లేస్",
        "marketplace_info": "📋 వ్యాపారులతో కనెక్ట్ కావడానికి మరియు మంచి ధరలు పొందడానికి లిస్టింగ్స్ సృష్టించండి",
        "select_crop": "పంటను ఎంచుకోండి",
        "quantity": "పరిమాణం (కిలోలు)",
        "quality_grade": "నాణ్యత గ్రేడ్",
        "price_per_kg": "కిలోకు ధర (₹)",
        "available_from": "లభ్యత ప్రారంభం",
        "available_until": "లభ్యత ముగింపు",
        "create_listing": "📤 లిస్టింగ్ సృష్టించండి",
        "listing_created": "✅ లిస్టింగ్ సృష్టించబడింది! వ్యాపారులు ఇప్పుడు చూడగలరు మరియు ఆఫర్లు చేయగలరు.",
        "intelligence_feed": "📡 మార్కెట్ ఇంటెలిజెన్స్ ఫీడ్",
        "rainfall_alert_title": "**తమిళనాడులో భారీ వర్షం వచ్చే అవకాశం**",
        "rainfall_alert_body": "మే 15-20: 60-80% వర్షం అవకాశం. తదుపరి 2-3 వారాల్లో సరఫరాను తగ్గించండి.",
        "sell_time_title": "**అమ్మకానికి ఉత్తమ సమయం: తదుపరి 48 గంటలు**",
        "sell_time_body": "ధర అంచనా: ₹2,650/కిలో (ఉన్నత డిమాండ్ విండో). వ్యాపారులు ప్రీమియం బియ్యం కోసం కొనుగోలు చేస్తున్నారు.",
        "scheme_alert_title": "**PM-KISAN సబ్సిడీ అందుబాటులో ఉంది**",
        "scheme_alert_body": "₹6,000 వార్షిక చెల్లింపు నమోదు కోసం తెరవబడింది. అర్హతను పరీక్షించండి - 5 నిమిషాలు పడుతుంది.",
        "active_deals_title": "💰 మీ సక్రియ డీల్‌లు",
        "active_deals_info": "వ్యాపారులతో మీ కొనసాగుతున్న లావాదేవీలను ట్రాక్ చేయండి",
        "active_deals": "సక్రియ డీల్‌లు",
        "pending_payment": "పెండింగ్ చెల్లింపు",
        "completed_this_month": "ఈ నెల పూర్తైనవి",
        "location_value": "📍 {district}, {state}",
        "land_acres": "🌾 {acres} ఎకరాలు",
        "status_label": "స్థితి",
        "grade_label": "గ్రేడ్",
        "quantity_kg_value": "{quantity} కిలోలు",
        "price_per_kg_value": "₹{price}/కిలో",
        "traders_count": "{count} వ్యాపారులు",
        "status_growing": "పెరుగుతోంది",
        "status_ready_harvest": "కోతకు సిద్ధం",
        "status_active_label": "సక్రియం",
        "status_verified": "ధృవీకరించబడింది",
        "status_pending": "పెండింగ్",
        "db_connection_failed": "❌ డేటాబేస్ కనెక్షన్ విఫలమైంది. మీ డేటాబేస్ కాన్ఫిగరేషన్‌ను తనిఖీ చేయండి.",
        "db_connection_info": "డెవలప్మెంట్ కోసం లోకల్ SQLite లేదా ప్రొడక్షన్ కోసం Streamlit Cloud లో DATABASE_URL ఉపయోగించండి.",
        "state_tn": "తమిళనాడు",
        "state_ap": "ఆంధ్రప్రదేశ్",
        "state_ka": "కర్ణాటక",
        "state_mh": "మహారాష్ట్ర",
        "state_tg": "తెలంగాణ",
        "state_up": "ఉత్తరప్రదేశ్",
        "soil_black": "నల్ల మట్టి",
        "soil_red": "ఎర్ర మట్టి",
        "soil_alluvial": "ఆల్యూవియల్",
        "soil_laterite": "లేటరైట్",
        "soil_clay": "చిక్కటి మట్టి",
        "crop_rice": "బియ్యం",
        "crop_wheat": "గోధుమ",
        "crop_corn": "మొక్కజొన్న",
        "crop_cotton": "పత్తి",
        "crop_sugarcane": "చెరకు",
        "crop_soybean": "సోయాబీన్",
    },
}


def set_language(lang_code):
    if lang_code in TRANSLATIONS:
        st.session_state.language = lang_code


def sync_language_query_param(lang_code=None):
    active_lang = lang_code or get_language()
    if active_lang in TRANSLATIONS:
        st.query_params["lang"] = active_lang


def clear_action_query_param():
    current_lang = st.query_params.get("lang", get_language())
    st.query_params.clear()
    if current_lang in TRANSLATIONS:
        st.query_params["lang"] = current_lang


def initialize_language_from_query():
    query_lang = st.query_params.get("lang")
    if query_lang in TRANSLATIONS:
        set_language(query_lang)
    else:
        sync_language_query_param(get_language())


def get_language():
    return st.session_state.get("language", "en")


def tr(key, **kwargs):
    lang_code = get_language()
    value = TRANSLATIONS.get(lang_code, TRANSLATIONS["en"]).get(
        key,
        TRANSLATIONS["en"].get(key, key),
    )
    if kwargs and isinstance(value, str):
        return value.format(**kwargs)
    return value


def build_query_href(**params):
    filtered = {key: value for key, value in params.items() if value is not None}
    return f"?{urlencode(filtered)}" if filtered else "?"


STATE_OPTIONS = [
    "Tamil Nadu",
    "Andhra Pradesh",
    "Karnataka",
    "Maharashtra",
    "Telangana",
    "Uttar Pradesh",
]

STATE_KEYS = {
    "Tamil Nadu": "state_tn",
    "Andhra Pradesh": "state_ap",
    "Karnataka": "state_ka",
    "Maharashtra": "state_mh",
    "Telangana": "state_tg",
    "Uttar Pradesh": "state_up",
}

SOIL_OPTIONS = ["Black Soil", "Red Soil", "Alluvial", "Laterite", "Clay"]

SOIL_KEYS = {
    "Black Soil": "soil_black",
    "Red Soil": "soil_red",
    "Alluvial": "soil_alluvial",
    "Laterite": "soil_laterite",
    "Clay": "soil_clay",
}

CROP_OPTIONS = ["Rice", "Wheat", "Corn", "Cotton", "Sugarcane", "Soybean"]

CROP_KEYS = {
    "Rice": "crop_rice",
    "Wheat": "crop_wheat",
    "Corn": "crop_corn",
    "Cotton": "crop_cotton",
    "Sugarcane": "crop_sugarcane",
    "Soybean": "crop_soybean",
}


def translate_option(value, mapping):
    return tr(mapping.get(value, value))


STATUS_KEYS = {
    "growing": "status_growing",
    "ready_harvest": "status_ready_harvest",
    "active": "status_active_label",
    "verified": "status_verified",
    "pending": "status_pending",
}


def translate_state_value(value):
    return translate_option(value, STATE_KEYS)


def translate_crop_value(value):
    return translate_option(value, CROP_KEYS)


def translate_status_value(value):
    normalized = str(value).strip().lower()
    return tr(STATUS_KEYS.get(normalized, value))


def render_language_switcher(widget_key, show_label=True):
    current_lang = get_language()
    widget_state_key = f"{widget_key}_language_choice"
    if st.session_state.get(widget_state_key) != current_lang:
        st.session_state[widget_state_key] = current_lang

    if show_label:
        label_col, select_col = st.columns([1.0, 1.7])
        with label_col:
            st.markdown(
                "<div style='padding-top: 0.45rem; color: #6b7d90; font-size: 0.95rem; font-weight: 500;'>"
                + tr("language_label")
                + "</div>",
                unsafe_allow_html=True,
            )
        with select_col:
            selected_lang = st.selectbox(
                tr("language_label"),
                options=["en", "te"],
                key=widget_state_key,
                label_visibility="collapsed",
                format_func=lambda code: tr("language_english") if code == "en" else tr("language_telugu"),
            )
    else:
        selected_lang = st.selectbox(
            tr("language_label"),
            options=["en", "te"],
            key=widget_state_key,
            label_visibility="collapsed",
            format_func=lambda code: tr("language_english") if code == "en" else tr("language_telugu"),
        )

    if selected_lang != current_lang:
        set_language(selected_lang)
        sync_language_query_param(selected_lang)
        st.rerun()


def go_to_page(page_name):
    """Centralized page switch helper."""
    sync_language_query_param()
    st.session_state.page = page_name
    st.rerun()


def reset_auth_flow():
    """Clear transient OTP state when leaving auth screens."""
    st.session_state.otp_code = None
    st.session_state.phone_temp = None
    st.session_state.landing_panel = None


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
    initialize_language_from_query()

    landing_action = st.query_params.get("action")
    if landing_action == "login":
        clear_action_query_param()
        reset_auth_flow()
        st.session_state.landing_panel = "login"
    if landing_action == "register":
        clear_action_query_param()
        reset_auth_flow()
        st.session_state.landing_panel = "register"
    if landing_action == "demo":
        clear_action_query_param()
        enter_demo_mode()

    current_lang = get_language()

    st.markdown(f"""
    <div class="landing-header-shell">
    <div class="promo-bar">
        {tr('promo_bar')} <a href="#demo">{tr('invite_link')}</a> {tr('promo_suffix')}
    </div>

    <div class="landing-nav">
        <div class="nav-brand">
            <div class="nav-mark">🌾</div>
            <div class="nav-brand-copy">
                <p class="nav-wordmark"><span class="nav-wordmark-primary">Crop</span><span class="nav-wordmark-secondary">Pulse</span></p>
            </div>
        </div>
        <div class="nav-menu">
            <div class="nav-item">
                <div class="nav-link">{tr('nav_products')} <span class="nav-menu-caret">&#9662;</span></div>
                <div class="nav-dropdown mega">
                    <div class="dropdown-grid">
                        <a class="dropdown-item" href="#features"><div class="dropdown-icon">&#127806;</div><div><h4>{tr('crop_rice')}</h4><p>{tr('crop_rice_desc')}</p></div></a>
                        <a class="dropdown-item" href="#features"><div class="dropdown-icon">&#127805;</div><div><h4>{tr('crop_wheat')}</h4><p>{tr('crop_wheat_desc')}</p></div></a>
                        <a class="dropdown-item" href="#features"><div class="dropdown-icon">&#127805;</div><div><h4>{tr('crop_corn')}</h4><p>{tr('crop_corn_desc')}</p></div></a>
                        <a class="dropdown-item" href="#features"><div class="dropdown-icon">&#127806;</div><div><h4>{tr('crop_cotton')}</h4><p>{tr('crop_cotton_desc')}</p></div></a>
                        <a class="dropdown-item" href="#features"><div class="dropdown-icon">&#127795;</div><div><h4>{tr('crop_sugarcane')}</h4><p>{tr('crop_sugarcane_desc')}</p></div></a>
                        <a class="dropdown-item" href="#features"><div class="dropdown-icon">&#127793;</div><div><h4>{tr('crop_soybean')}</h4><p>{tr('crop_soybean_desc')}</p></div></a>
                    </div>
                </div>
            </div>
            <div class="nav-item active">
                <div class="nav-link">{tr('nav_industry')} <span class="nav-menu-caret">&#9662;</span></div>
                <div class="nav-dropdown mega">
                    <div class="dropdown-grid">
                        <a class="dropdown-item" href="#workflows"><div class="dropdown-icon">&#127806;</div><div><h4>{tr('food_retail')}</h4><p>{tr('food_retail_desc')}</p></div></a>
                        <a class="dropdown-item" href="#workflows"><div class="dropdown-icon">&#128230;</div><div><h4>{tr('cpg_fmcg')}</h4><p>{tr('cpg_fmcg_desc')}</p></div></a>
                        <a class="dropdown-item" href="#workflows"><div class="dropdown-icon">&#127793;</div><div><h4>{tr('seed_manufacturing')}</h4><p>{tr('seed_manufacturing_desc')}</p></div></a>
                        <a class="dropdown-item" href="#workflows"><div class="dropdown-icon">&#127970;</div><div><h4>{tr('governments')}</h4><p>{tr('governments_desc')}</p></div></a>
                        <a class="dropdown-item" href="#workflows"><div class="dropdown-icon">&#127981;</div><div><h4>{tr('food_processing')}</h4><p>{tr('food_processing_desc')}</p></div></a>
                        <a class="dropdown-item" href="#workflows"><div class="dropdown-icon">&#129309;</div><div><h4>{tr('agri_teams')}</h4><p>{tr('agri_teams_desc')}</p></div></a>
                    </div>
                </div>
            </div>
            <div class="nav-item">
                <div class="nav-link">{tr('nav_solutions')} <span class="nav-menu-caret">&#9662;</span></div>
                <div class="nav-dropdown compact">
                    <div class="dropdown-list">
                        <a class="dropdown-item" href="#trust"><div class="dropdown-icon">&#9989;</div><div><h4>{tr('verified_network')}</h4><p>{tr('verified_network_desc')}</p></div></a>
                        <a class="dropdown-item" href="#trust"><div class="dropdown-icon">&#128274;</div><div><h4>{tr('protected_access')}</h4><p>{tr('protected_access_desc')}</p></div></a>
                        <a class="dropdown-item" href="#trust"><div class="dropdown-icon">&#9881;</div><div><h4>{tr('operational_focus')}</h4><p>{tr('operational_focus_desc')}</p></div></a>
                    </div>
                </div>
            </div>
            <div class="nav-item">
                <div class="nav-link">{tr('nav_crop_knowledge')}</div>
                <div class="nav-dropdown compact">
                    <div class="dropdown-list">
                        <a class="dropdown-item" href="#demo"><div class="dropdown-icon">&#127793;</div><div><h4>{tr('crop_signals')}</h4><p>{tr('crop_signals_desc')}</p></div></a>
                        <a class="dropdown-item" href="#demo"><div class="dropdown-icon">&#128161;</div><div><h4>{tr('decision_guidance')}</h4><p>{tr('decision_guidance_desc')}</p></div></a>
                    </div>
                </div>
            </div>
            <div class="nav-item">
                <div class="nav-link">{tr('nav_resources')} <span class="nav-menu-caret">&#9662;</span></div>
                <div class="nav-dropdown compact">
                    <div class="dropdown-list">
                        <a class="dropdown-item" href="#demo"><div class="dropdown-icon">&#128218;</div><div><h4>{tr('guides')}</h4><p>{tr('guides_desc')}</p></div></a>
                        <a class="dropdown-item" href="#demo"><div class="dropdown-icon">&#128202;</div><div><h4>{tr('case_examples')}</h4><p>{tr('case_examples_desc')}</p></div></a>
                    </div>
                </div>
            </div>
            <div class="nav-item">
                <div class="nav-link">{tr('nav_company')} <span class="nav-menu-caret">&#9662;</span></div>
                <div class="nav-dropdown compact">
                    <div class="dropdown-list">
                        <a class="dropdown-item" href="#demo"><div class="dropdown-icon">&#127759;</div><div><h4>{tr('about_croppulse')}</h4><p>{tr('about_croppulse_desc')}</p></div></a>
                        <a class="dropdown-item" href="#demo"><div class="dropdown-icon">&#128233;</div><div><h4>{tr('contact')}</h4><p>{tr('contact_desc')}</p></div></a>
                    </div>
                </div>
            </div>
            <div class="nav-item">
                <div class="nav-link">{tr('nav_user')} <span class="nav-menu-caret">&#9662;</span></div>
                <div class="nav-dropdown compact">
                    <div class="dropdown-list">
                        <a class="dropdown-item" href="#workflows"><div class="dropdown-icon">&#128104;&#8205;&#127806;</div><div><h4>{tr('user_farmer')}</h4><p>{tr('user_farmer_desc')}</p></div></a>
                        <a class="dropdown-item" href="#workflows"><div class="dropdown-icon">&#129489;&#8205;&#128188;</div><div><h4>{tr('user_traders')}</h4><p>{tr('user_traders_desc')}</p></div></a>
                        <a class="dropdown-item" href="#workflows"><div class="dropdown-icon">&#127970;</div><div><h4>{tr('user_fpo')}</h4><p>{tr('user_fpo_desc')}</p></div></a>
                    </div>
                </div>
            </div>
            <div class="nav-item">
                <div class="nav-link">{tr('nav_language')} <span class="nav-menu-caret">&#9662;</span></div>
                <div class="nav-dropdown compact">
                    <div class="dropdown-list">
                        <a class="dropdown-item" href="{build_query_href(lang='en')}"><div class="dropdown-icon">&#127760;</div><div><h4>{tr('language_english')}</h4><p>{tr('language_english_desc')}</p></div></a>
                        <a class="dropdown-item" href="{build_query_href(lang='te')}"><div class="dropdown-icon">&#127760;</div><div><h4>{tr('language_telugu')}</h4><p>{tr('language_telugu_desc')}</p></div></a>
                    </div>
                </div>
            </div>
        </div>
        <div class="nav-actions">
            <a class="nav-chip secondary" href="{build_query_href(lang=current_lang, action='login')}">{tr('login')}</a>
            <a class="nav-chip primary" href="#demo">&#8981;</a>
        </div>
    </div>
    </div>
    <div class="landing-header-spacer"></div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-grid">
            <div>
                <div class="section-kicker">{tr('section_kicker')}</div>
                <div class="hero-title">{tr('hero_title')}</div>
                <div class="hero-subtitle">{tr('hero_subtitle')}</div>
                <p class="hero-copy">
                    {tr('hero_copy')}
                </p>
                <div class="hero-tags">
                    <span class="hero-tag">{tr('tag_sell')}</span>
                    <span class="hero-tag">{tr('tag_trader')}</span>
                    <span class="hero-tag">{tr('tag_listing')}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.landing_panel:
        st.markdown('<div id="auth"></div>', unsafe_allow_html=True)
        if st.session_state.landing_panel == "login":
            page_login()
        elif st.session_state.landing_panel == "register":
            page_register()

    st.markdown(f"""
    <div id="features" class="section-shell">
        <div class="section-header">
            <p class="section-title">{tr('platform_features')}</p>
            <p class="section-description">{tr('platform_features_desc')}</p>
        </div>
        <div class="card-grid">
            <div class="section-card">
                <div class="icon-badge">📈</div>
                <h3>{tr('feature_price_title')}</h3>
                <p>{tr('feature_price_desc')}</p>
                <div class="pill">{tr('pill_live_market')}</div>
            </div>
            <div class="section-card">
                <div class="icon-badge">🌱</div>
                <h3>{tr('feature_crop_title')}</h3>
                <p>{tr('feature_crop_desc')}</p>
                <div class="pill">{tr('pill_farmer_workflow')}</div>
            </div>
            <div class="section-card">
                <div class="icon-badge">🛒</div>
                <h3>{tr('feature_market_title')}</h3>
                <p>{tr('feature_market_desc')}</p>
                <div class="pill">{tr('pill_listing_flow')}</div>
            </div>
            <div class="section-card">
                <div class="icon-badge">📍</div>
                <h3>{tr('feature_trader_title')}</h3>
                <p>{tr('feature_trader_desc')}</p>
                <div class="pill">{tr('pill_verified_network')}</div>
            </div>
            <div class="section-card">
                <div class="icon-badge">🤝</div>
                <h3>{tr('feature_deal_title')}</h3>
                <p>{tr('feature_deal_desc')}</p>
                <div class="pill">{tr('pill_execution_support')}</div>
            </div>
            <div class="section-card">
                <div class="icon-badge">🌦️</div>
                <h3>{tr('feature_weather_title')}</h3>
                <p>{tr('feature_weather_desc')}</p>
                <div class="pill">{tr('pill_action_ready')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div id="workflows" class="section-shell">
        <div class="section-header">
            <p class="section-title">{tr('workflows_title')}</p>
            <p class="section-description">{tr('workflows_desc')}</p>
        </div>
        <div class="workflow-grid">
            <div class="workflow-card">
                <div class="pill">{tr('farmer_view')}</div>
                <h3>{tr('farmer_workflow')}</h3>
                <p>{tr('farmer_workflow_desc')}</p>
                <ul>
                    <li>{tr('farmer_b1')}</li>
                    <li>{tr('farmer_b2')}</li>
                    <li>{tr('farmer_b3')}</li>
                    <li>{tr('farmer_b4')}</li>
                </ul>
            </div>
            <div class="workflow-card alt">
                <div class="pill">{tr('trader_desk')}</div>
                <h3>{tr('buyer_workflow')}</h3>
                <p>{tr('buyer_workflow_desc')}</p>
                <ul>
                    <li>{tr('buyer_b1')}</li>
                    <li>{tr('buyer_b2')}</li>
                    <li>{tr('buyer_b3')}</li>
                    <li>{tr('buyer_b4')}</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div id="trust" class="section-shell">
        <div class="section-header">
            <p class="section-title">{tr('trust_title')}</p>
            <p class="section-description">{tr('trust_desc')}</p>
        </div>
        <div class="card-grid">
            <div class="section-card">
                <div class="icon-badge">✅</div>
                <h3>{tr('trust_card_1')}</h3>
                <p>{tr('trust_card_1_desc')}</p>
            </div>
            <div class="section-card">
                <div class="icon-badge">🔐</div>
                <h3>{tr('trust_card_2')}</h3>
                <p>{tr('trust_card_2_desc')}</p>
            </div>
            <div class="section-card">
                <div class="icon-badge">📋</div>
                <h3>{tr('trust_card_3')}</h3>
                <p>{tr('trust_card_3_desc')}</p>
            </div>
            <div class="section-card">
                <div class="icon-badge">🛡️</div>
                <h3>{tr('trust_card_4')}</h3>
                <p>{tr('trust_card_4_desc')}</p>
            </div>
            <div class="section-card">
                <div class="icon-badge">📡</div>
                <h3>{tr('trust_card_5')}</h3>
                <p>{tr('trust_card_5_desc')}</p>
            </div>
            <div class="section-card">
                <div class="icon-badge">⚙️</div>
                <h3>{tr('trust_card_6')}</h3>
                <p>{tr('trust_card_6_desc')}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-shell">
        <div class="section-header">
            <p class="section-title">{tr('why_title')}</p>
            <p class="section-description">{tr('why_desc')}</p>
        </div>
        <div class="mini-grid">
            <div class="mini-card">
                <h3>{tr('mini_1')}</h3>
                <p>{tr('mini_1_desc')}</p>
            </div>
            <div class="mini-card">
                <h3>{tr('mini_2')}</h3>
                <p>{tr('mini_2_desc')}</p>
            </div>
            <div class="mini-card">
                <h3>{tr('mini_3')}</h3>
                <p>{tr('mini_3_desc')}</p>
            </div>
        </div>
        <div class="card-grid">
            <div class="detail-card">
                <div class="pill">{tr('detail_pill_1')}</div>
                <h3>{tr('detail_title_1')}</h3>
                <p>{tr('detail_desc_1')}</p>
                <ul>
                    <li>{tr('detail_1_b1')}</li>
                    <li>{tr('detail_1_b2')}</li>
                    <li>{tr('detail_1_b3')}</li>
                </ul>
            </div>
            <div class="detail-card">
                <div class="pill">{tr('detail_pill_2')}</div>
                <h3>{tr('detail_title_2')}</h3>
                <p>{tr('detail_desc_2')}</p>
                <ul>
                    <li>{tr('detail_2_b1')}</li>
                    <li>{tr('detail_2_b2')}</li>
                    <li>{tr('detail_2_b3')}</li>
                </ul>
            </div>
            <div class="detail-card">
                <div class="pill">{tr('detail_pill_3')}</div>
                <h3>{tr('detail_title_3')}</h3>
                <p>{tr('detail_desc_3')}</p>
                <ul>
                    <li>{tr('detail_3_b1')}</li>
                    <li>{tr('detail_3_b2')}</li>
                    <li>{tr('detail_3_b3')}</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-shell">
        <div class="section-header">
            <p class="section-title">{tr('help_title')}</p>
            <p class="section-description">{tr('help_desc')}</p>
        </div>
        <div class="feedback-card">
            <div class="feedback-row">
                <div>
                    <div class="pill">{tr('feedback_channel')}</div>
                    <h3 style="margin-top: 0;">{tr('feedback_title')}</h3>
                    <p>{tr('feedback_desc')}</p>
                </div>
                <div>
                    <div class="pill">{tr('product_improvement')}</div>
                    <p style="margin-bottom: 16px;">{tr('product_improvement_desc')}</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div id="demo" class="demo-shell">
        <div class="pill" style="margin: 0 auto 16px auto; background: rgba(255,255,255,0.14); color: white;">{tr('demo_pill')}</div>
        <p class="demo-title">{tr('demo_title')}</p>
        <p class="demo-copy">{tr('demo_desc')}</p>
        <div class="demo-pills">
            <span class="demo-pill">{tr('demo_p1')}</span>
            <span class="demo-pill">{tr('demo_p2')}</span>
            <span class="demo-pill">{tr('demo_p3')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    demo_left, demo_center, demo_right = st.columns([1.2, 1.4, 1.2])
    with demo_center:
        st.markdown(f"### {tr('continue_demo')}")
        st.caption(tr('continue_demo_desc'))
        st.text_input(tr('work_email'), placeholder="your@email.com", key="landing_demo_email")
        demo_action1, demo_action2 = st.columns(2)
        with demo_action1:
            if st.button(tr('continue_to_demo'), key="landing_demo_continue", use_container_width=True):
                enter_demo_mode()
        with demo_action2:
            if st.button(tr('create_account'), key="landing_demo_register", use_container_width=True):
                reset_auth_flow()
                go_to_page("register")

    st.markdown(f'<p class="landing-footer">{tr("landing_footer")}</p>', unsafe_allow_html=True)

def page_register():
    """Farmer Registration"""
    header_col, switcher_col = st.columns([4, 1.6])
    with header_col:
        st.markdown(f"## {tr('register_title').replace('## ', '')}")
    with switcher_col:
        render_language_switcher("register", show_label=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        
        # Step 1: Phone Registration
        st.subheader(tr("step_1_phone"))
        phone = st.text_input(tr("phone_number_10"), placeholder="9876543210")
        
        if st.button(tr("send_otp"), use_container_width=True):
            if phone and len(phone) == 10 and phone.isdigit():
                # Check if user exists
                existing_user = get_user_by_phone(phone)
                if existing_user:
                    st.error(tr("phone_registered"))
                else:
                    # Generate and show OTP
                    otp = generate_otp()
                    st.session_state.otp_code = otp
                    st.session_state.phone_temp = phone
                    st.success(tr("otp_sent_demo", otp=otp))
                    st.info(tr("otp_demo_info"))
            else:
                st.error(tr("valid_phone_error"))
        
        # Step 2: OTP Verification
        if st.session_state.otp_code:
            st.subheader(tr("step_2_verify"))
            otp_input = st.text_input(tr("enter_otp"), placeholder="123456")
            
            if otp_input and otp_input == st.session_state.otp_code:
                st.success(tr("otp_verified"))
                
                # Step 3: Farmer Details
                st.subheader(tr("step_3_details"))
                
                col_a, col_b = st.columns(2)
                with col_a:
                    name = st.text_input(tr("full_name"), placeholder=tr("placeholder_name"))
                
                with col_b:
                    state = st.selectbox(
                        tr("state"),
                        STATE_OPTIONS,
                        format_func=lambda value: translate_option(value, STATE_KEYS),
                    )
                
                col_c, col_d = st.columns(2)
                with col_c:
                    district = st.text_input(tr("district"), placeholder=tr("placeholder_district"))
                
                with col_d:
                    village = st.text_input(tr("village"), placeholder=tr("placeholder_village"))
                
                land_size = st.number_input(tr("land_size"), min_value=0.5, value=1.0)
                soil_type = st.selectbox(
                    tr("soil_type"),
                    SOIL_OPTIONS,
                    format_func=lambda value: translate_option(value, SOIL_KEYS),
                )
                
                if st.button(tr("register_now"), use_container_width=True):
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
                            st.success(tr("registration_success"))
                            st.rerun()
                    else:
                        st.error(tr("fill_all_fields"))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button(tr("back_to_landing")):
            reset_auth_flow()
            go_to_page("landing")

def page_login():
    """Login Page"""
    st.markdown(tr("sign_in"))
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        
        phone = st.text_input(tr("phone_number"), placeholder="9876543210")
        
        if st.button(tr("send_otp"), use_container_width=True):
            if phone and len(phone) == 10:
                user = get_user_by_phone(phone)
                if user:
                    otp = generate_otp()
                    st.session_state.otp_code = otp
                    st.session_state.phone_temp = phone
                    st.success(tr("otp_sent_demo", otp=otp))
                else:
                    st.error(tr("user_not_found"))
        
        if st.session_state.otp_code:
            otp_input = st.text_input(tr("enter_otp"))
            
            if otp_input and otp_input == st.session_state.otp_code:
                user = get_user_by_phone(st.session_state.phone_temp)
                st.session_state.user = user[0]
                st.session_state.user_role = user[3]
                st.session_state.page = "dashboard"
                st.success(tr("login_success"))
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button(tr("back_to_landing")):
            reset_auth_flow()
            go_to_page("landing")

def page_dashboard():
    """Main Dashboard for Farmers/Traders"""
    # Top Navigation
    col1, col2, col3 = st.columns([5.0, 2.2, 1.2])
    
    with col1:
        st.markdown(tr("dashboard_title"))

    with col2:
        render_language_switcher("dashboard", show_label=True)
    
    with col3:
        if st.button(tr("logout")):
            st.session_state.user = None
            st.session_state.page = "landing"
            st.rerun()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        tr("tab_dashboard"), tr("tab_marketplace"), tr("tab_intelligence"), tr("tab_deals")
    ])
    
    with tab1:
        st.subheader(tr("your_dashboard"))
        
        if st.session_state.user_role == "farmer":
            dashboard_data = get_farmer_dashboard(st.session_state.user)

            if st.session_state.user == -1:
                st.info(tr("demo_mode_info"))

                demo_col1, demo_col2, demo_col3 = st.columns(3)

                with demo_col1:
                    st.markdown("""
                    <div class="dashboard-card">
                        <h4>""" + tr("best_time_to_sell") + """</h4>
                        <p style="font-size: 28px; color: #27ae60;">""" + tr("next_48_hours") + """</p>
                        <p>""" + tr("buyer_demand_strong") + """</p>
                    </div>
                    """, unsafe_allow_html=True)

                with demo_col2:
                    st.markdown("""
                    <div class="dashboard-card">
                        <h4>""" + tr("active_buyer_interest") + """</h4>
                        <p style="font-size: 28px; color: #3498db;">""" + tr("traders_count", count=12) + """</p>
                        <p>""" + tr("verified_buyers_watching") + """</p>
                    </div>
                    """, unsafe_allow_html=True)

                with demo_col3:
                    st.markdown("""
                    <div class="dashboard-card">
                        <h4>""" + tr("weather_watch") + """</h4>
                        <p style="font-size: 28px; color: #f39c12;">""" + tr("rain_alert") + """</p>
                        <p>""" + tr("prepare_harvest") + """</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("""
                <div class="dashboard-card">
                    <h4>""" + tr("demo_overview") + """</h4>
                    <p>""" + tr("demo_overview_desc") + """</p>
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
                        <p>{tr('location_value', district=profile[3], state=translate_state_value(profile[2]))}</p>
                        <p>{tr('land_acres', acres=profile[5])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4>{tr('rating')}</h4>
                        <p style="font-size: 28px; color: #f39c12;">{profile[7]:.1f}</p>
                        <p>{tr('deals_completed', count=profile[8])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    kyc_color = "🟢" if profile[6] == 'verified' else "🟡"
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4>{tr('kyc_status')}</h4>
                        <p>{kyc_color} {translate_status_value(profile[6])}</p>
                        <p>{tr('verified_priority')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Active Crops
                if dashboard_data["crops"]:
                    st.subheader(tr("your_active_crops"))
                    for crop in dashboard_data["crops"]:
                        st.markdown(f"""
                        <div class="dashboard-card">
                            <b>{translate_crop_value(crop[1])}</b> • {tr('land_acres', acres=crop[2])} • {tr('status_label')}: {translate_status_value(crop[3])}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Recent Listings
                if dashboard_data["listings"]:
                    st.subheader(tr("your_recent_listings"))
                    for listing in dashboard_data["listings"]:
                        st.markdown(f"""
                        <div class="dashboard-card">
                            📦 {tr('quantity_kg_value', quantity=listing[1])} • {tr('grade_label')}: {listing[2]} • {tr('price_per_kg_value', price=listing[3])}
                            <br><span class="status-badge status-active">{translate_status_value(listing[4])}</span>
                        </div>
                        """, unsafe_allow_html=True)
        
        else:  # Trader
            st.info(tr("trader_dashboard_info"))
    
    with tab2:
        st.subheader(tr("marketplace_title"))
        st.info(tr("marketplace_info"))
        
        with st.form("listing_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                crop = st.selectbox(tr("select_crop"), ["Rice", "Wheat", "Corn"], format_func=lambda value: translate_option(value, CROP_KEYS))
                quantity = st.number_input(tr("quantity"), min_value=100.0, value=1000.0)
            
            with col2:
                quality = st.selectbox(tr("quality_grade"), ["A", "B", "C"])
                price = st.number_input(tr("price_per_kg"), min_value=10.0, value=2000.0)
            
            available_from = st.date_input(tr("available_from"))
            available_until = st.date_input(tr("available_until"))
            
            if st.form_submit_button(tr("create_listing")):
                st.success(tr("listing_created"))
    
    with tab3:
        st.subheader(tr("intelligence_feed"))
        
        # Weather Alert
        col1, col2 = st.columns([0.5, 2])
        with col1:
            st.markdown("🌦️")
        with col2:
            st.markdown(f"{tr('rainfall_alert_title')}\n\n{tr('rainfall_alert_body')}")
        
        st.divider()
        
        # Price Alert
        col1, col2 = st.columns([0.5, 2])
        with col1:
            st.markdown("📈")
        with col2:
            st.markdown(f"{tr('sell_time_title')}\n\n{tr('sell_time_body')}")
        
        st.divider()
        
        # Scheme Alert
        col1, col2 = st.columns([0.5, 2])
        with col1:
            st.markdown("💰")
        with col2:
            st.markdown(f"{tr('scheme_alert_title')}\n\n{tr('scheme_alert_body')}")
    
    with tab4:
        st.subheader(tr("active_deals_title"))
        st.info(tr("active_deals_info"))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(tr("active_deals"), 2)
        with col2:
            st.metric(tr("pending_payment"), "₹45,000")
        with col3:
            st.metric(tr("completed_this_month"), 5)

# ============================================================================
# MAIN APP ROUTER
# ============================================================================

def main():
    """Main app router"""
    # Initialize schema before serving any page.
    init_database()
    initialize_language_from_query()

    if not test_connection():
        st.error(tr("db_connection_failed"))
        st.info(tr("db_connection_info"))
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
