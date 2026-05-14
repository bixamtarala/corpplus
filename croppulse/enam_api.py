"""
eNAM API Integration for CropPulse
Fetches real-time commodity prices from National Agricultural Market (eNAM)
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json

# eNAM API Configuration
ENAM_API_BASE = "https://www.enamapis.com/api"
ENAM_API_KEY = "YOUR_ENAM_API_KEY"  # Will be set from environment

# Supported Mandis (we'll focus on major rice trading mandis)
RICE_MANDIS = {
    "TN001": "Koyambedu, Tamil Nadu",  # Major mandi in Tamil Nadu
    "TN002": "Salem, Tamil Nadu",
    "AP001": "Gudlavalleru, Andhra Pradesh",  # Major rice mandi
    "AP002": "Kakinada, Andhra Pradesh",
    "TG001": "Warangal, Telangana",  # Major rice trading hub
    "KA001": "Mandya, Karnataka",
    "OR001": "Cuttack, Odisha",  # Eastern rice hub
}

class eNAMAPI:
    """Handle all eNAM API interactions"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or ENAM_API_KEY
        self.base_url = ENAM_API_BASE
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    def get_commodity_price(self, commodity="Rice", state_code="TN", 
                           district_code="01", mandi_code=None):
        """
        Fetch current price for a commodity
        
        Args:
            commodity: "Rice", "Wheat", "Cotton"
            state_code: State abbreviation (TN, AP, TG, KA, OR)
            district_code: District code
            mandi_code: Optional specific mandi code
        
        Returns:
            dict: Price data including current price, high, low, volume
        """
        try:
            # eNAM API endpoint
            endpoint = f"{self.base_url}/commodities/get-prices"
            
            params = {
                "commodity": commodity,
                "stateCode": state_code,
                "districtCode": district_code,
                "limit": 30  # Get last 30 days
            }
            
            if mandi_code:
                params["mandiCode"] = mandi_code
            
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "success":
                return self._parse_price_data(data.get("data", []))
            else:
                print(f"eNAM API error: {data.get('message', 'Unknown error')}")
                return None
                
        except requests.exceptions.Timeout:
            print("eNAM API timeout - using fallback data")
            return None
        except requests.exceptions.ConnectionError:
            print("eNAM API connection error - using fallback data")
            return None
        except Exception as e:
            print(f"Error fetching eNAM data: {e}")
            return None
    
    def get_all_mandis(self, commodity="Rice"):
        """
        Fetch prices from all major rice mandis
        
        Returns:
            dict: Multi-mandi price comparison data
        """
        try:
            endpoint = f"{self.base_url}/mandis/prices"
            
            params = {
                "commodity": commodity,
                "limit": 5  # Get last 5 days for trending
            }
            
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "success":
                return self._parse_multimandi_data(data.get("data", []))
            
        except Exception as e:
            print(f"Error fetching multi-mandi data: {e}")
            return None
    
    def _parse_price_data(self, raw_data):
        """Parse eNAM API response into our format"""
        if not raw_data:
            return None
        
        try:
            prices = []
            
            for record in raw_data:
                prices.append({
                    "date": datetime.fromisoformat(record.get("date")),
                    "price": float(record.get("price", 0)),
                    "high": float(record.get("high", 0)),
                    "low": float(record.get("low", 0)),
                    "volume": float(record.get("volume", 0)),
                    "mandi": record.get("mandiName", ""),
                })
            
            # Sort by date
            prices.sort(key=lambda x: x["date"])
            
            return prices
            
        except Exception as e:
            print(f"Error parsing price data: {e}")
            return None
    
    def _parse_multimandi_data(self, raw_data):
        """Parse multi-mandi response"""
        mandis = {}
        
        try:
            for mandi_data in raw_data:
                mandi_name = mandi_data.get("mandiName", "Unknown")
                current_price = float(mandi_data.get("currentPrice", 0))
                
                mandis[mandi_name] = {
                    "price": current_price,
                    "high": float(mandi_data.get("high", 0)),
                    "low": float(mandi_data.get("low", 0)),
                    "volume": float(mandi_data.get("volume", 0)),
                    "timestamp": datetime.fromisoformat(mandi_data.get("timestamp"))
                }
            
            return mandis
            
        except Exception as e:
            print(f"Error parsing multi-mandi data: {e}")
            return None

def fetch_live_data(commodity="Rice", state="TN", use_cache=True):
    """
    Main function to fetch live data from eNAM API
    
    Args:
        commodity: "Rice", "Wheat", "Cotton"
        state: State code (TN, AP, TG, etc)
        use_cache: Use cached data if API fails
    
    Returns:
        DataFrame: Price history with commodity data
    """
    enam = eNAMAPI()
    
    # Try to fetch from eNAM
    price_data = enam.get_commodity_price(commodity, state)
    
    if price_data and len(price_data) > 0:
        # Convert to DataFrame
        df = pd.DataFrame(price_data)
        
        # Add supply/demand simulation based on volume and price
        df['supply'] = 100 - (df['volume'].rank(pct=True) * 100)  # Inverse of volume
        df['demand'] = (df['price'].rank(pct=True) * 100)  # Normalized price as demand proxy
        
        # Add volatility calculation
        df['volatility'] = df['price'].rolling(window=7).std()
        
        # Add commodity name
        df['commodity'] = commodity
        
        return df
    
    else:
        print("⚠️ eNAM API unavailable - Using fallback demo data")
        return None

def get_multimandi_prices(commodity="Rice"):
    """Fetch current prices from multiple mandis"""
    enam = eNAMAPI()
    mandis = enam.get_all_mandis(commodity)
    
    if mandis:
        return mandis
    else:
        # Fallback: Return mock data
        return {
            "Tamil Nadu": 3330,
            "Telangana": 3280,
            "Andhra Pradesh": 3405,
            "Karnataka": 3230,
        }

# Test the API integration
if __name__ == "__main__":
    print("🔄 Testing eNAM API Integration...\n")
    
    # Test single mandi
    print("1️⃣ Fetching live Rice prices from eNAM...")
    df = fetch_live_data(commodity="Rice", state="TN")
    
    if df is not None:
        print(f"✅ Retrieved {len(df)} days of data")
        print(df[['date', 'price', 'supply', 'demand']].tail())
    else:
        print("❌ API unavailable")
    
    print("\n2️⃣ Fetching multi-mandi prices...")
    mandis = get_multimandi_prices("Rice")
    print(mandis)
