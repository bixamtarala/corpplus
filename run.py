#!/usr/bin/env python
"""
Railway deployment entry point - Minimal and reliable
"""
import os
import sys

# Get port from environment (Railway will set this)
PORT = int(os.getenv("PORT", "8000"))
HOST = "0.0.0.0"

print("=" * 70)
print("🚀 CropPulse API Starting on Railway")
print("=" * 70)
print(f"Host: {HOST}:{PORT}")
print(f"Environment: {os.getenv('ENV', 'production')}")
print("=" * 70)

try:
    # Import app
    from phase2_backend.main import app
    import uvicorn
    
    # Start server
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info"
    )
    
except ImportError as e:
    print(f"ERROR: Failed to import app: {e}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
