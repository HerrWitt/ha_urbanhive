"""API Client for UrbanHive Farm."""
import logging
import aiohttp

_LOGGER = logging.getLogger(__name__)

class UrbanHiveApiClient:
    def __init__(self, host: str, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._host = host
        self._session = session
        self._base_url = f"http://{self._host}"

    async def async_get_farm_info(self) -> dict:
        """Get farm info from the API."""
        url = f"{self._base_url}/farm-info"
        try:
            async with self._session.get(url, timeout=10) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as exception:
            _LOGGER.error("Fehler beim Abrufen der Farm-Daten von %s: %s", url, exception)
            raise
