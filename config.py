import os
from dotenv import load_dotenv

# Ensure .env is loaded reliably even if running via WSGI/cPanel
basedir = os.path.abspath(os.path.dirname(__file__))
env_file = os.path.join(basedir, ".env")
if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    load_dotenv()

class Config:
    """Application configuration for hosting and development."""
    SECRET_KEY = os.getenv("SECRET_KEY", "coustomer-management-relationship-secret-key-2026")

    # MySQL Database Configuration (HostGator cPanel Defaults)
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "upayssmk_sidak")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "upayssmk_sidak_crm")
