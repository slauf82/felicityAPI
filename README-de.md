# README-DE

# Felicity API -- Deutsches Handbuch

## Willkommen

Felicity API ist eine moderne Home-Assistant-Integration zur Überwachung
von Felicity Solar Wechselrichtern und Batteriesystemen.

Der Schwerpunkt liegt auf einer vollständig lesenden (Read-Only)
Integration, die möglichst viele Informationen aus der offiziellen
Felicity-Cloud in Home Assistant bereitstellt.

## Funktionsumfang

### Wechselrichter

-   PV-Leistung
-   AC-Leistung
-   Netzbezug / Einspeisung
-   Hausverbrauch
-   Gerätestatus
-   Firmware
-   Warnungen
-   Energy Flow
-   Live-Diagnosedaten

### Batterie

-   SOC
-   SOH (Batteriegesundheit)
-   Batteriespannung
-   Batteriestrom
-   Batterieleistung
-   Kapazität
-   Working Mode
-   BMS Status
-   BMS Flags
-   Zellspannungen
-   Zelltemperaturen
-   Warnungen
-   Erweiterte Diagnosewerte

## Installation

### HACS

1.  Repository hinzufügen.
2.  Felicity API installieren.
3.  Home Assistant neu starten.
4.  Integration hinzufügen.
5.  Zugangsdaten eingeben.

### Manuelle Installation

Den Ordner

`custom_components/felicity_api`

nach

`/config/custom_components/`

kopieren und Home Assistant neu starten.

## Einrichtung

Nach der Installation erscheint die Integration unter **Einstellungen →
Geräte & Dienste**.

Es werden Benutzername und Passwort des Felicity-Cloud-Kontos benötigt.

## Sensoren

### Batterie

Die Batterie stellt aktuell über 50 Entitäten bereit, unter anderem:

-   Ladezustand (SOC)
-   Batteriegesundheit (SOH)
-   Spannung
-   Strom
-   Leistung
-   Working Mode
-   BMS-Diagnose
-   Warnungen
-   Zellspannungen
-   Zelltemperaturen

### Wechselrichter

Der Wechselrichter stellt derzeit rund 70 Entitäten bereit.

Dazu gehören:

-   PV-Werte
-   Netzwerte
-   Verbrauch
-   Energy Flow
-   Firmware
-   Gerätestatus
-   Warnungen

## Warnungen

Seit Version 1.2.0 werden Warnungen aus der Felicity-Cloud ausgelesen.

Diese können direkt für Automationen oder Benachrichtigungen verwendet
werden.

## BMS-Diagnose

Version 1.3.0 erweitert die Batterieüberwachung deutlich.

Neue Informationen:

-   Working Mode
-   BMS Status
-   BMS Flags
-   Zellspannungen
-   Zelltemperaturen
-   Diagnoseinformationen

## Roadmap

### Version 1.4.0

-   History API
-   Tageswerte
-   Monatswerte
-   Jahreswerte

### Version 1.5.0

-   Schreibfunktionen
-   Gerätekonfiguration

## FAQ

**Werden Einstellungen verändert?**

Nein. Die Integration arbeitet ausschließlich lesend.

**Werden Cloud-Zugangsdaten benötigt?**

Ja.

**Ist die Integration HACS-kompatibel?**

Ja.

## Lizenz

GNU GPL v3.0
