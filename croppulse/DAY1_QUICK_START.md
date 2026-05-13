# ⚡ DAY 1 - QUICK START (Copy-Paste Ready)
## GitHub Setup + Streamlit Deploy - 1.5 Hours

**Date:** May 12, 2026  
**Task:** Get app live at public URL  
**Output Needed:** Live app URL (save for Days 2-7)

---

## 🎯 YOUR MISSION (3-step)

1. **Create GitHub repo** (10 min)
2. **Push code to GitHub** (20 min)
3. **Deploy to Streamlit Cloud** (35 min + 15 min test)

---

## ✅ PREREQUISITES (Have These Ready)

- [ ] **GitHub Account** - Create at https://github.com (free, takes 2 min)
- [ ] **Git Installed** - Download from https://git-scm.com/ (Windows installer)
- [ ] **GitHub Username** - The name you'll use for login
- [ ] **Streamlit Account** - Sign up at https://share.streamlit.io (use GitHub login)

**If you don't have these yet, stop and create them first (5-10 minutes). This guide will wait.**

---

## 🔧 STEP 1: CREATE GITHUB REPOSITORY (10 minutes)

### 1️⃣ Go to GitHub.com
```
https://github.com
```

### 2️⃣ Click "New Repository" (green button, top right)

### 3️⃣ Fill in these fields:
```
Repository name: croppulse
Description: Agricultural Market Intelligence Platform
Visibility: PUBLIC (required for Streamlit Cloud!)
```

### 4️⃣ Click "Create Repository"

### ✅ Success Check:
You should see a screen that says:
```
"...or push an existing repository from the command line"
```

**Copy the repository URL** (looks like):
```
https://github.com/YOUR_USERNAME/croppulse.git
```

You'll need this in the next step.

---

## 💻 STEP 2: PUSH CODE TO GITHUB (20 minutes)

### Open Command Prompt or PowerShell (Windows):
Press **Windows Key + R**, type `cmd` or `powershell`, press Enter

### Copy-Paste These Commands (One at a time):

#### Command 1: Navigate to project
```
cd c:\Users\LENOVO\Desktop\Agritech\croppulse
```
Then press Enter

#### Command 2: Initialize git
```
git init
```
Then press Enter

#### Command 3: Add all files
```
git add .
```
Then press Enter

#### Command 4: Create first commit
```
git commit -m "CropPulse MVP - Phases 1-7 Complete"
```
Then press Enter

#### Command 5: Rename branch to main
```
git branch -M main
```
Then press Enter

#### Command 6: Add remote (⚠️ REPLACE YOUR_USERNAME)
```
git remote add origin https://github.com/YOUR_USERNAME/croppulse.git
```
Replace `YOUR_USERNAME` with your actual GitHub username, then press Enter

**Example:** 
```
git remote add origin https://github.com/johnsmith/croppulse.git
```

#### Command 7: Push to GitHub
```
git push -u origin main
```
Then press Enter

**You may be prompted for:**
- Username: Enter your GitHub username
- Password: Enter your GitHub personal access token (NOT your password!)

### ✅ Success Check:
You should see output like:
```
Enumerating objects: 45, done.
Compressing objects: 100% (42/42), done.
Writing objects: 100% (45/45), 2.5 MiB | 500 KiB/s, done.
Total 45 (delta 0), reused 0 (delta 0)
To https://github.com/YOUR_USERNAME/croppulse.git
 * [new branch]      main -> main
Branch 'main' is set up to track remote branch 'main' from 'origin'.
```

### Verify on GitHub:
1. Go to `https://github.com/YOUR_USERNAME/croppulse`
2. You should see your files there (croppulse_app.py, requirements.txt, data/, etc.)
3. ✅ If yes, you're done with Step 2!

---

## ☁️ STEP 3: DEPLOY TO STREAMLIT CLOUD (35 minutes)

### 1️⃣ Go to Streamlit Cloud
```
https://share.streamlit.io/
```

### 2️⃣ Click "New app" (blue button)
- Sign in with GitHub if prompted

### 3️⃣ Select Your Repository:

You'll see a form with 3 dropdowns:
```
Repository: YOUR_USERNAME/croppulse
Branch: main
Main file path: croppulse_app.py
```

### 4️⃣ Click "Deploy"

### ⏳ Wait for Deployment:
You'll see a console that says "Building..." 
- This takes 2-5 minutes
- Watch for progress messages
- When done, you'll see a green checkmark "✓ Running"

