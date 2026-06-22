from __future__ import annotations

from typing import Any, Optional

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfTemperature,
    PERCENTAGE,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, DEVICE_TYPE_INVERTER, DEVICE_TYPE_BATTERY


STRING_KEYS = {
    "deviceSn",
    "deviceModel",
    "deviceType",
    "subType",
    "status",
    "firmwareVersion",
    "energyState",
    "workingMode",
    "alarmText",
    "dataTimeStr",
    "lastWarningName",
    "lastWarningCode",
    "lastWarningType",
    "lastWarningTime",
    "warningSummary",
}


def _power_sensor(key: str) -> SensorEntityDescription:
    return SensorEntityDescription(
        key=key,
        translation_key=key,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    )


def _voltage_sensor(key: str) -> SensorEntityDescription:
    return SensorEntityDescription(
        key=key,
        translation_key=key,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    )


def _current_sensor(key: str) -> SensorEntityDescription:
    return SensorEntityDescription(
        key=key,
        translation_key=key,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    )


def _frequency_sensor(key: str) -> SensorEntityDescription:
    return SensorEntityDescription(
        key=key,
        translation_key=key,
        native_unit_of_measurement="Hz",
        state_class=SensorStateClass.MEASUREMENT,
    )


def _temperature_sensor(key: str) -> SensorEntityDescription:
    return SensorEntityDescription(
        key=key,
        translation_key=key,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    )


def _energy_sensor(key: str, total_increasing: bool = False) -> SensorEntityDescription:
    return SensorEntityDescription(
        key=key,
        translation_key=key,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING if total_increasing else None,
    )


