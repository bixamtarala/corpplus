# CropPulse - Screenshot Guide for Grant Materials

## Overview
This guide shows which screenshots to capture from the live dashboard for your pitch deck, landing page, and grant application.

---

## CRITICAL SCREENSHOTS (5-7 must-haves)

### Screenshot 1: Dashboard Hero (Primary)
**What to show:**
- Full dashboard with Rice selected
- All KPI cards visible (Price, Range, Volatility, Trend)
- Header with CropPulse branding
- Clean, centered layout

**Why:** This is the "first impression" image. It should look polished and professional.

**Where to use:**
- Pitch deck Slide 4 (Solution intro)
- Pitch deck Slide 5 (How it works)
- Landing page hero section
- Grant application (main screenshot)

**Capture size:** 1920x1080 (16:9)

---

### Screenshot 2: Price Chart in Action
**What to show:**
- 30-Day Price Trend chart with interactive point highlights
- Moving average line visible
- Price range clearly labeled
- Cursor hovering over a data point showing tooltip

**Why:** Demonstrates real-time data visualization capability.

**Where to use:**
- Pitch deck Slide 3 (Algorithm)
- Slide 6 (How It Works)
- Demo video at 20-35 seconds

**Capture size:** 1920x1080, focus on chart area

---

### Screenshot 3: Risk Assessment Deep Dive
**What to show:**
- Risk Score display (45/100 in green zone)
- Component breakdown with progress bars:
  - Volatility: 2.3%
  - Price Change: +5.2%
  - Supply: 72%
- Risk trend chart showing 7-day evolution
- Zone indicators (green = safe)

**Why:** This is the algorithm in action - evaluators want to see methodology.

**Where to use:**
- Pitch deck Slide 6 (Core Algorithm)
- Slide 12 (Traction - "MVP Validated")
- Demo video at 35-50 seconds

**Capture size:** 1920x1080, focus on risk section

---

### Screenshot 4: AI Insights with Confidence
**What to show:**
- Multiple insight cards displayed
- Each insight showing:
  - Emoji icon
  - Title
  - Description
  - **Confidence % badge** (important!)
  - Action recommendation
  - Color-coded (green = opportunity, yellow = caution)

**Example insights visible:**
- 📈 Sustained Strong Uptrend (Confidence: 85%)
- 📊 Above Average Pricing (Confidence: 78%)

**Why:** Confidence scoring is a key differentiator. Shows sophistication.

**Where to use:**
- Pitch deck Slide 7 (AI Insights Engine)
- Slide 8 (Why CropPulse Wins - "Actionability")
- Demo video at 65-85 seconds

**Capture size:** 1920x1080, focus on insights cards

---

### Screenshot 5: Wheat Commodity (Different Data)
**What to show:**
- Dashboard with Wheat selected
- Different metrics than Rice:
  - Price: ₹2,150 (different range)
  - Volatility: 1.8%
  - Trend: ↑ Strong Uptrend (different from Rice)
- Risk score: 38/100
- Different insights generated

**Why:** Proves system works for multiple commodities, not just one hardcoded view.

**Where to use:**
- Pitch deck Slide 8 (Demo variety)
- Demo video at 85-95 seconds (commodity switching)
- Grant materials (showing extensibility)

**Capture size:** 1920x1080

---

### Screenshot 6: Real-Time Alerts
**What to show:**
- Alerts section prominently displayed
- Examples:
  - 🚨 High Risk: "High Volatility Detected - Prices unpredictable"
  - ⚠️ Medium Risk: "High Demand Detected - Prices likely to continue rising"
- Severity color coding clear
- Alert timestamps visible

**Why:** Shows proactive risk management - key farmer concern.

**Where to use:**
- Pitch deck Slide 10 (Competitive Advantage - "Real-time processing")
- Demo video at 50-65 seconds
- Landing page features section

**Capture size:** 1920x1080, focus on alerts area

---

### Screenshot 7: Export & Footer
**What to show:**
- Export buttons visible: "📊 Export CSV", "📝 Export Summary"
- Quick reference guide
- Footer with:
  - CropPulse branding
  - Copyright
  - Disclaimer about data

**Why:** Shows data portability and professionalism (disclaimers matter to grants).

**Where to use:**
- Pitch deck Slide 9 (Features overview)
- Demo video at 95-110 seconds
- Landing page features

**Capture size:** 1920x1080, focus on export section

---

## BONUS SCREENSHOTS (3-5 optional)

### Screenshot 8: Supply & Demand Analysis
**What to show:**
- Current supply/demand balance
- 30-day supply trend (line chart)
- 30-day demand trend (line chart)
- Visual indicators (green = healthy, red = shortage)

**Use:** Pitch deck Slide 4 (Features) - detailed feature list

---

### Screenshot 9: Mobile Responsiveness
**What to show:**
- Same dashboard viewed on mobile device (iPhone 12)
- All elements readable
- Responsive design working

