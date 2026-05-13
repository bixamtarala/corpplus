# Day 1 Action Plan - Build CropPulse

## YOUR GOAL TODAY: Foundation is Ready

By end of Day 1, you'll have:
- ✅ Project structure created
- ✅ Backend API skeleton (FastAPI)
- ✅ Database schema designed (PostgreSQL)
- ✅ Frontend project initialized (Next.js)
- ✅ Both deployed to development servers
- ✅ Basic API endpoints tested

**Time Estimate**: 6-8 hours (aggressive but doable)

---

## TASK BREAKDOWN

### PART 1: Backend Setup (2 hours)

#### 1.1 Create Backend Project Structure
```bash
# Create project root
mkdir croppulse && cd croppulse

# Create backend folder
mkdir backend && cd backend

# Initialize Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create requirements.txt
```

**requirements.txt** (create this file):
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

#### 1.2 Create FastAPI Project
```bash
pip install -r requirements.txt

# Create main.py
touch main.py
```

**main.py** (create this):
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="CropPulse API",
    description="AI-powered agricultural market intelligence platform",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "CropPulse API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### 1.3 Create Database Models
Create **models.py**:
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(20), unique=True)
    user_type = Column(String(50))  # farmer, fpo, trader
    hashed_password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class Commodity(Base):
    __tablename__ = "commodities"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    ticker = Column(String(10), unique=True)
    category = Column(String(50))

class PriceData(Base):
    __tablename__ = "price_data"
    
    id = Column(Integer, primary_key=True)
    commodity_id = Column(Integer, ForeignKey("commodities.id"))
    date = Column(DateTime, default=datetime.utcnow)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)

class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    favorite_commodities = Column(String(500))  # comma-separated IDs

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    commodity_id = Column(Integer, ForeignKey("commodities.id"))
    action = Column(String(20))  # SELL, BUY, HOLD
    confidence = Column(Float)
    reason = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    alert_type = Column(String(50))  # price_jump, high_volatility, etc
    message = Column(String(500))
    risk_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### 1.4 Create Database Connection
Create **database.py**:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for development (easier setup)
# Change to PostgreSQL later
DATABASE_URL = "sqlite:///./croppulse.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 1.5 Create Initial API Routes
Create **routes/commodities.py**:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Commodity, PriceData
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/commodities", tags=["commodities"])

@router.get("/")
def list_commodities(db: Session = Depends(get_db)):
    """Get all commodities"""
    commodities = db.query(Commodity).all()
    return commodities

@router.post("/")
def create_commodity(name: str, ticker: str, category: str, db: Session = Depends(get_db)):
    """Create a new commodity"""
    commodity = Commodity(name=name, ticker=ticker, category=category)
    db.add(commodity)
    db.commit()
    db.refresh(commodity)
    return commodity

@router.get("/{commodity_id}/prices")
def get_prices_30days(commodity_id: int, db: Session = Depends(get_db)):
    """Get 30-day price history"""
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    prices = db.query(PriceData).filter(
        PriceData.commodity_id == commodity_id,
        PriceData.date >= thirty_days_ago
    ).order_by(PriceData.date).all()
    return prices

@router.get("/{commodity_id}/latest")
def get_latest_price(commodity_id: int, db: Session = Depends(get_db)):
    """Get latest price"""
    price = db.query(PriceData).filter(
        PriceData.commodity_id == commodity_id
    ).order_by(PriceData.date.desc()).first()
    return price
```

**Update main.py** to include routes:
```python
from routes.commodities import router as commodities_router

app.include_router(commodities_router)
```

#### 1.6 Create .env File
Create **.env**:
```
DATABASE_URL=sqlite:///./croppulse.db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
```

**Test Backend**:
```bash
python main.py
# Visit http://localhost:8000/docs to see API docs
```

---

### PART 2: Frontend Setup (2 hours)

#### 2.1 Create Next.js Project
```bash
# Go back to project root
cd ..

# Create Next.js app
npx create-next-app@latest frontend --typescript --tailwind
cd frontend
```

Choose these options:
- Use TypeScript: Yes
- ESLint: Yes
- Tailwind CSS: Yes
- Use `src/` directory: Yes
- Use App Router: Yes
- Customize import alias: No

#### 2.2 Create Environment Variables
**frontend/.env.local**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 2.3 Create API Client Hook
Create **frontend/src/lib/api.ts**:
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
  async get(endpoint: string) {
    const response = await fetch(`${API_URL}${endpoint}`);
    if (!response.ok) throw new Error('API Error');
    return response.json();
  },

  async post(endpoint: string, data: any) {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('API Error');
    return response.json();
  },
};
```

#### 2.4 Create Login Page
Create **frontend/src/app/page.tsx**:
```typescript
'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Call API
    console.log('Login:', phone, password);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-green-500 to-green-700">
      <div className="bg-white rounded-lg shadow-lg p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-8 text-green-700">
          CropPulse
        </h1>
        
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Phone Number</label>
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="10-digit phone number"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Enter password"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-green-600 text-white py-2 rounded-lg font-medium hover:bg-green-700 transition"
          >
            Login
          </button>
        </form>

        <p className="text-center mt-4 text-sm text-gray-600">
          Don't have an account?{' '}
          <Link href="/signup" className="text-green-600 hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}
```

