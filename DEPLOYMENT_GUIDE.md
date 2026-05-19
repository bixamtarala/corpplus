# CropPulse Landing Page - Deployment Guide

This guide covers multiple options to deploy your CropPulse landing page to the web.

---

## 🚀 Option 1: GitHub Pages (Free & Easy)

### Prerequisites:
- GitHub account
- Git installed on your computer

### Steps:

1. **Create a GitHub Repository**
   ```bash
   # Navigate to your project directory
   cd c:\Users\LENOVO\Desktop\Agritech\croppulse\landing_page
   
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Create initial commit
   git commit -m "Initial landing page commit"
   ```

2. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Name it: `croppulse-landing` or similar
   - Do NOT initialize with README, .gitignore, or license

3. **Push to GitHub**
   ```bash
   # Add remote (replace YOUR_USERNAME and REPO_NAME)
   git remote add origin https://github.com/YOUR_USERNAME/croppulse-landing.git
   
   # Push to main branch
   git branch -M main
   git push -u origin main
   ```

4. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Click Settings → Pages
   - Under "Source", select "Deploy from a branch"
   - Select branch: `main`
   - Select folder: `/ (root)`
   - Click Save

5. **Your site will be live at:**
   ```
   https://YOUR_USERNAME.github.io/croppulse-landing
   ```

### Add Custom Domain (Optional):
- Go to Settings → Pages
- Under "Custom domain", enter your domain (e.g., `croppulse.com`)
- Follow GitHub's DNS setup instructions

---

## 🌐 Option 2: Netlify (Free & Powerful)

### Prerequisites:
- GitHub, GitLab, or Bitbucket account (or just drag & drop files)

### Steps:

1. **Deploy via Drag & Drop (Easiest)**
   - Go to https://app.netlify.com
   - Create a free account (or sign in)
   - Drag and drop your `landing_page` folder
   - Your site will be live instantly!

2. **Deploy via Git (Recommended)**
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli
   
   # Login to Netlify
   netlify login
   
   # Deploy (from landing_page directory)
   netlify deploy --prod
   ```

3. **Your site will be at:**
   ```
   https://YOUR-SITE-NAME.netlify.app
   ```

### Connect Custom Domain:
- In Netlify dashboard → Domain settings
- Add your custom domain
- Update DNS records at your domain registrar

---

## 📊 Option 3: Vercel (Free & Fast)

### Steps:

1. **Connect Git Repository**
   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Select the `landing_page` folder as the root

2. **Deploy**
   - Vercel will auto-detect and deploy
   - Your site will be at:
   ```
   https://YOUR-PROJECT-NAME.vercel.app
   ```

---

## 📈 Add Google Analytics

### Steps:

1. **Create Google Analytics Account**
   - Go to https://analytics.google.com
   - Create new account
   - Set up a web property for your domain
   - Copy your Measurement ID (starts with `G-`)

2. **Add to Landing Page**
   - Find this line in `index.html`:
   ```javascript
   // gtag('config', 'GA_MEASUREMENT_ID');
   ```
   - Replace `GA_MEASUREMENT_ID` with your actual ID
   - Uncomment the line

3. **Add Google Analytics Script**
   - Add this before the `</head>` closing tag:
   ```html
   <!-- Google Analytics -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'YOUR_GA_ID');
   </script>
   ```

4. **Track Button Clicks**
   - The landing page already has click tracking set up
   - Monitor in Google Analytics → Engagement → Events

---

## 🔒 SEO & Performance Tips

### Improve SEO:
1. **Add meta tags to `<head>`:**
   ```html
   <meta name="description" content="Agricultural market intelligence platform for farmers, traders, and FPOs">
   <meta name="keywords" content="agriculture, commodities, market prices, farming">
   <meta name="author" content="CropPulse Team">
   
   <!-- Open Graph for social sharing -->
   <meta property="og:title" content="CropPulse - Agricultural Market Intelligence">
   <meta property="og:description" content="Real-time commodity insights for informed trading decisions">
   <meta property="og:type" content="website">
   <meta property="og:url" content="https://croppulse.com">
   ```

2. **Add sitemap.xml:**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     <url>
       <loc>https://croppulse.com/</loc>
       <lastmod>2026-05-13</lastmod>
       <priority>1.0</priority>
     </url>
   </urlset>
   ```

3. **Add robots.txt:**
   ```
   User-agent: *
   Allow: /
   Sitemap: https://croppulse.com/sitemap.xml
   ```

### Performance:
- Landing page is optimized with:
  - Minimal CSS (inline, no external dependencies)
  - No heavy libraries
  - Responsive design
  - Fast load times
  - Mobile-friendly

---

## 🔄 Continuous Deployment

### Auto-update from GitHub:
- **Netlify**: Automatically deploys on every push to main branch
- **Vercel**: Automatically deploys on every push to main branch
- **GitHub Pages**: Automatically updates on every push to main branch

### Deploy Workflow:
1. Make changes locally
2. Test in browser
3. Commit and push to GitHub
4. Platform auto-deploys
5. Live within seconds!

---

## 📲 Link Landing Page to Streamlit App

### In Streamlit App (`streamlit_app_phase2.py`):
```python
st.markdown("""
    <div style="text-align: center; padding: 1rem; background: #f0f0f0; border-radius: 8px;">
        <a href="https://YOUR-LANDING-PAGE-URL" target="_blank" style="color: #2ecc71; text-decoration: none; font-weight: bold;">
            ← Back to Landing Page
        </a>
    </div>
""", unsafe_allow_html=True)
```

---

## ✅ Deployment Checklist

- [ ] Landing page created with all sections
- [ ] Analytics code added
- [ ] Repository created on GitHub
- [ ] Files pushed to GitHub
- [ ] GitHub Pages / Netlify / Vercel configured
- [ ] Custom domain setup (optional)
- [ ] Links between landing page and Streamlit app working
- [ ] Mobile responsiveness tested
- [ ] Links tested in different browsers

---

## 🆘 Troubleshooting

### GitHub Pages not showing?
- Check Settings → Pages
- Ensure branch is set to `main` or `master`
- Wait 1-2 minutes for deployment

### Netlify site not updating?
- Clear browser cache (Ctrl+Shift+Delete)
- Check deployment logs in Netlify dashboard
- Redeploy manually if needed

### Custom domain not working?
- Check DNS propagation at https://dnschecker.org
- May take 24-48 hours to propagate fully

---

## 📞 Support

For issues or questions:
- Check platform's documentation
- Review deployment logs
- Test locally before deploying

**Your CropPulse landing page is now ready to go live! 🚀**
