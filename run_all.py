"""Launch the single Streamlit public app locally."""

import os
import subprocess
import sys


def run_streamlit():
    """Run the Streamlit-only public app."""
    print("🌾 Starting Streamlit public app...")
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app_phase2.py"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        check=False,
    )


if __name__ == "__main__":
    run_streamlit()
