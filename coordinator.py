from __future__ import annotations

from datetime import timedelta
from typing import Any, Dict
import logging
import json

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEVICE_TYPE_INVERTER, DEVICE_TYPE_BATTERY

_LOGGER = logging.getLogger(__name__)


class FelicityCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry, api):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.entry = entry
        self.api = api

    async def _safe_snapshot(self, device_sn: str) -> Dict[str, Any]:
        try:
            raw = await self.api.get_snapshot(device_sn)

            if not isinstance(raw, dict):
                return {}

            if raw.get("status") in (400, 401, 403, 404, 500):
                return {}

            if raw.get("code") not in (None, 200):
                return {}

            data = raw.get("data", raw)

            if isinstance(data, dict):
                self._parse_hot_json(data)
                return data

            return {}

        except Exception as err:
            _LOGGER.warning("Snapshot failed for %s: %s", device_sn, err)
            return {}

    async def _safe_basic(self, device_sn: str) -> Dict[str, Any]:
        try:
            raw = await self.api.get_device_basic(device_sn)

            if not isinstance(raw, dict):
                return {}

            data = raw.get("data", raw)
            return data if isinstance(data, dict) else {}

        except Exception:
            return {}

    def _parse_hot_json(self, data: Dict[str, Any]) -> None:
        hot = data.get("hotJson")

        if isinstance(hot, str) and hot:
            try:
                parsed = json.loads(hot)
                if isinstance(parsed, dict):
                    data.update(parsed)
            except Exception:
                pass

    def _extract_device_list(self, list_raw):
        if isinstance(list_raw, dict):
            return list_raw.get("data", {}).get("dataList", []) or []
        if isinstance(list_raw, list):
            return list_raw
        return []

    def _find_device(self, device_list, device_sn):
        if not device_sn:
            return {}

        for dev in device_list:
            if isinstance(dev, dict) and str(dev.get("deviceSn")) == str(device_sn):
                return dev

        return {}

    def _find_inverter_auto(self, device_list):
        for dev in device_list:
            if not isinstance(dev, dict):
                continue

            if str(dev.get("deviceType") or "").upper() == DEVICE_TYPE_INVERTER:
                return dev

        for dev in device_list:
            if not isinstance(dev, dict):
                continue

            model = str(dev.get("deviceModel") or "").upper()
            type_name = str(dev.get("type") or "").upper()
            alias = str(dev.get("alias") or "").lower()

            if "IVGM" in model or "IVGM" in type_name:
                return dev

            if "inverter" in alias or "wechselrichter" in alias:
                return dev

        return {}

    def _find_battery_auto(self, device_list):
        for dev in device_list:
            if not isinstance(dev, dict):
                continue

            if str(dev.get("deviceType") or "").upper() == DEVICE_TYPE_BATTERY:
                return dev

        for dev in device_list:
            if not isinstance(dev, dict):
                continue

            alias = str(dev.get("alias") or "").lower()

            if alias.startswith("batterie") or alias.startswith("battery"):
                return dev

        for dev in device_list:
            if not isinstance(dev, dict):
                continue

            if dev.get("battSoc") is not None:
                return dev

            if dev.get("bmsPower") is not None:
                return dev

        for dev in device_list:
            if not isinstance(dev, dict):
                continue

            model = str(dev.get("deviceModel") or "").upper()
            type_name = str(dev.get("type") or "").upper()

            if "LUX" in model or "LUX" in type_name:
                return dev

        return {}

    def _first(self, *values):
        for value in values:
            if value not in (None, "", "unknown", "unavailable", "null"):
                return value
        return None

    def _as_float(self, value, fallback=0.0):
        try:
            return float(value)
        except Exception:
            return fallback

    def _merge_device(
        self,
        list_device: Dict[str, Any],
        basic: Dict[str, Any],
        snapshot: Dict[str, Any],
    ) -> Dict[str, Any]:
        merged = {}
        merged.update(list_device or {})
        merged.update(basic or {})
        merged.update(snapshot or {})

        if merged.get("deviceSn") is not None:
            merged["deviceSn"] = str(merged.get("deviceSn"))

        return merged

    def _build_energy_state(self, inverter: Dict[str, Any]) -> str:
        pv = self._as_float(inverter.get("pvTotalPower"))

        grid = self._as_float(
            self._first(
                inverter.get("acTtlInpower"),
                inverter.get("ctPower"),
                inverter.get("ctAcTtlInPower"),
            )
        )

        bat = self._as_float(
            self._first(
                inverter.get("emsPower"),
                inverter.get("bmsPower"),
            )
        )

        if pv > 0 and grid < 0:
            return "Produktion & Einspeisung"

        if pv > 0 and grid > 0:
            return "Produktion & Netzbezug"

        if pv == 0 and grid > 0:
            return "Nur Netzbetrieb"

        if bat < 0:
            return "Batterie entlädt"

        if bat > 0:
            return "Batterie lädt"

        return "Leerlauf"

    def _normalize_inverter(self, inverter: Dict[str, Any]) -> None:
        inverter["alias"] = self._first(
            inverter.get("alias"),
            inverter.get("plantName"),
            "Garage",
        )

        inverter["firmwareVersion"] = self._first(
            inverter.get("moduleVersion"),
            inverter.get("collectorVersion2"),
            inverter.get("controlVersion"),
            inverter.get("firmwareVersion"),
        )

        inverter["pvTotalPower"] = self._first(inverter.get("pvTotalPower"))
        inverter["pv1Power"] = self._first(inverter.get("pvPower"), inverter.get("pv1Power"))
        inverter["pv2Power"] = self._first(inverter.get("pv2Power"))
        inverter["pv3Power"] = self._first(inverter.get("pv3Power"))
        inverter["pv4Power"] = self._first(inverter.get("pv4Power"))

        inverter["acTtlInpower"] = self._first(
            inverter.get("acTtlInpower"),
            inverter.get("ctPower"),
            inverter.get("ctAcTtlInPower"),
        )

        grid = self._as_float(inverter.get("acTtlInpower"), None)

        if grid is not None:
            inverter["grid_import"] = abs(grid) if grid < 0 else 0
            inverter["grid_export"] = grid if grid > 0 else 0
        else:
            inverter["grid_import"] = None
            inverter["grid_export"] = None

        inverter["ctPower"] = self._first(
            inverter.get("totalConsumPower"),
            inverter.get("ctPower"),
            inverter.get("meterPower"),
        )

        inverter["ePvToday"] = self._first(inverter.get("ePvToday"))
        inverter["eToday"] = self._first(inverter.get("eToday"))
        inverter["eGridFeedToday"] = self._first(inverter.get("eGridFeedToday"))
        inverter["eGridInToday"] = self._first(inverter.get("eGridInToday"))

        inverter["eBatCharToday"] = self._first(
            inverter.get("eBatCharToday"),
            inverter.get("ebatCharToday"),
        )

        inverter["eBatDisCharToday"] = self._first(
            inverter.get("eBatDisCharToday"),
            inverter.get("ebatDisCharToday"),
        )

        inverter["workingMode"] = self._first(
            inverter.get("workModeStr"),
            inverter.get("operMStr"),
            inverter.get("workMode"),
            "unknown",
        )

        inverter["energyState"] = self._build_energy_state(inverter)
        inverter["alarmCount"] = inverter.get("warningCount") or 0
        inverter["alarmText"] = self._first(inverter.get("failCode"), "")

    def _normalize_battery(
        self,
        battery: Dict[str, Any],
        battery_snapshot: Dict[str, Any],
        inverter: Dict[str, Any],
        battery_sn: str,
    ) -> None:
        battery["deviceSn"] = str(
            self._first(
                battery_snapshot.get("deviceSn"),
                battery.get("deviceSn"),
                battery_sn,
            )
        )

        battery["alias"] = self._first(
            battery_snapshot.get("alias"),
            battery.get("alias"),
            "Batterie-Garage",
        )

        battery["deviceType"] = self._first(
            battery_snapshot.get("deviceType"),
            battery.get("deviceType"),
            DEVICE_TYPE_BATTERY,
        )

        battery["deviceModel"] = self._first(
            battery_snapshot.get("deviceModel"),
            battery.get("deviceModel"),
        )

        battery["subType"] = self._first(
            battery_snapshot.get("subType"),
            battery.get("subType"),
        )

        battery["status"] = self._first(
            battery_snapshot.get("status"),
            battery.get("status"),
        )

        battery["firmwareVersion"] = self._first(
            battery_snapshot.get("moduleVersion"),
            battery_snapshot.get("collectorVersion2"),
            battery_snapshot.get("controlVersion"),
            battery.get("moduleVersion"),
            battery.get("collectorVersion2"),
            battery.get("controlVersion"),
            battery.get("firmwareVersion"),
        )

        battery["emsSoc"] = self._first(
            battery_snapshot.get("emsSoc"),
            battery_snapshot.get("battSoc"),
            battery.get("emsSoc"),
            battery.get("battSoc"),
        )

        battery["emsPower"] = self._first(
            battery_snapshot.get("bmsPower"),
            battery_snapshot.get("emsPower"),
            battery.get("bmsPower"),
            battery.get("emsPower"),
        )

        battery["emsVoltage"] = self._first(
            battery_snapshot.get("emsVoltage"),
            battery_snapshot.get("battVolt"),
            battery.get("emsVoltage"),
            battery.get("battVolt"),
        )

        battery["emsCurrent"] = self._first(
            battery_snapshot.get("emsCurrent"),
            battery_snapshot.get("battCurr"),
            battery.get("emsCurrent"),
            battery.get("battCurr"),
        )

        battery["emsSoh"] = self._first(
            battery_snapshot.get("battSoh"),
            battery_snapshot.get("emsSoh"),
            battery.get("battSoh"),
            battery.get("emsSoh"),
        )

        battery["emsCapacity"] = self._first(
            battery_snapshot.get("battCapacity"),
            battery_snapshot.get("batteryCapacity"),
            battery_snapshot.get("totalEmsCapacity"),
            battery.get("battCapacity"),
            battery.get("batteryCapacity"),
            battery.get("totalEmsCapacity"),
        )

        battery["eBatCharToday"] = self._first(
            inverter.get("eBatCharToday"),
            inverter.get("ebatCharToday"),
            battery_snapshot.get("eBatCharToday"),
            battery_snapshot.get("ebatCharToday"),
        )

        battery["eBatDisCharToday"] = self._first(
            inverter.get("eBatDisCharToday"),
            inverter.get("ebatDisCharToday"),
            battery_snapshot.get("eBatDisCharToday"),
            battery_snapshot.get("ebatDisCharToday"),
        )

        battery["workingMode"] = self._first(
            battery_snapshot.get("workModeStr"),
            battery_snapshot.get("operMStr"),
            battery.get("workModeStr"),
            battery.get("operMStr"),
            "unknown",
        )

        battery["energyState"] = self._first(
            battery_snapshot.get("status"),
            battery.get("status"),
            "unknown",
        )

        battery["alarmCount"] = self._first(
            battery_snapshot.get("warningCount"),
            battery.get("warningCount"),
            0,
        )

        battery["alarmText"] = self._first(
            battery_snapshot.get("failCode"),
            battery.get("failCode"),
            "",
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        try:
            configured_inverter_sn = self.entry.data.get("device_sn")
            configured_battery_sn = self.entry.data.get("battery_sn")

            list_raw = await self.api.get_device_list()
            list_data = self._extract_device_list(list_raw)

            # =====================================================
            # AUTO-ERKENNUNG ZUERST
            # =====================================================

            inverter_list = self._find_inverter_auto(list_data)
            battery_list = self._find_battery_auto(list_data)

            # =====================================================
            # MANUELLE SERIENNUMMERN NUR ALS FALLBACK
            # =====================================================

            if not inverter_list and configured_inverter_sn:
                inverter_list = self._find_device(list_data, configured_inverter_sn)

            if not battery_list and configured_battery_sn:
                battery_list = self._find_device(list_data, configured_battery_sn)

            inverter_sn = str(
                inverter_list.get("deviceSn")
                or configured_inverter_sn
                or ""
            )

            battery_sn = str(
                battery_list.get("deviceSn")
                or configured_battery_sn
                or ""
            )

            _LOGGER.warning("Felicity auto inverter_sn: %s", inverter_sn)
            _LOGGER.warning("Felicity auto battery_sn: %s", battery_sn)

            inverter_snapshot = await self._safe_snapshot(inverter_sn) if inverter_sn else {}
            inverter_basic = await self._safe_basic(inverter_sn) if inverter_sn else {}

            inverter = self._merge_device(
                inverter_list,
                inverter_basic,
                inverter_snapshot,
            )

            self._normalize_inverter(inverter)

            battery_snapshot = {}
            battery_basic = {}
            battery = {}

            if battery_sn:
                battery_snapshot = await self._safe_snapshot(battery_sn)
                battery_basic = await self._safe_basic(battery_sn)

                battery = self._merge_device(
                    battery_list,
                    battery_basic,
                    battery_snapshot,
                )

                self._normalize_battery(
                    battery,
                    battery_snapshot,
                    inverter,
                    battery_sn,
                )

            legacy_snapshot = {
                "deviceSn": inverter.get("deviceSn"),
                "deviceModel": inverter.get("deviceModel"),
                "deviceType": inverter.get("deviceType"),
                "subType": inverter.get("subType"),
                "status": inverter.get("status"),
                "firmwareVersion": inverter.get("firmwareVersion"),

                "pvTotalPower": inverter.get("pvTotalPower"),
                "pv1Power": inverter.get("pv1Power"),
                "pv2Power": inverter.get("pv2Power"),
                "pv3Power": inverter.get("pv3Power"),
                "pv4Power": inverter.get("pv4Power"),

                "acTtlInpower": inverter.get("acTtlInpower"),
                "grid_import": inverter.get("grid_import"),
                "grid_export": inverter.get("grid_export"),
                "ctPower": inverter.get("ctPower"),

                "emsSoc": self._first(
                    inverter.get("emsSoc"),
                    battery.get("emsSoc"),
                ),

                "emsPower": self._first(
                    inverter.get("emsPower"),
                    battery.get("emsPower"),
                ),

                "ePvToday": inverter.get("ePvToday"),
                "eToday": inverter.get("eToday"),
                "eGridFeedToday": inverter.get("eGridFeedToday"),
                "eGridInToday": inverter.get("eGridInToday"),

                "eBatCharToday": self._first(
                    inverter.get("eBatCharToday"),
                    battery.get("eBatCharToday"),
                ),

                "eBatDisCharToday": self._first(
                    inverter.get("eBatDisCharToday"),
                    battery.get("eBatDisCharToday"),
                ),

                "energyState": inverter.get("energyState"),
                "workingMode": inverter.get("workingMode"),
                "alarmCount": inverter.get("alarmCount"),
                "alarmText": inverter.get("alarmText"),

                "dataTimeStr": inverter.get("dataTimeStr"),
            }

            return {
                "snapshot": legacy_snapshot,
                "basic": legacy_snapshot,
                "device": legacy_snapshot,
                "devices_all": list_data,
                "devices": {
                    "inverter": inverter,
                    "battery": battery,
                },
            }

        except Exception as err:
            raise UpdateFailed(f"Felicity update failed: {err}") from err