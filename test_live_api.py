#!/usr/bin/env python
"""Test if Railway API is live"""
import requests

try:
    resp = requests.get('https://web-production-7295a.up.railway.app/', timeout=5)
    print(f'✅ Status: {resp.status_code}')
    data = resp.json()
    print(f'✅ Service: {data.get("service")}')
    print(f'✅ Version: {data.get("version")}')
    print('✅ API IS LIVE AND RESPONDING')
except requests.exceptions.Timeout:
    print('❌ Timeout - API may be restarting')
except requests.exceptions.ConnectionError:
    print('❌ Connection refused - API is down or not accessible')
except Exception as e:
    print(f'❌ Error: {type(e).__name__}: {e}')
