# CropPulse Phase 2 - Streamlit Upgrade Guide

## 🚀 Quick Start

This guide helps you upgrade from Phase 1 (CSV-based) to Phase 2 (PostgreSQL-powered) Streamlit app.

### What's New in Phase 2?

✅ **Landing Page** - Professional first impression  
✅ **User Authentication** - OTP-based registration & login  
✅ **Database Backend** - PostgreSQL instead of CSV files  
✅ **Farmer Dashboard** - Crop management & KYC status  
✅ **Marketplace Features** - Create listings, receive offers  
✅ **Intelligence Feed** - Real-time alerts & recommendations  
✅ **Deal Tracking** - Monitor active transactions  

---

## 📋 Prerequisites

- Python 3.9 or higher
- PostgreSQL 12+ (or Railway PostgreSQL)
- Streamlit account (for deployment)
- Git

---

## 🔧 Local Setup (5 minutes)

### 1. Install Dependencies

```bash
# Activate your virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Phase 2 dependencies
pip install -r requirements_phase2_streamlit.txt
```

### 2. Setup PostgreSQL

**Option A: Local PostgreSQL**

```bash
# Create database
createdb croppulse_phase2

# Get your connection string
# postgresql://postgres:your_password@localhost:5432/croppulse_phase2
```

**Option B: Railway PostgreSQL (Recommended for Deployment)**

1. Go to https://railway.app/
2. Create new project → Add PostgreSQL
3. Copy DATABASE_URL from the database details
4. Use this in your .env file

### 3. Configure Environment

```bash
# Copy example to .env
cp .env.example.streamlit .env

# Edit .env with your DATABASE_URL
nano .env
```

Example `.env`:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/croppulse_phase2
SECRET_KEY=your_random_secret_key
API_KEY=<set-a-strong-admin-key>
```

### 4. Initialize Database

```bash
python -c "from db_config import init_database; init_database()"
```

You should see:
```
✅ Database connection pool created
✅ Database tables initialized successfully
```

### 5. Run Streamlit App

```bash
streamlit run streamlit_app_phase2.py
```

Open http://localhost:8501 in your browser.

---

## 📱 Test the App

### User Flow 1: Register as Farmer

1. Click "👨‍🌾 Register as Farmer"
2. Enter phone: `9876543210`
3. Click "Send OTP" → See demo OTP on screen (e.g., `123456`)
4. Enter OTP
5. Fill farmer details (name, state, district, land size)
6. Click "Register Now"
7. See farmer dashboard with:
   - Profile card (location, land size)
   - Rating & deals count
   - KYC status
   - Active crops
   - Listings

### User Flow 2: Login as Trader

1. Click "🧑‍💼 Trader Login"
2. Use a registered phone number
3. Verify OTP
4. Access trader dashboard

### Features to Test

- **📊 Dashboard Tab** - View profile, crops, listings
- **🌱 Crops Tab** - Add new crops with details
- **🛒 Marketplace Tab** - Create listings (sell crops)
- **📡 Intelligence Tab** - See market alerts & recommendations
- **💰 Deals Tab** - Track active transactions

---

## 🗄️ Database Schema

### Core Tables

**users** - Phone, role (farmer/trader), JWT tracking  
**farmer_profiles** - Location, land size, KYC status, ratings  
**trader_profiles** - Business name, GST, license  
**crops** - Crop details, sowing/harvest dates  
**listings** - Items for sale (quantity, quality, price)  
**offers** - Trader offers on listings  
**deals** - Completed transactions  
**transactions** - Payment records  
**market_prices** - eNAM API cache  
**government_schemes** - Subsidy info  
**alert_logs** - Notifications sent  

See `db_config.py` for complete schema.

---

## 🚀 Deploy to Streamlit Cloud

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Phase 2: Streamlit upgrade with PostgreSQL"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select your GitHub repo
4. Set main file: `streamlit_app_phase2.py`
5. Add secrets in "Advanced settings":
   ```
   DATABASE_URL = your_railway_postgresql_url
   SECRET_KEY = your_secret_key
   API_KEY = your_api_key
   ```

### Step 3: Link to Railway PostgreSQL

Streamlit Cloud will run the app and connect to your Railway PostgreSQL automatically.

---

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `streamlit_app_phase2.py` | Main Streamlit app (landing + dashboard + auth) |
| `db_config.py` | PostgreSQL connection & schema management |
| `requirements_phase2_streamlit.txt` | All Python dependencies |
| `.env.example.streamlit` | Environment variable template |
| `.streamlit/config.toml` | Streamlit configuration |

---

## 🧪 Testing Commands

```bash
# Test database connection
python -c "from db_config import test_connection; print('OK' if test_connection() else 'FAILED')"

# Create test user
python << 'EOF'
from db_config import get_db_connection
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (phone, name, role) VALUES (%s, %s, %s) RETURNING id", ('9999999999', 'Test User', 'farmer'))
    print(f"User created: {cursor.fetchone()[0]}")
EOF

# List all users
python << 'EOF'
from db_config import get_db_connection
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT id, phone, name, role FROM users")
    for user in cursor.fetchall():
        print(user)
EOF
```

---

## 🛠️ Troubleshooting

### "Database connection failed"

❌ **Problem**: `psycopg2.OperationalError`

✅ **Solution**:
```bash
# Check DATABASE_URL
echo $DATABASE_URL

# Verify PostgreSQL is running
psql -l

# Test connection manually
python -c "import psycopg2; psycopg2.connect('your_database_url')"
```

### "ModuleNotFoundError: No module named 'db_config'"

✅ **Solution**:
```bash
# Make sure db_config.py is in the same directory as streamlit_app_phase2.py
ls db_config.py
```

### "Table 'users' does not exist"

✅ **Solution**:
```bash
# Reinitialize database
python -c "from db_config import init_database; init_database()"
```

### Streamlit Cloud deployment failing

✅ **Solutions**:
1. Check `.streamlit/secrets.toml` has DATABASE_URL
2. Verify Railway PostgreSQL connection string
3. Check Railway is running (not sleeping)
4. View deployment logs on Streamlit Cloud dashboard

---

## 📊 Analytics & Monitoring

### View Database Statistics

```bash
# Count users
psql $DATABASE_URL -c "SELECT COUNT(*) as total_users FROM users;"

# Count farmers
psql $DATABASE_URL -c "SELECT COUNT(*) as total_farmers FROM farmer_profiles;"

# Active listings
psql $DATABASE_URL -c "SELECT COUNT(*) as active_listings FROM listings WHERE status = 'active';"
```

---

## 🎯 Next Steps

1. ✅ **Run locally** - Test farmer registration & dashboard
2. ✅ **Deploy to Streamlit Cloud** - Make it live
3. ⏳ **Add more features**:
   - Image uploads (crops, KYC documents)
   - Real marketplace matching (show farmers other listings)
   - Notification system (SMS/WhatsApp)
   - Payment integration (Razorpay)
   - Analytics dashboard

---

## 📞 Support

For issues or questions:
1. Check logs: `tail -f .streamlit/logs/`
2. Review database: `psql $DATABASE_URL`
3. Test connection: `python -c "from db_config import test_connection; test_connection()"`

---

## 🎉 You're Ready!

Phase 2 Streamlit is production-ready. Deploy today and start scaling! 🚀

**Phase 2 Vision**: 50,000 farmers + 10,000 traders by Dec 2026  
**Revenue Target**: $50K/month in transaction commissions  
**Success Metric**: 40% 30-day retention rate  