**Use:** Landing page, proof of accessibility

**Capture:** Use Chrome DevTools → Mobile emulation → Pixel 5 (412x915)

---

### Screenshot 10: Cotton Commodity
**What to show:**
- Dashboard with Cotton selected
- Different price range (₹5,800-₹6,200)
- Different insights
- Show diversity of commodities

**Use:** Pitch deck, landing page features

---

## HOW TO CAPTURE SCREENSHOTS

### Method 1: Chrome DevTools (Recommended for Streamlit)
1. Open Streamlit app in Chrome
2. Right-click → Inspect (or F12)
3. DevTools opens
4. Click device toolbar icon (📱/💻)
5. Set resolution to 1920x1080
6. Right-click → Capture screenshot
7. Save to `screenshots/` folder

### Method 2: Windows Snipping Tool
1. Press Win + Shift + S
2. Select area to capture
3. Click to capture
4. Edit if needed
5. Save PNG

### Method 3: OBS Studio (for screen recording with zoom)
1. Open OBS Studio
2. Add screen capture source
3. Right-click → Screenshot output
4. Save to file

### Positioning Tips
- **Don't capture:** Scrollbars, browser tabs, address bar
- **Do capture:** Full dashboard content, centered, clean
- **Background:** White/clean (blend with materials)
- **Cursor:** Hide for static screenshots (show only in demo)

---

## SCREENSHOT ORGANIZATION

Create folder structure:
```
croppulse/
├── screenshots/
│   ├── 01_dashboard_hero.png           (Screenshot 1)
│   ├── 02_price_chart.png              (Screenshot 2)
│   ├── 03_risk_assessment.png          (Screenshot 3)
│   ├── 04_ai_insights.png              (Screenshot 4)
│   ├── 05_wheat_commodity.png          (Screenshot 5)
│   ├── 06_real_time_alerts.png         (Screenshot 6)
│   ├── 07_export_footer.png            (Screenshot 7)
│   ├── 08_supply_demand.png            (Screenshot 8 - optional)
│   ├── 09_mobile_responsive.png        (Screenshot 9 - optional)
│   └── 10_cotton_commodity.png         (Screenshot 10 - optional)
└── pitch_materials/
    ├── pitch_deck.pptx
    ├── demo_video.mp4
    ├── grant_application.pdf
    └── screenshots_for_reference.zip
```

---

## IMAGE OPTIMIZATION FOR MATERIALS

### For Pitch Deck (PowerPoint/Google Slides)
- Format: PNG (lossless)
- Size: 1920x1080 or 1280x720
- Compression: Medium (file size <500KB per image)
- Tool: ImageOptim (Mac) or IrfanView (Windows)

### For Landing Page
- Format: WebP (better compression)
- Size: 1280x720 (responsive)
- Compression: High (file size <100KB per image)
- Tool: Squoosh.app (free online)

### For Grant Application PDF
- Format: PNG or PDF embed
- DPI: 150 (good quality, smaller file)
- Size: 1000x600 (width-normalized)
- File size: <50KB per image

---

## SCREENSHOT CHECKLIST

Use this to verify each screenshot before saving:

- [ ] Image is clear and sharp
- [ ] Text is readable (at least 12pt when printed)
- [ ] Colors match CropPulse theme (green #2ecc71, white)
- [ ] No browser UI visible (tabs, address bar)
- [ ] No personal data visible (if using real data)
- [ ] Centered and well-framed
- [ ] File name is descriptive
- [ ] File size is optimized (<500KB for print, <100KB for web)
- [ ] Backed up to cloud storage (Google Drive, OneDrive)

---

## WHEN TO CAPTURE (Timeline)

**Day 1 (Today):** Capture all 7 core screenshots
- Deploy app to Streamlit Cloud first
- Ensure data is clean and realistic
- Take 2-3 versions of each screenshot

**Day 2:** Capture bonus screenshots (mobile, other commodities)

**Day 3:** Optimize and organize for materials

**Day 4-5:** Use in pitch deck, landing page, grant application

---

## EXPECTED USAGE

**Screenshot 1 (Dashboard Hero):**
- Pitch deck: Slide 4 (full slide background)
- Landing page: Hero section (cropped or featured)
- Grant app: Main screenshot (proof of working MVP)

**Screenshot 3 (Risk Assessment):**
- Pitch deck: Slide 6 (algorithm visualization)
- Landing page: Features section (risk card)

**Screenshot 4 (AI Insights):**
- Pitch deck: Slide 7 (core value prop)
- All marketing materials (confidence scoring differentiator)

**Screenshots 5, 6, 7:**
- Demo video (primary use)
- Pitch deck (feature variety)
- Landing page (carousel if needed)

---

**Ready to capture? Start with the live Streamlit app at:** https://croppulse.streamlit.app

**Pro Tip:** Screenshot fresh after each code update to show latest algorithm improvements!
