"""Privacy-first, on-demand Home Assistant diagnostics for Felicity API.

No credentials, device identifiers, measurements, free-form cloud values,
raw API responses or exception messages are exported.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Any

from homeassistant.const import __version__ as HA_VERSION

from .const import DOMAIN

# Unknown field names can themselves contain identifying data. Export only
# conventional API identifier names and reject suspicious names.
_FIELD_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,63}$")
_PRIVATE_NAME = re.compile(
    r"(token|secret|password|passwd|auth|cookie|session|serial|devicesn|"
    r"username|email|phone|address|location|latitude|longitude|gps|"
    r"wifi|ssid|macaddress|imei|imsi|account|customer|owner|user|"
    r"ipaddress|apikey|keyid|credential)", re.IGNORECASE
)


def _safe_field_name(value: Any) -> bool:
    return isinstance(value, str) and bool(_FIELD_NAME.fullmatch(value)) and not _PRIVATE_NAME.search(value)


def _value_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "other"


def _schema(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {}
    return {
        name: {"type": _value_type(value), "has_value": value is not None and value != ""}
        for name, value in sorted(record.items())
        if _safe_field_name(name)
    }


def _history_summary(history: Any) -> dict[str, Any]:
    """Never export untrusted error text, identifiers or arbitrary response values."""
    if not isinstance(history, dict):
        return {"status": "unknown"}
    status = history.get("status")
    if status not in ("data", "empty", "error"):
        status = "unknown"
    points = history.get("point_count")
    result: dict[str, Any] = {"status": status}
    if isinstance(points, int) and not isinstance(points, bool) and 0 <= points <= 1000000:
        result["point_count"] = points
    for key in ("response_keys", "fields"):
        values = history.get(key)
        if isinstance(values, list):
            result[key] = sorted({x for x in values if _safe_field_name(x)})[:100]
    # An exception message can include credentials, URLs or serial numbers.
    if status == "error":
        result["error_details"] = "See local Home Assistant logs; raw exception omitted for privacy"
    return result


async def async_get_config_entry_diagnostics(hass, entry) -> dict[str, Any]:
    coordinator = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    if coordinator is None:
        return {"diagnostics_version": 1, "error": "coordinator_unavailable"}

    data = coordinator.data if isinstance(coordinator.data, dict) else {}
    listed = [d for d in (data.get("devices_all") or []) if isinstance(d, dict)]
    mapped = data.get("devices_by_sn") or {}
    if not isinstance(mapped, dict):
        mapped = {}
    devices = [d for d in mapped.values() if isinstance(d, dict)]

    # Do not export keys of devices_by_sn or history_diagnostics: these are
    # device serial numbers. Do not export entry.data/options/title either.
    device_types = Counter(
        str(d.get("deviceType")) for d in listed
        if str(d.get("deviceType")) in ("OC", "BP")
    )
    summaries = []
    for device in devices[:30]:
        dtype = device.get("deviceType")
        summaries.append({
            "device_type": dtype if dtype in ("OC", "BP") else "other_or_unknown",
            "fields": _schema(device),
        })

    history = getattr(coordinator, "history_diagnostics", {})
    history_summaries = []
    if isinstance(history, dict):
        history_summaries = [_history_summary(item) for item in list(history.values())[:30]]

    return {
        "diagnostics_version": 1,
        "integration_version": "1.4.5",
        "home_assistant_version": HA_VERSION,
        "privacy": "No credentials, serial numbers, raw measurements or free-form values",
        "device_count": len(listed),
        "device_type_counts": dict(sorted(device_types.items())),
        "mapped_device_count": len(devices),
        "device_schemas": summaries,
        "history": history_summaries,
    }
