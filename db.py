"""
Database management helper for Basic_CRM.
Handles connection pooling, query execution, and database schema initialization.
Supports both mysql-connector-python and PyMySQL.
"""

import os
from config import Config

# Detect available MySQL driver
DB_DRIVER = None

try:
    import mysql.connector
    from mysql.connector import Error as DBError
    DB_DRIVER = "mysql.connector"
except Exception:
    try:
        import pymysql
        import pymysql.cursors
        from pymysql import Error as DBError
        DB_DRIVER = "pymysql"
    except Exception:
        DBError = Exception

def get_db_connection(use_database=True):
    """
    Establish and return a connection to MySQL.
    """
    if DB_DRIVER == "mysql.connector":
        connection_params = {
            "host": Config.MYSQL_HOST,
            "port": Config.MYSQL_PORT,
            "user": Config.MYSQL_USER,
            "password": Config.MYSQL_PASSWORD,
            "charset": "utf8mb4",
        }
        if use_database:
            connection_params["database"] = Config.MYSQL_DATABASE
        try:
            return mysql.connector.connect(**connection_params)
        except Exception as e:
            print(f"[DB Error via mysql.connector]: {e}")
            return None

    elif DB_DRIVER == "pymysql":
        import pymysql
        import pymysql.cursors
        connection_params = {
            "host": Config.MYSQL_HOST,
            "port": Config.MYSQL_PORT,
            "user": Config.MYSQL_USER,
            "password": Config.MYSQL_PASSWORD,
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
            "autocommit": False,
        }
        if use_database:
            connection_params["database"] = Config.MYSQL_DATABASE
        try:
            return pymysql.connect(**connection_params)
        except Exception as e:
            print(f"[DB Error via pymysql]: {e}")
            return None

    else:
        print("[DB Error] Neither mysql-connector nor PyMySQL is available.")
        return None

def init_db(schema_path="schema.sql"):
    """
    Initializes the database and tables defined in schema.sql.
    Safe for hosting:
    - Connects directly to Config.MYSQL_DATABASE first.
    - Runs CREATE TABLE IF NOT EXISTS while skipping CREATE DATABASE and USE commands.
    - If connecting to the target database fails, falls back to connecting without a database.
    """
    if not os.path.isabs(schema_path):
        schema_path = os.path.join(os.path.dirname(__file__), schema_path)

    if not os.path.exists(schema_path):
        return False, f"Schema file not found at: {schema_path}"

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    raw_statements = schema_sql.split(";")
    
    conn = get_db_connection(use_database=True)
    connected_to_db = True

    if not conn:
        conn = get_db_connection(use_database=False)
        connected_to_db = False

    if not conn:
        return False, (
            f"Failed to connect to MySQL server. Please verify your host '{Config.MYSQL_HOST}', "
            f"user '{Config.MYSQL_USER}', and password in .env or config.py."
        )

    cursor = None
    try:
        cursor = conn.cursor()
        for stmt in raw_statements:
            cleaned_stmt = stmt.strip()
            if not cleaned_stmt:
                continue

            upper_stmt = cleaned_stmt.upper()
            if connected_to_db and (upper_stmt.startswith("CREATE DATABASE") or upper_stmt.startswith("USE ")):
                continue

            cursor.execute(cleaned_stmt)
        conn.commit()
        return True, f"Database '{Config.MYSQL_DATABASE}' and tables verified successfully."
    except Exception as err:
        return False, f"Error initializing database: {err}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            try:
                conn.close()
            except Exception:
                pass

def query_one(sql, params=None):
    """
    Execute a SELECT query and return a single record as a dict, or None.
    """
    conn = get_db_connection()
    if not conn:
        return None

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True) if DB_DRIVER == "mysql.connector" else conn.cursor()
        cursor.execute(sql, params or ())
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"[DB Query Error]: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            try:
                conn.close()
            except Exception:
                pass

def query_all(sql, params=None):
    """
    Execute a SELECT query and return all matching records as a list of dicts.
    """
    conn = get_db_connection()
    if not conn:
        return []

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True) if DB_DRIVER == "mysql.connector" else conn.cursor()
        cursor.execute(sql, params or ())
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"[DB Query Error]: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            try:
                conn.close()
            except Exception:
                pass

def execute_commit(sql, params=None):
    """
    Execute an INSERT, UPDATE, or DELETE query.
    Returns (success: bool, last_row_id or error_message).
    """
    conn = get_db_connection()
    if not conn:
        return False, "Database connection unavailable"

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        last_id = getattr(cursor, "lastrowid", None)
        row_count = getattr(cursor, "rowcount", None)
        return True, last_id if last_id else row_count
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print(f"[DB Execute Error]: {e}")
        return False, str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            try:
                conn.close()
            except Exception:
                pass

if __name__ == "__main__":
    print(f"Active MySQL Driver: {DB_DRIVER}")
    print("Testing database initialization...")
    ok, message = init_db()
    print(f"Result: {ok} -> {message}")
