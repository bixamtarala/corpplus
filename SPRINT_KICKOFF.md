# 🚀 CropPulse Phase 2: SPRINT KICKOFF 
**Monday, May 20, 2026 | Week 1: Authentication + Farmer Dashboard**

---

## ✅ PRE-SPRINT CHECKLIST (Complete Before Monday 9 AM)

### [ ] Environment Setup
- [ ] Python 3.9+ installed (`python --version`)
- [ ] PostgreSQL client installed (`psql --version`)
- [ ] Node.js + npm installed (`node --version`, `npm --version`)
- [ ] Git installed (`git --version`)
- [ ] VS Code with extensions:
  - [ ] Python
  - [ ] REST Client (for Postman-like testing)
  - [ ] Prettier (code formatting)

### [ ] Accounts Created
- [ ] GitHub account (for code backup)
- [ ] Railway.app account (free tier, $5/month credits)
- [ ] Vercel account (free tier, for React deployment)

### [ ] Code Setup
- [ ] Clone/open Agritech workspace
- [ ] Create `.env` file in `phase2_backend/` (copy from `.env.example`)
- [ ] Fill in placeholder values (will get real ones this week)

### [ ] Mental Preparation
- [ ] Read through [WEEK_1_SPRINT_PLAN.md](WEEK_1_SPRINT_PLAN.md) (20 min read)
- [ ] Set daily standup time (9 AM? 10 AM?)
- [ ] Identify your code editor (VS Code recommended)
- [ ] Close Slack, email, other distractions (deep work mode)

---

## 📋 SPRINT GOALS (By Friday 6 PM)

### 🔴 MUST HAVE (Critical Path)
1. ✅ Phone OTP registration working
2. ✅ JWT token generation working
3. ✅ Farmer profile creation working
4. ✅ Dashboard page shows data
5. ✅ Deployed to Railway (backend) + Vercel (frontend)

### 🟡 SHOULD HAVE (High Value)
6. Crop management (add/list crops)
7. Mobile-responsive design
8. Basic error handling

### 🟢 NICE TO HAVE (Polish)
9. Beautiful styling (Tailwind)
10. Loading states
11. Form validation

**Focus**: MUST HAVE only. Everything else is bonus.

---

## 🎯 YOUR MISSION THIS WEEK

```
YOU: Solo founder, full-stack developer
TOOLS: Python, React, PostgreSQL, Railway
TIMEFRAME: 5 days (Mon-Fri), 8-10 hours/day
GOAL: Farmer registration → Dashboard → Crop management (working MVP)
DELIVERABLE: Live web app at vercel.app + API at railway.app
```

---

## 📊 TEAM STATUS

### Your Skills (Leverage Them)
- ✅ Backend (Python, FastAPI)
- ✅ Data (eNAM API integration)
- ✅ Deployment (you already used Railway in Phase 1)
- ✅ Problem-solving

### Your Constraints (Plan Around Them)
- ❌ Only 1 person (no QA, no designer, no DevOps specialist)
- ❌ Can't do everything in 8 weeks (Flutter requires 2 people)
- ❌ React is faster than Flutter for this sprint

### Your Advantage (What You Have)
- ✅ Working Phase 1 (proves product-market fit)
- ✅ 500 users already (validation)
- ✅ Architecture designed (models, endpoints planned)
- ✅ Infrastructure ready (Railway, Vercel experience)

**Math**: 1 person × 40 hours/week × 8 weeks = 320 hours = Enough for React MVP

---

## 🔧 TECH STACK (LOCKED IN)

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (on Railway)
- **Cache**: Redis (on Railway, optional Week 2)
- **Auth**: JWT tokens
- **Hosting**: Railway.app

### Frontend  
- **Framework**: React (Create React App)
- **Styling**: Tailwind CSS (no designer needed)
- **API Client**: Axios
- **Routing**: React Router
- **Hosting**: Vercel.app

### Why These Choices?
- FastAPI: Fastest Python framework, built-in docs, type validation
- React Web: Ship MVP in 8 weeks (Flutter would be 12-16 weeks)
- Tailwind: Beautiful UI without custom CSS
- Railway: You already know it, $5/month, simple
- Vercel: Deploy with `git push`, global CDN, free tier

---

## 📅 WEEKLY SCHEDULE

