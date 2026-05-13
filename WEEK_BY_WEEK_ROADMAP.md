# CropPulse - Week-by-Week Execution Roadmap

## OVERVIEW

**Goal**: Transform CropPulse into a fundable agri-intelligence MVP and submit to ICAR in 3 weeks  
**Success Metric**: Complete application package + working MVP + pitch materials  
**Team**: You + 1 developer (can hire freelancer if needed)  
**Budget**: ₹0-50,000 (mostly hosting, domain, freelancer if needed)

---

## WEEK 1: STRATEGY & FOUNDATION (Days 1-7)

### Daily Breakdown

#### Day 1: Planning & Decision-Making
**Morning (2 hours)**:
- [ ] Review this entire plan
- [ ] Make tech stack decisions (React + FastAPI recommended)
- [ ] Decide on MVP scope (5 commodities minimum)
- [ ] Identify data sources (which NCDEX/Agmarknet APIs)

**Afternoon (3 hours)**:
- [ ] Set up project repository (GitHub)
- [ ] Create folder structure
- [ ] Create a shared document with key decisions
- [ ] Schedule daily standup (15 min each morning)

**Evening (1 hour)**:
- [ ] Document decisions in shared doc
- [ ] Prepare shopping list of tools/services to set up

#### Day 2: Backend Foundation
**Focus**: Create backend API skeleton, database schema

**Tasks** (6 hours total):
- [ ] Set up FastAPI project (or Express if JavaScript preference)
- [ ] Create PostgreSQL database (use Supabase for managed solution)
- [ ] Design database schema:
  ```
  - users (id, name, email, phone, user_type, created_at)
  - commodities (id, name, ticker, category)
  - price_data (id, commodity_id, date, open, close, high, low)
  - recommendations (id, user_id, commodity_id, action, confidence)
  - alerts (id, user_id, type, message, created_at)
  ```
- [ ] Create basic API endpoints (auth, commodities, prices)
- [ ] Set up JWT authentication
- [ ] Deploy to Railway or Render (free tier)

**Deliverable**: Working API at `https://your-api.railway.app` with test endpoints

#### Day 3: Frontend Foundation
**Focus**: Create React app, basic navigation, login page

**Tasks** (6 hours total):
- [ ] Initialize Next.js or React app
- [ ] Install UI library (Material-UI or Shadcn)
- [ ] Create login page (email + password)
- [ ] Create navigation/sidebar layout
- [ ] Connect to backend API
- [ ] Deploy to Vercel

**Deliverable**: Login page works, can navigate to blank dashboards

#### Day 4: Data Pipeline Setup
**Focus**: Get real commodity price data flowing

**Tasks** (6 hours total):
- [ ] Research and set up data source connections:
  - [ ] NCDEX API (if available) or web scraping
  - [ ] Agmarknet scraping setup
  - [ ] Create Python script to fetch daily prices
- [ ] Load sample historical data (2 years minimum) into database
- [ ] Create daily cron job to fetch latest prices
- [ ] Test data pipeline with sample commodities (Rice, Wheat, Cotton, Sugar, Spices)

**Deliverable**: Database populated with price data, daily refresh working

#### Day 5: Commodity Dashboard
**Focus**: Build the main dashboard with live price charts

**Tasks** (6 hours total):
- [ ] Create commodity grid UI (5 commodities)
- [ ] Integrate price chart library (Recharts/Chart.js)
- [ ] Display:
  - Current price
  - 30-day trend chart
  - Price change % (7-day)
  - High/low/avg for month
  - Volatility %
- [ ] Test with real data
- [ ] Style to look professional

**Deliverable**: Working commodity dashboard with live charts

#### Day 6: Risk Scoring Algorithm
**Focus**: Build the risk calculation engine

**Tasks** (6 hours total):
- [ ] Code risk scoring algorithm:
  ```python
  def calculate_risk_score(commodity_id):
      volatility = calculate_30day_volatility(prices)
      weather_risk = get_weather_risk_score()
      supply_risk = estimate_supply_shortage()
      demand_risk = estimate_demand_shift()
      
      score = (0.30 * volatility + 0.25 * weather 
              + 0.25 * supply + 0.20 * demand)
      return score
  ```
