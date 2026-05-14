#!/usr/bin/env python3
"""
CropPulse - Agricultural Market Intelligence Platform
Main entry point for Streamlit Cloud deployment

This file serves as the entry point for Streamlit Cloud to properly deploy the application.
It imports and runs the main CropPulse app from the croppulse directory.
"""

import sys
import os
from pathlib import Path

# Add the croppulse directory to Python path so imports work correctly
project_root = Path(__file__).parent
croppulse_dir = project_root / "croppulse"
sys.path.insert(0, str(croppulse_dir))
sys.path.insert(0, str(project_root))

# Now we can import from croppulse_app_refactored
# This will run the entire Streamlit application with 9-module architecture
import croppulse_app_refactored  # noqa: F401

