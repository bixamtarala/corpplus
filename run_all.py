"""
Run both the landing page server and Streamlit app together
"""
import subprocess
import sys
import time
import os
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

def serve_landing_page():
    """Serve the landing page on port 8000"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = '/landing_page/index.html'
            return super().do_GET()
    
    server = HTTPServer(('localhost', 8000), MyHTTPRequestHandler)
    print("🌍 Landing page server running at http://localhost:8000")
    server.serve_forever()

def run_streamlit():
    """Run the Streamlit app"""
    time.sleep(2)  # Wait for landing page server to start
    print("\n🌾 Starting Streamlit app...")
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "croppulse/croppulse_app.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

if __name__ == "__main__":
    # Start landing page server in background
    server_thread = threading.Thread(target=serve_landing_page, daemon=True)
    server_thread.start()
    
    # Run Streamlit
    run_streamlit()