### Daily Pattern
```
9:00 AM   - Review yesterday's work, plan today
9:15 AM   - DEEP WORK: Code (2.5 hours)
11:45 AM  - Break: Walk, coffee, stretch (15 min)
12:00 PM  - DEEP WORK: Code (2.5 hours)
2:30 PM   - Lunch (1 hour)
3:30 PM   - DEEP WORK: Code (2 hours)
5:30 PM   - Testing & debugging (30 min)
6:00 PM   - Git commit, end of day
```

**Total**: 7.5 hours focused work + 1.5 hours breaks/admin = 9 hours day

### Weekly Milestones
- **Monday EOD**: Database + FastAPI auth working
- **Wednesday EOD**: Frontend login + Dashboard
- **Friday EOD**: Everything deployed + live demo

---

## 🚀 HOW TO START (MONDAY 9 AM)

### Step 1: Terminal Setup (5 min)
```bash
cd c:\Users\LENOVO\Desktop\Agritech
git status  # Check everything is saved
python --version  # Should be 3.9+
```

### Step 2: Database (10 min)
- Go to railway.app
- Create new project
- Add PostgreSQL database
- Copy connection string
- Paste into `.env` as DATABASE_URL
- Test: Open terminal, run `psql <connection_string>`

### Step 3: Virtual Environment (5 min)
```bash
cd phase2_backend
python -m venv venv
.\venv\Scripts\activate  # Windows
```

### Step 4: FastAPI (5 min)
```bash
pip install -r requirements_phase2.txt
python main_phase2.py
```
Visit: http://localhost:8000/health → Should see `{"status": "healthy"}`

### Step 5: React (10 min)
```bash
cd ../
npx create-react-app croppulse-web
cd croppulse-web
npm start
```
Visit: http://localhost:3000 → Should see React app

### Step 6: Read Week 1 Plan (20 min)
Open [WEEK_1_SPRINT_PLAN.md](WEEK_1_SPRINT_PLAN.md)  
Read Monday section in detail  
Create a checklist in your TODO app  

**By 10 AM**: Everything set up, ready to code.

---

## 💡 DAILY STANDUP QUESTIONS (Answer Nightly)

Each evening, write answers to these in a `standup.md` file:

```markdown
## [Day Name, May XX]

**What I built today:**
- [ ] ___________

**What worked:**
- [ ] ___________

**What blocked me:**
- [ ] ___________

**What I'm building tomorrow:**
- [ ] ___________

**Hours worked:**
- [ ] 7-9 hours (realistic)
- [ ] 10+ hours (burning out, take Friday off)

**Morale:**
- [ ] 🟢 Energized, on track
- [ ] 🟡 Tired, needs adjustment  
- [ ] 🔴 Frustrated, need help

**Next day priorities:**
1. _________
2. _________
3. _________
```

---

## 🎯 SUCCESS CRITERIA (Check Friday Evening)

### Technical (Must Have)
- [ ] 1. Phone registration endpoint working
- [ ] 2. OTP verification endpoint working
- [ ] 3. JWT tokens being generated
- [ ] 4. Farmer profile saved to database
- [ ] 5. Dashboard data being fetched
- [ ] 6. React login page functional
- [ ] 7. React dashboard page functional
- [ ] 8. Full flow tested (register → login → dashboard)
- [ ] 9. Deployed to Railway (backend)
- [ ] 10. Deployed to Vercel (frontend)

### Code Quality (Should Have)
- [ ] Clean code (understandable, not hacky)
- [ ] Error handling (graceful failures)
- [ ] Database schema matches models.py
- [ ] Git commits daily (backup)

### Documentation (Should Have)
- [ ] README.md updated with setup steps
- [ ] API endpoints documented
- [ ] Screenshots of working app

### Metrics (Nice to Have)
- [ ] Frontend loads in <3 seconds
- [ ] API responds in <500ms
- [ ] Mobile responsive (works on phone too)

---

## ⚠️ THINGS TO AVOID THIS WEEK

### ❌ DON'T DO THESE
1. ❌ Build the perfect UI (good enough is enough)
2. ❌ Add features not in Week 1 plan
3. ❌ Spend 12+ hours coding (burnout)
4. ❌ Work on weekends (rest is productive)
5. ❌ Optimize prematurely (make it work first)
6. ❌ Set up monitoring/alerts (Week 3)
7. ❌ Integrate Twilio SMS yet (Week 2)
8. ❌ Build admin panel (Phase 3)

