#!/usr/bin/python3
"""
Bulletproof CGI Handler for CoustomerManagementRelationship on HostGator Shared Hosting.
Supports CLI testing and web execution via Apache.
"""

import sys
import os
import glob
import traceback

# 1. Add application directory to sys.path
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# 2. Add user-installed site-packages from 'pip install --user'
user_sites = glob.glob(os.path.expanduser("~/.local/lib/python*/site-packages"))
for p in user_sites:
    if p not in sys.path:
        sys.path.insert(0, p)

# 3. Add explicit cPanel home site-packages path
cpanel_sites = glob.glob("/home/upayssmk/.local/lib/python*/site-packages")
for p in cpanel_sites:
    if p not in sys.path:
        sys.path.insert(0, p)

# 4. CLI test fallback: populate CGI environment variables if executed from terminal
if "REQUEST_METHOD" not in os.environ:
    os.environ["REQUEST_METHOD"] = "GET"
if "SERVER_NAME" not in os.environ:
    os.environ["SERVER_NAME"] = "localhost"
if "SERVER_PORT" not in os.environ:
    os.environ["SERVER_PORT"] = "80"
if "PATH_INFO" not in os.environ:
    os.environ["PATH_INFO"] = "/"
if "SCRIPT_NAME" not in os.environ:
    os.environ["SCRIPT_NAME"] = ""
if "SERVER_PROTOCOL" not in os.environ:
    os.environ["SERVER_PROTOCOL"] = "HTTP/1.1"
if "QUERY_STRING" not in os.environ:
    os.environ["QUERY_STRING"] = ""

try:
    from wsgiref.handlers import CGIHandler
    from app import app
    CGIHandler().run(app)
except Exception:
    # Ensure headers are sent so the browser displays the exact Python error
    print("Status: 500 Internal Server Error")
    print("Content-Type: text/html; charset=utf-8\n")
    print("<div style='font-family:sans-serif;max-width:800px;margin:30px auto;padding:20px;border:1px solid #e3342f;border-radius:6px;'>")
    print("<h2 style='color:#e3342f;margin-top:0;'>⚠️ CRM Application Startup Error</h2>")
    print("<p>The server encountered an error while starting the Flask application:</p>")
    print("<pre style='background:#f8f9fa;padding:15px;border-radius:4px;overflow-x:auto;color:#333;font-size:13px;'>")
    print(traceback.format_exc())
    print("</pre>")
    print("<p style='color:#666;font-size:12px;'>Tip: Verify database password in .env or config.py and ensure all dependencies are installed.</p>")
    print("</div>")
