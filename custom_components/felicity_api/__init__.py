import ssl

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import FelicityAPI
from .coordinator import FelicityCoordinator
from .const import DOMAIN, PLATFORMS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    session = async_get_clientsession(hass)

    # SSL trust-store loading is blocking I/O: perform it in the HA executor.
    # Preserve the pre-existing certificate policy until cloud trust is verified.
    ssl_context = await hass.async_add_executor_job(ssl.create_default_context)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    api = FelicityAPI(
        session,
        entry.data["username"],
        entry.data["password"],
        ssl_context=ssl_context,
    )

    coordinator = FelicityCoordinator(hass, entry, api)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok