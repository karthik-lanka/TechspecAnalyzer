#!/usr/bin/env python3
"""
Tech Spec Analyzer Pro - Main Entry Point
Professional technical document analysis with AI-powered parameter extraction
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app from backend
from backend.app import app

if __name__ == '__main__':
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)