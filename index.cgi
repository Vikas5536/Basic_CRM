#!/usr/bin/python3
"""
CGI Handler entry point for running Flask on shared hosting (HostGator)
Supports user site-packages from 'pip install --user'.
"""

import sys
import os
import glob
import cgitb

# Enable browser error display for debugging
cgitb.enable()

# Ensure project root is in sys.path
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Ensure user-installed packages from 'pip install --user' are included in CGI mode
user_sites = glob.glob(os.path.expanduser("~/.local/lib/python*/site-packages"))
for site_path in user_sites:
    if site_path not in sys.path:
        sys.path.insert(0, site_path)

# Also check explicit home path for cPanel user if expanduser is restricted
home_dir = f"/home/{os.environ.get('USER', 'upayssmk')}"
cpanel_sites = glob.glob(f"{home_dir}/.local/lib/python*/site-packages")
for cp_path in cpanel_sites:
    if cp_path not in sys.path:
        sys.path.insert(0, cp_path)

from wsgiref.handlers import CGIHandler
from app import app

if __name__ == "__main__":
    CGIHandler().run(app)
