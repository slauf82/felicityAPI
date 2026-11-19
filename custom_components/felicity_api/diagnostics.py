from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data

from .const import DOMAIN

TO_REDACT = {
    "password",
    "token",
    "accessToken",
    "refreshToken",
    "username",
    "deviceSn",
    "device_sn",
    "serialNumber",
    "serial",
    "email",
    "phone",
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
        "device_count": len(data.get("devices_all") or []),
        "device_types": sorted({str(d.get("deviceType") or "unknown") for d in (data.get("devices_all") or []) if isinstance(d, dict)}),
        "history_diagnostics": list(coordinator.history_diagnostics.values()),
    }

    return async_redact_data(diagnostics, TO_REDACT)
