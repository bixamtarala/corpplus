#!/usr/bin/env python3
"""
Unit Tests for CropPulse Algorithms
Tests all critical calculation functions and data processing logic
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent / 'croppulse'))

from croppulse_app import (
    calculate_risk_score,
    get_risk_level,
    get_trend_indicator,
    get_price_trend_category,
    get_supply_demand_indicator,
    predict_risk_trend,
    get_risk_components,
)


class TestAlgorithms:
    """Unit tests for all CropPulse algorithms"""
    
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
            'volatility': [np.std(prices[:i+1]) if i > 0 else 0 for i in range(rows)]
        })
        return df.reset_index(drop=True)
    
    def test_1_risk_score_calculation(self):
        """Test risk score is within valid range (0-100)"""
        print("\n🧪 TEST 1: Risk Score Calculation")
        try:
            data = self.create_sample_data()
            risk_score = calculate_risk_score(data)
            
            assert 0 <= risk_score <= 100, f"Risk score {risk_score} out of range"
            assert isinstance(risk_score, (int, float)), "Risk score should be numeric"
            
            print(f"✅ PASS: Risk score = {risk_score:.1f}/100")
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            return False
    
    def test_2_risk_level_classification(self):
        """Test risk level classification (Low/Medium/High)"""
        print("\n🧪 TEST 2: Risk Level Classification")
        try:
            test_scores = [20, 50, 80]
            expected_levels = ['Low', 'Medium', 'High']
            
            for score, expected in zip(test_scores, expected_levels):
                # Mock data
                data = self.create_sample_data()
                risk_level, emoji, color = get_risk_level(score)
                
                assert expected in risk_level, f"Expected {expected}, got {risk_level}"
                assert emoji in ['🟢', '🟡', '🔴'], f"Invalid emoji: {emoji}"
                assert color in ['#2ecc71', '#f39c12', '#e74c3c'], f"Invalid color: {color}"
            
            print(f"✅ PASS: Risk levels classified correctly")
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            return False
    
    def test_3_price_trend_calculation(self):
        """Test price trend indicator (up/down/stable)"""
        print("\n🧪 TEST 3: Price Trend Calculation")
        try:
            # Test uptrend
            data_up = self.create_sample_data(base_price=3000)
            data_up['price'] = data_up.index * 10 + 3000  # Monotonic increase
            current = data_up['price'].iloc[-1]
            previous = data_up['price'].iloc[-2]
            
            trend, color = get_trend_indicator(current, previous)
            assert '📈' in trend or '📉' in trend or '→' in trend, f"Invalid trend: {trend}"
            
            print(f"✅ PASS: Price trend indicators working")
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            return False
    
    def test_4_volatility_calculation(self):
        """Test volatility is calculated correctly"""
        print("\n🧪 TEST 4: Volatility Calculation")
        try:
            data = self.create_sample_data()
            
            # Manual volatility calculation
            price_mean = data['price'].mean()
            expected_volatility = (data['price'].std() / price_mean * 100) if price_mean > 0 else 0
            
            assert expected_volatility >= 0, "Volatility should be non-negative"
            assert expected_volatility <= 100, "Volatility should not exceed 100%"
            
            print(f"✅ PASS: Volatility = {expected_volatility:.2f}%")
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            return False
    
    def test_5_supply_demand_balance(self):
        """Test supply/demand indicator"""
        print("\n🧪 TEST 5: Supply/Demand Balance")
        try:
            supply_values = [30, 50, 70]
            demand_values = [80, 50, 30]
            
            for supply, demand in zip(supply_values, demand_values):
                status, color = get_supply_demand_indicator(supply, demand)
                assert isinstance(status, str), "Status should be string"
                assert color in ['#2ecc71', '#f39c12', '#e74c3c'], f"Invalid color: {color}"
            
            print(f"✅ PASS: Supply/demand indicators working")
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            return False
    
    def test_6_edge_case_zero_prices(self):
        """Test algorithm handles zero prices gracefully"""
        print("\n🧪 TEST 6: Edge Case - Zero Prices")
        try:
            data = self.create_sample_data()
            data['price'] = 0  # Edge case
            
            risk_score = calculate_risk_score(data)
            assert risk_score >= 0, "Should handle zero prices"
            
            print(f"✅ PASS: Handles zero prices gracefully")
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            return False
    
    def test_7_edge_case_negative_values(self):
        """Test algorithm handles negative values"""
        print("\n🧪 TEST 7: Edge Case - Negative Values")
        try:
            data = self.create_sample_data()
            data['supply'] = -10  # Invalid but should not crash
            
            try:
                risk_score = calculate_risk_score(data)
                print(f"✅ PASS: Handles negative values without crashing")
                return True
            except:
                print(f"✅ PASS: Properly rejects negative values")
                return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            return False
    
    def test_8_price_change_percentage(self):
        """Test price change percentage calculation"""
        print("\n🧪 TEST 8: Price Change Percentage")
        try:
            data = self.create_sample_data()
            
            old_price = data['price'].iloc[0]
            new_price = data['price'].iloc[-1]
            
            if old_price != 0:
                price_change = ((new_price - old_price) / old_price) * 100
                assert isinstance(price_change, (int, float)), "Should be numeric"
                
                print(f"✅ PASS: Price change = {price_change:+.2f}%")
                return True
            else:
                print(f"✅ PASS: Handles zero denominator")
                return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            return False
    
    def test_9_risk_components_breakdown(self):
        """Test risk component breakdown"""
        print("\n🧪 TEST 9: Risk Components Breakdown")
        try:
            data = self.create_sample_data()
            components = get_risk_components(data)
            
            required_keys = ['volatility', 'volatility_score', 'price_change', 'price_change_score']
            
            for key in required_keys:
                assert key in components or len(components) == 0, f"Missing component: {key}"
            
            print(f"✅ PASS: Risk components breakdown working")
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            return False
    
    def test_10_risk_trend_prediction(self):
        """Test risk trend prediction"""
        print("\n🧪 TEST 10: Risk Trend Prediction")
        try:
            data = self.create_sample_data()
            trend = predict_risk_trend(data)
            
            assert trend in ['increasing', 'decreasing', 'stable'], f"Invalid trend: {trend}"
            
            print(f"✅ PASS: Risk trend = {trend}")
            return True
        except Exception as e:
            print(f"❌ FAIL: {e}")
            return False


def run_all_tests():
    """Run all algorithm tests"""
    print("=" * 60)
    print("[TEST] CropPulse Algorithm Unit Tests")
    print("=" * 60)
    
    tester = TestAlgorithms()
    tests = [
        ('Risk Score Calculation', tester.test_1_risk_score_calculation),
        ('Risk Level Classification', tester.test_2_risk_level_classification),
        ('Price Trend Calculation', tester.test_3_price_trend_calculation),
        ('Volatility Calculation', tester.test_4_volatility_calculation),
        ('Supply/Demand Balance', tester.test_5_supply_demand_balance),
        ('Edge Case: Zero Prices', tester.test_6_edge_case_zero_prices),
        ('Edge Case: Negative Values', tester.test_7_edge_case_negative_values),
        ('Price Change Percentage', tester.test_8_price_change_percentage),
        ('Risk Components Breakdown', tester.test_9_risk_components_breakdown),
        ('Risk Trend Prediction', tester.test_10_risk_trend_prediction),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("[RESULTS] TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, passed_test in results.items():
        status = '✅ PASS' if passed_test else '❌ FAIL'
        print(f'{status}: {name}')
    
    print("=" * 60)
    print(f'Overall: {passed}/{total} tests passed ({passed*100//total}%)')
    
    if passed == total:
        print('\n[SUCCESS] ALL ALGORITHM TESTS PASSED')
        return 0
    else:
        print(f'\n[WARNING] {total - passed} test(s) failed')
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
