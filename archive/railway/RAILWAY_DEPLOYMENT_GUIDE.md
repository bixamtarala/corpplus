# CropPulse Phase 2 - Railway.app Deployment Guide

## Overview
This guide walks through deploying the CropPulse FastAPI backend to Railway.app with PostgreSQL database integration.

---

## Prerequisites
- ✅ GitHub account with repository https://github.com/bixamtarala/corpplus
- ✅ Railway.app account (free: https://railway.app)
- ✅ Phase 2 backend code in `phase2_backend/` folder
- ✅ `requirements.txt` with all dependencies
- ✅ `Procfile` for process management
- ✅ `.env.example` with environment variable template

---

## Step 1: Prepare GitHub Repository

### 1.1 Verify repository structure:
```
corpplus/
├── phase2_backend/
│   ├── main.py              (1,100+ lines, all endpoints)
│   ├── models.py            (SQLAlchemy ORM models - TODO)
│   ├── requirements.txt      (40+ dependencies)
│   └── SECURITY_IMPLEMENTATION.md
├── Procfile                 (Railway process definition)
├── railway.json             (Railway configuration)
├── .env.example             (Environment variables template)
├── .gitignore               (Excludes .env, logs/, __pycache__)
└── README.md
```

### 1.2 Ensure .gitignore excludes sensitive files:
```bash
# Check .gitignore contains:
.env
.env.local
*.log
logs/
__pycache__/
.venv/
.DS_Store
.vscode/
```

### 1.3 Commit deployment files:
```bash
cd c:\Users\LENOVO\Desktop\Agritech
git add Procfile railway.json .env.example
git commit -m "Add Railway deployment configuration and environment variables"
git push origin main
```

---

## Step 2: Create Railway Project

### 2.1 Go to Railway.app
1. Visit https://railway.app
2. Sign in with GitHub account
3. Click "New Project"

### 2.2 Deploy from GitHub
1. Select "Deploy from GitHub repo"
2. Choose repository: `bixamtarala/corpplus`
3. Select branch: `main`
4. Railway will auto-detect Procfile and start building

---

## Step 3: Configure PostgreSQL Database

### 3.1 Add PostgreSQL Plugin
1. In Railway project dashboard
2. Click "+ New" (top right)
3. Select "PostgreSQL"
4. Railway will provision a PostgreSQL instance

### 3.2 Configure Database Connection
1. Railway auto-injects `DATABASE_URL` environment variable
2. Verify in "Variables" tab:
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

### 3.3 Run Database Migrations (TODO)
Once deployed, run:
```bash
# Connect to Railway shell and run Alembic migrations
alembic upgrade head
```

---

## Step 4: Set Environment Variables

### 4.1 Add Environment Variables in Railway

Go to project → Variables tab. Add:

#### Security & API Keys
```
API_KEY_ADMIN=<set-a-strong-admin-key>
API_KEY_FARMER=croppulse_farmer_secret_key_12345
API_KEY_TRADER=croppulse_trader_secret_key_12345
JWT_SECRET=(generate with: python -c "import secrets; print(secrets.token_hex(32))")
```

#### Environment & Logging
```
ENV=production
DEBUG=false
LOG_LEVEL=INFO
```

#### Service Integrations (Add as available)
```
TWILIO_ACCOUNT_SID=(your SID)
TWILIO_AUTH_TOKEN=(your token)
TWILIO_PHONE_NUMBER=(your Twilio number)

SENDGRID_API_KEY=(your SendGrid API key)
SENDGRID_FROM_EMAIL=noreply@croppulse.com

STRIPE_SECRET_KEY=(your Stripe secret)
STRIPE_PUBLISHABLE_KEY=(your Stripe public)

WEATHER_API_KEY=(your weather API key)
ENAM_API_KEY=(your eNAM API key)
```

#### Frontend URLs
```
FRONTEND_URL=https://croppulse.streamlit.app
LANDING_PAGE_URL=https://croppulse.com
```

### 4.2 Mark variables as "reference" (not visible in logs)
- Toggle "Reference" for sensitive values
- This prevents secrets appearing in deployment logs

---

## Step 5: Deploy & Verify

### 5.1 Monitor Deployment
1. Railway dashboard shows build status
2. Watch logs in "Deployments" tab
3. Build should complete in 2-3 minutes

### 5.2 Get Deployment URL
- Railway assigns auto URL: `https://your-service-name.up.railway.app`
- Public domain section shows live API URL
- Example: `https://your-service-name.up.railway.app`

### 5.3 Test API Endpoints

```bash
# Test health check
curl https://your-service-name.up.railway.app/health

# Expected response:
{
  "status": "healthy",
  "service": "CropPulse API",
  "version": "2.0.0",
  "timestamp": "2026-05-14T12:30:58"
}

# Test with API key
curl -H "X-API-Key: croppulse_farmer_secret_key_12345" \
  https://your-service-name.up.railway.app/api/v1/prices/latest?commodity=rice
```

### 5.4 Verify Security Features
```bash
# Check security headers
curl -i https://your-service-name.up.railway.app/health | grep -E "x-frame-options|content-security-policy|hsts"

# Should see:
# x-frame-options: DENY
# content-security-policy: default-src 'self'...
# strict-transport-security: max-age=31536000
```

---

## Step 6: Connect to Streamlit Frontend

### 6.1 Update Streamlit app to use your backend URL
In `croppulse_app.py`:
```python
# Replace:
API_URL = "http://localhost:8000"

# With:
API_URL = "https://your-active-api-host"
```

### 6.2 Verify CORS is working
```bash
curl -H "Origin: https://croppulse.streamlit.app" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS \
  https://your-service-name.up.railway.app/api/v1/users
```

Should return CORS headers:
```
Access-Control-Allow-Origin: https://croppulse.streamlit.app
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
```

---

## Step 7: Configure Custom Domain (Optional)

### 7.1 Add Custom Domain
1. Railway project → Settings
2. Custom Domains section
3. Add: `api.croppulse.com`
4. Copy CNAME value from Railway

### 7.2 Update DNS
1. Go to your domain registrar (GoDaddy, Namecheap, etc.)
2. Add CNAME record:
   ```
   Subdomain: api
   Type: CNAME
   Value: (from Railway)
   TTL: 3600
   ```
3. Wait 15-30 minutes for DNS propagation

### 7.3 Verify custom domain
```bash
curl https://api.croppulse.com/health
```

---

## Step 8: Set Up Monitoring & Alerts (Optional)

### 8.1 Enable Railway Metrics
1. Project → Metrics tab
2. Monitor CPU, Memory, Network

### 8.2 Set up alerts
1. Settings → Alerts
2. Alert on: High CPU, High Memory, Deployment failure
3. Notification channel: Email

### 8.3 Integrate Sentry for error tracking
1. Create Sentry account: https://sentry.io
2. Create new project (Python/FastAPI)
3. Copy Sentry DSN
4. Add to Railway variables:
   ```
   SENTRY_DSN=https://xxxxx@sentry.io/project_id
   ```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
**Cause:** requirements.txt not found or dependencies not installed
**Solution:**
- Verify `requirements.txt` exists in project root
- Check all dependencies are listed
- Commit and push to GitHub → Railway redeploys automatically

### "Connection refused to postgresql://..."
**Cause:** PostgreSQL not provisioned or DATABASE_URL not set
**Solution:**
- Verify PostgreSQL plugin added in Railway
- Check DATABASE_URL environment variable is set
- Restart deployment

### "CORS error from Streamlit to API"
**Cause:** Frontend URL not in CORS whitelist
**Solution:**
- Update `main.py` line 368:
  ```python
  allow_origins=[
      "https://croppulse.streamlit.app",  # Your actual URL
      ...
  ]
  ```
- Commit, push, redeploy

### "API slow / timeout errors"
**Cause:** Database query or external API latency
**Solution:**
- Check PostgreSQL CPU/Memory usage
- Enable Redis caching
- Review logs in Railway deployment tab
- Add database indexes for frequent queries

---

## Deployment Checklist

- [ ] GitHub repository has all Phase 2 files
- [ ] Procfile created and committed
- [ ] railway.json configured
- [ ] .env.example with all variables
- [ ] .gitignore excludes .env and sensitive files
- [ ] All commits pushed to origin/main
- [ ] Railway project created and connected to GitHub
- [ ] PostgreSQL plugin added
- [ ] All environment variables set in Railway
- [ ] Deployment successful (no build errors)
- [ ] Health check endpoint responds with 200
- [ ] Security headers present in responses
- [ ] Streamlit frontend connected to API
- [ ] CORS working between Streamlit and Railway
- [ ] API responds to OTP/user/price endpoints
- [ ] Logs visible in Railway dashboard

---

## Next Steps (Phase 2 Continuation)

### Immediate (This week):
- [ ] Deploy PostgreSQL models/migrations
- [ ] Integrate Twilio for SMS OTP
- [ ] Set up Redis cache
- [ ] Create admin dashboard

### Next week:
- [ ] Deploy to production with custom domain
- [ ] Enable monitoring/alerting
- [ ] Implement rate limiting in production
- [ ] Load testing with 1000+ concurrent users

### Phase 2 Goals:
- [ ] 50,000 farmer sign-ups
- [ ] 10,000 trader migrations
- [ ] 1,000+ daily transactions
- [ ] $50K/month commission revenue

---

## Deployment URLs

After successful deployment, update these:

**API URL:** `https://your-service-name.up.railway.app` (or `https://api.croppulse.com`)
**API Docs:** `https://your-service-name.up.railway.app/api/docs`
**ReDoc:** `https://your-service-name.up.railway.app/api/redoc`
**OpenAPI:** `https://your-service-name.up.railway.app/api/openapi.json`

**Streamlit Frontend:** `https://croppulse.streamlit.app`
**Landing Page:** `https://croppulse.com`
**Admin Dashboard:** `https://admin.croppulse.com` (TODO)

---

**Status:** ✅ Phase 2 Backend Deployment Ready
**Date:** May 14, 2026
**Version:** FastAPI 0.104.0+ with OWASP TIER 1 Security
