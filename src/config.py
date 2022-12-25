"""Application settings.

Application settings be set using environment variables. Some meaningful
defaults are provided.
"""

import os
from dotenv import load_dotenv

root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
env_file = os.path.join(root_dir, ".env")

if os.path.exists(env_file):
    load_dotenv(dotenv_path=env_file)


def _getenv(env_name, default, prefix="SAEHAEKKAE"):
    """Return prefixed environment variable value or default value."""
    return os.getenv(f"{prefix}_{env_name}") or default


DB_FILE = _getenv("DB_FILE", "db.csv")
ENERGY_PRICE_SOURCE = _getenv("ENERGY_PRICE_SOURCE", "spot-hinta.fi")
ENERGY_CONSUMPTION_SOURCE = _getenv("ENERGY_CONSUMPTION_SOURCE", "json")
ENERGY_CONSUMPTION_FILE = _getenv("ENERGY_CONSUMPTION_FILE", "data/generic-data.json")

# Google settings, these are needed to make google calendar working!
GOOGLE_CREDENTIALS_FILE = _getenv("GOOGLE_CREDENTIALS_FILE", "google_credentials.json")
GOOGLE_CALENDAR_ID = _getenv("GOOGLE_CALENDAR_ID", None)

# Shelly ip
SHELLY_IP = _getenv("SHELLY_IP", "192.168.1.30")
