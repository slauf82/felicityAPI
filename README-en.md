# README-EN

# Felicity API -- User Guide

## Welcome

Felicity API is a modern Home Assistant integration for monitoring
Felicity Solar inverters and battery systems.

The integration focuses on providing a comprehensive **read-only**
monitoring solution with advanced diagnostics and seamless Home
Assistant integration.

## Features

### Inverter

-   PV production
-   Grid import / export
-   Household consumption
-   AC values
-   Energy Flow
-   Device status
-   Firmware information
-   Warning monitoring
-   Live diagnostics

### Battery

-   State of Charge (SOC)
-   State of Health (SOH)
-   Battery voltage
-   Battery current
-   Battery power
-   Capacity
-   Working Mode
-   BMS Status
-   BMS Flags
-   Cell voltages
-   Cell temperatures
-   Warning information
-   Advanced diagnostics

## Installation

### HACS

1.  Add the custom repository.
2.  Install **Felicity API**.
3.  Restart Home Assistant.
4.  Add the integration.
5.  Enter your Felicity Cloud credentials.

### Manual

Copy the folder:

`custom_components/felicity_api`

to

`/config/custom_components/`

and restart Home Assistant.

## Current Status

The integration currently provides more than **120 Home Assistant
entities**.

Typical installation:

-   Battery: \~50 entities
-   Inverter: \~70 entities

## Warning Monitoring

Version 1.2 introduced cloud warning support, allowing Home Assistant
automations and notifications based on inverter or battery warnings.

## Advanced BMS Diagnostics

Version 1.3 significantly extends battery monitoring with:

-   Working Mode
-   BMS Status
-   BMS Flags
-   Cell voltage monitoring
-   Cell temperature monitoring
-   Extended battery diagnostics

## Roadmap

### Version 1.4

-   History API
-   Daily statistics
-   Monthly statistics
-   Yearly statistics

### Version 1.5

-   Write functions
-   Device configuration

## FAQ

**Does the integration modify device settings?**

No. The integration is completely read-only.

**Does it require a Felicity Cloud account?**

Yes.

**Is it HACS compatible?**

Yes.

## License

GNU General Public License v3.0 (GPL-3.0)

------------------------------------------------------------------------

Thank you to everyone who contributed feedback, testing and ideas to
improve this project.
