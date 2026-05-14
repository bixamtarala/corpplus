# eNAM API Integration Setup Guide

## Overview
CropPulse now connects to the **National Agricultural Market (eNAM) API** for real-time commodity prices from mandis across India.

---

## Getting Started with eNAM API

### Step 1: Register with eNAM
1. Visit: https://www.enamapis.com/developer
2. Sign up for a developer account
3. Create a new application
4. Get your **API Key**

### Step 2: Set Environment Variables

**Option A: Windows (PowerShell)**
```powershell
$env:ENAM_API_KEY = "your_api_key_here"
$env:ENAM_API_BASE = "https://www.enamapis.com/api"
```

**Option B: Create `.env` file** (in the croppulse folder)
```
ENAM_API_KEY=your_api_key_here
ENAM_API_BASE=https://www.enamapis.com/api
```

**Option C: Update Python code** (temporary, not recommended for production)
Edit `enam_api.py` line 11:
```python
ENAM_API_KEY = "your_api_key_here"  # Replace with your key
```

### Step 3: Test the Integration

```bash
cd c:\Users\LENOVO\Desktop\Agritech\croppulse
python enam_api.py
```

Expected output:
```
🔄 Testing eNAM API Integration...

1️⃣ Fetching live Rice prices from eNAM...
✅ Retrieved 30 days of data
   date  price  supply  demand
...

2️⃣ Fetching multi-mandi prices...
{'Tamil Nadu': 3330, 'Telangana': 3280, ...}
```

---

## API Endpoints Used

### 1. Get Commodity Prices (Single Mandi)
```
GET /commodities/get-prices
Parameters:
  - commodity: Rice, Wheat, Cotton
  - stateCode: TN, AP, TG, KA, OR
  - districtCode: 01, 02, etc.
  - limit: 30 (days)
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "date": "2026-05-14T00:00:00Z",
      "price": 3330,
      "high": 3400,
      "low": 3200,
      "volume": 5000,
      "mandiName": "Koyambedu, Tamil Nadu"
    }
  ]
}
```

### 2. Get Multi-Mandi Prices
```
GET /mandis/prices
Parameters:
  - commodity: Rice, Wheat, Cotton
  - limit: 5 (days)
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "mandiName": "Tamil Nadu",
      "currentPrice": 3330,
      "high": 3400,
      "low": 3200,
      "volume": 5000,
      "timestamp": "2026-05-14T10:30:00Z"
    }
  ]
}
```

---

## Features Now Using Live Data

✅ **Feature 1: Trading Signal** - Uses live prices & supply/demand
✅ **Feature 2: Current Price Ticker** - Real-time eNAM prices
✅ **Feature 3: Risk Meter** - Based on live volatility
✅ **Feature 4: Multi-Mandi Comparison** - All 4 mandis from eNAM
✅ **Feature 5: Price Forecast** - Historical + eNAM data
✅ **Feature 6: Profit Calculator** - Uses live buy/sell prices
✅ **Feature 7: Trade Logger** - Can track real deals
✅ **Feature 8: Alert Settings** - Monitors live prices
✅ **Feature 9: Market Balance** - Live supply/demand ratios

---

## Fallback Strategy

If eNAM API is unavailable:
1. ⚠️ Tries eNAM API (3-second timeout)
2. 📊 Falls back to cached CSV demo data
3. ✅ App always works (no data = app still runs)

---

## Performance Optimization

- **Caching:** 1-hour cache (data refreshes hourly)
- **Request Timeout:** 10 seconds (prevents hanging)
- **Compression:** gzip response compression enabled
- **Rate Limiting:** Respects eNAM API rate limits

---

## Troubleshooting

### Problem: "API Key Invalid"
```python
# Check in enam_api.py line 11
ENAM_API_KEY = "your_key_here"  # Must be valid
```

### Problem: "Connection Timeout"
- Check internet connection
- eNAM servers might be down
- App will use CSV fallback automatically

### Problem: "Empty Data"
- Commodity might not be available in that mandi
- Try different state_code: TN, AP, TG, KA, OR
- Use fallback data temporarily

### Problem: "Module Not Found"
```bash
# Ensure enam_api.py is in same folder
cd c:\Users\LENOVO\Desktop\Agritech\croppulse
ls -la enam_api.py
```

---

## Running the App with Live Data

```bash
cd c:\Users\LENOVO\Desktop\Agritech\croppulse

# Set API key (PowerShell)
$env:ENAM_API_KEY = "your_api_key"

# Run app
streamlit run croppulse_app.py
```

You'll see:
- 🔄 "Fetching live data from eNAM API..."
- ✅ "Live eNAM data loaded!" (success)
- Or 📊 "Using demo data (CSV fallback)" (if API unavailable)

---

## Next Steps

1. ✅ Get eNAM API key (https://www.enamapis.com/developer)
2. ✅ Set environment variable with API key
3. ✅ Test integration: `python enam_api.py`
4. ✅ Run app with live data: `streamlit run croppulse_app.py`
5. 📱 Add WhatsApp integration (next phase)
6. 💾 Add database storage (phase after)

---

## API Rate Limits

- **Free Tier:** 1000 requests/day
- **Commercial Tier:** Unlimited
- **Recommended:** Cache for 1 hour to reduce requests

---

## Support

For eNAM API issues: support@enamapis.com
For CropPulse issues: Create an issue in GitHub

