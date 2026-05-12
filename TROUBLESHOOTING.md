# Troubleshooting Guide - Common Issues & Solutions

## PART 1: Backend Issues

### Issue 1: "ModuleNotFoundError: No module named 'fastapi'"

**Cause**: Requirements not installed

**Solution**:
```bash
# Make sure you're in backend folder with venv activated
cd backend
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install requirements
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic python-jose passlib

# Or use requirements.txt
pip install -r requirements.txt
```

---

### Issue 2: "Address already in use" on port 8000

**Cause**: Another service is using port 8000

**Solution**:
```bash
# Option 1: Use different port
python -m uvicorn main:app --port 8001

# Option 2: Kill process on port 8000
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
# Note the PID, then:
taskkill /PID [PID] /F
```

---

### Issue 3: Database file keeps resetting

**Cause**: Database getting deleted or recreated

**Solution**:
```bash
# Keep your croppulse.db file
# Check that database.py uses correct path:

# Good:
DATABASE_URL = "sqlite:///./croppulse.db"

# Avoid:
DATABASE_URL = "sqlite:///:memory:"  # This is in-memory (resets)

# Back up your data before reinit:
cp croppulse.db croppulse.db.backup
python init_db.py  # This will overwrite
cp croppulse.db.backup croppulse.db  # Restore if needed
```

---

### Issue 4: API returns empty commodity list

**Cause**: Database not initialized

**Solution**:
```bash
# Run initialization script
python init_db.py

# Verify commodities were added:
python
# Then run:
from database import SessionLocal
from models import Commodity
db = SessionLocal()
commodities = db.query(Commodity).all()
print(f"Total commodities: {len(commodities)}")
for c in commodities:
    print(f"- {c.name} ({c.ticker})")
```

---

### Issue 5: CORS error in frontend console

**Error**: "Access to XMLHttpRequest blocked by CORS policy"

**Cause**: Backend CORS not configured for frontend URL

**Solution**:
```python
# In backend/main.py, update CORS setup:

from fastapi.middleware.cors import CORSMiddleware

# LOCAL DEVELOPMENT:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PRODUCTION (after deployment):
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-vercel-url.vercel.app",
        "https://yourdomain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then restart backend: `python main.py`

---

### Issue 6: Import errors in routes

**Error**: "cannot import name 'SessionLocal' from database"

**Cause**: Circular imports or wrong file structure

**Solution**:
```bash
# Check your folder structure matches:
backend/
├── main.py
├── models.py
├── database.py
├── routes/
│   └── commodities.py
├── services/
│   └── price_service.py
└── venv/

# In routes/commodities.py, import like this:
from database import get_db
from models import Commodity, PriceData

# NOT like this:
from backend.database import get_db  # Wrong!
```

---

## PART 2: Frontend Issues

### Issue 1: "Cannot find module '@/lib/api'"

**Cause**: Path alias not configured

**Solution**:
```bash
# Create tsconfig.json (should be auto-created by create-next-app)
# It should have:
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}

# Restart dev server:
npm run dev
```

---

### Issue 2: Axios/Recharts not working

**Cause**: Dependencies not installed

**Solution**:
```bash
cd frontend
npm install axios recharts lucide-react

# Clear cache if still failing:
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

### Issue 3: "Cannot GET /dashboard"

**Cause**: Page file not created or App Router not setup

**Solution**:
```bash
# Make sure you have:
src/app/dashboard/layout.tsx
src/app/dashboard/page.tsx

# File structure should be:
frontend/src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx (login)
│   └── dashboard/
│       ├── layout.tsx
│       └── page.tsx
```

---

### Issue 4: API calls returning 404

**Cause**: Wrong backend URL or endpoint

**Solution**:
```typescript
// frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

// If using Vercel deployed backend:
NEXT_PUBLIC_API_URL=https://your-railway-backend.up.railway.app

// In services/commodityService.ts:
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Test the actual URL works:
curl http://localhost:8000/api/commodities/
// Should return JSON, not 404
```

---

### Issue 5: Chart not displaying

**Cause**: No data being passed to chart component

**Solution**:
```typescript
// In dashboard/page.tsx:

// Check if chartData is populated:
console.log('Chart data:', chartData);

// Add loading state:
{chartData.length > 0 ? (
  <PriceChart data={chartData} />
) : (
  <div>Loading chart...</div>
)}

// Ensure backend returns chart data format:
[
  { date: "2024-05-01", open: 3000, close: 3050, high: 3100, low: 2950 },
  ...
]
```

---

### Issue 6: "Port 3000 already in use"

**Solution**:
```bash
# Use different port:
npm run dev -- -p 3001

# Or kill port 3000:
# Mac/Linux:
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID [PID] /F
```

