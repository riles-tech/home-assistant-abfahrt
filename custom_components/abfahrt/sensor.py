"""Sensor platform for the Abfahrt Transit integration."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AbfahrtCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Abfahrt sensors from a config entry."""
    coordinator: AbfahrtCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AbfahrtDeparturesSensor(coordinator, entry)])


class AbfahrtDeparturesSensor(CoordinatorEntity, SensorEntity):
    """Sensor showing transit departures."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:bus-clock"

    def __init__(self, coordinator: AbfahrtCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_departures"
        self._attr_name = "Departures"

    @property
    def native_value(self) -> int | None:
        """Return the number of upcoming departures."""
        if not self.coordinator.data:
            return None
        departures = self.coordinator.data.get("departures", [])
        return len(departures)

    @property
    def extra_state_attributes(self) -> dict:
        """Return departure data as attributes."""
        if not self.coordinator.data:
            return {}

        data = self.coordinator.data
        departures = data.get("departures", [])

        attrs = {
            "departures": departures,
            "stations": data.get("stations", []),
            "region": data.get("region"),
            "city": data.get("city"),
            "realtime": data.get("realtime"),
        }

        # Convenience attributes for the next departure
        if departures:
            next_dep = departures[0]
            attrs["next_line"] = next_dep.get("line")
            attrs["next_direction"] = next_dep.get("direction")
            attrs["next_time"] = next_dep.get("time")
            attrs["next_delay"] = next_dep.get("delay", 0)
            attrs["next_mode"] = next_dep.get("mode")
            attrs["next_stop"] = next_dep.get("stop")

        return attrs
