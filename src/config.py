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
    return os.getenv("%s_%s" % (prefix, env_name)) or default


DB_FILE = _getenv("DB_FILE", "db.csv")

# Options, "test", "local", "internet"
ENERGY_PRICE_SOURCE = _getenv("ENERGY_PRICE_SOURCE", "test")
ENERGY_PRICE_URI = _getenv("PRICE_URI", "https://api.spot-hinta.fi/TodayAndDayForward")
ENERGY_PRICE_FILE = _getenv("PRICE_FILE", "data/prices.json")

# Options, "test", "local"
ENERGY_CONSUMPTION_SOURCE = _getenv("ENERGY_CONSUMPTION_SOURCE", "test")
ENERGY_CONSUMPTION_FILE = _getenv("ENERGY_CONSUMPTION_FILE", "data/consumption.csv")
