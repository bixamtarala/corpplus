#!/usr/bin/env python
"""
Railway deployment entry point
Handles environment variable expansion for PORT and starts the app
"""
import os
import sys
import uvicorn

def main():
    # Get environment variables
    port = int(os.getenv("PORT", "8000"))
    host = "0.0.0.0"
    env = os.getenv("ENV", "production")
    
    print("=" * 60)
    print("🚀 CropPulse API - Railway Deployment")
    print("=" * 60)
    print(f"✓ Host: {host}")
    print(f"✓ Port: {port}")
    print(f"✓ Environment: {env}")
    print(f"✓ Debug: {env == 'development'}")
    print("=" * 60)
    print()
    
    try:
        # Start the FastAPI app with uvicorn
        uvicorn.run(
            "phase2_backend.main:app",
            host=host,
            port=port,
            reload=env == "development",
            log_level="info",
            access_log=True,
        )
    except Exception as e:
        print(f"\n❌ ERROR: Failed to start app")
        print(f"Details: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
