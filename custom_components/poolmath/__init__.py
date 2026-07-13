"""The Pool Math integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_SCAN_INTERVAL_MINUTES,
    CONF_SHARE_ID,
    DEFAULT_SCAN_INTERVAL_MINUTES,
)
from .coordinator import PoolMathCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

type PoolMathConfigEntry = ConfigEntry[PoolMathCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: PoolMathConfigEntry) -> bool:
    """Set up Pool Math from a config entry."""
    scan_minutes = entry.options.get(
        CONF_SCAN_INTERVAL_MINUTES, DEFAULT_SCAN_INTERVAL_MINUTES
    )
    coordinator = PoolMathCoordinator(
        hass,
        share_id=entry.data[CONF_SHARE_ID],
        update_interval=timedelta(minutes=scan_minutes),
    )
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def _async_update_listener(
    hass: HomeAssistant, entry: PoolMathConfigEntry
) -> None:
    """Reload the entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: PoolMathConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
