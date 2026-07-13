"""Config flow for the Pool Math integration."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
)

from .const import (
    API_URL,
    CONF_SCAN_INTERVAL_MINUTES,
    CONF_SHARE_ID,
    CONF_TEMP_UNIT,
    DEFAULT_SCAN_INTERVAL_MINUTES,
    DEFAULT_TEMP_UNIT,
    DOMAIN,
    MIN_SCAN_INTERVAL_MINUTES,
)
from .coordinator import extract_share_id, parse_pool_data

_LOGGER = logging.getLogger(__name__)


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidShareId(Exception):
    """Error to indicate the share id is invalid."""


async def _validate_share_id(hass: HomeAssistant, share_id: str) -> dict[str, Any]:
    """Validate the share id by fetching the API and return parsed pool data."""
    session = async_get_clientsession(hass)
    url = API_URL.format(share_id=share_id)
    try:
        async with asyncio.timeout(15):
            response = await session.get(url)
            if response.status == 404:
                raise InvalidShareId
            response.raise_for_status()
            raw = await response.json(content_type=None)
    except InvalidShareId:
        raise
    except (TimeoutError, aiohttp.ClientError) as err:
        raise CannotConnect from err

    if not isinstance(raw, dict):
        raise InvalidShareId
    return parse_pool_data(raw)


class PoolMathConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pool Math."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            share_id = extract_share_id(user_input[CONF_SHARE_ID])
            if not share_id:
                errors["base"] = "invalid_share_id"
            else:
                await self.async_set_unique_id(share_id)
                self._abort_if_unique_id_configured()
                try:
                    pool = await _validate_share_id(self.hass, share_id)
                except CannotConnect:
                    errors["base"] = "cannot_connect"
                except InvalidShareId:
                    errors["base"] = "invalid_share_id"
                except Exception:  # noqa: BLE001
                    _LOGGER.exception("Unexpected exception during validation")
                    errors["base"] = "unknown"
                else:
                    return self.async_create_entry(
                        title=pool["name"],
                        data={CONF_SHARE_ID: share_id},
                        options={
                            CONF_SCAN_INTERVAL_MINUTES: DEFAULT_SCAN_INTERVAL_MINUTES,
                            CONF_TEMP_UNIT: DEFAULT_TEMP_UNIT,
                        },
                    )

        schema = vol.Schema(
            {
                vol.Required(CONF_SHARE_ID): TextSelector(),
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> PoolMathOptionsFlow:
        """Create the options flow."""
        return PoolMathOptionsFlow()


class PoolMathOptionsFlow(OptionsFlow):
    """Handle options for Pool Math."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        options = self.config_entry.options
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_SCAN_INTERVAL_MINUTES,
                    default=options.get(
                        CONF_SCAN_INTERVAL_MINUTES, DEFAULT_SCAN_INTERVAL_MINUTES
                    ),
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=MIN_SCAN_INTERVAL_MINUTES,
                        max=1440,
                        step=1,
                        mode=NumberSelectorMode.BOX,
                        unit_of_measurement="min",
                    )
                ),
                vol.Required(
                    CONF_TEMP_UNIT,
                    default=options.get(CONF_TEMP_UNIT, DEFAULT_TEMP_UNIT),
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=["celsius", "fahrenheit"],
                        mode=SelectSelectorMode.DROPDOWN,
                        translation_key="temp_unit",
                    )
                ),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
