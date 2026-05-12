# Day 2 Action Plan - Commodity Dashboard with Charts

## YOUR GOAL TODAY: Visual Dashboard is Live

By end of Day 2, you'll have:
- ✅ Price chart component showing 30-day trends
- ✅ Commodity cards with current price + change %
- ✅ Real data flowing from backend to frontend
- ✅ Mobile-responsive design
- ✅ Interactive charts (click to view more details)

**Time Estimate**: 5-6 hours

---

## PART 1: Backend - Enhanced Price Endpoints (1 hour)

### 1.1 Create Chart Data Formatter

Create **backend/services/chart_service.py**:

```python
from sqlalchemy.orm import Session
from models import PriceData
from datetime import datetime, timedelta
from services.price_service import PriceService

class ChartService:
    @staticmethod
    def get_chart_data(commodity_id: int, db: Session, days: int = 30):
        """
        Format price data for chart.js / recharts
        Returns array of {date, open, close, high, low}
        """
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        prices = db.query(PriceData).filter(
            PriceData.commodity_id == commodity_id,
            PriceData.date >= cutoff_date
        ).order_by(PriceData.date).all()
        
        chart_data = []
        for price in prices:
            chart_data.append({
                "date": price.date.strftime("%Y-%m-%d"),
                "timestamp": price.date.isoformat(),
                "open": round(price.open, 2),
                "close": round(price.close, 2),
                "high": round(price.high, 2),
                "low": round(price.low, 2),
            })
        
        return chart_data
    
    @staticmethod
    def get_candlestick_data(commodity_id: int, db: Session, days: int = 30):
        """
        Format data for candlestick charts
        """
        return ChartService.get_chart_data(commodity_id, db, days)
    
    @staticmethod
    def get_summary_with_chart(commodity_id: int, db: Session):
        """
        Get complete data: summary + chart data
        """
        chart_data = ChartService.get_chart_data(commodity_id, db)
        stats = PriceService.get_statistics(commodity_id, db)
        
        return {
            "chart": chart_data,
            "stats": stats,
        }
```

### 1.2 Add Chart Endpoint to API

Update **backend/routes/commodities.py**:

```python
@router.get("/{commodity_id}/chart")
def get_commodity_chart(commodity_id: int, days: int = 30, db: Session = Depends(get_db)):
    """Get chart data with statistics"""
    from services.chart_service import ChartService
    
    commodity = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Commodity not found")
    
    data = ChartService.get_summary_with_chart(commodity_id, db)
    
    return {
        "commodity": {
            "id": commodity.id,
            "name": commodity.name,
            "ticker": commodity.ticker,
        },
        "data": data,
    }
```

### 1.3 Test the Endpoint

```bash
# Backend should still be running
curl http://localhost:8000/api/commodities/1/chart
# Returns chart data for commodity ID 1
```

---

## PART 2: Frontend - Install Chart Library (30 minutes)

### 2.1 Install Dependencies

```bash
cd frontend

# Install Recharts (React charting library)
npm install recharts

# Install axios for better API calls
npm install axios

# Install lucide-react for icons
npm install lucide-react
```

### 2.2 Create API Service

Create **frontend/src/services/commodityService.ts**:

```typescript
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const commodityService = {
  // Get all commodities with current prices
  async getAllCommodities() {
    const response = await apiClient.get('/api/commodities/');
    return response.data;
  },

  // Get single commodity with details
  async getCommodity(id: number) {
    const response = await apiClient.get(`/api/commodities/${id}`);
    return response.data;
  },

  // Get chart data for a commodity
  async getChartData(id: number, days: number = 30) {
    const response = await apiClient.get(`/api/commodities/${id}/chart?days=${days}`);
    return response.data;
  },

  // Get price statistics
  async getStatistics(id: number) {
    const response = await apiClient.get(`/api/commodities/${id}/statistics`);
    return response.data;
  },
};
```

---

## PART 3: Frontend - Build Chart Components (2 hours)

### 3.1 Create Commodity Card Component

Create **frontend/src/components/CommodityCard.tsx**:

```typescript
import React from 'react';
import { ArrowUp, ArrowDown } from 'lucide-react';

interface CommodityCardProps {
  name: string;
  ticker: string;
  currentPrice: number;
  changePercent: number;
  onClick?: () => void;
}

export const CommodityCard: React.FC<CommodityCardProps> = ({
  name,
  ticker,
  currentPrice,
  changePercent,
  onClick,
}) => {
  const isPositive = changePercent >= 0;
  const colorClass = isPositive ? 'text-green-600' : 'text-red-600';

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg shadow p-4 cursor-pointer hover:shadow-lg transition"
    >
      <div className="flex justify-between items-start mb-2">
        <div>
          <h3 className="font-bold text-lg">{name}</h3>
          <p className="text-xs text-gray-500">{ticker}</p>
        </div>
      </div>

      <p className="text-2xl font-bold text-gray-800 mb-2">
        ₹{currentPrice.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
      </p>

      <div className={`flex items-center gap-1 ${colorClass} text-sm font-semibold`}>
        {isPositive ? (
          <ArrowUp size={16} />
        ) : (
          <ArrowDown size={16} />
        )}
        <span>{Math.abs(changePercent).toFixed(2)}% (7 days)</span>
      </div>
    </div>
  );
};
```

