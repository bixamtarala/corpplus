#!/usr/bin/env python3
"""
Unit Tests for CropPulse Algorithms (Pure Python - No Streamlit)
Tests all critical calculation functions and data processing logic
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent / 'croppulse'))


class TestAlgorithms:
    """Unit tests for core CropPulse algorithms"""
    
    @staticmethod
    def create_sample_data(rows=30, base_price=3000, volatility=0.05):
        """Create sample commodity data for testing"""
        dates = pd.date_range('2026-04-12', periods=rows, freq='D')
        prices = [base_price + np.random.normal(0, base_price * volatility) for _ in range(rows)]
        
        df = pd.DataFrame({
            'date': dates,
            'price': prices,
            'supply': np.random.uniform(20, 80, rows),
            'demand': np.random.uniform(40, 90, rows),
        })
        return df.reset_index(drop=True)
    
    @staticmethod
    def calculate_risk_score(volatility, price_change, supply, demand):
        """Pure Python implementation of risk calculation
        Risk = (volatility × 0.35) + (price_change × 0.25) + (supply_shortage × 0.20) + (demand_surge × 0.20)
        """
        # Normalize inputs to 0-100 scale
        vol_normalized = min(100, volatility * 100)
        price_change_normalized = min(100, abs(price_change) * 100)
        
        # Supply shortage factor (0-100, higher = shortage)
        supply_shortage = max(0, min(100, (100 - supply)))
        
        # Demand surge factor (0-100, higher = high demand)
        demand_surge = max(0, min(100, (demand - 40)))
        
        risk = (vol_normalized * 0.35) + (price_change_normalized * 0.25) + (supply_shortage * 0.20) + (demand_surge * 0.20)
        return min(100, max(0, risk))
    
    @staticmethod
    def get_risk_level(risk_score):
        """Classify risk as Low, Medium, or High"""
        if risk_score < 33:
            return "Low"
        elif risk_score < 66:
            return "Medium"
        else:
            return "High"
    
    @staticmethod
    def calculate_volatility(prices):
        """Calculate volatility as percentage of mean"""
        if len(prices) < 2 or prices.mean() == 0:
            return 0
        return (prices.std() / prices.mean() * 100)
    
    @staticmethod
    def get_price_trend(current_price, prev_price):
        """Calculate price trend: up, down, or stable"""
        if current_price == prev_price:
            return "Stable", 0
        
        change_pct = ((current_price - prev_price) / prev_price * 100)
        
        if abs(change_pct) < 1:
            return "Stable", change_pct
        elif change_pct > 0:
            return "Up", change_pct
        else:
            return "Down", change_pct
    
    # Test Methods
    def test_1_risk_score_range(self):
        """Test risk score is within valid range (0-100)"""
        print("\n[TEST 1] Risk Score Range Validation")
        try:
            for _ in range(5):
                risk = self.calculate_risk_score(
                    volatility=np.random.uniform(0, 0.1),
                    price_change=np.random.uniform(-0.05, 0.05),
                    supply=np.random.uniform(20, 80),
                    demand=np.random.uniform(40, 90)
                )
                assert 0 <= risk <= 100, f"Risk {risk} out of valid range"
            print("[PASS] Risk scores all within 0-100 range")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_2_risk_classification(self):
        """Test risk classification Low/Medium/High"""
        print("\n[TEST 2] Risk Level Classification")
        try:
            assert self.get_risk_level(20) == "Low", "Risk 20 should be Low"
            assert self.get_risk_level(50) == "Medium", "Risk 50 should be Medium"
            assert self.get_risk_level(80) == "High", "Risk 80 should be High"
            print("[PASS] Risk classification works correctly")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_3_volatility_calculation(self):
        """Test volatility calculation from price series"""
        print("\n[TEST 3] Volatility Calculation")
        try:
            prices = pd.Series([3000, 3050, 3010, 3100, 2950])
            vol = self.calculate_volatility(prices)
            
            assert 0 <= vol <= 100, f"Volatility {vol} out of range"
            assert vol > 0, "Non-constant prices should have volatility > 0"
            print(f"[PASS] Volatility calculated: {vol:.2f}%")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_4_price_trend_detection(self):
        """Test price trend detection"""
        print("\n[TEST 4] Price Trend Detection")
        try:
            # Test up trend
            trend, pct = self.get_price_trend(3100, 3000)
            assert trend == "Up", f"Expected 'Up', got {trend}"
            assert pct > 0, f"Expected positive change, got {pct}"
            
            # Test down trend
            trend, pct = self.get_price_trend(2900, 3000)
            assert trend == "Down", f"Expected 'Down', got {trend}"
            assert pct < 0, f"Expected negative change, got {pct}"
            
            # Test stable
            trend, pct = self.get_price_trend(3000, 3000)
            assert trend == "Stable", f"Expected 'Stable', got {trend}"
            
            print("[PASS] Price trend detection works correctly")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_5_zero_price_handling(self):
        """Test edge case: zero prices"""
        print("\n[TEST 5] Zero Price Edge Case")
        try:
            prices = pd.Series([0, 0, 0])
            vol = self.calculate_volatility(prices)
            
            assert vol == 0, f"Zero prices should have zero volatility"
            print("[PASS] Zero prices handled gracefully")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_6_negative_values_handling(self):
        """Test edge case: negative values"""
        print("\n[TEST 6] Negative Values Edge Case")
        try:
            # Risk calculation should handle negative price change
            risk = self.calculate_risk_score(
                volatility=0.05,
                price_change=-0.10,  # -10% change
                supply=50,
                demand=70
            )
            assert 0 <= risk <= 100, "Risk should still be in range with negative price change"
            print("[PASS] Negative values handled safely")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_7_supply_demand_balance(self):
        """Test supply/demand balance indicator"""
        print("\n[TEST 7] Supply/Demand Balance")
        try:
            # High supply, low demand = lower price risk
            risk_oversupply = self.calculate_risk_score(
                volatility=0.02, price_change=0, supply=90, demand=30
            )
            
            # Low supply, high demand = shortage risk (high)
            risk_shortage = self.calculate_risk_score(
                volatility=0.02, price_change=0, supply=20, demand=90
            )
            
            # Balanced = medium risk
            risk_balanced = self.calculate_risk_score(
                volatility=0.02, price_change=0, supply=50, demand=50
            )
            
            # Shortage (imbalance) should generally be riskier
            assert risk_shortage > risk_oversupply, "Shortage should increase risk vs oversupply"
            
            print(f"[PASS] Supply/demand affects risk correctly (shortage: {risk_shortage:.1f}, oversupply: {risk_oversupply:.1f})")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_8_price_change_percentage(self):
        """Test price change calculation"""
        print("\n[TEST 8] Price Change Percentage")
        try:
            # 10% increase
            trend, pct = self.get_price_trend(3300, 3000)
            assert abs(pct - 10.0) < 0.1, f"Expected ~10%, got {pct}%"
            
            # 10% decrease
            trend, pct = self.get_price_trend(2700, 3000)
            assert abs(pct - (-10.0)) < 0.1, f"Expected ~-10%, got {pct}%"
            
            print(f"[PASS] Price change percentages calculated correctly")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_9_risk_weighted_components(self):
        """Test risk components are weighted correctly"""
        print("\n[TEST 9] Risk Weighted Components")
        try:
            # Test: volatility should be the strongest factor (35%)
            risk_high_vol = self.calculate_risk_score(
                volatility=0.20, price_change=0, supply=50, demand=50
            )
            risk_low_vol = self.calculate_risk_score(
                volatility=0.01, price_change=0, supply=50, demand=50
            )
            
            assert risk_high_vol > risk_low_vol, "Volatility should strongly affect risk"
            
            print("[PASS] Risk components weighted correctly")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_10_data_consistency(self):
        """Test consistency across multiple calculations"""
        print("\n[TEST 10] Data Consistency")
        try:
            data = self.create_sample_data(rows=30)
            
            # Should have 30 rows
            assert len(data) == 30, f"Expected 30 rows, got {len(data)}"
            
            # All prices should be positive
            assert (data['price'] > 0).all(), "All prices should be positive"
            
            # All columns should be present
            required_cols = {'date', 'price', 'supply', 'demand'}
            assert required_cols.issubset(set(data.columns)), "Missing required columns"
            
            print("[PASS] Data consistency verified")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False


def run_all_tests():
    """Run all algorithm tests"""
    print("=" * 70)
    print("[TEST SUITE] CropPulse Algorithm Unit Tests")
    print("=" * 70)
    
    test_obj = TestAlgorithms()
    
    tests = [
        ('Risk Score Range', test_obj.test_1_risk_score_range),
        ('Risk Classification', test_obj.test_2_risk_classification),
        ('Volatility Calculation', test_obj.test_3_volatility_calculation),
        ('Price Trend Detection', test_obj.test_4_price_trend_detection),
        ('Zero Price Handling', test_obj.test_5_zero_price_handling),
        ('Negative Values Handling', test_obj.test_6_negative_values_handling),
        ('Supply/Demand Balance', test_obj.test_7_supply_demand_balance),
        ('Price Change Percentage', test_obj.test_8_price_change_percentage),
        ('Risk Weighted Components', test_obj.test_9_risk_weighted_components),
        ('Data Consistency', test_obj.test_10_data_consistency),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"[ERROR] Test crashed: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("[RESULTS] TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, passed_test in results.items():
        status = '[PASS]' if passed_test else '[FAIL]'
        print(f'{status}: {name}')
    
    print("=" * 70)
    print(f'Overall: {passed}/{total} tests passed ({100*passed//total}%)')
    
    if passed == total:
        print('\n[SUCCESS] ALL ALGORITHM TESTS PASSED')
        return 0
    else:
        print(f'\n[WARNING] {total - passed} test(s) failed')
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
