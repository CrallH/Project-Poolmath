"""Diagnostics support for the Pool Math integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import PoolMathConfigEntry
from .const import CONF_SHARE_ID

TO_REDACT = {CONF_SHARE_ID, "raw"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: PoolMathConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return {
        "entry_data": async_redact_data(dict(entry.data), TO_REDACT),
        "coordinator_data": async_redact_data(coordinator.data, TO_REDACT),
    }
