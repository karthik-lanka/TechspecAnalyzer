#!/usr/bin/env python3
"""
Main entry point - redirects to new Tech Spec Analyzer Pro structure
"""

import sys
import os

# Redirect to the new application structure
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tech-spec-analyzer-pro'))

from backend.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
