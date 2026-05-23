# 🚀 DEPLOY PHASE 2 TO RAILWAY - STEP BY STEP

## ⏱️ Total Time: ~20 minutes

---

## STEP 1️⃣: Create Railway Account (2 min)

### Action:
1. Open: https://railway.app
2. Click **"Start Free"**
3. Click **"Continue with GitHub"**
4. Authorize Railway to access your GitHub account
5. Done! ✅

---

## STEP 2️⃣: Create New Railway Project (3 min)

### Action:
1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Search for: `corpplus`
4. Select: `bixamtarala/corpplus`
5. Confirm branch: `main`
6. Click **"Deploy"** ✅

**What happens:**
- Railway detects `Procfile`
- Starts building Docker image
- Build takes 2-3 minutes
- Watch logs in dashboard

---

## STEP 3️⃣: Add PostgreSQL Database (2 min)

### Action:
1. In Railway project dashboard, click **"+ New"** (top right)
2. Click **"Database"**
3. Select **"PostgreSQL"**
4. Click **"Add Plugin"** ✅

**What happens:**
- Railway provisions PostgreSQL instance
- Auto-injects `DATABASE_URL` environment variable
- Database ready in ~30 seconds

**Verify:**
- Go to **"Variables"** tab
- Should see `DATABASE_URL=postgresql://...`

---

## STEP 4️⃣: Set Environment Variables (3 min)

### Action:
1. Go to **"Variables"** tab in Railway
2. Click **"New Variable"** for each:

```
Variable Name          | Value
API_KEY_ADMIN         | <set-a-strong-admin-key>
API_KEY_FARMER        | croppulse_farmer_secret_key_12345
API_KEY_TRADER        | croppulse_trader_secret_key_12345
JWT_SECRET            | [Generate: python -c "import secrets; print(secrets.token_hex(32))"]
ENV                   | production
DEBUG                 | false
LOG_LEVEL             | INFO
FRONTEND_URL          | https://croppulse.streamlit.app
LANDING_PAGE_URL      | https://croppulse.com
```

3. For sensitive values (JWT_SECRET, API_KEYS):
   - Toggle **"Reference"** checkbox
   - This hides them from logs

4. Click **"Save"** ✅

**Done!** Railway automatically redeploys with new variables.

---

## STEP 5️⃣: Get Your Deployment URL (1 min)

### Action:
1. Go to **"Deployments"** tab
2. Wait for latest deployment to show ✅ (green checkmark)
3. Click on deployment row
4. Look for **"Domains"** section
5. Copy the URL (format: `https://xxxx.up.railway.app`)

### Example:
```
https://your-service-name.up.railway.app
```

**Save this URL!** You'll need it for Streamlit and testing.

---

## STEP 6️⃣: Test API is Working (3 min)

### Action (use PowerShell):

```powershell
# Replace YOUR_URL with actual Railway URL
$URL = "https://YOUR_URL.up.railway.app"

# Test 1: Health Check
curl "$URL/health" -Headers @{"Accept"="application/json"}

# Should return:
# {
#   "status": "healthy",
#   "service": "CropPulse API",
#   "version": "2.0.0"
# }

# Test 2: API Docs
Start-Process "$URL/api/docs"
# Opens Swagger UI in browser - should load instantly

# Test 3: Security Headers
curl -I "$URL/health"
# Should show security headers like x-frame-options, hsts, etc.
```

### Expected Results:
- ✅ Health check returns 200 with JSON
- ✅ Swagger UI loads with all 22 endpoints listed
- ✅ Response headers include security headers
- ✅ No error messages in logs

---

## STEP 7️⃣: Connect Streamlit to Your Backend (2 min)

### Action:

1. Open: `c:\Users\LENOVO\Desktop\Agritech\croppulse\croppulse_app.py`

2. Find this line (around line 1):
   ```python
   API_URL = "http://localhost:8000"
   ```

3. Replace with:
   ```python
   API_URL = "https://your-active-api-host"  # Your actual backend URL
   ```

4. Save the file

5. Commit and push:
   ```powershell
   cd c:\Users\LENOVO\Desktop\Agritech
   git add croppulse/croppulse_app.py
   git commit -m "Update API URL to Railway deployment"
   git push origin main
   ```

**What happens:**
- Streamlit Cloud detects changes
- Auto-redeployes Streamlit app
- Streamlit now uses your configured backend URL
- Takes 1-2 minutes

---

## STEP 8️⃣: Verify Integration (2 min)

### Action:

1. Open Streamlit app: https://croppulse.streamlit.app
2. Wait for app to load
3. Check for these signs:
   - ✅ Dashboard loads without errors
   - ✅ Data displays (see Rice prices)
   - ✅ Commodity dropdown works
   - ✅ Charts render properly
   - ✅ No error messages in browser console

