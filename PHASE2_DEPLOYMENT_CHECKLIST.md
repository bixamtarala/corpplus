# Phase 2 Deployment Checklist - May 14, 2026

## 🎯 Goal: Deploy FastAPI Backend to Railway.app

**Timeline:** May 14-15, 2026
**Status:** ✅ Code Ready | ⏳ Deployment In Progress

---

## ✅ Pre-Deployment Checklist (COMPLETE)

- [x] FastAPI backend built (1,100+ lines)
- [x] All TIER 1 security features implemented
- [x] 22 endpoints fully functional
- [x] Pydantic v2 compatible (4 fixes applied)
- [x] All dependencies installed and tested
- [x] 9 startup tests passing
- [x] Procfile created
- [x] railway.json configured
- [x] Dockerfile created
- [x] docker-compose.yml created
- [x] .env.example with 70+ variables
- [x] All files committed to GitHub
- [x] Repository ready at: https://github.com/bixamtarala/corpplus

---

## 🚀 Deployment Steps (IN PROGRESS)

### Step 1: Create Railway Account & Project
- [ ] Go to https://railway.app
- [ ] Sign in with GitHub (authorize corpplus repo)
- [ ] Create new project
- [ ] Connect to repository: `bixamtarala/corpplus`
- [ ] Select branch: `main`
- [ ] Let Railway auto-detect Procfile
- [ ] Click "Deploy"

**Expected Time:** 5 minutes
**Est. Build Time:** 2-3 minutes

### Step 2: Provision PostgreSQL Database
- [ ] In Railway dashboard, click "+ New"
- [ ] Select "PostgreSQL"
- [ ] Railway auto-provisions database
- [ ] Copy DATABASE_URL from Variables tab
- [ ] Should auto-inject into app

**Expected Time:** 2 minutes
**Automatic Setup:** Yes

### Step 3: Configure Environment Variables
- [ ] Go to Variables tab in Railway
- [ ] Add these 10 critical variables:

```
API_KEY_ADMIN = croppulse_admin_secret_key_12345
API_KEY_FARMER = croppulse_farmer_secret_key_12345
API_KEY_TRADER = croppulse_trader_secret_key_12345
JWT_SECRET = (generate: python -c "import secrets; print(secrets.token_hex(32))")
ENV = production
DEBUG = false
LOG_LEVEL = INFO
FRONTEND_URL = https://croppulse.streamlit.app
LANDING_PAGE_URL = https://croppulse.com
DATABASE_URL = (auto-injected by PostgreSQL plugin)
```

**Expected Time:** 5 minutes
**Mark as Reference:** Yes (for sensitive values)

### Step 4: Verify Deployment
- [ ] Check deployment logs in Railway
- [ ] Wait for "Build successful" message
- [ ] Get deployment URL (format: `https://xxxx.up.railway.app`)
- [ ] Test health endpoint:
  ```bash
  curl https://[YOUR_URL]/health
  ```
- [ ] Should return 200 with healthy status

**Expected Time:** 5 minutes
**Success Indicator:** 200 response + security headers present

### Step 5: Test API Endpoints
- [ ] Health check: `/health` → 200 ✓
- [ ] API docs: `/api/docs` → Swagger UI loads ✓
- [ ] OTP request: `POST /api/v1/auth/otp/request` → 200 ✓
- [ ] User creation: `POST /api/v1/users` → 200 ✓
- [ ] Price fetch: `GET /api/v1/prices/latest?commodity=rice` → 200 ✓
- [ ] Verify security headers present ✓

**Expected Time:** 10 minutes
**Test Tool:** curl or Postman

### Step 6: Connect Streamlit Frontend
- [ ] Update `croppulse_app.py` (replace API_URL):
  ```python
  # OLD: API_URL = "http://localhost:8000"
  # NEW:
  API_URL = "https://[YOUR_RAILWAY_URL]"
  ```
- [ ] Commit and push changes
- [ ] Streamlit Cloud auto-redeploys
- [ ] Verify Streamlit can reach API

**Expected Time:** 5 minutes
**Auto-Redeploy:** Yes (on GitHub push)

### Step 7: Test Integration
- [ ] Open Streamlit app: `https://croppulse.streamlit.app`
- [ ] Dashboard loads without errors ✓
- [ ] Commodity selector works ✓
- [ ] Price charts display ✓
- [ ] Risk assessment calculates ✓
- [ ] No CORS errors in browser console ✓

**Expected Time:** 5 minutes
**Success:** Seamless frontend-backend integration

---

## 📊 Deployment Architecture

```
┌─────────────────────────────────────────────────────┐
│                   PRODUCTION STACK                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Streamlit Cloud (Frontend)                         │
│  https://croppulse.streamlit.app                    │
│         ↓                                           │
│  CORS enabled ✓                                     │
│         ↓                                           │
│  Railway.app (Backend API)                          │
│  https://[YOUR_URL].up.railway.app                  │
│         ↓                                           │
│  FastAPI (22 endpoints)                             │
│  Security Headers ✓ Rate Limiting ✓                │
│  Audit Logging ✓ Input Validation ✓                │
│         ↓                                           │
│  PostgreSQL (Database)                              │
│  Auto-provisioned by Railway                        │
│         ↓                                           │
│  Netlify (Landing Page)                             │
│  https://croppulse.netlify.app (static HTML)        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔐 Security Verification

After deployment, verify these security features:

```bash
# 1. Check security headers
curl -i https://[YOUR_URL]/health | grep -E "x-frame-options|hsts|csp"
# Should show: x-frame-options: DENY, hsts: max-age=31536000, csp present

