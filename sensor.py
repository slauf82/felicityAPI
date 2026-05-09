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
    PERCENTAGE,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER


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
}


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

    "pvTotalPower": SensorEntityDescription(
        key="pvTotalPower",
        translation_key="pvTotalPower",
        icon="mdi:solar-power",
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
        icon="mdi:battery",
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
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "emsCurrent": SensorEntityDescription(
        key="emsCurrent",
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
    "emsSoc",
    "emsPower",
    "emsVoltage",
    "emsCurrent",
    "emsSoh",
    "emsCapacity",
    "eBatCharToday",
    "eBatDisCharToday",
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for key in INVERTER_KEYS:
        desc = SENSOR_MAP.get(key)
        if desc:
            entities.append(FelicitySensor(coordinator, entry, desc, "inverter"))

    for key in BATTERY_KEYS:
        desc = SENSOR_MAP.get(key)
        if desc:
            entities.append(FelicitySensor(coordinator, entry, desc, "battery"))

    async_add_entities(entities)


class FelicitySensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, description, device_group: str):
        super().__init__(coordinator)
        self.entity_description = description
        self._device_group = device_group
        self._attr_unique_id = f"{entry.entry_id}-{device_group}-{description.key}"

    def _device_data(self) -> dict:
        data = self.coordinator.data or {}
        devices = data.get("devices", {})
        return devices.get(self._device_group, {}) or {}

    def _get(self, data, key):
        val = data.get(key)
        if val in (None, "unknown", "unavailable", ""):
            return None
        return val

    def _device_name(self, data: dict) -> str:
        alias = data.get("alias") or data.get("plantName") or self._device_group.title()

        if self._device_group == "inverter":
            if str(alias).lower().startswith("inverter-"):
                return str(alias)
            return f"Inverter-{alias}"

        if str(alias).lower().startswith("batterie-") or str(alias).lower().startswith("battery-"):
            return str(alias)

        return f"Batterie-{alias}"

    @property
    def device_info(self):
        data = self._device_data()
        sn = data.get("deviceSn") or self._device_group

        if self._device_group == "inverter":
            suggested_area = "Garage"
            icon = "mdi:solar-power"
        else:
            suggested_area = "Garage"
            icon = "mdi:battery"

        return {
            "identifiers": {(DOMAIN, str(sn))},
            "name": self._device_name(data),
            "manufacturer": MANUFACTURER,
            "model": data.get("deviceModel"),
            "sw_version": data.get("firmwareVersion") or data.get("moduleVersion"),
            "suggested_area": suggested_area,
            "configuration_url": "https://shine.felicitysolar.com",
        }

    @property
    def native_value(self) -> Optional[Any]:
        data = self._device_data()
        key = self.entity_description.key

        if self._device_group == "battery":
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
            val = self._get(data, "acTtlInpower") or self._get(data, "ctAcTtlInPower")
            try:
                val = float(val)
                return abs(val) if val < 0 else 0
            except Exception:
                return None

        if key == "grid_export":
            val = self._get(data, "acTtlInpower") or self._get(data, "ctAcTtlInPower")
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