- [ ] Integrate weather API (OpenWeatherMap)
- [ ] Create risk display UI
- [ ] Test scoring logic

**Deliverable**: Risk score calculated daily, displayed on dashboard

#### Day 7: Review & Refinement
**Focus**: Review Week 1 progress, fix bugs, prepare for Week 2

**Tasks** (4 hours total):
- [ ] Test entire system end-to-end
- [ ] Fix any bugs or broken links
- [ ] Verify data is updating daily
- [ ] Deploy latest version
- [ ] Document what's working, what needs fixing
- [ ] Plan Week 2 with any adjustments

**End of Week 1 Status**:
- ✅ Backend API deployed and working
- ✅ Frontend with login and navigation
- ✅ Commodity price dashboard live
- ✅ Risk scoring engine running
- ✅ Real data flowing
- ⏳ Next: AI recommendations + alerts

---

## WEEK 2: FEATURES & DEMO PREP (Days 8-14)

### Daily Breakdown

#### Day 8: Risk Alert System
**Focus**: Build automated alert generation

**Tasks** (6 hours total):
- [ ] Create alert types:
  - Price Jump (>5% in 24h)
  - High Volatility (>50% increase)
  - Weather Risk (extreme forecast)
  - Supply Alert (shortage detected)
  - Opportunity (low prices)
- [ ] Build alert generation service (runs daily)
- [ ] Create alert dashboard UI
- [ ] Add alert notification preferences

**Deliverable**: Alerts generating daily, visible on dashboard

#### Day 9: AI Recommendation Engine - Part 1
**Focus**: Build price forecasting model

**Tasks** (6 hours total):
- [ ] Train forecasting models on historical data:
  - [ ] ARIMA model for each commodity
  - [ ] Prophet model as backup
  - [ ] Calculate historical accuracy
- [ ] Create API endpoint: `GET /api/recommendations/{user_id}`
- [ ] Test forecast accuracy on test data (aim for 80%+)
- [ ] Document model performance

**Deliverable**: Forecasting models trained, API endpoint ready

#### Day 10: AI Recommendation Engine - Part 2
**Focus**: Generate actionable recommendations

**Tasks** (6 hours total):
- [ ] Create recommendation logic:
  ```python
  def generate_recommendations(user_id):
      favs = get_user_favorite_commodities(user_id)
      recs = []
      for commodity in favs:
          forecast = get_price_forecast(commodity)
          risk = get_risk_score(commodity)
          action = determine_action(forecast, risk)  # SELL, BUY, WAIT
          confidence = forecast.confidence_score
          recs.append({
              'commodity': commodity,
              'action': action,
              'confidence': confidence,
              'reason': explain_recommendation(forecast, risk),
              'time_window': '5-7 days',
              'est_benefit': calculate_benefit(forecast)
          })
      return recs
  ```
- [ ] Test with real data
- [ ] Tune confidence thresholds
- [ ] Create explanation generation

**Deliverable**: Recommendations generating with 85%+ confidence

#### Day 11: Recommendations UI & Dashboard Updates
**Focus**: Display recommendations beautifully

**Tasks** (6 hours total):
- [ ] Build recommendation cards with:
  - Action (SELL/BUY/HOLD) with emoji/icon
  - Confidence score (0-100%)
  - Clear reasoning
  - Time window
  - Estimated benefit
  - Historical accuracy
- [ ] Add recommendation history/tracking
- [ ] Create recommendations list page
- [ ] Make mobile-responsive
- [ ] Test on phone

**Deliverable**: Beautiful recommendations UI, mobile-optimized

#### Day 12: Screenshots & Demo Prep
**Focus**: Prepare materials for incubator pitch

**Tasks** (4 hours total)**:
- [ ] Create 8 high-quality screenshots:
  1. Login page
  2. Dashboard (commodities)
  3. Commodity detail + chart
  4. Risk alerts
  5. Recommendations
  6. Mobile view
  7. User profile
  8. Data refresh indicator
