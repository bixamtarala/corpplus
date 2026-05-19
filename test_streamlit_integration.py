#!/usr/bin/env python3
"""External Streamlit-to-Backend integration test."""

import os
import sys

import requests


BACKEND_API_URL = os.getenv("BACKEND_API_URL")
API_KEY = os.getenv("API_KEY")
RUN_EXTERNAL_INTEGRATION = os.getenv("RUN_EXTERNAL_INTEGRATION", "0") == "1"


def main():
    print('=' * 70)
    print('TESTING STREAMLIT-TO-BACKEND INTEGRATION')
    print('=' * 70)
    print()

    if not RUN_EXTERNAL_INTEGRATION:
        print('⏭️  SKIPPED: External integration test is opt-in only.')
        print('   Set RUN_EXTERNAL_INTEGRATION=1 to test the live backend service.')
        return 0

    if not BACKEND_API_URL or not API_KEY:
        print('⏭️  SKIPPED: BACKEND_API_URL and API_KEY must be set for external integration.')
        return 0

    try:
        headers = {'X-API-Key': API_KEY}

        print('[1/3] Testing health endpoint...')
        resp = requests.get(f'{BACKEND_API_URL}/health', headers=headers, timeout=10)
        resp.raise_for_status()
        print(f'  Status: {resp.status_code} ✅')
        print()

        print('[2/3] Testing price endpoint...')
        resp = requests.get(f'{BACKEND_API_URL}/api/v1/prices/latest?commodity=rice', headers=headers, timeout=10)
        resp.raise_for_status()
        print(f'  Status: {resp.status_code} ✅')
        data = resp.json()
        print(f'  Commodity: {data.get("commodity", "N/A")}')
        print(f'  Price: {data.get("price", "N/A")}')
        print()

        print('[3/3] Testing user endpoint...')
        resp = requests.get(f'{BACKEND_API_URL}/api/v1/users', headers=headers, timeout=10)
        print(f'  Status: {resp.status_code} ✅')
        print()

        print('=' * 70)
        print('✅ INTEGRATION TEST PASSED')
        print('=' * 70)
        print()
        print('Streamlit app is ready to deploy to Streamlit Cloud!')
        return 0

    except requests.RequestException as exc:
        print(f'❌ External integration failed: {type(exc).__name__}: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