### ✅ DO THESE INSTEAD
1. ✅ Copy code from templates (faster)
2. ✅ Focus on making 1 feature work completely
3. ✅ Stop at 6 PM (seriously)
4. ✅ Take breaks (every 2 hours)
5. ✅ Test as you build (catch bugs early)
6. ✅ Ask for help if stuck > 30 min (GitHub issues, Stack Overflow)
7. ✅ Celebrate wins (endpoint works! push to git!)
8. ✅ Review code at day's end (what could be better?)

---

## 🆘 IF YOU GET STUCK

### For Backend Errors
1. Read the error message carefully (it tells you the problem)
2. Check `print()` statements you added
3. Look at the line number mentioned
4. Google the error (exact message in quotes)
5. Check GitHub issues on FastAPI repo
6. Ask on Stack Overflow

### For React Errors
1. Open browser console (F12)
2. Look for red error messages
3. Check network tab (see API response)
4. Add console.log() before and after suspicious code
5. Restart dev server (`npm start`)
6. Clear browser cache

### For Database Errors
1. Check connection string in .env
2. Verify Railway project is running
3. Test with psql directly
4. Check table exists: `\dt` (in psql)
5. Check column names match

### For Deployment Errors
1. Check Railway logs (deployment may have crashed)
2. Check environment variables set in Railway
3. Try running locally first
4. Push to GitHub, check if Railway auto-deploys
5. Use Railway CLI for debugging

**Rule**: Every error has a solution. Google it first.

---

## 📞 QUICK REFERENCE

### Useful Commands
```bash
# Python
python -m venv venv                    # Create virtual env
.\venv\Scripts\activate                # Activate (Windows)
pip install -r requirements.txt        # Install packages
python main.py                         # Run FastAPI

# Database
psql <connection_string>               # Connect to PostgreSQL
\dt                                    # List tables
\d table_name                          # Describe table
SELECT * FROM users LIMIT 5;          # View data

# React
npx create-react-app app-name         # Create project
npm start                              # Dev server
npm run build                          # Production build
npm install package-name               # Add dependency

# Git
git status                             # Check changes
git add .                              # Stage all changes
git commit -m "message"                # Commit
git push                               # Push to GitHub

# Railway
railway up                             # Deploy current app

# Testing
curl -X POST http://localhost:8000/api/v2/auth/request-otp \
  -H "Content-Type: application/json" \
  -d '{"phone":"+919876543210"}'
```

---

## 🎓 LEARNING RESOURCES

If you get stuck and need to understand something:

- **FastAPI**: https://fastapi.tiangolo.com (official docs, excellent)
- **React**: https://react.dev (official docs)
- **PostgreSQL**: https://www.postgresql.org/docs (for SQL questions)
- **Railway**: https://railway.app/docs (deployment)
- **Vercel**: https://vercel.com/docs (React deployment)

**Time-saving tip**: The docs are usually clearer than tutorials. Go to the official docs first.

---

## 🎉 YOU'RE READY!

By Friday evening, you'll have:
- ✅ A working farmer registration system
- ✅ An authentication backend
- ✅ A dashboard UI
- ✅ A live web app anyone can access
- ✅ All deployed and scalable

**This is huge progress.** From zero to deployed MVP in 1 week. 

**Incubation Application Timeline**:
- Week 2-4: Marketplace features
- Week 5-7: AI features + polish
- Week 8: Deploy to production + go live with 5K farmers
- Week 9: Apply to incubation programs with working product + metrics

---

## 📌 BEFORE YOU START CODING

### Read These in Order (30 minutes total)
1. [WEEK_1_SPRINT_PLAN.md](WEEK_1_SPRINT_PLAN.md) (20 min) ← Daily reference
2. [INCUBATION_QUICK_START.md](INCUBATION_QUICK_START.md) (5 min) ← Remind yourself why
3. This file (5 min) ← You're reading it now

### Then Start Coding (Monday 9 AM)
- [ ] Setup (database, Python, React)
- [ ] Monday plan (auth endpoints)
- [ ] Code like your life depends on it!

---

**THE BEST TIME TO BUILD WAS 3 MONTHS AGO.**  
**THE SECOND BEST TIME IS NOW.**

---

## 🚀 LET'S GO

You've got this. 

By Friday, you'll have built something you can show to farmers and traders. Something that works. Something that validates the idea.

**That's incredible progress.**

Now stop reading and start coding.

**Monday 9 AM sharp. See you then.**

---

**CropPulse Phase 2 Sprint Kickoff v1.0**  
**Date**: May 20, 2026  
**Status**: 🟢 READY TO EXECUTE  
**Your mission**: Make it work by Friday 6 PM.
