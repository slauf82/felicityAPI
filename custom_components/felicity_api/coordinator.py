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


    async def _safe_energy_flow(self, device_sn: str) -> Dict[str, Any]:
        try:
            raw = await self.api.get_energy_flow(device_sn)

            if not isinstance(raw, dict):
                return {}

            if raw.get("status") in (400, 401, 403, 404, 500):
                return {}

            if raw.get("code") not in (None, 200):
                return {}

            data = raw.get("data", raw)
            return data if isinstance(data, dict) else {}

        except Exception as err:
            _LOGGER.warning("Energy flow failed for %s: %s", device_sn, err)
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

    async def _safe_warnings(self) -> list[Dict[str, Any]]:
        try:
            raw = await self.api.get_warnings()

            if not isinstance(raw, dict):
                return []

            if raw.get("status") in (400, 401, 403, 404, 500):
                return []

            if raw.get("code") not in (None, 200):
                return []

            data = raw.get("data", {})
            if not isinstance(data, dict):
                return []

            warnings = data.get("dataList", []) or []
            return [item for item in warnings if isinstance(item, dict)]

        except Exception as err:
            _LOGGER.warning("Warnings fetch failed: %s", err)
            return []

    def _warnings_by_sn(self, warnings: list[Dict[str, Any]]) -> Dict[str, list[Dict[str, Any]]]:
        result: Dict[str, list[Dict[str, Any]]] = {}

        for warning in warnings:
            device_sn = warning.get("deviceSn")
            if not device_sn:
                continue

            result.setdefault(str(device_sn), []).append(warning)

        for device_warnings in result.values():
            device_warnings.sort(
                key=lambda item: self._as_float(
                    self._first(item.get("dataTime"), item.get("createDate")),
                    0,
                ),
                reverse=True,
            )

        return result

    def _apply_warning_state(self, device: Dict[str, Any], warnings: list[Dict[str, Any]]) -> None:
        active_warnings = [
            warning
            for warning in warnings
            if str(warning.get("status", 0)) == "0"
        ]

        latest = active_warnings[0] if active_warnings else (warnings[0] if warnings else {})

        device["activeWarningCount"] = len(active_warnings)
        device["lastWarningName"] = self._first(latest.get("warringName"), latest.get("warningName"), "")
        device["lastWarningCode"] = self._first(latest.get("warnCode"), "")
        device["lastWarningLevel"] = self._first(latest.get("level"), "")
        device["lastWarningType"] = self._first(latest.get("warringTypeStr"), latest.get("warringType"), "")
        device["lastWarningTime"] = self._first(latest.get("dataTimeStr"), latest.get("createDateStr"), "")

        if active_warnings:
            device["warningSummary"] = "; ".join(
                str(self._first(warning.get("warringName"), warning.get("warnCode"), "Warnung"))
                for warning in active_warnings[:5]
            )
        else:
            device["warningSummary"] = "Keine aktive Warnung"

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

    def _merge_device(self, *sources: Dict[str, Any]) -> Dict[str, Any]:
        merged = {}

        for source in sources:
            if isinstance(source, dict):
                merged.update(source)

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
            inverter.get("acTtlInPower"),
            inverter.get("acTtlInpower"),
            inverter.get("totalAcTtlInPower"),
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

        inverter["totalEnergy"] = self._first(inverter.get("totalEnergy"), inverter.get("ePvTotal"))
        inverter["tempMax"] = self._first(inverter.get("tempMax"))
        inverter["devTempMax"] = self._first(inverter.get("devTempMax"))
        inverter["loadPercent"] = self._first(inverter.get("loadPercent"))

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

        battery["remainingBatteryEnergy1"] = self._first(
            battery_snapshot.get("remainingBatteryEnergy1"),
            battery.get("remainingBatteryEnergy1"),
            battery_snapshot.get("ratedEnergy"),
            battery.get("ratedEnergy"),
        )

        battery["tempMax"] = self._first(battery_snapshot.get("tempMax"), battery.get("tempMax"))
        battery["tempMin"] = self._first(battery_snapshot.get("tempMin"), battery.get("tempMin"))
        battery["bmsState"] = self._first(battery_snapshot.get("bmsState"), battery.get("bmsState"))
        battery["bmsChargingState"] = self._first(battery_snapshot.get("bmsChargingState"), battery.get("bmsChargingState"))
        battery["maxVoltage2bms"] = self._first(battery_snapshot.get("maxVoltage2bms"), battery.get("maxVoltage2bms"))
        battery["minVoltage2bms"] = self._first(battery_snapshot.get("minVoltage2bms"), battery.get("minVoltage2bms"))
        battery["cellNumber"] = self._first(battery_snapshot.get("cellNumber"), battery.get("cellNumber"))
        battery["batCount"] = self._first(battery_snapshot.get("batCount"), battery.get("batCount"))
        battery["batLineCount"] = self._first(battery_snapshot.get("batLineCount"), battery.get("batLineCount"))
        battery["ratedEnergy"] = self._first(battery_snapshot.get("ratedEnergy"), battery.get("ratedEnergy"))

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
            inverter_energy_flow = await self._safe_energy_flow(inverter_sn) if inverter_sn else {}
            inverter_basic = await self._safe_basic(inverter_sn) if inverter_sn else {}

            inverter = self._merge_device(
                inverter_list,
                inverter_basic,
                inverter_snapshot,
                inverter_energy_flow,
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

            warnings_raw = await self._safe_warnings()
            warnings_by_sn = self._warnings_by_sn(warnings_raw)

            if inverter_sn and inverter:
                self._apply_warning_state(inverter, warnings_by_sn.get(str(inverter_sn), []))

            if battery_sn and battery:
                self._apply_warning_state(battery, warnings_by_sn.get(str(battery_sn), []))

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

                "activeWarningCount": inverter.get("activeWarningCount"),
                "lastWarningName": inverter.get("lastWarningName"),
                "lastWarningCode": inverter.get("lastWarningCode"),
                "lastWarningLevel": inverter.get("lastWarningLevel"),
                "lastWarningType": inverter.get("lastWarningType"),
                "lastWarningTime": inverter.get("lastWarningTime"),
                "warningSummary": inverter.get("warningSummary"),

                "dataTimeStr": inverter.get("dataTimeStr"),
            }
            
            devices_by_sn = {}

            if inverter_sn and inverter:
                devices_by_sn[str(inverter_sn)] = inverter

            if battery_sn and battery:
                devices_by_sn[str(battery_sn)] = battery

            _LOGGER.debug(
                "Felicity devices_by_sn keys: %s",
                list(devices_by_sn.keys()),
            )

            return {
                "snapshot": legacy_snapshot,
                "basic": legacy_snapshot,
                "device": legacy_snapshot,
                "devices_all": list_data,

                # Neue dynamische Struktur
                "devices_by_sn": devices_by_sn,

                # Legacy-Kompatibilität
                "devices": {
                    "inverter": inverter,
                    "battery": battery,
                },
            }

        except Exception as err:
            raise UpdateFailed(f"Felicity update failed: {err}") from err