# 2. Test rate limiting (make 101 requests quickly)
for i in {1..101}; do curl https://[YOUR_URL]/health; done
# Request 101 should return 429 (Too Many Requests)

# 3. Test input validation
curl -X POST https://[YOUR_URL]/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"phone":"12345","name":"A","user_type":"farmer","state":"TN","village":"xyz"}'
# Should return 422 (Validation Error)

# 4. Test API key requirement (if protected)
curl https://[YOUR_URL]/api/v1/prices/latest \
  -H "X-API-Key: invalid_key"
# Should return 403 (Forbidden)
```

---

## 📈 Performance Benchmarks (After Deployment)

Monitor these metrics in Railway dashboard:

| Metric | Target | Status |
|--------|--------|--------|
| API Response Time | <200ms | ⏳ TBD |
| Health Check | <50ms | ⏳ TBD |
| Database Query | <100ms | ⏳ TBD |
| CPU Usage | <30% | ⏳ TBD |
| Memory Usage | <200MB | ⏳ TBD |
| Uptime | 99.9% | ⏳ TBD |

---

## 🎉 Success Criteria

Deployment is successful when:

✅ **API Status:**
- [ ] Health endpoint returns 200
- [ ] All 22 endpoints respond correctly
- [ ] Database connection active
- [ ] All security headers present

✅ **Frontend Integration:**
- [ ] Streamlit loads without errors
- [ ] API calls succeed from Streamlit
- [ ] No CORS errors in console
- [ ] Charts and data display correctly

✅ **Security:**
- [ ] Rate limiting active
- [ ] Security headers verified
- [ ] API keys enforced
- [ ] Input validation working
- [ ] Audit logging operational

✅ **Performance:**
- [ ] API response time <200ms
- [ ] No timeout errors
- [ ] CPU usage normal
- [ ] Memory stable

---

## 🚨 Rollback Plan

If issues arise:

1. **Check Railway Logs:**
   ```
   Railway Dashboard → Deployments → View Logs
   ```

2. **Common Issues:**
   - ModuleNotFoundError → requirements.txt missing
   - DATABASE_URL error → PostgreSQL not provisioned
   - CORS error → Update CORS origins in main.py
   - Port error → Ensure Procfile uses $PORT variable

3. **Rollback to Previous Version:**
   ```
   Railway Dashboard → Deployments → Select previous build → Redeploy
   ```

4. **Quick Fixes:**
   - Edit environment variables → Auto-redeploys
   - Push new code to GitHub → Auto-redeploys
   - Restart service → Railway dashboard button

---

## 📞 Troubleshooting Guide

### Issue: "Build Failed"
```
Check: requirements.txt exists in root directory
Fix: git add requirements.txt && git push
```

### Issue: "ModuleNotFoundError"
```
Check: All imports are in requirements.txt
Fix: pip freeze > requirements.txt && git push
```

### Issue: "Connection to database failed"
```
Check: DATABASE_URL variable is set
Check: PostgreSQL plugin is added
Fix: Railway auto-retries, or restart service
```

### Issue: "CORS error from Streamlit"
```
Check: Streamlit URL in CORS whitelist
Fix: Update main.py line 368, commit, push
```

### Issue: "Rate limiting not working"
```
Check: slowapi is installed
Check: @limiter.limit() decorators present
Fix: Should work by default, check Railway logs
```

---

## ✅ Post-Deployment Actions

After successful deployment:

1. **Update Documentation:**
   - [ ] Add API URL to README.md
   - [ ] Update DEPLOYMENT_GUIDE.md with actual URL
   - [ ] Add to GitHub repo description

2. **Monitor Performance:**
   - [ ] Set up Railway alerts
   - [ ] Enable Sentry error tracking (optional)
   - [ ] Monitor logs daily for first week

3. **Team Communication:**
   - [ ] Share API URL with team
   - [ ] Share API docs URL: `/api/docs`
   - [ ] Share Swagger UI link

4. **Continue Development:**
   - [ ] Implement database migrations
   - [ ] Add SMS/Twilio integration
   - [ ] Deploy Redis cache
   - [ ] Set up admin dashboard

---

## 📊 Phase 2 Timeline

| Date | Milestone | Status |
|------|-----------|--------|
| May 14 | Code complete, all tests passing | ✅ COMPLETE |
| May 14 | Deployment config created | ✅ COMPLETE |
| May 14-15 | **Deploy to Railway** | ⏳ IN PROGRESS |
| May 15 | API testing & integration | ⏳ PENDING |
| May 16 | Database setup & migrations | ⏳ PENDING |
| May 17-19 | Third-party integrations | ⏳ PENDING |
| May 20 | Load testing & optimization | ⏳ PENDING |
| May 21-31 | Production monitoring | ⏳ PENDING |

---

## 🎯 Next Big Milestones (Phase 2)

After deployment:
1. **Week 1:** PostgreSQL migrations + Farmer signup
2. **Week 2:** Marketplace matching algorithm
3. **Week 3:** Payment integration (Stripe)
4. **Week 4:** Mobile app beta launch

---

## 📝 Notes

**API Endpoint:** (will update after deployment)
**API Docs:** (will update after deployment)
**Streamlit URL:** https://croppulse.streamlit.app (auto-updates)
**Landing Page:** https://croppulse.netlify.app (static)

**GitHub:** https://github.com/bixamtarala/corpplus
**Branch:** main
**Latest Commit:** ce97a05 (Deployment config)

---

**Status:** ✅ Ready to Deploy
**Date:** May 14, 2026
**Version:** Phase 2 v1.0
**Security Level:** OWASP TIER 1 ✅
