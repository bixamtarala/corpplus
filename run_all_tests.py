#!/usr/bin/env python3
"""
Master Test Runner for CropPulse
Executes all test suites and generates comprehensive report
"""

import subprocess
import sys
import os
import re
from pathlib import Path
from datetime import datetime


STREAMLIT_WARNING_PATTERNS = [
    re.compile(r"missing ScriptRunContext", re.IGNORECASE),
    re.compile(r"No runtime found, using MemoryCacheStorageManager", re.IGNORECASE),
    re.compile(r"Warning: to view this Streamlit app on a browser", re.IGNORECASE),
    re.compile(r"streamlit run .* \[ARGUMENTS\]", re.IGNORECASE),
]


def split_output_lines(text):
    return [line for line in text.splitlines() if line.strip()]


def is_streamlit_warning(line):
    return any(pattern.search(line) for pattern in STREAMLIT_WARNING_PATTERNS)


def summarize_output(text):
    lines = split_output_lines(text)
    filtered_lines = [line for line in lines if not is_streamlit_warning(line)]
    warning_lines = [line for line in lines if is_streamlit_warning(line)]
    return filtered_lines, warning_lines

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
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env,
        )

        stdout_lines, stdout_warnings = summarize_output(result.stdout)
        stderr_lines, stderr_warnings = summarize_output(result.stderr)
        meaningful_output = stdout_lines + stderr_lines
        warning_count = len(stdout_warnings) + len(stderr_warnings)

        if meaningful_output:
            for line in meaningful_output:
                print(line)

        if warning_count:
            print(f"[INFO] Suppressed {warning_count} known Streamlit bare-mode warning lines")

        if result.returncode != 0 and not meaningful_output and warning_count:
            print("[INFO] Command failed without actionable output beyond suppressed warnings")

        return result.returncode == 0
    except Exception as e:
        print(f"ERROR running {test_file}: {e}")
        return False

def main():
    """Run all test suites"""
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
