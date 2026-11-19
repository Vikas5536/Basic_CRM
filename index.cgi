#!/usr/bin/python3
"""
CGI Handler entry point for running Flask on shared hosting (e.g. HostGator)
without CloudLinux 'Setup Python App'.
"""

import sys
import os

# Ensure project root is in sys.path
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Support bundled packages in /lib or user site-packages if pip is unavailable globally
lib_dir = os.path.join(app_dir, "lib")
if os.path.exists(lib_dir) and lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

from wsgiref.handlers import CGIHandler
from app import app

if __name__ == "__main__":
    CGIHandler().run(app)
