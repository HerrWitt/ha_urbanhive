"""The UrbanHive integration."""
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import UrbanHiveApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up UrbanHive from a config entry."""
    host = entry.data["host"]
    session = async_get_clientsession(hass)
    client = UrbanHiveApiClient(host, session)

    async def async_update_data():
        """Fetch data from API endpoint."""
        try:
            return await client.async_get_farm_info()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    # Coordinator definieren (Intervall: 30 Sekunden)
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=30),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Leitet die Einrichtung an die Sensor-Plattform weiter
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
