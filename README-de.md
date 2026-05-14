# Felicity API für Home Assistant

Benutzerdefinierte Home-Assistant-Integration für Felicity Solar Cloud Geräte.

Diese Integration verbindet sich direkt mit der Felicity Solar Cloud API und stellt Sensordaten in Home Assistant bereit.

## Unterstützte Bereiche

- Wechselrichter
- Batterien
- PV-Produktion
- Netzbezug und Einspeisung
- Batterie-Laden und Entladen
- Tages-Energiestatistiken
- Gerätestatus
- Diagnosedaten

---

## Aktueller Projektstatus

**Version:** `v0.2.1-beta`  
**Status:** Frühe Beta / aktive Entwicklung

Die Integration ist bereits für den täglichen Einsatz nutzbar, befindet sich aber weiterhin in aktiver Entwicklung.

Der aktuelle Stand enthält bereits eine dynamische Geräteerkennung mit seriennummernbasierter Sensorerzeugung und Legacy-Fallback-Struktur.

---

## Bereits funktionsfähig

- Zentrale API-Schicht
- Zentrale Request-Verarbeitung
- Zentrale Authentifizierung
- Token-Handling
- SSL-Handling-Workaround
- Automatische Geräteerkennung über `list_device_all_type`
- Seriennummernbasierte Gerätezuordnung
- Dynamische Sensorerzeugung pro erkanntem Gerät
- Legacy-Fallback für Wechselrichter und Batterie
- Gerätegrennung innerhalb von Home Assistant
- PV-Leistungssensoren
- Netzleistungs-Sensoren
- Batterie-SOC und Batterieleistung
- Tägliche Energie-Statistiken
- HotJson-Auswertung
- Config-Flow Einrichtung
- Home-Assistant-Geräteregistrierung

---

## Aktuell in Arbeit

- Erweiterte dynamische Multi-Geräte-Unterstützung
- Unterstützung mehrerer Wechselrichter
- Unterstützung mehrerer Batterien
- Verbesserte Sensor-Abstraktion
- Erweiterte Diagnosefunktionen
- Options-Flow
- HACS-Vorbereitung
- Code-Bereinigung und Optimierung

---

## Funktionen

### Wechselrichter-Sensoren

- Seriennummer
- Gerätemodell
- Gerätetyp
- Firmware-Version
- Gerätestatus
- Betriebsmodus
- Energiezustand
- Alarmanzahl
- Alarmtext
- PV Gesamtleistung
- PV String-Leistungen
- Netzleistung
- Netzbezug aktuell
- Netzeinspeisung aktuell
- Hausverbrauch
- PV Energie heute
- Gesamtenergie heute
- Netzbezug heute
- Netzeinspeisung heute
- Batterie Laden heute
- Batterie Entladen heute

### Batterie-Sensoren

- Seriennummer
- Gerätemodell
- Gerätetyp
- Firmware-Version
- Gerätestatus
- Batterie-Ladezustand
- Batterieleistung
- Batteriespannung
- Batteriestrom
- Batterie-Gesundheit / SOH
- Batteriekapazität
- Batterie Laden heute
- Batterie Entladen heute

---

## Unterstützung mehrerer Geräte

Die Integration ist darauf ausgelegt, mehrere Felicity-Geräte gleichzeitig zu unterstützen.

Intern werden Geräte aus `list_device_all_type` anhand ihrer Seriennummer indexiert und Sensoren dynamisch pro Gerät erzeugt.

Aktuell getestet mit:

- 1 Wechselrichter
- 1 Batterie

Community-Tests werden noch benötigt für:

- mehrere Wechselrichter
- mehrere Batterien
- größere gemischte Anlagen
- unterschiedliche Felicity-Gerätemodelle

---

## Installation

### Manuelle Installation

Den Integrationsordner nach folgendem Pfad kopieren:
/config/custom_components/felicity_api/

Anschließend Home Assistant neu starten.

Konfiguration

Die Integration unterstützt:

* Benutzername
* Passwort
* Optionale Wechselrichter-Seriennummer
* Optionale Batterie-Seriennummer

Wichtig
Seriennummern sind optional.

Die Integration versucht zuerst eine automatische Geräteerkennung über die Felicity API-Geräteliste.

Manuelle Seriennummern dienen nur als Fallback.

SSL-Hinweis

Felicity verwendet aktuell SSL-Zertifikate, die innerhalb mancher Home-Assistant-Umgebungen keine vollständige Zertifikatsvalidierung ermöglichen.

Daher verwendet die Integration derzeit bewusst einen gelockerten SSL-Kontext.

Dies ist aktuell eine Kompatibilitätslösung, bis Felicity die Zertifikatskette verbessert oder eine saubere Validierung zuverlässig möglich ist.

# Architektur

Die Integration befindet sich im Übergang von einer festen Zwei-Geräte-Struktur zu einer dynamischen Multi-Geräte-Architektur.

Der aktuelle interne Aufbau umfasst:

* zentrale API-Schicht
* zentrale Request-Verarbeitung
* zentrale Authentifizierungsverwaltung
* zentrale SSL-Verwaltung
* Coordinator-basierte Geräteverwaltung
* devices_by_sn als dynamische Gerätebasis
* Legacy-Fallback für bestehende Wechselrichter-/Batterie-Struktur

# Anforderungen

Die Integration benötigt aktuell:

"requirements": [
  "pycryptodomex"
]
Home Assistant Kompatibilität

Getestet mit aktuellen Home-Assistant-Versionen einschließlich:

* 2025.x
* 2026.x

# Bekannte Einschränkungen
Einige Felicity API-Felder sind undokumentiert.
API-Strukturen können sich je nach Firmware-Generation unterscheiden.
SSL-Validierung ist aktuell bewusst gelockert.
Multi-Geräte-Setups benötigen noch Community-Tests.
Einige Sensoren verwenden derzeit noch Fallback-Mappings.
Entwicklungsziele

# Geplante Verbesserungen:

* Vollständig dynamische Geräteverwaltung
* Unterstützung mehrerer Wechselrichter
* Unterstützung mehrerer Batterien
* Erweiterte Diagnosefunktionen
* Sauberere Sensor-Abstraktion
* Entity-Kategorien
* Options-Flow
* Gerätesteuerungen
* Echtzeit-/WebSocket-Unterstützung, falls möglich
* HACS-Release
* Verbesserte Übersetzungen
* Repair-Flow-Unterstützung

# Haftungsausschluss

Dieses Projekt steht in keiner Verbindung zu Felicity Solar und wird nicht offiziell unterstützt.

Verwendung auf eigene Verantwortung.

# Danksagung
* Felicity Solar Cloud Plattform
* Home Assistant Community
* Reverse Engineering und Tests durch die Community

# Lizenz
GNU General Public License v3.0 (GPL-3.0)
