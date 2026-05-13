# Phase 6: Deployment & Landing Page

## Overview
CropPulse is deployed to Streamlit Cloud for free hosting with automatic GitHub integration.

## Current Deployment Status

### ✅ What's Ready
- `croppulse_app.py` - Complete Streamlit application (Phases 1-5)
- `data/commodity_prices.csv` - Sample market data
- `.streamlit/config.toml` - Theme configuration
- `requirements.txt` - Python dependencies
- `landing_page/index.html` - Professional landing page

### 📋 Deployment Checklist

#### 1. **Prepare GitHub Repository**
```bash
# Initialize Git (if not done)
git init
git add .
git commit -m "CropPulse MVP - Phases 1-5 Complete"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/croppulse.git
git push -u origin main
```

#### 2. **Deploy to Streamlit Cloud**
1. Go to https://share.streamlit.io/
2. Sign in with GitHub account
3. Click "New app"
4. Select:
   - Repository: `YOUR_USERNAME/croppulse`
   - Branch: `main`
   - Main file path: `croppulse_app.py`
5. Click "Deploy"

**Result:** Live app at `https://croppulse.streamlit.app` (or assigned URL)

#### 3. **Landing Page Deployment (Option A: GitHub Pages)**
1. Create folder: `docs/`
2. Move `landing_page/index.html` to `docs/index.html`
3. Commit and push
4. In repo Settings → Pages:
   - Source: Deploy from branch
   - Branch: main
   - Folder: /docs
5. Click Save

**Result:** Landing page at `https://YOUR_USERNAME.github.io/croppulse`

#### 3. **Landing Page Deployment (Option B: Netlify - Recommended)**
1. Go to https://app.netlify.com/
2. Click "Add new site" → "Deploy manually"
3. Drag `landing_page/` folder
4. Connect custom domain (optional)

**Result:** Landing page auto-deployed with every folder upload

#### 4. **Update Landing Page**
Edit `landing_page/index.html` line 240:
```html
<a href="https://croppulse.streamlit.app" target="_blank" class="cta-button-primary">
```
Replace with your actual Streamlit Cloud URL.

## File Structure After Deployment

```
croppulse/
├── croppulse_app.py              ← Streamlit app (deployed to Cloud)
├── data/
│   └── commodity_prices.csv
├── landing_page/
│   └── index.html                ← Landing page (GitHub Pages or Netlify)
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── README.md
├── .gitignore
└── .git/
```

## Post-Deployment Testing

### ✅ Streamlit App Testing
1. Open https://croppulse.streamlit.app
2. Verify dashboard loads (should see Rice data)
3. Test commodity selector (Rice → Wheat → Cotton)
4. Verify all charts render
5. Check risk assessment section
6. Test insights display
7. Test export buttons (CSV, TXT)

### ✅ Landing Page Testing
1. Open landing page URL
2. Check "Launch Dashboard" button links to Streamlit app
3. Verify responsive design (mobile view)
4. Test all navigation links

## Troubleshooting

### "ModuleNotFoundError" on Streamlit Cloud
- Ensure `requirements.txt` is at project root
- Check for typos in dependency names
- Solution: Commit, push to GitHub → Cloud redeploys automatically

### "FileNotFoundError: data/commodity_prices.csv"
- Ensure `data/` folder committed to GitHub
- Check file path in `load_data()`
- Solution: Add to git, commit, push

### Landing page button not working
- Verify Streamlit Cloud URL is correct
- Update `index.html` with correct URL
- Test URL directly in browser

## Next Phase
**Phase 7: Pitch Materials** (Days 18-21)
- Screenshots of live app
- 2-minute demo video
- 15-slide pitch deck
- Grant application documents

## Deployment URLs
- **Streamlit App**: [To be filled after deployment]
- **Landing Page**: [To be filled after deployment]

---

**Phase 6 Status**: ✅ COMPLETE (Deployment ready)
