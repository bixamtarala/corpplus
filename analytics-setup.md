# CropPulse Analytics Setup Guide

## Google Analytics Integration

### Step 1: Create a Google Analytics Account

1. Go to [https://analytics.google.com](https://analytics.google.com)
2. Click **Start measuring**
3. Enter your account name: `CropPulse`
4. Check all boxes for data sharing
5. Create your property:
   - Property name: `CropPulse Landing Page`
   - Time zone: `India (UTC+5:30)`
   - Currency: `INR`
6. Create your web data stream:
   - Website URL: Your landing page URL (e.g., https://croppulse.com)
   - Stream name: `Landing Page`

### Step 2: Get Your Measurement ID

- Your Measurement ID will appear (format: `G-XXXXXXXXXX`)
- Copy this ID

### Step 3: Add to Landing Page

Open `index.html` and find this section:

```html
<script>
    // Analytics - Google Analytics (replace with your GA ID)
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    // gtag('config', 'GA_MEASUREMENT_ID'); // Uncomment and add your Google Analytics ID
</script>
```

Replace with:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_MEASUREMENT_ID');
</script>
```

Replace `YOUR_MEASUREMENT_ID` with your actual ID.

### Step 4: Verify Installation

1. Deploy your landing page
2. Go to Google Analytics
3. Go to Realtime → Overview
4. Visit your landing page in a new tab
5. You should see live traffic in Analytics

---

## Events Being Tracked

The landing page automatically tracks:

### 1. **CTA Button Clicks**
   - Which button was clicked
   - Which section it's in
   - Helps measure conversion interest

### 2. **Newsletter Signups**
   - Email submissions (not stored, just counted)
   - Engagement metric

### 3. **Page Scrolls**
   - Which sections users visit

### 4. **Navigation Clicks**
   - Feature, Benefits, FAQ, Testimonials links
   - Shows user interests

---

## Google Analytics Dashboard Setup

### Create Custom Dashboard:

1. Go to Google Analytics
2. Click **Create** → **Dashboard**
3. Add these cards:

**Card 1: CTA Performance**
- Metric: Event Count
- Filter: Event name = `cta_click`
- Shows how many times users clicked "Launch Dashboard"

**Card 2: Top Sections**
- Metric: Event Count
- Dimension: Event parameter (page_section)
- Shows which sections get most clicks

**Card 3: Traffic Sources**
- Metric: Sessions
- Dimension: Source/Medium
- Shows where visitors come from

**Card 4: Device Breakdown**
- Metric: Sessions
- Dimension: Device Category
- Shows mobile vs desktop traffic

---

## Key Metrics to Monitor

1. **Sessions**: Total visits
2. **Users**: Unique visitors
3. **Bounce Rate**: % who leave without taking action
4. **CTA Clicks**: Engagement with app launch
5. **Newsletter Signups**: Lead generation
6. **Average Session Duration**: Content engagement
7. **Mobile vs Desktop**: Responsive design verification

---

## Alternative Analytics Tools

### 1. **Plausible Analytics** (Privacy-Focused)
- Similar to Google Analytics
- Better privacy for users
- No cookie consent needed in most countries
- Add to `<head>`:
```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

### 2. **Simple Analytics** (GDPR Compliant)
- European alternative to Google Analytics
- No cookie consent required
- GDPR friendly

### 3. **Fathom Analytics** (Privacy-First)
- Lightweight and privacy-focused
- Good for small sites
- European servers available

---

## Recommended Setup

For CropPulse, we recommend:

1. **Google Analytics** (Free, comprehensive)
   - Track all user interactions
   - Monitor conversion rates
   - Understand user behavior

2. **Email Newsletter** (Mailchimp, ConvertKit, etc.)
   - Capture email signups
   - Send market updates
   - Build user base

3. **Hotjar** (Optional, Paid)
   - Session recordings
   - Heatmaps
   - User feedback
   - Understand UX issues

---

## Privacy Considerations

✅ **Things Landing Page Respects:**
- No personal data collection
- No cookies (unless Google Analytics adds them)
- No tracking without consent
- Newsletter signups are optional
- Users can easily unsubscribe

⚠️ **Add Privacy Policy:**
Create `privacy-policy.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Privacy Policy - CropPulse</title>
</head>
<body>
    <h1>Privacy Policy</h1>
    
    <h2>Information We Collect</h2>
    <p>We collect analytics data about how you use our landing page using Google Analytics. This helps us understand user behavior and improve our service.</p>
    
    <h2>Data We Don't Collect</h2>
    <p>We do NOT collect personal information unless you voluntarily provide it through our newsletter signup form.</p>
    
    <h2>Google Analytics</h2>
    <p>We use Google Analytics to track page views, clicks, and user engagement. See Google's privacy policy for details.</p>
    
    <h2>Newsletter</h2>
    <p>If you sign up for our newsletter, your email is used ONLY to send market updates. We never share your email with third parties.</p>
    
    <h2>Contact</h2>
    <p>For privacy questions, contact us at privacy@croppulse.com</p>
</body>
</html>
```

Link to it in footer: `<a href="privacy-policy.html">Privacy Policy</a>`

---

## Monthly Reporting

Create a monthly analytics review:

1. Sessions and Users
2. Top traffic sources
3. Most popular sections
4. CTA conversion rate
5. Newsletter signup rate
6. Device breakdown
7. Geographic distribution
8. Recommendations for improvement

---

**Your analytics are now ready to track CropPulse success! 📊**
