"""The Abfahrt Transit integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
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
from .coordinator import AbfahrtCoordinator

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Abfahrt Transit from a config entry."""
    coordinator = AbfahrtCoordinator(
        hass,
        api_key=entry.data[CONF_API_KEY],
        latitude=entry.data[CONF_LATITUDE],
        longitude=entry.data[CONF_LONGITUDE],
        radius=entry.data.get(CONF_RADIUS, DEFAULT_RADIUS),
        stops=entry.data.get(CONF_STOPS) or None,
        # Entries set up with the old 60 s default would run out of the daily
        # request allowance after about 12 hours, so raise them to the minimum.
        scan_interval=max(
            entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL), MIN_SCAN_INTERVAL
        ),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
