# DAY 1 TROUBLESHOOTING GUIDE
## GitHub + Streamlit Deployment Issues & Solutions

---

## 🔴 CRITICAL ISSUES

### "App won't load / Blank page"

**Cause:** Streamlit still deploying or dependency missing

**Solution:**
1. Wait 30 seconds and refresh (F5)
2. Check Streamlit Cloud console:
   - Go to: https://share.streamlit.io
   - Click your app name
   - Click "Settings" → "Advanced"
   - Click "Reboot app"
3. Wait 2-3 minutes for rebuild
4. Refresh browser

**Still failing?** Check for Python errors:
- Open Streamlit Cloud dashboard
- Click your app → "Settings"
- Look for error messages in logs
- Verify requirements.txt is committed to GitHub

---

### "ModuleNotFoundError: No module named 'streamlit'"

**Cause:** Streamlit not in requirements.txt or file not committed

**Solution:**
1. Verify requirements.txt exists:
   ```
   ls c:\Users\LENOVO\Desktop\Agritech\croppulse\requirements.txt
   ```
2. If missing, create it with:
   ```
   pip list > requirements.txt
   ```
3. Commit and push:
   ```
   git add requirements.txt
   git commit -m "Add requirements.txt"
   git push
   ```
4. Reboot app in Streamlit Cloud

---

### "Error loading CSV file / data/commodity_prices.csv not found"

**Cause:** Data file not pushed to GitHub

**Solution:**
1. Verify file exists locally:
   ```
   ls c:\Users\LENOVO\Desktop\Agritech\croppulse\data\
   ```
2. Should see: commodity_prices.csv

3. Commit data folder:
   ```
   cd c:\Users\LENOVO\Desktop\Agritech\croppulse
   git add data/
   git commit -m "Add commodity data"
   git push
   ```

4. Reboot Streamlit app

---

### "Permission denied (publickey) / Authentication failed"

**Cause:** GitHub credentials wrong or SSH key issue

**Solution Option 1 - Use Personal Access Token:**
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token"
3. Name it: "CropPulse Deployment"
4. Select scopes:
   - ✓ repo
   - ✓ read:user
5. Click "Generate token"
6. Copy the token (long string)
7. When git asks for password, paste this token

**Solution Option 2 - Use HTTPS instead of SSH:**
```
git remote set-url origin https://github.com/YOUR_USERNAME/croppulse.git
git push -u origin main
```

Then paste personal access token when prompted.

---

### ".streamlit/config.toml not found" / Theme not loading

**Cause:** Config file not committed to GitHub

**Solution:**
1. Verify file exists:
   ```
   ls c:\Users\LENOVO\Desktop\Agritech\croppulse\.streamlit\
   ```

2. Add to git:
   ```
   git add .streamlit/config.toml
   git commit -m "Add Streamlit configuration"
   git push
   ```

3. Reboot app in Streamlit Cloud

---

## 🟡 COMMON ISSUES

### "Repository not found / Cannot access repository"

**Cause:** Repository URL wrong or not public

**Solution:**
1. Verify repository is PUBLIC:
   - Go to: https://github.com/YOUR_USERNAME/croppulse
   - Click "Settings"
   - Scroll to "Danger Zone"
   - Verify "Public" is selected

2. Verify URL format:
   ```
   # Should look like:
   https://github.com/YOUR_USERNAME/croppulse
   
   # NOT:
   https://github.com/YOUR_USERNAME/croppulse.git (if you used .git above)
   ```

3. In Streamlit Cloud, check repo URL entered exactly matches

---

### "Deployment stuck on 'Building'"

**Cause:** Build process taking too long or stalled

**Solution:**
1. Wait 5 minutes (first deployments are slower)
2. Check Streamlit Cloud console for progress
3. If no progress after 10 minutes, cancel and retry:
   - Click your app → Settings → "Cancel current deployment"
   - Click "Deploy" again

---

### "Sidebar dropdown doesn't work / Commodity selector broken"

**Cause:** Streamlit caching issue or code error

**Solution:**
1. Hard refresh browser: Ctrl+Shift+R (not just F5)
2. Clear browser cache and cookies
3. Reboot Streamlit app:
   - Settings → Advanced → Reboot
