"""Config flow for the Abfahrt Transit integration."""

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import (
    API_URL,
    CONF_API_KEY,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_RADIUS,
    CONF_SCAN_INTERVAL,
    CONF_STOPS,
    DEFAULT_RADIUS,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MIN_SCAN_INTERVAL,
)


async def validate_input(hass: HomeAssistant, data: dict) -> dict:
    """Validate the user input by making a test API call."""
    params: dict[str, str | int | float] = {
        "lat": data[CONF_LATITUDE],
        "lon": data[CONF_LONGITUDE],
        "radius": data.get(CONF_RADIUS, DEFAULT_RADIUS),
        "limit": 1,
    }

    if data.get(CONF_STOPS):
        params["stops"] = data[CONF_STOPS]

    headers = {"x-api-key": data[CONF_API_KEY]}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            API_URL,
            params=params,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as resp:
            if resp.status == 401:
                raise InvalidAuth
            if resp.status != 200:
                raise CannotConnect

            result = await resp.json()
            if "error" in result:
                raise CannotConnect

            return {
                "title": result.get("city") or result.get("region", "Abfahrt"),
            }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Abfahrt Transit."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

        # Pre-fill with HA home location
        home_lat = self.hass.config.latitude
        home_lon = self.hass.config.longitude

        schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_LATITUDE, default=home_lat): vol.Coerce(float),
                vol.Required(CONF_LONGITUDE, default=home_lon): vol.Coerce(float),
                vol.Optional(CONF_RADIUS, default=DEFAULT_RADIUS): vol.All(
                    vol.Coerce(int), vol.Range(min=100, max=5000)
                ),
                vol.Optional(CONF_STOPS, default=""): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL, max=900)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