### 3.2 Create Price Chart Component

Create **frontend/src/components/PriceChart.tsx**:

```typescript
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface ChartDataPoint {
  date: string;
  open: number;
  close: number;
  high: number;
  low: number;
}

interface PriceChartProps {
  data: ChartDataPoint[];
  height?: number;
}

export const PriceChart: React.FC<PriceChartProps> = ({ data, height = 300 }) => {
  if (!data || data.length === 0) {
    return <div className="text-center py-8">No data available</div>;
  }

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="date"
          tick={{ fontSize: 12 }}
          interval={Math.floor(data.length / 6)}
        />
        <YAxis />
        <Tooltip
          formatter={(value: number) => `₹${value.toFixed(2)}`}
          labelFormatter={(label: string) => `Date: ${label}`}
        />
        <Legend />
        
        {/* Close price line (main indicator) */}
        <Line
          type="monotone"
          dataKey="close"
          stroke="#10b981"
          dot={false}
          name="Close Price"
          isAnimationActive={false}
        />
        
        {/* High/Low range (optional) */}
        <Line
          type="monotone"
          dataKey="high"
          stroke="#d1d5db"
          dot={false}
          name="High"
          strokeDasharray="5 5"
          isAnimationActive={false}
        />
        <Line
          type="monotone"
          dataKey="low"
          stroke="#d1d5db"
          dot={false}
          name="Low"
          strokeDasharray="5 5"
          isAnimationActive={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
```

### 3.3 Create Statistics Panel Component

Create **frontend/src/components/StatisticsPanel.tsx**:

```typescript
import React from 'react';

interface Stats {
  current_price: number;
  high_30day: number;
  low_30day: number;
  avg_30day: number;
  volatility: number;
  trend: {
    trend: string;
    change_percent: number;
  };
}

interface StatisticsPanelProps {
  stats: Stats;
}

export const StatisticsPanel: React.FC<StatisticsPanelProps> = ({ stats }) => {
  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up':
        return 'text-green-600';
      case 'down':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-4 bg-white rounded-lg shadow p-6">
      <StatItem label="Current Price" value={`₹${stats.current_price}`} />
      
      <StatItem label="30-Day High" value={`₹${stats.high_30day.toFixed(0)}`} />
      
      <StatItem label="30-Day Low" value={`₹${stats.low_30day.toFixed(0)}`} />
      
      <StatItem label="30-Day Avg" value={`₹${stats.avg_30day.toFixed(0)}`} />
      
      <StatItem label="Volatility" value={`${stats.volatility.toFixed(2)}%`} />
      
      <div className="text-center">
        <p className="text-sm text-gray-600 mb-1">30-Day Trend</p>
        <p className={`text-lg font-bold ${getTrendColor(stats.trend.trend)}`}>
          {stats.trend.trend === 'up' ? '↑' : stats.trend.trend === 'down' ? '↓' : '→'}
          {' '}
          {Math.abs(stats.trend.change_percent).toFixed(2)}%
        </p>
      </div>
    </div>
  );
};

const StatItem: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="text-center">
    <p className="text-sm text-gray-600 mb-1">{label}</p>
    <p className="text-lg font-bold text-gray-800">{value}</p>
  </div>
);
```

---

## PART 4: Frontend - Update Dashboard (2 hours)

### 4.1 Update Dashboard Page

Update **frontend/src/app/dashboard/page.tsx**:

