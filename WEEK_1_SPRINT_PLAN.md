# CropPulse Phase 2: Week 1 Sprint Plan (May 20-26, 2026)
**For: Solo Founder | Frontend: React Web (Phase 2) + Flutter (Phase 3) | Backend: FastAPI**

---

## 🎯 WEEK 1 GOAL
**Get farmer registration + authentication working. You should have:**
- ✅ PostgreSQL database ready
- ✅ FastAPI skeleton deployed on Railway
- ✅ Phone OTP registration endpoint working
- ✅ Basic React login page (at least mockup)
- ✅ Farmer dashboard skeleton (even if not functional)

**Success Criteria**: 
- Farmer can register with phone
- JWT token generated on OTP verify
- Dashboard page loads (even if empty)

---

## ⏰ TIMELINE & CAPACITY

### Realistic Workload (Solo Founder)
- **Monday-Friday**: 8-10 hours/day on development
- **Wednesday evening**: 1.5-hour planning session (what to focus on next)
- **Friday afternoon**: Demo + review what works
- **Saturday morning**: Rest & buffer for blockers

**Total Available**: ~45 hours this week

### Week 1 Allocation
- **Backend (FastAPI)**: 15 hours
- **Frontend (React)**: 15 hours  
- **DevOps / Setup**: 8 hours
- **Testing**: 5 hours
- **Buffer**: 2 hours

---

## 📋 DAILY BREAKDOWN

### MONDAY (May 20) - Setup & Database

#### Morning (3 hours)
- [ ] **Database Setup** (Railway PostgreSQL)
  - Create Railway project (if not existing)
  - Create PostgreSQL database
  - Get connection string
  - Test connection from local machine
  - `psql postgresql://user:pass@host/dbname`
  
- [ ] **Local Development Environment**
  - Python 3.9+ installed?
  - Create virtual environment: `python -m venv venv`
  - Activate: `source venv/Scripts/activate` (Windows) or `source venv/bin/activate`
  - Install requirements: `pip install -r phase2_backend/requirements_phase2.txt`

#### Afternoon (4 hours)
- [ ] **FastAPI Project Setup**
  - Copy `main_phase2.py` → `main.py` (or work with existing)
  - Create `database.py` for SQLAlchemy setup
  - Create database connection function
  - Test: `python main.py` → See "Starting Uvicorn"
  - API should be accessible at `http://localhost:8000`
  - Check `/health` endpoint returns status

- [ ] **Database Migrations** (use Alembic later, for now create tables manually)
  - Read `models.py` 
  - Create migration script to create initial tables
  - Or use SQLAlchemy: `Base.metadata.create_all(bind=engine)`

#### Evening (1.5 hours)
- [ ] **Git Commit**
  - `git add .`
  - `git commit -m "Week 1 Monday: Database setup + FastAPI skeleton"`
  - `git push`

**End of Monday**: FastAPI running locally, PostgreSQL connected, health check working

---

### TUESDAY (May 21) - Authentication Backend

