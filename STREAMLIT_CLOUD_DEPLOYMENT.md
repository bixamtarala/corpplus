# Phase 2.2: Streamlit Cloud Deployment Guide

## Overview

Deploy the CropPulse Streamlit frontend to Streamlit Cloud while keeping the FastAPI backend on Railway.

---

## Architecture After Deployment

```
┌─────────────────────────────────────────┐
│  Streamlit Cloud (Frontend)             │
│  https://app.croppulse.com              │
│                                         │
│  - Dashboard UI                         │
│  - Charts & Analytics                   │
│  - User Interface                       │
└──────────────┬──────────────────────────┘
               │ API Calls
               ↓
┌─────────────────────────────────────────┐
│  Railway (Backend)                      │
│  https://api.croppulse.com              │
│                                         │
│  - 22 REST Endpoints                    │
│  - Authentication                       │
│  - Business Logic                       │
│  - Rate Limiting                        │
└──────────────┬──────────────────────────┘
               │ SQL Queries
               ↓
┌─────────────────────────────────────────┐
│  PostgreSQL Database                    │
│  (Railway or Supabase)                  │
└─────────────────────────────────────────┘
```

---

## Step-by-Step Deployment

### Step 1: Create Streamlit Cloud Account

1. Go to https://streamlit.io/cloud
2. Click "Sign Up"
3. Sign in with GitHub (required for Streamlit Cloud)

### Step 2: Deploy from GitHub

1. Go to https://share.streamlit.io
2. Click "Create App"
3. Select repository: `bixamtarala/croppulse`
4. Main file path: `croppulse/croppulse_app.py`
5. Click "Deploy"

**Streamlit automatically detects:**
- `requirements.txt` for dependencies
- `.streamlit/config.toml` for settings

### Step 3: Configure Secrets

**Streamlit Cloud uses `secrets.toml` stored securely in their platform:**

1. In Streamlit Cloud dashboard → Select your app
2. Click "⋮ (More)" → "Manage Secrets"
3. Add these secrets:

```toml
BACKEND_API_URL = "https://web-production-7295a.up.railway.app"
API_KEY = "croppulse_admin_secret_key_12345"
ENVIRONMENT = "production"
```

**Important:** Never commit secrets to GitHub. Local `.streamlit/secrets.toml` is in `.gitignore`.

### Step 4: Verify Deployment

1. Wait for build to complete (usually 2-3 minutes)
2. App is live at: `https://croppulse-<random>.streamlit.app`
3. Check logs for errors
4. Test by clicking "Always rerun" to see live updates

### Step 5: Custom Domain (Optional)

1. In Streamlit Cloud dashboard
2. Click "Settings" for your app
3. Add custom domain: `app.croppulse.com`
4. Update DNS with CNAME record

---

## Key Changes Made to Frontend

### Updated API Integration

**Before:**
```python
# Hardcoded test data
df = pd.read_csv('commodity_prices.csv')
```

**After:**
```python
# Live API data from Railway
BACKEND_API_URL = "https://web-production-7295a.up.railway.app"
response = requests.get(f"{BACKEND_API_URL}/api/v1/prices/latest")
data = response.json()
```

### Fallback Chain

1. **Primary:** CropPulse Backend API (Railway)
2. **Secondary:** eNAM API (if available)
3. **Tertiary:** CSV demo data (local testing)

---

## Testing Locally

Before deploying to Streamlit Cloud, test locally:

```bash
cd croppulse
streamlit run croppulse_app.py
```

The app will:
1. Try to connect to Railway backend
2. Show "✅ Live data from CropPulse Backend API!"
3. Display real data from your API

---

## Environment Variables

### For Streamlit Cloud

Add in Dashboard → App settings → Secrets:

```toml
BACKEND_API_URL = "https://web-production-7295a.up.railway.app"
API_KEY = "croppulse_admin_secret_key_12345"
```

### For Local Development

