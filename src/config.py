"""Application settings.

Application settings be set using environment variables. Some meaningful
defaults are provided.
"""

import os

DB_FILE = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "db.csv"))

# Options, "test", "local", "internet"
ENERGY_PRICE_SOURCE = "test"
ENERGY_PRICE_URI = "https://api.spot-hinta.fi/TodayAndDayForward"
ENERGY_PRICE_FILE = "data/energy-prices.json"

ENERGY_CONSUMPTION_SOURCE = "test"
ENERGY_CONSUMPTION_FILE = "data/energy-consumption.csv"

if "SAEHAEKKAE_ENERGY_CONSUMPTION_FILE" in os.environ:
    ENERGY_CONSUMPTION_FILE = os.environ["SAEHAEKKAE_ENERGY_CONSUMPTION_FILE"]

if "SAEHAEKKAE_ENERGY_PRICE_FILE" in os.environ:
    ENERGY_PRICE_FILE = os.environ["SAEHAEKKAE_ENERGY_PRICE_FILE"]