- [ ] Use design tools to add annotations if needed
- [ ] Create demo user accounts with good sample data
- [ ] Write 2-3 paragraph product description

**Deliverable**: 8 polished screenshots ready for pitch deck

#### Day 13: Product Demo Video Recording
**Focus**: Record 2-3 minute video walkthrough

**Tasks** (3 hours total)**:
- [ ] Plan demo script:
  - Problem statement (30 sec)
  - Solution overview (20 sec)
  - Feature walkthrough (60 sec)
  - Impact/benefit (20 sec)
- [ ] Record screen walkthrough (use Loom/OBS)
- [ ] Add voiceover narration
- [ ] Edit video (intro + outro)
- [ ] Upload to YouTube (unlisted link)
- [ ] Create transcript/subtitles

**Deliverable**: Professional 2-3 min demo video

#### Day 14: Week 2 Review & Bug Fixes
**Focus**: Polish everything, fix bugs, prepare for final week

**Tasks** (4 hours total)**:
- [ ] End-to-end testing of entire product
- [ ] Fix any bugs found
- [ ] Optimize performance (aim for <2sec load time)
- [ ] Test on mobile devices
- [ ] Verify data freshness
- [ ] Document any limitations
- [ ] Prepare status report

**End of Week 2 Status**:
- ✅ Commodity dashboard
- ✅ Risk alert system
- ✅ AI recommendations
- ✅ Beautiful UI, mobile-responsive
- ✅ 8 demo screenshots
- ✅ Product demo video
- ⏳ Next: Pitch materials + application

---

## WEEK 3: PITCH MATERIALS & APPLICATION (Days 15-21)

### Daily Breakdown

#### Day 15: Pitch Deck Creation
**Focus**: Create compelling 15-slide pitch deck

**Tasks** (4 hours total)**:
- [ ] Create slides 1-5 (Problem, Opportunity, Solution)
  - Slide 1: Title
  - Slide 2: Problem statement
  - Slide 3: Market size
  - Slide 4: Solution overview
  - Slide 5: How it works
- [ ] Add visuals and statistics
- [ ] Keep design clean and professional
- [ ] Use consistent colors (agricultural green theme)

**Deliverable**: First 5 slides completed

#### Day 16: Pitch Deck - Business & Team
**Focus**: Complete slides 6-12

**Tasks** (4 hours total)**:
- [ ] Create slides 6-12:
  - Slide 6: Product demo/screenshots
  - Slide 7: Competition
  - Slide 8: Business model
  - Slide 9: Traction (pilot results if any)
  - Slide 10: Go-to-market
  - Slide 11: Technology
  - Slide 12: Team
- [ ] Add team photos
- [ ] Include business model visualization

**Deliverable**: Slides 6-12 completed

#### Day 17: Pitch Deck - Financials & Closing
**Focus**: Complete slides 13-15

**Tasks** (3 hours total)**:
- [ ] Create slides 13-15:
  - Slide 13: Financial projections
  - Slide 14: Impact & sustainability
  - Slide 15: Ask & closing
- [ ] Add financial charts/graphs
- [ ] Review entire deck for flow
- [ ] Create PDF version

**Deliverable**: Complete 15-slide pitch deck (PDF)

#### Day 18: Business Documents
**Focus**: Write key business documents

**Tasks** (4 hours total)**:
- [ ] Write executive summary (1 page)
- [ ] Write problem statement (1 page)
- [ ] Write business plan (2-3 pages)
- [ ] Prepare financial projections (spreadsheet + summary)
- [ ] Write competitive analysis (1-2 pages)

**Deliverable**: Complete business documents ready for submission

#### Day 19: Team & Legal Documents
**Focus**: Compile team info and legal materials

**Tasks** (3 hours total)**:
- [ ] Write founder biography (250-300 words each)
- [ ] Prepare founder CVs (1-2 pages each)
- [ ] Document team structure
- [ ] Gather legal documents:
  - Company registration certificate
  - Founder ID proofs
  - Bank details
  - GST certificate (if registered)
