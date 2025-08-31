"""
Production WSGI entry point for Money Laundering Detection System
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment
os.environ.setdefault('FLASK_ENV', 'production')

# Import the Flask app
from app import app

if __name__ == "__main__":
    # This is for development only
    # In production, use: gunicorn wsgi:app
    app.run(host='0.0.0.0', port=5000)
