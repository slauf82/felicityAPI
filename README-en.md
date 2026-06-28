

## Official Felicity Documentation

- Web Manual: https://om.felicitysolar.com/vue/1.html
- App Manual: https://shine.felicitysolar.com/app_operation_manualen.html

# Felicity API for Home Assistant

Custom Home Assistant integration for Felicity Solar Cloud devices.

This integration connects directly to the Felicity Solar Cloud API and provides sensor data inside Home Assistant.

## Supported Areas

- Inverters
- Batteries
- PV production
- Grid import and export
- Battery charging and discharging
- Daily energy statistics
- Device status
- Diagnostic data

---

## Current Project Status

**Version:** `v1.0.0` 

The integration is already usable for daily operation but is still under active development.

The current version already includes dynamic device detection with serial-number-based sensor creation and a legacy fallback structure.

---

## Already Functional

- Central API layer
- Central request handling
- Central authentication handling
- Token management
- SSL handling workaround
- Automatic device detection via `list_device_all_type`
- Serial-number-based device assignment
- Dynamic sensor creation per detected device
- Legacy fallback for inverter and battery
- Device separation inside Home Assistant
- PV power sensors
- Grid power sensors
- Battery SOC and battery power
- Daily energy statistics
- HotJson parsing
- Config flow setup
- Home Assistant device registry support

---

## Currently in Progress

- Extended dynamic multi-device support
- Support for multiple inverters
- Support for multiple batteries
- Improved sensor abstraction
- Extended diagnostics
- Options flow
- HACS preparation
- Code cleanup and optimization

---

## Features

### Inverter Sensors

- Serial number
- Device model
- Device type
- Firmware version
- Device status
- Operating mode
- Energy state
- Alarm count
- Alarm text
- Total PV power
- PV string power
- Grid power
- Current grid import
- Current grid export
- House consumption
- PV energy today
- Total energy today
- Grid import today
- Grid export today
- Battery charge today
- Battery discharge today

### Battery Sensors

- Serial number
- Device model
- Device type
- Firmware version
- Device status
- Battery state of charge
- Battery power
- Battery voltage
- Battery current
- Battery health / SOH
- Battery capacity
- Battery charge today
- Battery discharge today

---

## Multi-Device Support

The integration is designed to support multiple Felicity devices.

Internally, devices returned by `list_device_all_type` are indexed by serial number and sensors are created dynamically per device.

Currently tested with:

- 1 inverter
- 1 battery

Community testing is still needed for:

- multiple inverters
- multiple batteries
- larger mixed installations
- different Felicity device models

---

## Installation

### Manual Installation

Copy the integration folder to:
/config/custom_components/felicity_api/

Then restart Home Assistant.

# Configuration

The integration supports:

* Username
* Password
* Optional inverter serial number
* Optional battery serial number

Important
Serial numbers are optional.

The integration first attempts automatic device detection via the Felicity API device list.

Manual serial numbers are only used as fallback.

SSL Notice

Felicity currently uses SSL certificates that may not allow full certificate validation in some Home Assistant environments.

Therefore, the integration currently uses a relaxed SSL context intentionally.

This is currently a compatibility workaround until Felicity improves their certificate chain or proper validation becomes reliably possible.

# Architecture

The integration is currently transitioning from a fixed two-device structure to a dynamic multi-device architecture.

The current internal structure includes:

* central API layer
* central request processing
* central authentication management
* central SSL management
* coordinator-based device management
* devices_by_sn as dynamic device base
* legacy fallback for existing inverter/battery structure

# Requirements

The integration currently requires:

"requirements": [
  "pycryptodomex"
]
Home Assistant Compatibility

Tested with current Home Assistant versions including:

* 2025.x
* 2026.x

# Known Limitations
* Some Felicity API fields are undocumented.
* API structures may vary depending on firmware generation.
* SSL validation is currently intentionally relaxed.
* Multi-device setups still require community testing.
* Some sensors currently still use fallback mappings.

# Development Goals

Planned improvements:

* Fully dynamic device management
* Support for multiple inverters
* Support for multiple batteries
* Extended diagnostics
* Cleaner sensor abstraction
* Entity categories
* Options flow
* Device controls
* Real-time/WebSocket support if possible
* HACS release
* Improved translations
* Repair flow support

# Disclaimer

This project is not affiliated with Felicity Solar and is not officially supported.

Use at your own risk.

Acknowledgements
* Felicity Solar Cloud platform
* Home Assistant Community
* Reverse engineering and testing by the community

# License
GNU General Public License v3.0 (GPL-3.0)
