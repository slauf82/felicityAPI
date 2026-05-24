from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data

from .const import DOMAIN

TO_REDACT = {
    "password",
    "token",
    "accessToken",
    "refreshToken",
}


async def async_get_config_entry_diagnostics(
    hass,
    entry,
) -> dict[str, Any]:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    data = coordinator.data or {}

    diagnostics = {
        "entry": {
            "title": entry.title,
            "data": dict(entry.data),
            "options": dict(entry.options),
        },
        "devices": data.get("devices"),
        "devices_by_sn": data.get("devices_by_sn"),
        "devices_all": data.get("devices_all"),
        "snapshot": data.get("snapshot"),
    }

    return async_redact_data(diagnostics, TO_REDACT)
