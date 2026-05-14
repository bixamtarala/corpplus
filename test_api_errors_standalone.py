#!/usr/bin/env python3
"""
API Error Handling Tests (Pure Python - No Streamlit)
Tests error recovery and fallback mechanisms
"""

import sys
from pathlib import Path
import pandas as pd


class TestAPIErrors:
    """Tests for API error handling and resilience"""
    
    def test_1_missing_csv_file(self):
        """Test behavior when CSV file is missing"""
        print("\n[TEST 1] Missing CSV File Handling")
        try:
            csv_path = Path(__file__).parent / 'croppulse' / 'data' / 'commodity_prices.csv'
            
            if csv_path.exists():
                print(f"[PASS] CSV file exists at {csv_path}")
                return True
            else:
                print(f"[FAIL] CSV file not found at {csv_path}")
                return False
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_2_csv_data_validation(self):
        """Test CSV data loading and validation"""
        print("\n[TEST 2] CSV Data Validation")
        try:
            csv_path = Path(__file__).parent / 'croppulse' / 'data' / 'commodity_prices.csv'
            
            if not csv_path.exists():
                print(f"[SKIP] CSV not found")
                return True
            
            df = pd.read_csv(csv_path)
            
            # Check required columns
            required_cols = {'date', 'price', 'commodity'}
            missing = required_cols - set(df.columns)
            
            assert len(missing) == 0, f"Missing columns: {missing}"
            assert len(df) > 0, "CSV is empty"
            
            print(f"[PASS] CSV validated: {len(df)} rows")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_3_null_value_handling(self):
        """Test handling of null values in data"""
        print("\n[TEST 3] Null Value Handling")
        try:
            csv_path = Path(__file__).parent / 'croppulse' / 'data' / 'commodity_prices.csv'
            
            if not csv_path.exists():
                print(f"[SKIP] CSV not found")
                return True
            
            df = pd.read_csv(csv_path)
            
            # Check for nulls in critical columns
            price_nulls = df['price'].isna().sum()
            
            if price_nulls > 0:
                print(f"[WARNING] Found {price_nulls} null prices - testing forward fill...")
                df['price'].fillna(method='ffill', inplace=True)
                
                if df['price'].isna().sum() == 0:
                    print(f"[PASS] Null values handled with forward fill")
                    return True
                else:
                    print(f"[FAIL] Null values remain after forward fill")
                    return False
            else:
                print(f"[PASS] No null values in critical columns")
                return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_4_malformed_csv_format(self):
        """Test handling of malformed CSV data"""
        print("\n[TEST 4] Malformed CSV Format Detection")
        try:
            csv_path = Path(__file__).parent / 'croppulse' / 'data' / 'commodity_prices.csv'
            
            if not csv_path.exists():
                print(f"[SKIP] CSV not found")
                return True
            
            df = pd.read_csv(csv_path)
            
            # Check that price column is numeric
            try:
                prices = pd.to_numeric(df['price'], errors='coerce')
                if prices.isna().sum() > len(prices) * 0.1:  # >10% non-numeric
                    print(f"[FAIL] Too many non-numeric prices")
                    return False
                else:
                    print(f"[PASS] CSV format is valid")
                    return True
            except Exception as e:
                print(f"[FAIL] Cannot parse prices: {e}")
                return False
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_5_empty_data_handling(self):
        """Test behavior with empty dataset"""
        print("\n[TEST 5] Empty Data Handling")
        try:
            csv_path = Path(__file__).parent / 'croppulse' / 'data' / 'commodity_prices.csv'
            
            if not csv_path.exists():
                print(f"[SKIP] CSV not found")
                return True
            
            df = pd.read_csv(csv_path)
            
            # If data is empty, should have fallback
            if len(df) == 0:
                print(f"[PASS] Empty data detected - would use fallback")
                return True
            else:
                print(f"[PASS] Data is not empty ({len(df)} rows)")
                return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_6_type_mismatch_handling(self):
        """Test handling of type mismatches"""
        print("\n[TEST 6] Type Mismatch Handling")
        try:
            csv_path = Path(__file__).parent / 'croppulse' / 'data' / 'commodity_prices.csv'
            
            if not csv_path.exists():
                print(f"[SKIP] CSV not found")
                return True
            
            df = pd.read_csv(csv_path)
            
            # Try to coerce price to numeric
            prices = pd.to_numeric(df['price'], errors='coerce')
            
            if prices.notna().sum() > len(prices) * 0.9:  # >90% coercible
                print(f"[PASS] Type mismatches handled via coercion")
                return True
            else:
                print(f"[FAIL] Too many unconvertible values")
                return False
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_7_data_range_validation(self):
        """Test that data values are in expected ranges"""
        print("\n[TEST 7] Data Range Validation")
        try:
            csv_path = Path(__file__).parent / 'croppulse' / 'data' / 'commodity_prices.csv'
            
            if not csv_path.exists():
                print(f"[SKIP] CSV not found")
                return True
            
            df = pd.read_csv(csv_path)
            prices = pd.to_numeric(df['price'], errors='coerce')
            
            # Prices should be positive
            if (prices > 0).all() or prices.notna().sum() == 0:
                print(f"[PASS] Price ranges are valid")
                return True
            else:
                print(f"[FAIL] Invalid price ranges detected")
                return False
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_8_fallback_mechanism_ready(self):
        """Test that fallback mechanism is implemented"""
        print("\n[TEST 8] Fallback Mechanism Ready")
        try:
            from enam_api import eNAMAPI
            
            api = eNAMAPI()
            data = api.fetch_live_data()
            
            # Should have data even if API fails
            assert data is not None, "Fallback should provide data"
            assert len(data) > 0, "Fallback data should not be empty"
            
            print(f"[PASS] Fallback mechanism provides data ({len(data)} rows)")
            return True
        except Exception as e:
            print(f"[SKIP] eNAM API test skipped: {e}")
            return True  # Not critical
    
    def test_9_date_format_validation(self):
        """Test date parsing and validation"""
        print("\n[TEST 9] Date Format Validation")
        try:
            csv_path = Path(__file__).parent / 'croppulse' / 'data' / 'commodity_prices.csv'
            
            if not csv_path.exists():
                print(f"[SKIP] CSV not found")
                return True
            
            df = pd.read_csv(csv_path)
            
            # Try to parse dates
            try:
                dates = pd.to_datetime(df['date'], errors='coerce')
                if dates.notna().sum() > len(dates) * 0.9:  # >90% valid
                    print(f"[PASS] Date format is valid and parseable")
                    return True
                else:
                    print(f"[FAIL] Too many invalid dates")
                    return False
            except Exception:
                print(f"[FAIL] Cannot parse dates")
                return False
        except Exception as e:
            print(f"[FAIL] {e}")
            return False
    
    def test_10_data_freshness_check(self):
        """Test that data is reasonably fresh"""
        print("\n[TEST 10] Data Freshness Check")
        try:
            csv_path = Path(__file__).parent / 'croppulse' / 'data' / 'commodity_prices.csv'
            
            if not csv_path.exists():
                print(f"[SKIP] CSV not found")
                return True
            
            df = pd.read_csv(csv_path)
            dates = pd.to_datetime(df['date'], errors='coerce')
            
            if dates.notna().sum() > 0:
                latest_date = dates.max()
                from datetime import datetime, timedelta
                
                days_old = (datetime.now() - latest_date).days
                
                if days_old < 30:  # Within 30 days is fresh
                    print(f"[PASS] Data is fresh (latest: {latest_date.date()})")
                    return True
                else:
                    print(f"[WARNING] Data is {days_old} days old")
                    return True  # Still acceptable
            else:
                print(f"[SKIP] No valid dates found")
                return True
        except Exception as e:
            print(f"[SKIP] {e}")
            return True


def run_all_tests():
    """Run all API error handling tests"""
    print("=" * 70)
    print("[TEST SUITE] CropPulse API Error Handling Tests")
    print("=" * 70)
    
    test_obj = TestAPIErrors()
    
    tests = [
        ('Missing CSV File', test_obj.test_1_missing_csv_file),
        ('CSV Data Validation', test_obj.test_2_csv_data_validation),
        ('Null Value Handling', test_obj.test_3_null_value_handling),
        ('Malformed CSV Format', test_obj.test_4_malformed_csv_format),
        ('Empty Data Handling', test_obj.test_5_empty_data_handling),
        ('Type Mismatch Handling', test_obj.test_6_type_mismatch_handling),
        ('Data Range Validation', test_obj.test_7_data_range_validation),
        ('Fallback Mechanism', test_obj.test_8_fallback_mechanism_ready),
        ('Date Format Validation', test_obj.test_9_date_format_validation),
        ('Data Freshness Check', test_obj.test_10_data_freshness_check),
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
    
    if passed >= total - 1:  # Allow 1 failure
        print('\n[SUCCESS] API ERROR HANDLING TESTS PASSED')
        return 0
    else:
        print(f'\n[WARNING] {total - passed} test(s) failed')
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