### 🎉 Get Your Live URL:
At the top of the page, you'll see your app URL:
```
https://croppulse.streamlit.app
```
or something similar like `https://croppulse-abc123.streamlit.app`

**⭐ SAVE THIS URL ⭐**
You need it for Days 2-7!

---

## ✅ VERIFICATION (15 minutes)

### 1️⃣ Open Your Live App
Go to your Streamlit Cloud URL in a web browser (takes 10-15 seconds to load)

### 2️⃣ Test Each Commodity (Copy This Checklist)

**Rice (Default):**
- [ ] Dashboard loads without errors
- [ ] Price shows around ₹3,200
- [ ] KPI cards visible: Price, Range, Volatility, Trend
- [ ] Price chart displays correctly
- [ ] Risk score shows (around 45/100)
- [ ] Insights display with confidence badges (85%, 78%, etc.)

**Wheat (Switch via sidebar):**
- [ ] Sidebar dropdown works
- [ ] Data changes to Wheat (~₹2,150)
- [ ] Chart updates
- [ ] Risk score different (around 38/100)
- [ ] Insights regenerated

**Cotton (Switch via sidebar):**
- [ ] Data changes to Cotton (~₹5,900)
- [ ] All features work correctly

**Export:**
- [ ] Scroll down to export section
- [ ] Click "📊 Export CSV" - should download file
- [ ] Click "📝 Export Summary" - should download file

**Mobile Test:**
- [ ] Press F12 (browser DevTools)
- [ ] Click mobile icon (📱)
- [ ] Select "iPhone 12" or "Pixel 5"
- [ ] Layout adjusts properly (no horizontal scrolling)

### ✅ All Tests Pass?
**Congratulations! Day 1 is COMPLETE! 🎉**

---

## 📝 SAVE THIS INFORMATION

Create a new file: `DEPLOYMENT_INFO.txt`

**Location:** `c:\Users\LENOVO\Desktop\Agritech\croppulse\DEPLOYMENT_INFO.txt`

**Content:**
```
DEPLOYMENT INFORMATION
======================
Date: May 12, 2026
GitHub Username: [YOUR_USERNAME]
Repository URL: https://github.com/YOUR_USERNAME/croppulse
Live App URL: https://croppulse.streamlit.app

ACCOUNTS VERIFIED:
✓ GitHub account created
✓ Git installed and working
✓ Streamlit Cloud connected
✓ Repository pushed to GitHub
✓ App deployed to Streamlit Cloud

TESTS COMPLETED:
✓ Rice commodity tested
✓ Wheat commodity tested  
✓ Cotton commodity tested
✓ Export CSV working
✓ Export Summary working
✓ Mobile responsiveness verified

STATUS: READY FOR DAY 2
```

---

## 🆘 TROUBLESHOOTING

### Error: "Remote origin already exists"
```
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/croppulse.git
```

### Error: "Permission denied (publickey)"
Use personal access token instead:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: repo, read:user
4. Copy the token
5. When prompted for password in git, paste the token

### Error: "requirements.txt not found" on Streamlit
1. Go to Streamlit Cloud → Your app → Settings → Advanced
2. Clear cache and reboot
3. Or verify requirements.txt is committed to GitHub

### App shows error about CSV file
1. Verify `data/commodity_prices.csv` exists
2. Commit to GitHub: `git add data/commodity_prices.csv`
3. Reboot app in Streamlit Cloud

### Still have issues?
- Check Streamlit Cloud console for detailed error
- Go to Settings → Reboot app
- Restart deployment

---

## 📋 DAY 1 CHECKLIST

- [ ] GitHub account created ✓
- [ ] Git installed ✓
- [ ] GitHub repository "croppulse" created ✓
- [ ] Code pushed to GitHub ✓
- [ ] Streamlit Cloud account connected ✓
- [ ] App deployed successfully ✓
- [ ] Live URL obtained and saved ✓
- [ ] All commodities tested ✓
- [ ] Exports working ✓
- [ ] Mobile responsive ✓
- [ ] DEPLOYMENT_INFO.txt created ✓

---

## 🎯 NEXT STEP

**Tomorrow (Day 2):** Capture 7 screenshots
1. Open: `EXECUTION_DAY2.md`
2. Use the live app URL from today
3. Capture dashboard images

---

## ⏱️ TIME TRACKING

- Pre-flight: 5 min
- Create repo: 10 min
- Push to GitHub: 20 min
- Deploy: 35 min
- Verify: 15 min
- **Total: 1 hour 25 minutes** ✓

**Well done! Day 1 is your foundation for everything else.** 💪

---

**Start Step 1 now. You've got this! 🚀**
