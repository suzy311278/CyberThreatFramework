import os
import sys

# Add the src directory to the path so imports work
# Assuming file is in /api/index.py, we need to go up one level to root, then into src
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(root_dir, 'src'))

# Import the Flask app
from CyberThreatFramework.dashboard import app

# Vercel requires the app object to be named 'app'