SENSOR_MAP = {
    "deviceSn": SensorEntityDescription(key="deviceSn", translation_key="deviceSn"),
    "deviceModel": SensorEntityDescription(key="deviceModel", translation_key="deviceModel"),
    "deviceType": SensorEntityDescription(key="deviceType", translation_key="deviceType"),
    "subType": SensorEntityDescription(key="subType", translation_key="subType"),
    "status": SensorEntityDescription(key="status", translation_key="status"),
    "firmwareVersion": SensorEntityDescription(key="firmwareVersion", translation_key="firmwareVersion"),

    "energyState": SensorEntityDescription(key="energyState", translation_key="energyState"),
    "workingMode": SensorEntityDescription(key="workingMode", translation_key="workingMode"),
    "alarmCount": SensorEntityDescription(
        key="alarmCount",
        translation_key="alarmCount",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "alarmText": SensorEntityDescription(key="alarmText", translation_key="alarmText"),

    "activeWarningCount": SensorEntityDescription(
        key="activeWarningCount",
        translation_key="activeWarningCount",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "lastWarningName": SensorEntityDescription(key="lastWarningName", translation_key="lastWarningName"),
    "lastWarningCode": SensorEntityDescription(key="lastWarningCode", translation_key="lastWarningCode"),
    "lastWarningLevel": SensorEntityDescription(
        key="lastWarningLevel",
        translation_key="lastWarningLevel",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "lastWarningType": SensorEntityDescription(key="lastWarningType", translation_key="lastWarningType"),
    "lastWarningTime": SensorEntityDescription(key="lastWarningTime", translation_key="lastWarningTime"),
    "warningSummary": SensorEntityDescription(key="warningSummary", translation_key="warningSummary"),

    "pvTotalPower": SensorEntityDescription(
        key="pvTotalPower",
        translation_key="pvTotalPower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "pv1Power": SensorEntityDescription(
        key="pv1Power",
        translation_key="pv1Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "pv2Power": SensorEntityDescription(
        key="pv2Power",
        translation_key="pv2Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "pv3Power": SensorEntityDescription(
        key="pv3Power",
        translation_key="pv3Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "pv4Power": SensorEntityDescription(
        key="pv4Power",
        translation_key="pv4Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    "acTtlInpower": SensorEntityDescription(
        key="acTtlInpower",
        translation_key="acTtlInpower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "grid_import": SensorEntityDescription(
        key="grid_import",
        translation_key="grid_import",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "grid_export": SensorEntityDescription(
        key="grid_export",
        translation_key="grid_export",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    "ctPower": SensorEntityDescription(
        key="ctPower",
        translation_key="ctPower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    "emsSoc": SensorEntityDescription(
        key="emsSoc",
        translation_key="emsSoc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "emsPower": SensorEntityDescription(
        key="emsPower",
        translation_key="emsPower",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "emsVoltage": SensorEntityDescription(
        key="emsVoltage",
        translation_key="emsVoltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "emsCurrent": SensorEntityDescription(
        key="emsCurrent",
        translation_key="emsCurrent",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "emsSoh": SensorEntityDescription(
        key="emsSoh",
        translation_key="emsSoh",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "emsCapacity": SensorEntityDescription(
        key="emsCapacity",
        translation_key="emsCapacity",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),

    "ePvToday": SensorEntityDescription(
        key="ePvToday",
        translation_key="ePvToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    "eToday": SensorEntityDescription(
        key="eToday",
        translation_key="eToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    "eGridFeedToday": SensorEntityDescription(
        key="eGridFeedToday",
        translation_key="eGridFeedToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    "eGridInToday": SensorEntityDescription(
        key="eGridInToday",
        translation_key="eGridInToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    "eBatCharToday": SensorEntityDescription(
        key="eBatCharToday",
        translation_key="eBatCharToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    "eBatDisCharToday": SensorEntityDescription(
        key="eBatDisCharToday",
        translation_key="eBatDisCharToday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),

    # Inverter live values from get_energy_flow / snapshot
    "pvVolt": _voltage_sensor("pvVolt"),
    "pv2Volt": _voltage_sensor("pv2Volt"),
    "pvInCurr": _current_sensor("pvInCurr"),
    "pv2InCurr": _current_sensor("pv2InCurr"),

    "acRInVolt": _voltage_sensor("acRInVolt"),
    "acSInVolt": _voltage_sensor("acSInVolt"),
    "acTInVolt": _voltage_sensor("acTInVolt"),
    "acRInCurr": _current_sensor("acRInCurr"),
    "acSInCurr": _current_sensor("acSInCurr"),
    "acTInCurr": _current_sensor("acTInCurr"),
    "acRInFreq": _frequency_sensor("acRInFreq"),
    "acSInFreq": _frequency_sensor("acSInFreq"),
    "acTInFreq": _frequency_sensor("acTInFreq"),

    "acROutVolt": _voltage_sensor("acROutVolt"),
    "acSOutVolt": _voltage_sensor("acSOutVolt"),
    "acTOutVolt": _voltage_sensor("acTOutVolt"),
    "acROutCurr": _current_sensor("acROutCurr"),
    "acSOutCurr": _current_sensor("acSOutCurr"),
    "acTOutCurr": _current_sensor("acTOutCurr"),
    "acROutFreq": _frequency_sensor("acROutFreq"),
    "acSOutFreq": _frequency_sensor("acSOutFreq"),
    "acTOutFreq": _frequency_sensor("acTOutFreq"),

    "loadPercent": SensorEntityDescription(
        key="loadPercent",
        translation_key="loadPercent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "tempMax": _temperature_sensor("tempMax"),
    "tempMin": _temperature_sensor("tempMin"),
    "devTempMax": _temperature_sensor("devTempMax"),

    "totalEnergy": _energy_sensor("totalEnergy"),
    "ePvMonth": _energy_sensor("ePvMonth"),
    "ePvYear": _energy_sensor("ePvYear"),
    "ePvTotal": _energy_sensor("ePvTotal"),
    "eGridFeedMonth": _energy_sensor("eGridFeedMonth"),
    "eGridFeedYear": _energy_sensor("eGridFeedYear"),
    "eGridFeedTotal": _energy_sensor("eGridFeedTotal"),
    "eBatCharMonth": _energy_sensor("eBatCharMonth"),
    "eBatCharYear": _energy_sensor("eBatCharYear"),
    "eBatCharTotal": _energy_sensor("eBatCharTotal"),
    "eBatDisCharMonth": _energy_sensor("eBatDisCharMonth"),
    "eBatDisCharYear": _energy_sensor("eBatDisCharYear"),
    "eBatDisCharTotal": _energy_sensor("eBatDisCharTotal"),

    # Battery snapshot values
    "remainingBatteryEnergy1": _energy_sensor("remainingBatteryEnergy1"),
    "ratedEnergy": _energy_sensor("ratedEnergy"),
    "bmsState": SensorEntityDescription(key="bmsState", translation_key="bmsState"),
    "bmsChargingState": SensorEntityDescription(key="bmsChargingState", translation_key="bmsChargingState"),
    "maxVoltage2bms": _voltage_sensor("maxVoltage2bms"),
    "minVoltage2bms": _voltage_sensor("minVoltage2bms"),
    "cellNumber": SensorEntityDescription(key="cellNumber", translation_key="cellNumber", state_class=SensorStateClass.MEASUREMENT),
    "batCount": SensorEntityDescription(key="batCount", translation_key="batCount", state_class=SensorStateClass.MEASUREMENT),
    "batLineCount": SensorEntityDescription(key="batLineCount", translation_key="batLineCount", state_class=SensorStateClass.MEASUREMENT),

}


INVERTER_KEYS = [
    "deviceSn",
    "deviceModel",
    "deviceType",
    "subType",
    "status",
    "firmwareVersion",
    "energyState",
    "workingMode",
    "alarmCount",
    "alarmText",
    "activeWarningCount",
    "lastWarningName",
    "lastWarningCode",
    "lastWarningLevel",
    "lastWarningType",
    "lastWarningTime",
    "warningSummary",
    "pvTotalPower",
    "pv1Power",
    "pv2Power",
    "pv3Power",
    "pv4Power",
    "acTtlInpower",
    "grid_import",
    "grid_export",
    "ctPower",
    "emsSoc",
    "emsPower",
    "ePvToday",
    "eToday",
    "eGridFeedToday",
    "eGridInToday",
    "pvVolt",
    "pv2Volt",
    "pvInCurr",
    "pv2InCurr",
    "acRInVolt",
    "acSInVolt",
    "acTInVolt",
    "acRInCurr",
    "acSInCurr",
    "acTInCurr",
    "acRInFreq",
    "acSInFreq",
    "acTInFreq",
    "acROutVolt",
    "acSOutVolt",
    "acTOutVolt",
    "acROutCurr",
    "acSOutCurr",
    "acTOutCurr",
    "acROutFreq",
    "acSOutFreq",
    "acTOutFreq",
    "loadPercent",
    "tempMax",
    "devTempMax",
    "totalEnergy",
    "ePvMonth",
    "ePvYear",
    "ePvTotal",
    "eGridFeedMonth",
    "eGridFeedYear",
    "eGridFeedTotal",
    "eBatCharMonth",
    "eBatCharYear",
    "eBatCharTotal",
    "eBatDisCharMonth",
    "eBatDisCharYear",
    "eBatDisCharTotal",
]

BATTERY_KEYS = [
    "deviceSn",
    "deviceModel",
    "deviceType",
    "subType",
    "status",
    "firmwareVersion",
    "energyState",
    "workingMode",
    "alarmCount",
    "alarmText",
    "activeWarningCount",
    "lastWarningName",
    "lastWarningCode",
    "lastWarningLevel",
    "lastWarningType",
    "lastWarningTime",
    "warningSummary",
    "emsSoc",
    "emsPower",
    "emsVoltage",
    "emsCurrent",
    "emsSoh",
    "emsCapacity",
    "eBatCharToday",
    "eBatDisCharToday",
    "tempMax",
    "tempMin",
    "remainingBatteryEnergy1",
    "ratedEnergy",
    "bmsState",
    "bmsChargingState",
    "maxVoltage2bms",
    "minVoltage2bms",
    "cellNumber",
    "batCount",
    "batLineCount",
]


def _device_kind_from_data(data: dict) -> str:
    device_type = str(data.get("deviceType") or "").upper()
    alias = str(data.get("alias") or "").lower()
    model = str(data.get("deviceModel") or "").upper()
    type_name = str(data.get("type") or "").upper()

    if device_type == DEVICE_TYPE_INVERTER or "IVGM" in model or "IVGM" in type_name:
        return "inverter"

    if (
        device_type == DEVICE_TYPE_BATTERY
        or alias.startswith("batterie")
        or alias.startswith("battery")
        or "LUX" in model
        or "LUX" in type_name
        or data.get("battSoc") is not None
        or data.get("bmsPower") is not None
    ):
        return "battery"

    return "unknown"


def _keys_for_kind(kind: str) -> list[str]:
    if kind == "inverter":
        return INVERTER_KEYS

    if kind == "battery":
        return BATTERY_KEYS

    return [
        "deviceSn",
        "deviceModel",
        "deviceType",
        "status",
        "firmwareVersion",
    ]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    data = coordinator.data or {}
    devices_by_sn = data.get("devices_by_sn") or {}

    # Dynamischer Pfad: alle Geräte aus devices_by_sn
    if devices_by_sn:
        for device_sn, device_data in devices_by_sn.items():
            if not isinstance(device_data, dict):
                continue

            kind = _device_kind_from_data(device_data)
            keys = _keys_for_kind(kind)

            for key in keys:
                desc = SENSOR_MAP.get(key)
                if desc:
                    entities.append(
                        FelicitySensor(
                            coordinator=coordinator,
                            entry=entry,
                            description=desc,
                            device_kind=kind,
                            device_sn=str(device_sn),
                        )
                    )

    # Legacy-Fallback: falls devices_by_sn noch nicht verfügbar ist
    if not entities:
        for key in INVERTER_KEYS:
            desc = SENSOR_MAP.get(key)
            if desc:
                entities.append(
                    FelicitySensor(
                        coordinator=coordinator,
                        entry=entry,
                        description=desc,
                        device_kind="inverter",
                        device_sn=None,
                    )
                )

        for key in BATTERY_KEYS:
            desc = SENSOR_MAP.get(key)
            if desc:
                entities.append(
                    FelicitySensor(
                        coordinator=coordinator,
                        entry=entry,
                        description=desc,
                        device_kind="battery",
                        device_sn=None,
                    )
                )

    async_add_entities(entities)


class FelicitySensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator,
        entry,
        description,
        device_kind: str,
        device_sn: str | None,
    ):
        super().__init__(coordinator)

        self.entity_description = description
        self._device_kind = device_kind
        self._device_sn = device_sn

        unique_device_part = device_sn or device_kind
        self._attr_unique_id = f"{entry.entry_id}-{unique_device_part}-{description.key}"

    def _device_data(self) -> dict:
        data = self.coordinator.data or {}

        if self._device_sn:
            devices_by_sn = data.get("devices_by_sn") or {}
            device_data = devices_by_sn.get(self._device_sn)

            if isinstance(device_data, dict):
                return device_data

        devices = data.get("devices", {})
        return devices.get(self._device_kind, {}) or {}

    def _get(self, data, key):
        val = data.get(key)

        if val in (None, "unknown", "unavailable", ""):
            return None

        return val

    def _device_name(self, data: dict) -> str:
        alias = data.get("alias") or data.get("plantName") or self._device_kind.title()

        if self._device_kind == "inverter":
            if str(alias).lower().startswith("inverter-"):
                return str(alias)
            return f"Inverter-{alias}"

        if self._device_kind == "battery":
            if str(alias).lower().startswith("batterie-") or str(alias).lower().startswith("battery-"):
                return str(alias)
            return f"Batterie-{alias}"

        return str(alias)

    @property
    def device_info(self):
        data = self._device_data()
        sn = data.get("deviceSn") or self._device_sn or self._device_kind

        if self._device_kind == "inverter":
            model = data.get("deviceModel") or "IVGM100600"
            model_id = "OC"

        elif self._device_kind == "battery":
            model = data.get("deviceModel") or "LUX-X-96050HG01"
            model_id = "BP"
            
        else:
            model = data.get("deviceModel")
            model_id = None

        device_info = {
            "identifiers": {(DOMAIN, str(sn))},
            "name": self._device_name(data),
            "manufacturer": MANUFACTURER,
            "model": model,
            "sw_version": data.get("firmwareVersion") or data.get("moduleVersion"),
            "configuration_url": "https://shine.felicitysolar.com",
            "suggested_area": data.get("plantName") or "Garage",
        }

        if model_id:
            device_info["model_id"] = model_id

        return device_info

    @property
    def native_value(self) -> Optional[Any]:
        data = self._device_data()
        key = self.entity_description.key

        if self._device_kind == "battery":
            battery_key_map = {
                "emsSoc": ["emsSoc", "battSoc"],
                "emsPower": ["bmsPower", "emsPower"],
                "emsVoltage": ["emsVoltage", "battVolt"],
                "emsCurrent": ["emsCurrent", "battCurr"],
                "emsSoh": ["battSoh", "emsSoh"],
                "emsCapacity": ["battCapacity", "batteryCapacity", "totalEmsCapacity", "emsCapacity"],
            }

            if key in battery_key_map:
                for source_key in battery_key_map[key]:
                    value = self._get(data, source_key)
                    if value is not None:
                        try:
                            return float(value)
                        except Exception:
                            return value
                return None

        if key == "grid_import":
            val = self._get(data, "acTtlInpower") or self._get(data, "acTtlInPower") or self._get(data, "ctAcTtlInPower")
            try:
                val = float(val)
                return abs(val) if val < 0 else 0
            except Exception:
                return None

        if key == "grid_export":
            val = self._get(data, "acTtlInpower") or self._get(data, "acTtlInPower") or self._get(data, "ctAcTtlInPower")
            try:
                val = float(val)
                return val if val > 0 else 0
            except Exception:
                return None

        value = self._get(data, key)

        if value is None:
            return None

        if key in STRING_KEYS:
            return str(value)

        try:
            return float(value)
        except Exception:
            return value
