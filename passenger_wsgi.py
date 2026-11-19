"""
cPanel Phusion Passenger WSGI entry point for CoustomerManagementRelationship.
Enables running the Flask application under cPanel 'Setup Python App'.
"""

import os
import sys

# Add application directory to sys.path
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Import the Flask application instance
from app import app as application