#### 2.5 Create Dashboard Layout
Create **frontend/src/app/dashboard/layout.tsx**:
```typescript
'use client';

import Link from 'next/link';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-green-700 text-white shadow-lg">
        <div className="p-6">
          <h2 className="text-2xl font-bold">CropPulse</h2>
        </div>
        
        <nav className="space-y-2 p-4">
          <Link href="/dashboard" className="block px-4 py-2 rounded hover:bg-green-600">
            Dashboard
          </Link>
          <Link href="/dashboard/commodities" className="block px-4 py-2 rounded hover:bg-green-600">
            Commodities
          </Link>
          <Link href="/dashboard/alerts" className="block px-4 py-2 rounded hover:bg-green-600">
            Alerts
          </Link>
          <Link href="/dashboard/recommendations" className="block px-4 py-2 rounded hover:bg-green-600">
            Recommendations
          </Link>
          <Link href="/dashboard/profile" className="block px-4 py-2 rounded hover:bg-green-600">
            Profile
          </Link>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <header className="bg-white shadow">
          <div className="px-6 py-4">
            <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
          </div>
        </header>
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
```

#### 2.6 Create Dashboard Page
Create **frontend/src/app/dashboard/page.tsx**:
```typescript
'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

export default function Dashboard() {
  const [commodities, setCommodities] = useState([]);

  useEffect(() => {
    // TODO: Fetch commodities
    console.log('Loading commodities...');
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Commodity Intelligence</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Commodity cards will go here */}
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-bold text-lg">Rice</h3>
          <p className="text-2xl font-bold text-green-600">₹3,200</p>
          <p className="text-sm text-gray-600">↑ +2.5% (7 days)</p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-bold text-lg">Wheat</h3>
          <p className="text-2xl font-bold text-green-600">₹2,100</p>
          <p className="text-sm text-gray-600">↑ +1.2% (7 days)</p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-bold text-lg">Cotton</h3>
          <p className="text-2xl font-bold text-red-600">₹5,500</p>
          <p className="text-sm text-gray-600">↓ -0.8% (7 days)</p>
        </div>
      </div>
    </div>
  );
}
```

**Test Frontend**:
```bash
npm run dev
# Visit http://localhost:3000
```

---

### PART 3: Database Initialization (30 minutes)

#### 3.1 Create Initialization Script
Create **backend/init_db.py**:
```python
from database import engine, SessionLocal
from models import Base, Commodity
import os

# Create all tables
Base.metadata.create_all(bind=engine)

# Add sample commodities
db = SessionLocal()

commodities_data = [
    {"name": "Rice", "ticker": "RICE", "category": "Cereals"},
    {"name": "Wheat", "ticker": "WHEAT", "category": "Cereals"},
    {"name": "Cotton", "ticker": "COTTON", "category": "Cash Crops"},
    {"name": "Sugarcane", "ticker": "SUGAR", "category": "Cash Crops"},
    {"name": "Spices", "ticker": "SPICE", "category": "Spices"},
]

for data in commodities_data:
    commodity = Commodity(**data)
    db.add(commodity)

db.commit()
print("✅ Database initialized with sample commodities")
db.close()
```

**Run it**:
```bash
python init_db.py
```

---

### PART 4: Deployment Setup (1 hour)

#### 4.1 Deploy Backend (Railway)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Deploy from backend folder
cd backend
railway init
railway up
# Note the deployed URL (e.g., https://croppulse-api.up.railway.app)
```

#### 4.2 Deploy Frontend (Vercel)
```bash
cd ../frontend

# Deploy to Vercel
npm i -g vercel
vercel

# Update NEXT_PUBLIC_API_URL with deployed backend URL
# Re-deploy: vercel
```

---

## CHECKLIST FOR END OF DAY 1

- [ ] Backend FastAPI project created and running locally
- [ ] Database models designed and initialized
- [ ] Basic API endpoints working (`/api/commodities`, `/health`)
- [ ] Frontend Next.js project created
- [ ] Login page and dashboard layout created
- [ ] API client hook created
- [ ] Backend deployed to Railway (or similar)
- [ ] Frontend deployed to Vercel
- [ ] Both talking to each other (test with `/health` endpoint)
- [ ] Database with 5 sample commodities loaded

---

## IF YOU FINISH EARLY

1. Add sample price data to the database (2 years of historical RICE prices)
2. Create `/api/commodities/{id}/prices` endpoint that returns price chart data
3. Build a simple price chart component in React

---

## NEXT: Day 2

Tomorrow you'll:
- Add real commodity price data (from NCDEX/Agmarknet)
- Build the commodity dashboard with charts
- Implement risk scoring algorithm

**See WEEK_BY_WEEK_ROADMAP.md Day 2 section for details**
