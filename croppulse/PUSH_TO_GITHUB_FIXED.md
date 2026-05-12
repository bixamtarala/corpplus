# Push CropPulse to GitHub - Complete Instructions

## Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository named `croppulse` (or your preferred name)
3. **DO NOT** initialize with README, .gitignore, or license
4. Copy the repository URL (e.g., `https://github.com/YOUR_USERNAME/croppulse.git`)

---

## Step 2: Open Terminal in Project Directory
Navigate to the project folder:
```powershell
cd C:\Users\LENOVO\Desktop\Agritech\croppulse
```

---

## Step 3: Initialize & Configure Git
Run these commands in order:

```powershell
# Initialize git repository
git init

# Configure your git user (use your GitHub credentials)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Verify configuration
git config --list
```

---

## Step 4: Stage All Changes
```powershell
# Add all files to staging area
git add .

# Verify what will be committed
git status
```

**Expected output:** You should see all files listed as "Changes to be committed" (green text)

---

## Step 5: Create Initial Commit
```powershell
git commit -m "Initial commit: CropPulse MVP with all phases (1-7) complete and division-by-zero errors fixed"
```

**Expected output:** Shows files changed, insertions/deletions

---

## Step 6: Add Remote & Push to GitHub
Replace `YOUR_USERNAME` and `REPO_NAME` with your actual GitHub username and repository name:

```powershell
# Add GitHub as remote origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Set default branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**First time only:** You'll be prompted to authenticate:
- Use your GitHub username
- For password, use a **Personal Access Token** (not your password)
  - Generate at: https://github.com/settings/tokens
  - Need scope: `repo` (full control of private repositories)

---

## Step 7: Verify Push Success
Check your GitHub repository online. You should see:
- ✅ All project files uploaded
- ✅ croppulse_app.py with latest fixes
- ✅ data/commodity_prices.csv
- ✅ requirements.txt
- ✅ .streamlit/config.toml
- ✅ All documentation files

---

## Step 8: Deploy to Streamlit Cloud (Next Step)
Once pushed to GitHub, deploy with:

1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select your GitHub repository
4. Choose branch: `main`
5. Choose file: `croppulse_app.py`
6. Click "Deploy"

Streamlit will automatically:
- Install requirements from `requirements.txt`
- Run your app
- Generate a public URL (e.g., `https://croppulse-app.streamlit.app`)

---

## Troubleshooting

### "fatal: not a git repository"
- Verify you're in the correct directory: `cd C:\Users\LENOVO\Desktop\Agritech\croppulse`
- Confirm `.git` folder exists: `ls -la` (PowerShell: `dir -Force`)

### Authentication failed
- Create Personal Access Token: https://github.com/settings/tokens
- Use token instead of password when prompted

### "refusing to merge unrelated histories"
- Run: `git pull origin main --allow-unrelated-histories`
- Then: `git push -u origin main`

---

## Commands Summary (Copy & Paste Ready)

```powershell
# Navigate to project
cd C:\Users\LENOVO\Desktop\Agritech\croppulse

# Initialize git
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Stage & commit
git add .
git commit -m "Initial commit: CropPulse MVP - all phases complete, division-by-zero errors fixed"

# Add remote (replace USERNAME and REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

---

## Status After Push
✅ Code backed up to GitHub
✅ Ready for Streamlit Cloud deployment
✅ Team can access repository
✅ Changes tracked with git history

**Next:** Deploy to Streamlit Cloud → Get live app URL → Day 2 begins (capture screenshots)
