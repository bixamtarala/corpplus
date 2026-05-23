# Phase 2 Deployment - Quick Start

## 🚀 Deploy in 5 Minutes

### Prerequisites:
- ✅ GitHub account at https://github.com/bixamtarala/corpplus
- ✅ Railway.app account at https://railway.app

---

## Option A: Deploy to Railway (Recommended)

### Step 1: Create Railway Project
```bash
# 1. Go to https://railway.app
# 2. Click "New Project"
# 3. Select "Deploy from GitHub"
# 4. Choose: bixamtarala/corpplus (main branch)
# 5. Click Deploy
```

### Step 2: Add PostgreSQL
```
In Railway dashboard:
1. Click "+ New"
2. Select "PostgreSQL"
3. Done! Database auto-provisioned
```

### Step 3: Set Environment Variables
```
Go to Variables tab, add:
- API_KEY_ADMIN=<set-a-strong-admin-key>
- API_KEY_FARMER=croppulse_farmer_secret_key_12345
- API_KEY_TRADER=croppulse_trader_secret_key_12345
- JWT_SECRET=(generate new secure value)
- ENV=production
```

### Step 4: Verify Deployment
```bash
# Get your Railway URL from dashboard, then:
curl https://your-url.up.railway.app/health

# Should return:
{
  "status": "healthy",
  "service": "CropPulse API",
  "version": "2.0.0"
}
```

---

## Option B: Deploy Locally with Docker

### Prerequisites:
- Docker Desktop installed

### Step 1: Start Services
```bash
cd c:\Users\LENOVO\Desktop\Agritech
docker-compose up -d
```

### Step 2: Verify Services
```bash
# API should be available at:
curl http://localhost:8000/health

# PostgreSQL available at:
localhost:5432

# Redis available at:
localhost:6379
```

### Step 3: Stop Services
```bash
docker-compose down
```

---

## Files Created for Deployment

✅ **Procfile** - Railway process definition
✅ **railway.json** - Railway configuration
✅ **Dockerfile** - Container image definition
✅ **docker-compose.yml** - Local testing with PostgreSQL + Redis
✅ **.env.example** - Environment variables template
✅ **DEPLOY_TO_STREAMLIT_CLOUD.md** - Active Streamlit deployment guide

---

## Deployment Checklist

- [ ] Files committed to GitHub (Procfile, Dockerfile, etc.)
- [ ] Railway project created
- [ ] PostgreSQL added to Railway
- [ ] Environment variables configured
- [ ] Deployment successful
- [ ] Health check returns 200
- [ ] Update Streamlit to use your active backend URL (if you are using an external API)

---

## Important URLs After Deployment

```
API Base: https://your-app.up.railway.app
API Docs: https://your-app.up.railway.app/api/docs
Health: https://your-app.up.railway.app/health
```

---

## Next Steps

1. **Database Setup** (Phase 2):
   ```bash
   # Run migrations (once deployed):
   alembic upgrade head
   ```

2. **Third-party Services**:
   - Integrate Twilio for SMS OTP
   - Add Stripe for payments
   - Connect weather API

3. **Monitoring**:
   - Enable Sentry for error tracking
   - Set up Railway alerts
   - Monitor database performance

---

For detailed instructions, see: **DEPLOY_TO_STREAMLIT_CLOUD.md**

Older Railway-focused docs have been archived under `archive/railway/` for historical reference only.

**Status:** ✅ Ready to deploy
**Version:** FastAPI 0.104.0+ with TIER 1 Security