```typescript
'use client';

import { useEffect, useState } from 'react';
import { commodityService } from '@/services/commodityService';
import { CommodityCard } from '@/components/CommodityCard';
import { PriceChart } from '@/components/PriceChart';
import { StatisticsPanel } from '@/components/StatisticsPanel';
import { Loader } from 'lucide-react';

interface ChartDataPoint {
  date: string;
  open: number;
  close: number;
  high: number;
  low: number;
}

interface Stats {
  current_price: number;
  high_30day: number;
  low_30day: number;
  avg_30day: number;
  volatility: number;
  trend: {
    trend: string;
    change_percent: number;
  };
}

interface Commodity {
  id: number;
  name: string;
  ticker: string;
  category: string;
  stats: Stats;
}

export default function Dashboard() {
  const [commodities, setCommodities] = useState<Commodity[]>([]);
  const [selectedCommodity, setSelectedCommodity] = useState<Commodity | null>(null);
  const [chartData, setChartData] = useState<ChartDataPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load all commodities on mount
  useEffect(() => {
    const loadCommodities = async () => {
      try {
        setLoading(true);
        const data = await commodityService.getAllCommodities();
        setCommodities(data);
        
        if (data.length > 0) {
          setSelectedCommodity(data[0]);
          await loadChartData(data[0].id);
        }
      } catch (err) {
        setError('Failed to load commodities');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadCommodities();
  }, []);

  // Load chart data when commodity is selected
  const loadChartData = async (commodityId: number) => {
    try {
      const data = await commodityService.getChartData(commodityId);
      setChartData(data.data.chart);
    } catch (err) {
      console.error('Failed to load chart data:', err);
    }
  };

  const handleSelectCommodity = (commodity: Commodity) => {
    setSelectedCommodity(commodity);
    loadChartData(commodity.id);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader className="animate-spin" size={40} />
      </div>
    );
  }

  if (error) {
    return <div className="text-red-600 text-center">{error}</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Commodity Intelligence Dashboard</h1>
        <p className="text-gray-600">Real-time market prices and AI-powered insights</p>
      </div>

      {/* Commodity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {commodities.map((commodity) => (
          <div
            key={commodity.id}
            onClick={() => handleSelectCommodity(commodity)}
            className={`cursor-pointer transition ${
              selectedCommodity?.id === commodity.id
                ? 'ring-2 ring-green-600'
                : ''
            }`}
          >
            <CommodityCard
              name={commodity.name}
              ticker={commodity.ticker}
              currentPrice={commodity.stats.current_price}
              changePercent={commodity.stats.trend.change_percent}
            />
          </div>
        ))}
      </div>

      {/* Selected Commodity Details */}
      {selectedCommodity && selectedCommodity.stats && (
        <div className="space-y-6">
          {/* Statistics Panel */}
          <StatisticsPanel stats={selectedCommodity.stats} />

          {/* Chart */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">
              {selectedCommodity.name} - 30-Day Price Trend
            </h2>
            <PriceChart data={chartData} height={400} />
          </div>

          {/* Additional Info */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              <strong>💡 Tip:</strong> Click on any commodity card above to view its detailed
              price history and statistics.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
```

### 4.2 Fix CORS Issue (If Needed)

If you get CORS errors, update **backend/main.py**:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## PART 5: Testing (30 minutes)

### 5.1 Start Both Services

```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 5.2 Test the Dashboard

1. Visit `http://localhost:3000/dashboard`
2. You should see:
   - 5 commodity cards (Rice, Wheat, Cotton, Sugar, Spices)
   - Current prices from database
   - Trend arrows and percentage changes
   - Click on a card to see:
     - 30-day price chart
     - Statistics (high, low, avg, volatility)
     - Trend analysis

### 5.3 Common Issues & Fixes

**Issue**: "Failed to load commodities"
**Fix**: Check backend is running on `http://localhost:8000`

**Issue**: CORS errors in console
**Fix**: Update CORS middleware in `backend/main.py`

**Issue**: Chart is empty
**Fix**: Run `python generate_sample_data.py` to populate prices

**Issue**: Types/compilation errors
**Fix**: Run `npm install` to ensure all dependencies are installed

---

## CHECKLIST FOR END OF DAY 2

- [ ] Price chart component created and working
- [ ] Commodity cards showing current prices
- [ ] Statistics panel showing high/low/avg/volatility
- [ ] Click on commodity to view its chart
- [ ] Chart displays 30-day price history
- [ ] Responsive design (works on mobile)
- [ ] Frontend fetching data from backend API
- [ ] No CORS errors in console
- [ ] Deployed to Vercel (same URL as before)

---

## WHAT YOU'LL SEE

Beautiful dashboard like this:

```
┌─────────────────────────────────────────────────────┐
│ Commodity Intelligence Dashboard                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Rice ₹3,200 ↑2.5%] [Wheat ₹2,100 ↑1.2%] ...   │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │ Current: ₹3,200  High: ₹3,450  Low: ₹3,100 │  │
│  │ 30-day Avg: ₹3,250  Volatility: 4.2%       │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │         [Price Chart - 30 Days]             │  │
│  │  ₹3500 ┐                                    │  │
│  │  ₹3400 ├──┐                                 │  │
│  │  ₹3300 ├──┴──┐                              │  │
│  │  ₹3200 ┴─────┘                              │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## NEXT: Day 3

Tomorrow you'll:
- Build risk alert system
- Implement risk scoring algorithm
- Create alert dashboard

**See WEEK_BY_WEEK_ROADMAP.md Day 3 section for details**