4. Try again after 2 minutes

---

### "Charts not showing / Data visualization blank"

**Cause:** Plotly library missing or data format wrong

**Solution:**
1. Verify requirements.txt includes:
   ```
   plotly==5.17.0
   ```

2. Commit if missing:
   ```
   git add requirements.txt
   git commit -m "Add Plotly dependency"
   git push
   ```

3. Reboot app

---

### "Export buttons don't work / Download fails"

**Cause:** File permission or encoding issue

**Solution:**
1. Test locally first:
   ```
   python c:\Users\LENOVO\Desktop\Agritech\croppulse\croppulse_app.py
   ```
   Try export buttons locally.

2. If works locally but not in cloud:
   - Reboot app in Streamlit Cloud
   - Clear browser cache (Ctrl+Shift+Delete)
   - Try export again

3. Check console for errors (F12 → Console)

---

### "Mobile view shows horizontal scroll / Layout broken"

**Cause:** CSS or Streamlit responsive design issue

**Solution:**
1. This is usually normal for Streamlit on mobile
2. Verify minimum functionality works:
   - Text readable
   - Buttons clickable
   - Charts visible (may need scroll)

3. To improve, update `.streamlit/config.toml`:
   ```
   [client]
   toolbarMode = "minimal"
   ```

4. Commit and push, then reboot

---

## 🟢 VERIFICATION TESTS

### Test 1: Check Git Status
```
cd c:\Users\LENOVO\Desktop\Agritech\croppulse
git status
```
**Expected output:**
```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

**If not:** You have uncommitted changes
```
git add .
git commit -m "Update"
git push
```

---

### Test 2: Verify GitHub Push
```
cd c:\Users\LENOVO\Desktop\Agritech\croppulse
git log --oneline
```
**Expected:** See your commits listed

**Alternative:** Go to https://github.com/YOUR_USERNAME/croppulse and verify files appear

---

### Test 3: Test App Locally
```
cd c:\Users\LENOVO\Desktop\Agritech\croppulse
streamlit run croppulse_app.py
```
**Expected:** App opens in browser at http://localhost:8501

**If works locally but not in cloud:** Your code is good, deployment issue only

---

### Test 4: Check Live App Console
1. Open your Streamlit app
2. Press F12 (DevTools)
3. Click "Console" tab
4. Look for red errors
5. Report errors to Streamlit support if needed

---

## 📞 GETTING HELP

### If You're Still Stuck:

**Step 1: Collect Information**
- Screenshot of error message
- Error from Streamlit Cloud console
- Output from your local git/terminal
- Your GitHub username (don't share token)

**Step 2: Check These Resources**
- Streamlit Docs: https://docs.streamlit.io
- Git Docs: https://git-scm.com/doc
- GitHub Docs: https://docs.github.com
- Streamlit Community: https://discuss.streamlit.io

**Step 3: Create Issue on GitHub**
- Go to your repo: https://github.com/YOUR_USERNAME/croppulse
- Click "Issues"
- Click "New Issue"
- Describe problem clearly with:
  - What you tried
  - What happened
  - What you expected
  - Screenshots of error

**Step 4: Ask for Help**
- Streamlit Community Forum: https://discuss.streamlit.io
- Stack Overflow tag: streamlit
- GitHub Discussions (in your repo)

---

## ✅ SUCCESS INDICATORS

### You know it's working when:

- ✓ `git push` completes without errors
- ✓ GitHub shows your files at https://github.com/YOUR_USERNAME/croppulse
- ✓ Streamlit Cloud shows green checkmark (✓ Running)
- ✓ Your live app URL works and shows the dashboard
- ✓ All 3 commodities load different data
- ✓ Charts and graphs display correctly
- ✓ Export buttons work
- ✓ Mobile view is readable (even if scrolling needed)

**If all above are checked:** Day 1 is COMPLETE! 🎉

---

## 🚀 READY FOR DAY 2?

Once Day 1 is complete:
1. Save your live app URL somewhere safe
2. Open `EXECUTION_DAY2.md`
3. Begin capturing screenshots (uses your live app)

---

**Day 1 is the foundation. Take your time to get it right!**  
**Once deployed, Days 2-7 will be much faster.** ⚡