#### Morning (3 hours)
- [ ] **OTP Request Endpoint**
  - Write `POST /api/v2/auth/request-otp` endpoint (in `main.py`)
  - Input: `{phone: "+919876543210"}`
  - For now: Send OTP via print (don't setup Twilio yet)
  - Store OTP in Redis (or memory cache) with 10-min expiry
  - Response: `{message: "OTP sent", phone: "...", expires_in: 600}`
  - Test with Postman: `curl -X POST http://localhost:8000/api/v2/auth/request-otp -H "Content-Type: application/json" -d '{"phone":"+919876543210"}'`

#### Afternoon (4 hours)
- [ ] **OTP Verification + JWT Token**
  - Write `POST /api/v2/auth/verify-otp` endpoint
  - Input: `{phone: "+919876543210", otp: "123456"}`
  - Validate OTP against Redis cache
  - Create User record in database (if doesn't exist)
  - Generate JWT token (SECRET_KEY in .env)
  - Response: `{access_token: "...", token_type: "bearer", user_id: "...", phone: "..."}`
  - Test with Postman

- [ ] **Authentication Middleware**
  - Create `get_current_user()` dependency
  - Validate JWT token in request header
  - Extract user_id from token
  - Test: Add auth header to any endpoint

#### Evening (1 hour)
- [ ] **Git Commit**
  - `git commit -m "Week 1 Tuesday: OTP auth + JWT token generation"`

**End of Tuesday**: Farmer can register with phone + OTP. Backend generates JWT token.

---

### WEDNESDAY (May 22) - Farmer Profile + React Setup

#### Morning (3 hours)
- [ ] **Farmer Profile Endpoint (Backend)**
  - Write `POST /api/v2/farmer/profile` endpoint
  - Input: Name, state, district, village, land size, soil type, lat/long, bank account
  - Save to `farmer_profiles` table
  - Require JWT authentication
  - Response: Farmer profile with KYC status = "pending"
  - Also write `GET /api/v2/farmer/profile` endpoint

- [ ] **Farmer Dashboard Endpoint (Backend)**
  - Write `GET /api/v2/farmer/dashboard` endpoint
  - Return dummy data for now:
    ```json
    {
      "user": {name, kyc_status},
      "weather": {temp, condition, humidity},
      "crops": {total, active},
      "market_prices": {Rice: 2500, ...},
      "active_listings": 1,
      "wallet_balance": 5000
    }
    ```
  - This is the main landing page after login

#### Afternoon (4 hours)
- [ ] **React Project Setup**
  - Create React project: `npx create-react-app croppulse-web` (in landing_page folder or new)
  - Install dependencies:
    - `npm install axios` (API calls)
    - `npm install react-router-dom` (navigation)
    - `npm install tailwindcss` (styling)
  - Project structure:
    ```
    src/
      pages/
        LoginPage.js
        DashboardPage.js
        RegisterPage.js
      components/
        Header.js
        NavBar.js
      services/
        api.js
      App.js
      index.js
    ```

- [ ] **Login Page (React)**
  - Create `src/pages/LoginPage.js`
  - Input: Phone number
  - Button: "Request OTP"
  - Call backend: `POST /api/v2/auth/request-otp`
  - Show: "OTP sent to +91..."
  - Input: OTP field appears
  - Button: "Verify & Login"
  - Call backend: `POST /api/v2/auth/verify-otp`
  - On success: Save JWT token to localStorage
  - Redirect: `/dashboard`
  - **Design**: Simple, mobile-friendly (Tailwind)

#### Evening (1 hour)
- [ ] **Git Commit**
  - `git commit -m "Week 1 Wednesday: Farmer profile + React login setup"`

**End of Wednesday**: 
- Backend: Profile + Dashboard endpoints ready
- Frontend: Login page working (connects to backend)

---

### THURSDAY (May 23) - Dashboard & Crop Management

#### Morning (3 hours)
- [ ] **Dashboard Page (React)**
  - Create `src/pages/DashboardPage.js`
  - After login, shows farmer's main page
  - Layout (5 cards):
    ```
    [Dashboard]
    ┌─────────────┐
    │ Weather     │
    │ 32°C, Sunny │
    └─────────────┘
    ┌─────────────┐
    │ Crops       │
    │ 2 active    │
    └─────────────┘
    ┌─────────────┐
    │ Market      │
    │ Rice: ₹2500 │
    └─────────────┘
    ┌─────────────┐
    │ Listings    │
    │ 1 active    │
    └─────────────┘
    ┌─────────────┐
    │ Wallet      │
    │ ₹5,000      │
    └─────────────┘
    ```
  - Call `/api/v2/farmer/dashboard` on load
  - Display data in cards
  - Bottom navigation (5 buttons for future pages)

- [ ] **Add Crop Endpoint (Backend)**
  - Write `POST /api/v2/farmer/crops` endpoint
  - Input: Crop name, variety, area, sowing date, expected harvest date, irrigation type
  - Save to `crops` table
  - Response: Crop record with ID

#### Afternoon (4 hours)
- [ ] **Crop Management Page (React)**
  - Create `src/pages/CropsPage.js`
  - Show list of farmer's crops (call `GET /api/v2/farmer/crops`)
  - Each crop card shows:
    - Crop name + variety
    - Area (acres)
    - Status (growing, harvested, sold)
    - Sowing date
  - Button: "Add Crop" → opens form
  - Form: Name, variety, area, sowing date, expected harvest, irrigation type
  - On submit: `POST /api/v2/farmer/crops`
  - Success: Close form, refresh list

- [ ] **Navigation Setup (React)**
  - Create bottom navigation (5 tabs):
    1. Dashboard (home icon)
    2. Marketplace (cart icon)
    3. Intelligence (brain icon)
    4. Community (people icon)
    5. Profile (user icon)
  - Only Dashboard page functional this week
  - Other pages show "Coming Soon"

#### Evening (1 hour)
- [ ] **Git Commit & Merge**
  - `git commit -m "Week 1 Thursday: Dashboard + Crop management"`

**End of Thursday**: Farmer can see dashboard, add crops, see list of crops

---

### FRIDAY (May 24) - Testing & Deployment

#### Morning (3 hours)
- [ ] **Backend Testing**
  - Test all endpoints with Postman (request-otp, verify-otp, profile, dashboard, crops)
  - Check database records created
  - Verify JWT tokens work
  - Test error cases (invalid phone, wrong OTP)

- [ ] **Frontend Testing**
  - Login → Dashboard flow
  - Add crop flow
  - Check API calls in browser network tab
  - Responsive design: Test on mobile (Chrome DevTools)

#### Afternoon (3 hours)
- [ ] **Deploy to Railway** (Backend)
  - Create Railway project (if not done)
  - Connect GitHub repo
  - Set environment variables (DATABASE_URL, SECRET_KEY, etc.)
  - Deploy: `git push` → Automatic deploy
  - Test: `curl https://your-railway-app.up.railway.app/health`

- [ ] **Deploy to Vercel** (Frontend)
  - Create Vercel account (free)
  - Import React project from GitHub
  - Set environment variable: `REACT_APP_API_URL=https://your-railway-app.up.railway.app/api/v2`
  - Deploy: Automatic
  - Test: Open app in browser

#### Evening (1 hour)
- [ ] **Weekly Demo**
  - Record 2-minute video: Phone registration → OTP → Dashboard → Add crop
  - Share with yourself (archive for later)

**End of Friday**: Full app deployed and live! 
- Web app: https://your-vercel-app.vercel.app
- API: https://your-railway-app.up.railway.app

---

### SATURDAY (May 25) - Buffer & Planning

#### Morning (2 hours)
- [ ] **Bug Fixes**
  - Review Friday's testing results
  - Fix any issues found
  - Verify mobile responsiveness

- [ ] **Documentation**
  - Update README.md with API endpoints
  - Document database schema
  - Create step-by-step setup guide for future team

#### Afternoon (2 hours)
- [ ] **Plan Week 2**
  - Review what works
  - What needs improvement?
  - Plan marketplace features for Week 2
  - Rest!

---

## ✅ WEEK 1 DELIVERABLES (Checklist)

### Backend (FastAPI)
- [ ] PostgreSQL database on Railway
- [ ] SQLAlchemy models created (User, FarmerProfile, Crop, etc.)
- [ ] `/api/v2/auth/request-otp` → Accepts phone, returns OTP
- [ ] `/api/v2/auth/verify-otp` → Validates OTP, returns JWT token
- [ ] `/api/v2/farmer/profile` → POST/GET farmer profile
- [ ] `/api/v2/farmer/dashboard` → Returns main dashboard data
- [ ] `/api/v2/farmer/crops` → POST/GET crop management
- [ ] Authentication middleware (JWT validation)
- [ ] Error handling for invalid requests
- [ ] Deployed on Railway.app

### Frontend (React)
- [ ] Phone registration page
- [ ] OTP verification page  
- [ ] Dashboard page (5 cards: weather, crops, prices, listings, wallet)
- [ ] Crop management page (list + add crop form)
- [ ] Bottom navigation (5 tabs, only dashboard functional)
- [ ] Mobile-responsive design (Tailwind CSS)
- [ ] API integration (Axios)
- [ ] LocalStorage for JWT token
- [ ] Deployed on Vercel

### Documentation
- [ ] API endpoint list
- [ ] Database schema diagram
- [ ] Setup guide for local development
- [ ] Week 1 retrospective & Week 2 plan

### Metrics
- [ ] Phone registration working ✅
- [ ] OTP verification working ✅
- [ ] Dashboard loads ✅
- [ ] Farmer can add crops ✅
- [ ] All deployed and live ✅

---

## 🚨 POTENTIAL BLOCKERS & SOLUTIONS

### Blocker 1: Database Connection Issues
**Problem**: Can't connect to Railway PostgreSQL  
**Solution**:
- Check connection string format (postgresql://user:pass@host:port/db)
- Verify Railway project is active
- Check firewall (Railway allows all IPs by default)
- Test locally first with local PostgreSQL

### Blocker 2: CORS Issues (React ↔ FastAPI)
**Problem**: `No 'Access-Control-Allow-Origin' header`  
**Solution**:
- In `main.py`, add CORS middleware:
  ```python
  from fastapi.middleware.cors import CORSMiddleware
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],  # Configure properly in production
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

### Blocker 3: React API Calls Failing
**Problem**: Axios calls to backend return error  
**Solution**:
- Check API URL in React (use environment variable)
- Check JWT token format (Bearer token in header)
- Use browser DevTools → Network → Check request/response
- Backend health check: `curl https://your-api.up.railway.app/health`

### Blocker 4: OTP System (No Twilio Yet)
**Problem**: Can't send real SMS  
**Solution**:
- For MVP: Print OTP to backend console
- Farmer reads from logs or you show them
- Replace with real Twilio later (Week 2)

---

## 💡 TIPS FOR SOLO FOUNDER

1. **Time Management**
   - Use 25-minute Pomodoro sessions (25 min work, 5 min break)
   - Schedule breaks, don't skip them
   - 8-10 hours is maximum sustainable
   - Stop at 6 PM, relax, sleep well

2. **Code Quality**
   - Write simple code first, optimize later
   - Use copy-paste from templates (don't reinvent)
   - Test as you write (1 endpoint at a time)
   - Commit to GitHub daily (backup + history)

3. **Debugging**
   - Print/log everything (`print(f"Debug: {variable}")`)
   - Use browser DevTools (F12 → Network tab)
   - Read error messages carefully (they tell you the problem)
   - Google the exact error message

4. **Morale**
   - Celebrate small wins (endpoint works! ✅)
   - Don't aim for perfection this week, aim for working
   - By Friday, you'll have a working MVP (amazingly fast!)
   - Take Saturday off entirely (you earned it)

---

## 📞 DECISION POINT: REACT vs FLUTTER

### Why React First (Recommended for Week 1-8)
- ✅ Single codebase works on desktop + mobile (web browser)
- ✅ Faster to build (less boilerplate)
- ✅ Deploy in 2 minutes (Vercel)
- ✅ Easier debugging (browser DevTools)
- ✅ Can launch MVP in 8 weeks as 1 person

### Why Flutter Later (Phase 2.5, Weeks 9-14)
- ✅ Better UX (native iOS + Android apps)
- ✅ Offline support, push notifications
- ✅ App store presence
- ✅ With 2 people, build in 6 weeks

**Recommendation**: Build React MVP first (Weeks 1-8), then add Flutter mobile (Weeks 9-14) with a 2nd hire.

**Decision**: Should we proceed with React this week, or do you want Flutter? (If Flutter, timeline is 12-16 weeks for solo founder)

---

## 📊 PROGRESS TRACKING

Add this to your daily standup (record these):

```
[Week 1 Progress]

Monday (May 20):
- [ ] Database ready
- [ ] FastAPI running
- Blockers: _____

Tuesday (May 21):
- [ ] OTP endpoint
- [ ] JWT working
- Blockers: _____

Wednesday (May 22):
- [ ] Profile endpoint
- [ ] React login
- Blockers: _____

Thursday (May 23):
- [ ] Dashboard page
- [ ] Crop management
- Blockers: _____

Friday (May 24):
- [ ] All deployed
- [ ] Full flow tested
- Blockers: _____
```

---

## 🎯 SUCCESS LOOKS LIKE

By Friday evening, you should be able to:

1. **Visit** https://your-vercel-app.vercel.app
2. **Enter phone** +919876543210
3. **Click "Request OTP"** → See success message
4. **Enter OTP** (check console for the number) → 123456
5. **Click "Verify"** → Redirected to Dashboard
6. **See dashboard** with 5 cards (weather, crops, prices, etc.)
7. **Click "Add Crop"** → Fill form → Crop appears in list
8. **Refresh page** → Data persists (from database)
9. **Logout** → Back to login page

If all 8 work, you've completed Week 1 successfully! 🎉

---

**Next Steps After Week 1**: Review this document Friday evening, plan Week 2 (Marketplace)

**Questions?** Review the INCUBATION_QUICK_START.md and INCUBATION_BUILD_PLAN.md for context.

---

**Week 1 Sprint Plan v1.0**  
**Status**: Ready to Execute  
**Start Date**: Monday, May 20, 2026