Create `.streamlit/secrets.toml`:

```toml
BACKEND_API_URL = "http://localhost:8000"
API_KEY = "croppulse_admin_secret_key_12345"
```

---

## Troubleshooting

### Issue: "Connection refused" or "Cannot reach API"

**Cause:** Railway backend not accessible

**Solution:**
1. Verify Railway API is running: `https://web-production-7295a.up.railway.app/`
2. Check API key is correct in secrets
3. Verify CORS is enabled on backend

### Issue: "Module not found" error

**Cause:** Dependencies not in `requirements.txt`

**Solution:**
1. Ensure all imports are in `croppulse/requirements.txt`
2. Check Python version compatibility
3. Reinstall locally: `pip install -r croppulse/requirements.txt`

### Issue: Dashboard shows cached/old data

**Cause:** Streamlit cache not refreshing

**Solution:**
1. Click "Always rerun" during testing
2. Cache TTL is 5 minutes by default
3. Manually clear cache: "Rerun" button at top

### Issue: API returns 401 Unauthorized

**Cause:** Invalid API key

**Solution:**
1. Verify key in Streamlit Cloud secrets
2. Ensure key matches: `croppulse_admin_secret_key_12345`
3. Check Railway backend is still running

---

## Performance Optimization

### Caching Strategy

```python
@st.cache_data(ttl=300)  # 5 minutes - prices change frequently
def load_prices():
    return api.get_prices()

@st.cache_data(ttl=3600)  # 1 hour - historical data stable
def load_history():
    return api.get_history()
```

### Connection Pooling

Streamlit automatically manages connection pooling. No additional configuration needed.

---

## Monitoring

### Streamlit Cloud Logs

1. Go to your app in Streamlit Cloud
2. Click "⋮ (More)" → "View logs"
3. Monitor for:
   - API connection errors
   - Missing dependencies
   - Performance issues

### Railway Logs

1. Go to Railway dashboard
2. Select "web" service
3. Check "Deploy logs" for backend errors

---

## Security Checklist

- [ ] API key NOT exposed in code (using secrets)
- [ ] CORS configured on FastAPI backend
- [ ] HTTPS enforced (automatic on both platforms)
- [ ] Rate limiting active on backend
- [ ] Input validation on backend
- [ ] Audit logging enabled

---

## Next Steps After Deployment

1. **Test all user flows:**
   - Load dashboard
   - Check price updates
   - View risk analysis
   - Run forecasts

2. **Monitor performance:**
   - Check API response times
   - Monitor error rates
   - Track user analytics

3. **Prepare for Phase 3:**
   - Add mobile app support
   - Integrate payment system
   - Deploy logistics module

---

## Rolling Back

If something breaks:

1. **Streamlit Cloud:**
   - Go to app settings
   - Select previous working deployment
   - Click "Revert"

2. **Git method:**
   ```bash
   git revert <bad-commit>
   git push origin main
   # Streamlit auto-redeploys
   ```

---

## Frequently Asked Questions

**Q: Can I use localhost for API calls?**
A: No, Streamlit Cloud runs on servers. Must use public URLs like Railway.

**Q: How often does it redeploy?**
A: Automatically on every GitHub push to `main` branch.

**Q: What's the free tier limit?**
A: 1 free app, 1GB RAM, shared CPU. Upgrade to Pro for scaling.

**Q: Can I add authentication to the Streamlit app?**
A: Yes, use `streamlit-authenticator` library for login flows.

**Q: How do I update the API endpoint?**
A: Change `BACKEND_API_URL` in Streamlit Cloud secrets.

---

## Deployment Completed! 🎉

Your CropPulse Phase 2 architecture is now:
- **Backend**: Production-ready on Railway ✅
- **Frontend**: Live on Streamlit Cloud ✅
- **Database**: Ready to connect ⏳
- **Full integration**: Auto-updating dashboard ✅

Next: Phase 3 (Logistics + Finance modules)
