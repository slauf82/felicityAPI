

## Official Felicity Documentation

- Web Manual: https://om.felicitysolar.com/vue/1.html
- App Manual: https://shine.felicitysolar.com/app_operation_manualen.html

# Felicity API for Home Assistant

Custom Home Assistant integration for Felicity Solar Cloud devices.

---

## Documentation

- German README: [README-de.md](README-de.md)
- English README: [README-en.md](README-en.md)

---

## Features

- HACS compatible
- Dynamic device detection
- Inverter support
- Battery support
- Diagnostics support
- Automatic serial number detection
- Dynamic sensor creation

---

## Installation

### HACS (recommended)

Add custom repository:

https://github.com/slauf82/felicityAPI

Category:

Integration

Then install:

Felicity API

---

## License

GNU General Public License v3.0 (GPL-3.0)

---

## Additional license information

AI-generated or AI-assisted products based on this project must also remain under the GPL 3.0 license.

---

## Disclaimer

This project is not affiliated with Felicity Solar and is not officially supported.

## v1.4.5

- Added anonymized diagnostics export using Home Assistant's “Download diagnostics” feature.
- Includes structured information about detected device types, API/sensor fields, and history diagnostics.
- No automatic transmission of diagnostic data; please review the JSON file before sharing.
- Expanded multi-device detection and model recognition, including M1-1600 and IVAM (additional real-world testing required).
- Improved SSL initialization and history request error diagnostics.
- Retains v1.4.2 History/Chart parsing with `xaxis` timeline and `dataList` fallback.
- The integration remains read-only; write operations are not yet supported.
