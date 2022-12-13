"""Application settings.

Application settings be set using environment variables. Some meaningful
defaults are provided.
"""

import os

# Options, "test", "local", "internet"
ENERGY_PRICE_SOURCE = "test"
ENERGY_PRICE_URI = "https://api.spot-hinta.fi/TodayAndDayForward"
ENERGY_PRICE_FILE = "data/energy-prices.json"

if "SAEHAEKKAE_ENERGY_PRICE_FILE" in os.environ:
    ENERGY_PRICE_FILE = os.environ["SAEHAEKKAE_ENERGY_PRICE_FILE"]