---

## PART 3: Database Issues

### Issue 1: Prices not showing up

**Cause**: No price data in database

**Solution**:
```bash
# Run generate_sample_data.py
python generate_sample_data.py

# Verify data was added:
python
from database import SessionLocal
from models import PriceData, Commodity
db = SessionLocal()
rice = db.query(Commodity).filter(Commodity.name == "Rice").first()
prices = db.query(PriceData).filter(PriceData.commodity_id == rice.id).count()
print(f"Total rice prices: {prices}")
```

---

### Issue 2: "database is locked"

**Cause**: Multiple processes writing to SQLite simultaneously

**Solution**:
```bash
# SQLite doesn't handle concurrent writes well
# For development: Just one person using it is fine

# For later (production): Switch to PostgreSQL
# Update database.py:
DATABASE_URL = "postgresql://user:password@localhost/croppulse"

# Install psycopg2:
pip install psycopg2-binary
```

---

### Issue 3: Data persists after app restart

**Cause**: Not sure if this is right behavior

**Note**: 
```bash
# SQLite data IS persistent between restarts
# To clear data and start fresh:
rm croppulse.db
python init_db.py
python generate_sample_data.py
```

---

## PART 4: Deployment Issues

### Issue 1: Railway deployment fails

**Solution**:
```bash
# Make sure you have Procfile in backend folder:
# File: backend/Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT

# Or requirements.txt in backend/:
# File: backend/requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
...

# Then:
railway login
cd backend
railway init
railway up

# Check logs:
railway logs
```

---

### Issue 2: Vercel deployment fails

**Solution**:
```bash
# Make sure vercel.json exists in frontend/:
# File: frontend/vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next"
}

# Then:
cd frontend
vercel
# Follow prompts

# Check deployment:
vercel logs [your-project]
```

---

### Issue 3: Deployed frontend can't reach deployed backend

**Solution**:
```bash
# Update frontend/.env.production with deployed backend URL:
NEXT_PUBLIC_API_URL=https://your-railway-backend.up.railway.app

# Redeploy frontend:
cd frontend
vercel

# Test the connection:
# Open browser console, run:
fetch('https://your-railway-backend.up.railway.app/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

---

## PART 5: General Debugging

### Enable Debug Logging

**Backend**:
```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Then in routes:
import logging
logger = logging.getLogger(__name__)

@router.get("/commodities")
def list_commodities():
    logger.debug("Fetching commodities...")
    # ...
```

**Frontend**:
```typescript
// In services/commodityService.ts
export const commodityService = {
  async getAllCommodities() {
    console.log('Fetching commodities from:', API_URL);
    const response = await apiClient.get('/api/commodities/');
    console.log('Response:', response.data);
    return response.data;
  },
}
```

---

### Check Network Requests

**Browser DevTools**:
1. Open Chrome DevTools (F12)
2. Go to Network tab
3. Reload page
4. Look for failed requests (red text)
5. Click on request, see what error was returned

---

### Create a Test Script

**backend/test_api.py**:
```python
import requests

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health: {response.json()}")

def test_commodities():
    response = requests.get(f"{BASE_URL}/api/commodities/")
    print(f"Commodities: {response.json()}")

def test_chart():
    response = requests.get(f"{BASE_URL}/api/commodities/1/chart")
    print(f"Chart: {response.json()}")

if __name__ == "__main__":
    print("Testing API endpoints...\n")
    test_health()
    test_commodities()
    test_chart()
```

Run it:
```bash
python test_api.py
```

---

## PART 6: Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Page looks ugly | Use Tailwind classes, refer to examples |
| Data not updating | Manually call API endpoint in browser or use test script |
| Something broke | Check git diff, see what changed last |
| Don't know what to do | Read the DAY_X_ACTION_PLAN.md for that day |
| Need different port | Change port number in startup command |
| Package version conflict | Delete node_modules, run npm install again |

---

## If All Else Fails

1. **Delete and start over** (takes 15 minutes)
   ```bash
   rm -rf backend frontend
   # Follow DAY_1_ACTION_PLAN.md again
   ```

2. **Check git status**
   ```bash
   git status
   git diff  # See what changed
   git reset --hard HEAD  # Undo changes
   ```

3. **Ask in the docs**
   - Read the relevant DAY_X_ACTION_PLAN.md
   - Search for error message in README.md
   - Check MVP_BUILD_PLAN.md for architecture info

---

## YOU'RE NOT ALONE

Most of these issues are **normal** and **fixable** in 5-10 minutes.

Keep moving. Don't get stuck for more than 15 minutes on any issue.

**Done is better than perfect.** 🚀
