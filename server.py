import os
import sys
import logging
from waitress import serve

# Import your main application file (more.py must be in the same folder)
try:
    from more import app
except ImportError:
    print("[!] CRITICAL ERROR: Could not find 'more.py' in this directory.")
    print("Ensure prod_server.py is placed inside the exact same folder as more.py!")
    sys.exit(1)

# Turn off unsafe Flask terminal debugging leaks for production safety
app.config['DEBUG'] = False
app.config['ENV'] = 'production'

# Set up clean terminal event logging layout metrics
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("waitress")


def launch_production_system():
    PORT = 5000       # Port matching your internal proxy bridge channels
    HOST = "0.0.0.0"  # Broadcasts across your entire network mapping interface
    THREADS = 8       # Multi-threaded concurrent processing pool for 2G handsets

    print("=" * 65)
    print("  PRODUCTION INITIALIZATION: SECURE FREE 2G CHATROOM PLATFORM")
    print("  WSGI ENGINE: WAITRESS GATEWAY MULTI-THREAD PIPELINES LIVE")
    print(f"  Listening for mobile phone hits on: http://localhost:{PORT}")
    print("=" * 65)

    # Fire up the production listener loop
    serve(
        app,
        host=HOST,
        port=PORT,
        threads=THREADS,
        channel_timeout=30,
        max_request_body_size=1024 * 5  # Limits request sizes to protect 2G speeds
    )


if __name__ == '__main__':
    launch_production_system()