- [ ] Create README file explaining submission package

**Deliverable**: Complete team & legal documents folder

#### Day 20: Landing Page & Final Assembly
**Focus**: Create simple landing page, assemble all submission materials

**Tasks** (3 hours total)**:
- [ ] Create simple landing page (1 page):
  - Problem + solution
  - Key features
  - Demo video embedded
  - Screenshots
  - Team bios
  - Contact info
  - CTA (early access form)
- [ ] Deploy landing page
- [ ] Create submission package folder structure
- [ ] Verify all files are ready
- [ ] Create submission checklist

**Deliverable**: Live landing page + complete submission package

#### Day 21: Final Review & Submission
**Focus**: Final quality check, submit application

**Tasks** (2 hours total)**:
- [ ] Final proofread of all documents
- [ ] Verify all links work
- [ ] Test demo video plays
- [ ] Check file formats (PDFs readable)
- [ ] Verify file sizes reasonable
- [ ] Create backup copies
- [ ] **SUBMIT APPLICATION** before deadline
- [ ] Send confirmation email
- [ ] Document submission details

**End of Week 3 Status**:
- ✅ Complete pitch deck (15 slides)
- ✅ All business documents
- ✅ Product demo video
- ✅ Screenshots
- ✅ Landing page
- ✅ Submission package assembled
- ✅ **APPLICATION SUBMITTED**

---

## DAILY STANDUPS (15 minutes each morning)

**Format**: Quick sync with your developer/co-founder

**Topics**:
1. What did I complete yesterday?
2. What am I working on today?
3. Any blockers or issues?
4. Do I need help from someone else?

**Example Standup (Day 3)**:
> "Yesterday: Set up API skeleton and database. Today: Building React frontend and login page. Blocker: Need to decide on authentication library. Let's use Supabase auth to save time. Should take 6 hours."

---

## PARALLEL WORKSTREAMS

While building the MVP, you can parallelize work:

### Developer's Track (Days 1-14)
- Days 1-5: Backend + Frontend + Data pipeline
- Days 6-10: Risk scoring + AI models
- Days 11-14: UI polish + performance optimization

### Your Track (Days 1-21)
- Days 1-7: Planning + business documents
- Days 8-14: Screenshots + demo video
- Days 15-21: Pitch deck + submission

---

## KEY MILESTONES & GATES

### Gate 1: End of Day 5 (Friday, Week 1)
**Minimum Criteria**:
- [ ] API deployed and responding
- [ ] Database with price data
- [ ] Basic frontend with login

**Decision Point**: If this doesn't work by Friday EOD, pivot to no-code solution (Bubble.io/Webflow + Google Sheets)

### Gate 2: End of Day 10 (Friday, Week 2 AM)
**Minimum Criteria**:
- [ ] Commodity dashboard working with real data
- [ ] Risk alerts generating
- [ ] AI recommendations running

**Decision Point**: If recommendations quality is poor (<75% accuracy), use simpler heuristic rules instead

### Gate 3: End of Day 14 (Friday, Week 2 EOD)
**Minimum Criteria**:
- [ ] Product looks professional
- [ ] Works on mobile
- [ ] Demo video ready
- [ ] 8 screenshots ready

**Decision Point**: If design is poor, hire freelance designer for 2-3 days (₹20-30K) to polish

---

## CONTINGENCY PLANS

### If Building Takes Longer...

**Option 1: Reduce Scope**
- Keep only 3 commodities (Rice, Wheat, Cotton)
- Remove secondary features (regional comparison, historical accuracy tracking)
- Use simpler recommendation rules (not ML)

**Option 2: No-Code Alternative**
- Use Bubble.io for frontend
- Use Google Sheets + Zapier for data pipeline
- Manually update commodity prices
- Much faster to build, still looks professional

**Option 3: Hire Help**
- Hire developer on Upwork (₹50-150/hour) for 1-2 weeks
- Hire designer on Dribbble (₹30-50K) to make it look great
- Can compress timeline to 2 weeks instead of 3

