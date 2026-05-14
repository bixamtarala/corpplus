#!/usr/bin/env python3
"""
Master Test Runner for CropPulse
Executes all test suites and generates comprehensive report
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_test_file(test_file):
    """Execute a single test file and return results"""
    print(f"\n{'='*70}")
    print(f"Running: {test_file}")
    print('='*70)
    
    try:
        # Set UTF-8 encoding for Windows compatibility
        env = {**dict(os.environ), 'PYTHONIOENCODING': 'utf-8'}
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=str(Path(__file__).parent),
            capture_output=False,
            env=env
        )
        return result.returncode == 0
    except Exception as e:
        print(f"ERROR running {test_file}: {e}")
        return False

def main():
    """Run all test suites"""
    import os
    
    print("\n" + "="*70)
    print("CROPPULSE COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_files = [
        'test_saas.py',           # Phase 1 validation (8 tests)
        'test_algorithms.py',      # Algorithm unit tests (10 tests)
        'test_api_errors.py',      # API error handling (10 tests)
        'test_security_load.py',   # Security & load tests (15 tests)
    ]
    
    results = {}
    
    for test_file in test_files:
        test_path = Path(__file__).parent / test_file
        if test_path.exists():
            results[test_file] = run_test_file(test_file)
        else:
            print(f"[SKIP] {test_file} not found")
            results[test_file] = None
    
    # Summary
    print("\n" + "="*70)
    print("TEST EXECUTION SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    total = len(results)
    
    for test_file, result in results.items():
        if result is True:
            status = "[PASS]"
        elif result is False:
            status = "[FAIL]"
        else:
            status = "[SKIP]"
        print(f"{status} {test_file}")
    
    print("="*70)
    print(f"Total: {passed} PASSED, {failed} FAILED, {skipped} SKIPPED")
    print(f"Pass Rate: {passed}/{total} ({100*passed//total if total > 0 else 0}%)")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed == 0 and passed >= total - skipped:
        print("\n[SUCCESS] All available tests passed!")
        return 0
    else:
        print(f"\n[WARNING] {failed} test suite(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
