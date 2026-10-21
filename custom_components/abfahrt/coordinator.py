"""DataUpdateCoordinator for the Abfahrt Transit integration."""

import logging
from datetime import timedelta

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL

_LOGGER = logging.getLogger(__name__)


class AbfahrtCoordinator(DataUpdateCoordinator):
    """Fetch departure data from the Abfahrt API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        latitude: float,
        longitude: float,
        radius: int = 500,
        stops: str | None = None,
        scan_interval: int = 180,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Abfahrt Transit",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.stops = stops

    async def _async_update_data(self) -> dict:
        """Fetch data from the API."""
        params: dict[str, str | int | float] = {
            "lat": self.latitude,
            "lon": self.longitude,
        }

        if self.stops:
            params["stops"] = self.stops
        else:
            params["radius"] = self.radius

        headers = {"x-api-key": self.api_key}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    API_URL,
                    params=params,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    if resp.status == 429:
                        raise UpdateFailed("API rate limit exceeded")
                    if resp.status == 401:
                        raise UpdateFailed("Invalid API key")
                    if resp.status != 200:
                        raise UpdateFailed(f"API returned HTTP {resp.status}")

                    data = await resp.json()

                    if "error" in data:
                        raise UpdateFailed(f"API error: {data['error']}")

                    return data

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Connection error: {err}") from err
