# Sample Data Generation & Price Data Setup

## PART 1: Generate Historical Price Data (Run After Day 1)

Create **backend/generate_sample_data.py**:

```python
from database import SessionLocal
from models import Commodity, PriceData
from datetime import datetime, timedelta
import random

db = SessionLocal()

# Get commodities
commodities = db.query(Commodity).all()

# Generate 2 years of sample price data for each commodity
for commodity in commodities:
    print(f"Generating price data for {commodity.name}...")
    
    # Base prices (realistic ranges)
    base_prices = {
        "RICE": 3000,      # ₹/quintal
        "WHEAT": 2000,     # ₹/quintal
        "COTTON": 5500,    # ₹/kg
        "SUGAR": 3500,     # ₹/quintal
        "SPICE": 8000,     # ₹/kg
    }
    
    base_price = base_prices.get(commodity.ticker, 3000)
    
    # Generate daily prices for 730 days (2 years)
    start_date = datetime.utcnow() - timedelta(days=730)
    
    for day in range(730):
        current_date = start_date + timedelta(days=day)
        
        # Simulate price movement (random walk with trend)
        daily_change = random.uniform(-2, 2)  # ±2% daily change
        price = base_price * (1 + daily_change / 100)
        
        # Add some seasonal patterns
        month = current_date.month
        if month in [5, 6, 7]:  # Monsoon season - prices typically lower
            price *= 0.95
        elif month in [10, 11]:  # Harvest season - prices typically higher
            price *= 1.05
        
        # Create OHLC data
        open_price = price
        close_price = price * random.uniform(0.99, 1.01)
        high_price = max(open_price, close_price) * random.uniform(1.01, 1.03)
        low_price = min(open_price, close_price) * random.uniform(0.97, 0.99)
        
        price_data = PriceData(
            commodity_id=commodity.id,
            date=current_date,
            open=round(open_price, 2),
            close=round(close_price, 2),
            high=round(high_price, 2),
            low=round(low_price, 2),
        )
        
        db.add(price_data)
    
    db.commit()
    print(f"✅ Generated 730 price points for {commodity.name}")

print("\n✅ All sample data generated successfully!")
db.close()
```

**Run it**:
```bash
python generate_sample_data.py
```

---

## PART 2: Real Commodity Price Fetching (For Later)

### Option A: NCDEX Futures Prices (Recommended)

Create **backend/services/ncdex_service.py**:

```python
import requests
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from models import PriceData, Commodity

# Note: NCDEX has rate limits. Use with caution.
# For MVP, use historical data first, then add live updates later

class NCDEXService:
    def __init__(self):
        self.base_url = "https://www.ncdex.com"  # Example - check actual API
        
    def get_current_prices(self):
        """
        Fetch current commodity prices
        Note: NCDEX may not have free public API
        Alternative: Use Agmarknet or third-party API
        """
        pass
    
    def get_historical_prices(self, commodity_ticker: str, days: int = 30):
        """
        Fetch historical prices for a commodity
        """
        pass

# For MVP: Use manually updated daily prices or web scraping
```

### Option B: Agmarknet Web Scraping (Free Government Source)

Create **backend/services/agmarknet_service.py**:

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session
from models import PriceData, Commodity

