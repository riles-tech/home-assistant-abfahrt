"""Constants for the Abfahrt Transit integration."""

DOMAIN = "abfahrt"

API_URL = "https://api.abfahrt.now/departures"

CONF_API_KEY = "api_key"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_RADIUS = "radius"
CONF_STOPS = "stops"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_RADIUS = 500
# The Home Assistant plan allows 750 requests per day. 180 s = 480 per day;
# 120 s = 720 per day is the shortest interval that stays inside the plan.
DEFAULT_SCAN_INTERVAL = 180
MIN_SCAN_INTERVAL = 120
