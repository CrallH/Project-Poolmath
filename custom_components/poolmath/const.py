"""Constants for the Pool Math integration."""

from datetime import timedelta

DOMAIN = "poolmath"

CONF_SHARE_ID = "share_id"
CONF_TEMP_UNIT = "temp_unit"
CONF_SCAN_INTERVAL_MINUTES = "scan_interval_minutes"

DEFAULT_SCAN_INTERVAL_MINUTES = 15
MIN_SCAN_INTERVAL_MINUTES = 5
DEFAULT_TEMP_UNIT = "celsius"

API_URL = "https://api.poolmathapp.com/share/{share_id}.json"
SHARE_URL = "https://api.poolmathapp.com/share/{share_id}"

ATTR_LAST_MEASURED = "last_measured"
ATTR_POOL_NAME = "pool_name"
ATTR_POOL_VOLUME = "pool_volume"

DEFAULT_TIMEOUT = timedelta(seconds=15)
