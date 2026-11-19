#!/usr/bin/env python3
"""
Diagnostic script to test MySQL database connection and dependencies on hosting.
Run via cPanel terminal: python3 test_db.py
"""

import sys
import os

print(f"1. Python executable: {sys.executable}")
print(f"2. Python version: {sys.version.split()[0]}")

# Test importing Flask
try:
    import flask
    print(f"3. Flask: OK (version {flask.__version__})")
except Exception as e:
    print(f"3. Flask: FAILED ({e})")

# Test importing mysql.connector
try:
    import mysql.connector
    print(f"4. mysql-connector: OK (version {mysql.connector.__version__})")
except Exception as e:
    print(f"4. mysql-connector: FAILED ({e})")

# Test Database Connection
print("\nTesting Database Connection...")
try:
    from config import Config
    print(f" - Host: {Config.MYSQL_HOST}:{Config.MYSQL_PORT}")
    print(f" - Database: {Config.MYSQL_DATABASE}")
    print(f" - User: {Config.MYSQL_USER}")
    masked_pw = "********" if Config.MYSQL_PASSWORD else "[EMPTY/NOT SET]"
    print(f" - Password: {masked_pw}")

    import mysql.connector
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        charset="utf8mb4"
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"\n SUCCESS! Connected to database '{Config.MYSQL_DATABASE}'.")
    print(f" Found tables: {', '.join(tables) if tables else 'None'}")
    cursor.close()
    conn.close()
except Exception as err:
    print(f"\n❌ DB CONNECTION FAILED: {err}")