4. Open browser Console (F12 → Console tab)
   - Should show NO red error messages
   - If CORS errors: Check API_URL matches exactly

---

## STEP 9️⃣: Final Verification Checklist

### ✅ API Tests:

```powershell
$URL = "https://YOUR_RAILWAY_URL"

# All should return 200
curl "$URL/health"
curl "$URL/"
curl "$URL/api/v1/prices/latest?commodity=rice"
curl "$URL/api/docs"
curl "$URL/api/redoc"
```

### ✅ Security Tests:

```powershell
# Test rate limiting (should get 429 on request 101)
for ($i=1; $i -le 101; $i++) {
    $response = curl -s -w "%{http_code}" "$URL/health"
    if ($response -like "*429*") { Write-Host "Rate limiting working!"; break }
}

# Test input validation
curl -X POST "$URL/api/v1/users" `
  -H "Content-Type: application/json" `
  -d '{"phone":"12345","name":"A","user_type":"farmer","state":"TN","village":"xyz"}'
# Should return 422 (Validation Error)
```

### ✅ Streamlit Integration:
- Dashboard loads
- No CORS errors
- Data displays
- API responds to queries

---

## 🎉 SUCCESS CRITERIA

Deployment is complete when:

- [ ] Railway app deploys successfully (green checkmark)
- [ ] PostgreSQL connected and variable set
- [ ] All environment variables configured
- [ ] Health check returns 200
- [ ] Streamlit connects to the configured backend
- [ ] Dashboard loads without errors
- [ ] All 22 API endpoints accessible
- [ ] Security headers present
- [ ] Rate limiting works (429 after 100 requests)

---

## 🚨 TROUBLESHOOTING

### "Build Failed" Error
```
Solution:
1. Check Railway logs for error message
2. Verify requirements.txt exists in root directory
3. Commit: git add requirements.txt && git push
4. Railway auto-retries
```

### "Connection refused" / "PostgreSQL error"
```
Solution:
1. Verify PostgreSQL plugin added in Railway
2. Check Variables tab has DATABASE_URL
3. Restart deployment (Railway → Deployments → Restart)
4. Check logs for connection error
```

### "CORS error" from Streamlit
```
Solution:
1. Verify Streamlit URL in API CORS config
2. Update main.py line 368:
   allow_origins=["https://croppulse.streamlit.app", ...]
3. Commit: git add phase2_backend/main.py && git push
4. Railway auto-redeploys
```

### "ModuleNotFoundError" for fastapi/pydantic/slowapi
```
Solution:
1. Verify all packages in requirements.txt
2. Check for typos in package names
3. Commit: git add requirements.txt && git push
4. Railway rebuilds and retries
```

### "Port already in use" or "Can't bind to 0.0.0.0:8000"
```
Solution:
1. Not an issue on Railway (auto-manages ports)
2. Check Procfile uses $PORT variable
3. Verify: web: uvicorn phase2_backend.main:app --host 0.0.0.0 --port $PORT
```

---

## 📊 DEPLOYMENT SUMMARY

| Component | Status | URL |
|-----------|--------|-----|
| FastAPI Backend | 🟢 Live | `https://your-service-name.up.railway.app` |
| PostgreSQL DB | 🟢 Live | (auto-connected) |
| Streamlit Frontend | 🟢 Live | `https://croppulse.streamlit.app` |
| API Docs | 🟢 Live | `https://your-service-name.up.railway.app/api/docs` |
| Health Check | 🟢 Live | `https://your-service-name.up.railway.app/health` |

---

## 📈 NEXT STEPS AFTER DEPLOYMENT

**This Week:**
- [ ] Monitor Railway logs for errors
- [ ] Test all 22 API endpoints
- [ ] Load test with 1000+ concurrent users
- [ ] Set up error monitoring (Sentry)

**Next Week:**
- [ ] Implement database migrations
- [ ] Add SMS/Twilio integration for OTP
- [ ] Deploy Redis cache layer
- [ ] Create admin dashboard

**Phase 2 Goals (4 weeks):**
- [ ] 5,000 farmer sign-ups
- [ ] 10,000 trader migrations
- [ ] 1,000+ daily transactions
- [ ] $50K/month revenue

---

## ✨ YOU'RE LIVE!

Once complete:

```
🎉 Phase 2 Backend is deployed to production!
🎉 Streamlit frontend connected to your configured backend!
🎉 PostgreSQL database operational!
🎉 TIER 1 security active on all 22 endpoints!
🎉 Ready for farmer & trader onboarding!
```

---

**Estimated Total Time:** 15-20 minutes
**Difficulty:** Easy (mostly clicking buttons)
**Support:** All error messages linked to solutions above

Ready? Let's go! 🚀
