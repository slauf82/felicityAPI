# Felicity API

> **Eine moderne Home-Assistant-Integration für Felicity Solar
> Wechselrichter und Batteriesysteme**

![Version](https://img.shields.io/badge/version-v1.3.0-blue) ![Home
Assistant](https://img.shields.io/badge/Home%20Assistant-Compatible-success)
![License](https://img.shields.io/badge/License-GPLv3-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## Überblick

**Felicity API** ist eine Home-Assistant-Integration zur Überwachung von
Felicity-Solar-Wechselrichtern und Batteriesystemen.

Der Schwerpunkt liegt auf einer vollständig lesenden (Read-Only)
Integration mit umfangreichen Diagnoseinformationen.

## Highlights

-   Über 120 Home-Assistant-Entitäten
-   Wechselrichter-Überwachung
-   Batterie-Überwachung
-   Energy-Flow-Daten
-   Warnungen und Alarme
-   Erweiterte BMS-Diagnose
-   Login-Kompatibilitäts-Fallbacks
-   HACS-kompatibel

## Unterstützte Funktionen

  Funktion                      Status
  --------------------------- -----------
  Live-Sensordaten                ✅
  Batterieüberwachung             ✅
  Wechselrichterüberwachung       ✅
  Energy Flow                     ✅
  Warnungen                       ✅
  BMS-Diagnose                    ✅
  Historische Daten            🚧 v1.4.0
  Schreibfunktionen            🚧 v1.5.0

## Installation

### HACS

1.  Benutzerdefiniertes Repository hinzufügen.
2.  Integration installieren.
3.  Home Assistant neu starten.
4.  Integration konfigurieren.

### Manuell

Den Ordner `custom_components/felicity_api` nach
`/config/custom_components/` kopieren und Home Assistant neu starten.

## Aktueller Funktionsumfang (v1.3.0)

### Batterie

-   SOC
-   SOH
-   Spannung
-   Strom
-   Leistung
-   Kapazität
-   Working Mode
-   BMS-Status
-   BMS-Flags
-   Zellspannungen
-   Zelltemperaturen
-   Warnungen
-   Diagnosewerte

### Wechselrichter

-   PV-Leistung
-   Netzbezug / Einspeisung
-   Hausverbrauch
-   AC-Werte
-   Energy Flow
-   Gerätestatus
-   Firmware
-   Warnungen

## Roadmap

### v1.4.0

-   History API
-   Tages-, Monats- und Jahreswerte

### v1.5.0

-   Schreibfunktionen
-   Gerätekonfiguration

## Changelog

-   **v1.3.0** -- Erweiterte Batterie- und BMS-Diagnose
-   **v1.2.1** -- Payload-Fallback
-   **v1.2.0** -- Warnungen und Login-Kompatibilität
-   **v1.1.0** -- Erweiterte Live-Sensoren
-   **v1.0.0** -- Erste Veröffentlichung

## Dokumentation

Weitere Informationen: - README-DE.md - README-EN.md

## Lizenz

GNU GPL v3.0

## Lizenzergänzung

Jegliche Änderung, Umschreibung, Umformulierung o.ä. die mittels KI / AI erstellt wurde, muss zwingend wieder unter die GNU GPL v3.0 gestellt werden.
