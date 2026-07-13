"""Data update coordinator for the Pool Math integration."""

from __future__ import annotations

import asyncio
import logging
import re
from datetime import timedelta
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, DOMAIN

_LOGGER = logging.getLogger(__name__)


def extract_share_id(value: str) -> str:
    """Extract the share id from a full share URL or a bare id."""
    value = value.strip()
    match = re.search(r"share/([A-Za-z0-9]+)", value)
    if match:
        return match.group(1)
    # Bare id, strip possible .json suffix
    return value.removesuffix(".json").strip("/")


def _find_pool(data: dict[str, Any]) -> dict[str, Any]:
    """Locate the pool object in the API response, defensively."""
    pools = data.get("pools")
    if isinstance(pools, list) and pools:
        first = pools[0]
        if isinstance(first, dict):
            if isinstance(first.get("pool"), dict):
                return first["pool"]
            return first
    if isinstance(data.get("pool"), dict):
        return data["pool"]
    return data


def parse_pool_data(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize the PoolMath API response into a flat structure."""
    pool = _find_pool(raw)
    overview: dict[str, Any] = pool.get("overview") or {}

    return {
        "name": pool.get("name") or "Pool",
        "volume": pool.get("volume"),
        "volume_units": pool.get("volumeUnits") or pool.get("volume_units"),
        "build_type": pool.get("buildType") or pool.get("build_type"),
        "overview": overview,
        "raw": pool,
    }


class PoolMathCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that polls the PoolMath share endpoint."""

    def __init__(
        self,
        hass: HomeAssistant,
        share_id: str,
        update_interval: timedelta,
    ) -> None:
        """Initialize the coordinator."""
        self.share_id = share_id
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{share_id}",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the PoolMath API."""
        session = async_get_clientsession(self.hass)
        url = API_URL.format(share_id=self.share_id)
        try:
            async with asyncio.timeout(15):
                response = await session.get(url)
                if response.status == 404:
                    raise UpdateFailed(f"Share id '{self.share_id}' not found (404)")
                response.raise_for_status()
                raw = await response.json(content_type=None)
        except TimeoutError as err:
            raise UpdateFailed("Timeout communicating with PoolMath API") from err
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with PoolMath API: {err}") from err

        if not isinstance(raw, dict):
            raise UpdateFailed("Unexpected response from PoolMath API")

        return parse_pool_data(raw)