### If You're Behind Schedule...

**Day 10 Checkpoint**: 
- If MVP isn't working by end of Day 10, switch to no-code
- Sacrifice some features, but submit on time

**Day 15 Checkpoint**:
- If pitch deck isn't done by Day 15, use template + swap in your content
- Quality matters, but completion matters more

---

## TOOLS & SERVICES TO SET UP

### Free Tier Services (Recommended for MVP)

**Database & Backend**:
- [ ] Supabase.com (PostgreSQL + Auth + APIs)
- [ ] Railway.app or Render.com (Backend hosting)

**Frontend**:
- [ ] Vercel (Next.js hosting)
- [ ] GitHub (code repository)

**Design & Video**:
- [ ] Figma (design tool, free tier)
- [ ] Loom (screen recording, free tier)
- [ ] Canva (graphics, free tier)

**Landing Page**:
- [ ] Webflow (free tier) OR
- [ ] GitHub Pages + Hugo (free static site)

**Domain**:
- [ ] Namecheap (~₹300-500/year)
- [ ] GoDaddy (~₹500-800/year)

**APIs & Data**:
- [ ] OpenWeatherMap (free tier, 1000 calls/day)
- [ ] NCDEX (contact for API access)
- [ ] Agmarknet (web scraping, free)

**Total Cost**: ₹5,000-20,000 for domain + paid tiers

---

## SUCCESS CRITERIA CHECKLIST

### By End of Week 3, You Must Have:

**Product**:
- [ ] Working MVP deployed
- [ ] 3+ commodities with live data
- [ ] Risk alerts generating
- [ ] AI recommendations running
- [ ] Mobile-responsive design
- [ ] <2 second load time

**Pitch Materials**:
- [ ] 15-slide pitch deck (PDF)
- [ ] Product demo video (2-3 min)
- [ ] 8 product screenshots
- [ ] Landing page live

**Business Documents**:
- [ ] Executive summary (1 page)
- [ ] Problem statement (1 page)
- [ ] Business plan (2-3 pages)
- [ ] Financial projections (3-year)
- [ ] Competitive analysis (1-2 pages)

**Legal & Team**:
- [ ] Founder bios (250-300 words each)
- [ ] Team structure document
- [ ] Company registration certificate
- [ ] Founder ID proofs

**Submission**:
- [ ] Complete submission package assembled
- [ ] Application submitted
- [ ] Confirmation email received

---

## POST-SUBMISSION (What Happens Next)

### Week 4-6: ICAR Initial Review
- ICAR team screens all applications
- They'll evaluate your pitch deck, MVP quality, business plan
- About 30% of applications move to next round

### Week 6-8: Shortlist Announcement
- You'll receive email if shortlisted
- Will be invited to pitch event (virtual or in-person)

### Week 8-10: Pitch Event
- Present your MVP live
- Answer questions from evaluators
- About 10-15% of applicants get selected

### Week 10-12: Final Announcement
- Winners announced
- Funding disbursement begins

---

## MOTIVATIONAL NOTES

✅ **You can do this in 3 weeks.** Thousands of founders have built MVPs faster.

✅ **Perfect is the enemy of done.** Focus on functional MVP, not polished product.

✅ **Even if you don't win:** The process of building this will:
- Sharpen your product positioning
- Validate your market
- Give you materials for future fundraising
- Connect you with government ecosystem

✅ **Worst case scenario:** You build a working agri-intelligence tool that thousands of farmers will use, and you don't win ICAR. That's still a win.

---

## FINAL CHECKLIST

**Week 1 Complete?**
- [ ] Backend deployed
- [ ] Frontend running
- [ ] Data pipeline flowing
- [ ] Commodity dashboard working

**Week 2 Complete?**
- [ ] Risk alerts generating
- [ ] AI recommendations running
- [ ] Demo video recorded
- [ ] 8 screenshots taken

**Week 3 Complete?**
- [ ] Pitch deck finished
- [ ] All documents written
- [ ] Landing page live
- [ ] Application submitted

**GO TIME** 🚀
