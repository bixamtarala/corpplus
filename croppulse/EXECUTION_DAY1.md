# DAY 1 EXECUTION: GitHub Setup & Streamlit Cloud Deployment
## Estimated Time: 1.5 hours

---

## ✅ PRE-FLIGHT CHECK (5 minutes)

Before starting, verify you have:
- [ ] GitHub account (create at github.com if needed - use your email)
- [ ] Git installed on Windows (download from git-scm.com)
- [ ] Streamlit account (sign up with GitHub at share.streamlit.io)
- [ ] Project files ready in: `c:\Users\LENOVO\Desktop\Agritech\croppulse\`

---

## 🔧 STEP 1: CREATE GITHUB REPOSITORY (10 minutes)

### On GitHub.com:
1. Sign in to github.com (create account if needed)
2. Click "New repository" (green button, top right)
3. **Repository Name:** `croppulse`
4. **Description:** Agricultural Market Intelligence Platform
5. **Visibility:** Public (required for Streamlit Cloud)
6. Leave other options default
7. Click "Create repository"

**You'll get a quick setup screen - follow these instructions next:**

---

## 🖥️ STEP 2: PUSH CODE TO GITHUB (20 minutes)

### Open Windows Command Prompt/PowerShell:

**Navigate to project folder:**
```
cd c:\Users\LENOVO\Desktop\Agritech\croppulse
```

**Initialize git (first time only):**
```
git init
```

**Add files:**
```
git add .
```

**Create first commit:**
```
git commit -m "CropPulse MVP - Phases 1-7 Complete"
```

**Add remote (replace YOUR_USERNAME with your GitHub username):**
```
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/croppulse.git
git push -u origin main
```

**You'll be prompted for credentials - use your GitHub username + personal access token (or password if enabled).**

### Verify on GitHub:
1. Go to github.com/YOUR_USERNAME/croppulse
2. You should see all your files there
3. Copy the repository URL for next step

---

## ☁️ STEP 3: DEPLOY TO STREAMLIT CLOUD (35 minutes)

### Go to Streamlit Cloud:
1. Open https://share.streamlit.io/
2. Click "New app" (blue button)
3. Sign in with GitHub if prompted

### Configuration:
- **Repository:** Select `YOUR_USERNAME/croppulse`
- **Branch:** `main`
- **Main file path:** `croppulse_app.py`
- Click "Deploy"

### Wait for Deployment:
- You'll see "Building..." for 2-5 minutes
- Console will show building progress
- When complete, you'll see "Running" status and a green checkmark

### Get Your Live URL:
- Your app is now live at: `https://croppulse.streamlit.app` 
  - (or a similar generated URL if that's taken)
- **SAVE THIS URL** - you'll need it for everything else!

---

## ✅ VERIFICATION (15 minutes)

### Test Your Live App:

1. **Open the app:**
   - Go to your Streamlit Cloud URL in browser
   - Wait 10-15 seconds for page to load

2. **Test Rice commodity:**
   - [ ] Dashboard loads without errors
   - [ ] KPI cards show: Price (₹3,200), Range, Volatility, Trend
   - [ ] Price chart displays correctly
   - [ ] Risk assessment shows score (around 45)
   - [ ] Alerts display (if any)
   - [ ] Insights show with confidence badges

3. **Test Wheat commodity:**
   - [ ] Switch to Wheat using sidebar dropdown
   - [ ] Verify different data displays (price ~₹2,150)
   - [ ] Chart updates
   - [ ] Risk score changes

4. **Test Cotton commodity:**
   - [ ] Switch to Cotton (price ~₹5,900)
   - [ ] Verify data loads correctly

5. **Test Export:**
   - [ ] Scroll to export section
   - [ ] Click "📊 Export CSV" - should download
   - [ ] Click "📝 Export Summary" - should download

6. **Test on Mobile:**
   - [ ] Use browser DevTools (F12)
   - [ ] Click device icon (📱)
   - [ ] Select iPhone 12 or Pixel 5
   - [ ] Verify layout works on mobile

### If Errors Occur:

**App won't load:**
- Check Streamlit Cloud console for errors
- Go to Settings → Advanced → Reboot app

**Missing data/CSV error:**
- Verify `data/commodity_prices.csv` was pushed to GitHub
- Re-deploy: Settings → Reboot

**Theme not loading:**
- Verify `.streamlit/config.toml` is committed
- Re-deploy

---

## 📝 SAVE CRITICAL INFORMATION

Create a file: `DEPLOYMENT_INFO.txt` with:

```
DEPLOYMENT INFORMATION
======================
Date: May 12, 2026
GitHub Username: [YOUR_USERNAME]
Repository URL: https://github.com/YOUR_USERNAME/croppulse
Live App URL: https://croppulse.streamlit.app
Streamlit Cloud: https://share.streamlit.io

CREDENTIALS SAVED:
- GitHub: ✓
- Streamlit Cloud: ✓

TEST RESULTS:
- Rice: ✓
- Wheat: ✓
- Cotton: ✓
- Exports: ✓
- Mobile: ✓
```

Save this in: `c:\Users\LENOVO\Desktop\Agritech\croppulse\DEPLOYMENT_INFO.txt`

---

## ✅ DAY 1 COMPLETION CHECKLIST

- [ ] GitHub account created
- [ ] Repository `croppulse` created and public
- [ ] All code pushed to GitHub (git push successful)
- [ ] Streamlit Cloud deployment complete
- [ ] Live app URL obtained
- [ ] All 3 commodities tested ✓
- [ ] Exports tested ✓
- [ ] Mobile responsiveness verified ✓
- [ ] Deployment info saved
- [ ] Screenshot verification list ready (Day 2)

---

## 🎯 SUCCESS INDICATOR

**You'll know Day 1 is complete when:**
- ✅ App is live at public URL
- ✅ All features work without errors
- ✅ You can share the link with others and they see working app

---

## 🆘 TROUBLESHOOTING

### "Remote origin already exists"
```
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/croppulse.git
```

### "Permission denied (publickey)"
- Generate GitHub SSH key: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- OR use personal access token instead of password

### "requirements.txt not found"
- Verify file exists in project root
- Or create it in Streamlit Cloud settings

### Still stuck?
- Restart Streamlit Cloud app (Settings → Reboot)
- Check Streamlit Cloud logs for error details
- Verify all files are committed to GitHub

---

**Day 1 Time: 1.5 hours | Status: Ready for Day 2**
