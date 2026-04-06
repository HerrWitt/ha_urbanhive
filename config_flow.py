"""Config flow for UrbanHive integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import UrbanHiveApiClient
from .const import DOMAIN

class UrbanHiveConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for UrbanHive."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input["host"]
            
            try:
                # Validierung: Können wir die Farm erreichen?
                session = async_get_clientsession(self.hass)
                client = UrbanHiveApiClient(host, session)
                await client.async_get_farm_info()
                
                # Wenn erfolgreich, Eintrag erstellen
                return self.async_create_entry(
                    title=f"UrbanHive Farm ({host})", 
                    data=user_input
                )
            except Exception:
                errors["base"] = "cannot_connect"

        # Formular anzeigen
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
            }),
            errors=errors,
        )
