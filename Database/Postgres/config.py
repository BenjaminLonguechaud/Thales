"""
Configuration file for PostgreSQL connection settings.
Reads from database_config.json file to avoid storing credentials in code.
"""

import os
import json
from pathlib import Path

# Get the directory where this config.py file is located
CONFIG_DIR = Path(__file__).parent
CONFIG_FILE = CONFIG_DIR / "database_config.json"

def load_config_file():
    """Load configuration from database_config.json file."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}\n"
            "Please create database_config.json with your database credentials."
        )

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {CONFIG_FILE}: {e}")

# Load the configuration file
_config = load_config_file()

# Database Connection Configuration
# Supports environment variable overrides for flexibility
# Priority: Environment Variables > Config File > Defaults
DB_CONFIG = {
    "host": os.getenv("DB_HOST", _config["database"].get("host", "localhost")),
    "port": int(os.getenv("DB_PORT", _config["database"].get("port", 5432))),
    "database": os.getenv("POSTGRES_DB", _config["database"].get("database", "postgresdb")),
    "user": os.getenv("POSTGRES_USER", _config["database"].get("user", "postgresadmin")),
    "password": os.getenv("POSTGRES_PASSWORD", _config["database"].get("password", "admin123")),
    "min_connections": int(os.getenv("DB_MIN_CONN", _config["database"].get("min_connections", 2))),
    "max_connections": int(os.getenv("DB_MAX_CONN", _config["database"].get("max_connections", 10))),
}

# Application Settings
APP_CONFIG = {
    "debug": os.getenv("DEBUG", str(_config["application"].get("debug", True))).lower() == "true",
    "log_level": os.getenv("LOG_LEVEL", _config["application"].get("log_level", "INFO")),
}

# Connection String for reference
CONNECTION_STRING = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

print(f"Database Configuration: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")

