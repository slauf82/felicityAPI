# Felicity API for Home Assistant
Version 1.1.0

Custom Home Assistant integration for Felicity Solar cloud devices.

This integration connects directly to the official Felicity Solar cloud API and provides sensor data for:

- Inverters
- Batteries
- Energy statistics
- PV production
- Grid import/export
- Battery charging/discharging
- Device status and diagnostics

---

# Current Project Status

Early beta / active development.

The integration is already stable enough for daily use, but the internal architecture is still being improved and refactored.

## Currently Working

- Inverter detection
- Battery detection
- Automatic device discovery
- Optional manual serial number fallback
- Device separation inside Home Assistant
- PV power sensors
- Grid power sensors
- Battery SOC and battery power
- Daily energy statistics
- HotJson parsing
- Config Flow setup
- SSL handling workaround
- Home Assistant device registry support

## Currently In Progress

- Dynamic multi-device architecture
- Coordinator refactoring
- Improved sensor abstraction
- Better diagnostics
- HACS preparation
- Options flow
- Cleanup and optimization

---

# Features

## Device Support

### Inverter Sensors

- PV total power
- PV string power
- Grid import/export
- Daily PV production
- Daily grid import
- Daily grid export
- Battery charging/discharging
- Firmware version
- Device status
- Working mode
- Energy state

### Battery Sensors

- Battery SOC
- Battery power
- Battery voltage
- Battery current
- Battery SOH
- Battery capacity
- Daily charge/discharge energy

---

# Installation

## Manual Installation

Copy the integration folder to:

/config/custom_components/felicity_api/

Restart Home Assistant afterwards.

Configuration

The integration supports:

* Username
* Password
* Optional inverter serial number
* Optional battery serial number

Important
Serial numbers are optional.

The integration first tries automatic device discovery using the Felicity API device list.

Manual serial numbers are only used as fallback.

SSL Information

Felicity currently uses SSL certificates that may fail strict validation inside Home Assistant environments.

Because of this, the integration currently uses a relaxed SSL context intentionally.

This is a temporary compatibility solution until Felicity improves certificate compatibility.

Architecture

The integration is currently transitioning from a fixed two-device structure to a fully dynamic multi-device architecture.

Current internal structure:

* centralized API layer
* centralized request handling
* centralized authentication handling
* centralized SSL handling
* coordinator-based device management
# Development Goals
Planned Improvements
* Fully dynamic device handling
* Multiple inverter support
* Multiple battery support
* Better diagnostics
* Cleaner sensor abstraction
* Entity categories
* Device controls
* Realtime/WebSocket support (if possible)
* HACS release
* Translation improvements
* Repair flow support
# Known Limitations
* Some Felicity API fields are undocumented
* API structures may differ between firmware generations
* SSL validation currently relaxed intentionally
* Some sensors still rely on fallback mappings

Requirements

The integration currently requires:

"requirements": [
  "pycryptodomex"
]
Home Assistant Compatibility

Tested with recent Home Assistant versions including:

2025.x
2026.x
Disclaimer

This project is not affiliated with or endorsed by Felicity Solar.

Use at your own risk.

Credits
Felicity Solar cloud platform
Home Assistant community
Reverse engineering and testing by the community

License
GNU General Public License v3.0 (GPL-3.0)
