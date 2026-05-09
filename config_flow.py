import voluptuous as vol
import logging
from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, CONF_DEVICE_SN, CONF_BATTERY_SN
from homeassistant import config_entries

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class FelicityConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            _LOGGER.debug("Felicity Config Input: %s", user_input)

            return self.async_create_entry(
                title=f"Felicity Solar ({user_input.get('username')})",
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required("username"): str,
            vol.Required("password"): str,
            vol.Optional(CONF_DEVICE_SN): str,
            vol.Optional(CONF_BATTERY_SN): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )