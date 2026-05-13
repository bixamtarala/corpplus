# 🚀 PUSH TO GITHUB - COPY-PASTE COMMANDS
## May 12, 2026 | Execution Ready

---

## ⚡ QUICK START (Copy These Commands)

**Open Command Prompt/PowerShell and run these commands one-by-one:**

### Command 1: Navigate to your project
```
cd c:\Users\LENOVO\Desktop\Agritech\croppulse
```

### Command 2: Initialize git (if first time)
```
git init
```

### Command 3: Add all files
```
git add .
```

### Command 4: Create first commit
```
git commit -m "CropPulse MVP - Phases 1-7 Complete - All Materials Ready"
```

### Command 5: Set branch to main
```
git branch -M main
```

### Command 6: Add remote (⚠️ REPLACE YOUR_USERNAME WITH YOUR GITHUB USERNAME)
```
git remote add origin https://github.com/YOUR_USERNAME/croppulse.git
```

**Example (if your username is "johnsmith"):**
```
git remote add origin https://github.com/johnsmith/croppulse.git
```

### Command 7: Push to GitHub
```
git push -u origin main
```

**You'll be prompted for credentials:**
- Username: Your GitHub username
- Password: Your GitHub personal access token (NOT your password!)

---

## ✅ VERIFY SUCCESS

After pushing, check:

```
1. Go to: https://github.com/YOUR_USERNAME/croppulse
2. You should see all your files there
3. Verify all files are present:
   ✓ croppulse_app.py
   ✓ requirements.txt
   ✓ data/commodity_prices.csv
   ✓ .streamlit/config.toml
   ✓ landing_page/index.html
   ✓ All Day 1-7 guides
   ✓ All templates and scripts
```

---

## 🆘 IF YOU GET AN ERROR

### Error: "repository does not exist"
→ Create it first at github.com/new

### Error: "remote origin already exists"
→ Run: `git remote remove origin`
→ Then re-run Command 6-7

### Error: "Permission denied (publickey)"
→ Use personal access token instead of password
→ Get token at: https://github.com/settings/tokens

---

## 📝 YOUR GITHUB USERNAME
(Fill this in)
```
GitHub Username: _________________
```

---

**Then you're ready for Streamlit deployment!**