class AgmarknetService:
    """
    Scrapes daily APMC prices from Agmarknet (Indian government source)
    Free, reliable, covers all major commodities and markets
    """
    
    def __init__(self):
        self.base_url = "https://agmarknet.gov.in"
    
    def get_today_prices(self, commodity_code: str):
        """
        Get today's prices from Agmarknet
        commodity_code: "rice", "wheat", "cotton", etc.
        """
        url = f"{self.base_url}/SearchCommodityPrices.aspx"
        
        params = {
            'hiddenflag': commodity_code,
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse HTML and extract prices
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find price table
            table = soup.find('table', {'id': 'gvDetails'})
            
            if table:
                rows = table.find_all('tr')[1:]  # Skip header
                
                prices = []
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        market = cols[0].text.strip()
                        modal_price = float(cols[3].text.strip())
                        
                        prices.append({
                            'market': market,
                            'price': modal_price,
                            'date': datetime.now(),
                        })
                
                return prices
        
        except Exception as e:
            print(f"Error fetching Agmarknet data: {e}")
            return None
    
    def save_prices_to_db(self, commodity_id: int, prices: list, db: Session):
        """Save fetched prices to database"""
        for price_data in prices:
            # Use modal price as close price
            price_entry = PriceData(
                commodity_id=commodity_id,
                date=price_data['date'],
                open=price_data['price'],
                close=price_data['price'],
                high=price_data['price'] * 1.02,
                low=price_data['price'] * 0.98,
            )
            db.add(price_entry)
        
        db.commit()
```

### Option C: Simple Daily Price Update Script

Create **backend/update_prices.py** (Run daily via cron):

```python
from database import SessionLocal
from models import Commodity, PriceData
from datetime import datetime
import random

db = SessionLocal()

commodities = db.query(Commodity).all()

for commodity in commodities:
    # Get last price
    last_price = db.query(PriceData).filter(
        PriceData.commodity_id == commodity.id
    ).order_by(PriceData.date.desc()).first()
    
    if last_price:
        current_price = last_price.close
    else:
        current_price = 3000
    
    # Simulate small daily change
    daily_change = random.uniform(-1.5, 1.5)  # ±1.5% daily
    new_price = current_price * (1 + daily_change / 100)
    
    # Add new price entry
    new_entry = PriceData(
        commodity_id=commodity.id,
        date=datetime.utcnow(),
        open=round(new_price * 0.99, 2),
        close=round(new_price, 2),
        high=round(new_price * 1.01, 2),
        low=round(new_price * 0.98, 2),
    )
    
    db.add(new_entry)
    db.commit()
    
    print(f"✅ Updated {commodity.name}: ₹{new_price:.2f}")

print("\n✅ Daily prices updated!")
db.close()
```

**Setup daily cron job** (Linux/Mac):
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 10 AM
0 10 * * * cd /path/to/backend && python update_prices.py
```

**For Windows**, use Task Scheduler to run the script daily.

---

## PART 3: Statistics Helper Functions

Create **backend/services/price_service.py**:

```python
from sqlalchemy.orm import Session
from models import PriceData, Commodity
from datetime import datetime, timedelta
import statistics

class PriceService:
    @staticmethod
    def get_30day_prices(commodity_id: int, db: Session):
        """Get 30-day price history"""
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        prices = db.query(PriceData).filter(
            PriceData.commodity_id == commodity_id,
            PriceData.date >= thirty_days_ago
        ).order_by(PriceData.date).all()
        return prices
    
    @staticmethod
    def calculate_volatility(prices: list) -> float:
        """Calculate 30-day price volatility (standard deviation)"""
        if len(prices) < 2:
            return 0
        
        closes = [p.close for p in prices]
        returns = [
            ((closes[i] - closes[i-1]) / closes[i-1]) * 100
            for i in range(1, len(closes))
        ]
        
        if len(returns) < 2:
            return 0
        
        volatility = statistics.stdev(returns)
        return round(volatility, 2)
    
    @staticmethod
    def calculate_trend(prices: list) -> dict:
        """Calculate price trend"""
        if len(prices) < 2:
            return {"trend": "neutral", "change_percent": 0}
        
        first_price = prices[0].close
        last_price = prices[-1].close
        change = ((last_price - first_price) / first_price) * 100
        
        if change > 2:
            trend = "up"
        elif change < -2:
            trend = "down"
        else:
            trend = "neutral"
        
        return {"trend": trend, "change_percent": round(change, 2)}
    
    @staticmethod
    def get_statistics(commodity_id: int, db: Session) -> dict:
        """Get all price statistics"""
        prices = PriceService.get_30day_prices(commodity_id, db)
        
        if not prices:
            return None
        
        closes = [p.close for p in prices]
        
        return {
            "current_price": round(prices[-1].close, 2),
            "high_30day": round(max(closes), 2),
            "low_30day": round(min(closes), 2),
            "avg_30day": round(statistics.mean(closes), 2),
            "volatility": PriceService.calculate_volatility(prices),
            "trend": PriceService.calculate_trend(prices),
        }
```

---

## PART 4: Update API Endpoints

Update **backend/routes/commodities.py**:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Commodity, PriceData
from services.price_service import PriceService
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/commodities", tags=["commodities"])

@router.get("/")
def list_commodities(db: Session = Depends(get_db)):
    """Get all commodities with current stats"""
    commodities = db.query(Commodity).all()
    
    result = []
    for commodity in commodities:
        stats = PriceService.get_statistics(commodity.id, db)
        result.append({
            "id": commodity.id,
            "name": commodity.name,
            "ticker": commodity.ticker,
            "category": commodity.category,
            "stats": stats,
        })
    
    return result

@router.get("/{commodity_id}")
def get_commodity(commodity_id: int, db: Session = Depends(get_db)):
    """Get commodity details"""
    commodity = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Commodity not found")
    
    stats = PriceService.get_statistics(commodity_id, db)
    
    return {
        "id": commodity.id,
        "name": commodity.name,
        "ticker": commodity.ticker,
        "category": commodity.category,
        "stats": stats,
    }

@router.get("/{commodity_id}/prices")
def get_prices_30days(commodity_id: int, db: Session = Depends(get_db)):
    """Get 30-day price data"""
    prices = PriceService.get_30day_prices(commodity_id, db)
    
    return [
        {
            "date": p.date.isoformat(),
            "open": p.open,
            "close": p.close,
            "high": p.high,
            "low": p.low,
        }
        for p in prices
    ]

@router.get("/{commodity_id}/statistics")
def get_price_statistics(commodity_id: int, db: Session = Depends(get_db)):
    """Get price statistics"""
    stats = PriceService.get_statistics(commodity_id, db)
    if not stats:
        raise HTTPException(status_code=404, detail="No price data found")
    return stats
```

---

## TESTING THE DATA LAYER

```bash
# Start backend
python main.py

# In another terminal, test the API
curl http://localhost:8000/api/commodities/

# Should return all commodities with current prices
```

---

## YOU'RE NOW READY FOR DAY 2

After Day 1, you'll have:
✅ Real sample data (2 years of historical prices)
✅ API endpoints returning price data
✅ Statistics calculation functions
✅ Foundation for building the dashboard

**Next: Day 2 - Build the Commodity Dashboard**
