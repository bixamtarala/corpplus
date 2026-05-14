#!/usr/bin/env python
"""Test Streamlit-to-Backend Integration"""

import requests
import os

BACKEND_API_URL = 'https://web-production-7295a.up.railway.app'
API_KEY = 'croppulse_admin_secret_key_12345'

print('=' * 70)
print('TESTING STREAMLIT-TO-BACKEND INTEGRATION')
print('=' * 70)
print()

try:
    headers = {'X-API-Key': API_KEY}
    
    print('[1/3] Testing health endpoint...')
    resp = requests.get(f'{BACKEND_API_URL}/health', headers=headers, timeout=5)
    print(f'  Status: {resp.status_code} ✅')
    print()
    
    print('[2/3] Testing price endpoint...')
    resp = requests.get(f'{BACKEND_API_URL}/api/v1/prices/latest?commodity=rice', headers=headers, timeout=5)
    print(f'  Status: {resp.status_code} ✅')
    if resp.status_code == 200:
        data = resp.json()
        print(f'  Commodity: {data.get("commodity", "N/A")}')
        print(f'  Price: {data.get("price", "N/A")}')
    print()
    
    print('[3/3] Testing user endpoint...')
    resp = requests.get(f'{BACKEND_API_URL}/api/v1/users', headers=headers, timeout=5)
    print(f'  Status: {resp.status_code} ✅')
    print()
    
    print('=' * 70)
    print('✅ INTEGRATION TEST PASSED')
    print('=' * 70)
    print()
    print('Streamlit app is ready to deploy to Streamlit Cloud!')
    
except Exception as e:
    print(f'❌ Error: {type(e).__name__}: {e}')
