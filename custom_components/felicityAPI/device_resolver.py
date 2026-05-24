from typing import Dict, Any, List, Tuple, Optional


class DeviceResolver:
    """
    DEVICE TRUTH LAYER v2

    RULE:
    - OC = Inverter / Controller
    - BP = Battery Pack
    - deviceSn = always real serial
    """

    def __init__(self, devices: List[Dict[str, Any]]):
        self.devices = devices or []

    # =========================================================
    # PUBLIC API
    # =========================================================
    def resolve(self) -> Dict[str, Any]:

        inverter = self._get_by_type("OC")
        battery = self._get_by_type("BP")

        return {
            "inverter": self._normalize(inverter, "inverter"),
            "battery": self._normalize(battery, "battery"),
            "all_devices": self._normalize_list(),
        }

    # =========================================================
    # DEVICE SELECTION (TRUTH ONLY)
    # =========================================================
    def _get_by_type(self, device_type: str) -> Dict[str, Any]:

        for d in self.devices:
            if (d.get("deviceType") or "").upper() == device_type:
                return d

        return {}

    # =========================================================
    # NORMALIZATION (IMPORTANT FIXES HERE)
    # =========================================================
    def _normalize(self, device: Dict[str, Any], role: str) -> Dict[str, Any]:

        if not device:
            return {
                "role": role,
                "device_sn": None,
                "model": None,
                "type": None,
                "subtype": None,
                "firmware": None,
                "status": None,
            }

        return {
            "role": role,

            # 🔴 ABSOLUTE RULE: REAL SERIAL ONLY
            "device_sn": device.get("deviceSn"),

            "model": device.get("deviceModel"),
            "type": device.get("deviceType"),
            "subtype": device.get("subType"),

            "firmware": self._get_firmware(device),

            "status": device.get("status"),

            # useful debugging
            "alias": device.get("alias"),
            "plant": device.get("plantName"),
        }

    # =========================================================
    # FIRMWARE NORMALIZATION
    # =========================================================
    def _get_firmware(self, device: Dict[str, Any]):

        return (
            device.get("firmwareVersion")
            or device.get("moduleVersion")
            or device.get("displayVersion")
        )

    # =========================================================
    # DEBUG LIST (OPTIONAL)
    # =========================================================
    def _normalize_list(self):

        result = []

        for d in self.devices:
            result.append({
                "device_sn": d.get("deviceSn"),
                "type": d.get("deviceType"),
                "model": d.get("deviceModel"),
            })

        return result