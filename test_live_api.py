#!/usr/bin/env python
"""Test if the deployed Streamlit app is reachable."""
import requests


BASE_URL = 'https://corpplus.streamlit.app'
TIMEOUT_SECONDS = 20


def check_endpoint(url: str) -> bool:
    try:
        resp = requests.get(url, timeout=TIMEOUT_SECONDS, allow_redirects=True)
        print(f'URL: {url}')
        print(f'✅ Status: {resp.status_code}')
        print(f'✅ Final URL: {resp.url}')

        if resp.status_code >= 500:
            print(f'❌ Server error body: {resp.text[:200]}')
            return False

        content_type = resp.headers.get('content-type', '')
        if 'text/html' in content_type:
            print(f'✅ HTML response detected: {resp.text[:200]}')
        else:
            print(f'✅ Response: {resp.text[:200]}')

        return 200 <= resp.status_code < 500
    except requests.exceptions.Timeout:
        print(f'❌ Timeout after {TIMEOUT_SECONDS}s: {url}')
        return False
    except requests.exceptions.ConnectionError:
        print(f'❌ Connection refused: {url}')
        return False
    except Exception as e:
        print(f'❌ Error for {url}: {type(e).__name__}: {e}')
        return False


if __name__ == '__main__':
    passed = check_endpoint(BASE_URL)
    if passed:
        print('✅ STREAMLIT DEPLOYMENT IS REACHABLE')
    else:
        print('❌ STREAMLIT DEPLOYMENT IS NOT HEALTHY')
