# Felicity API für Home Assistant

Benutzerdefinierte Home-Assistant-Integration für Felicity Solar Cloud Geräte.

Diese Integration verbindet sich direkt mit der offiziellen Felicity Solar Cloud API und stellt Sensordaten für folgende Geräte bereit:

- Wechselrichter
- Batterien
- Energie-Statistiken
- PV-Produktion
- Netzbezug und Einspeisung
- Batterie-Laden und Entladen
- Gerätestatus und Diagnosedaten

---

# Aktueller Projektstatus

Frühe Beta / aktive Entwicklung.

Die Integration ist bereits stabil genug für den täglichen Einsatz, die interne Architektur wird jedoch aktuell noch verbessert und refactored.

## Bereits funktionsfähig

- Wechselrichter-Erkennung
- Batterie-Erkennung
- Automatische Geräteerkennung
- Optionale manuelle Seriennummern als Fallback
- Gerätegrennung innerhalb von Home Assistant
- PV-Leistungssensoren
- Netzleistungs-Sensoren
- Batterie-SOC und Batterieleistung
- Tägliche Energie-Statistiken
- HotJson-Auswertung
- Config-Flow Einrichtung
- SSL-Handling-Workaround
- Unterstützung der Home-Assistant-Geräteregistrierung

## Aktuell in Arbeit

- Dynamische Multi-Geräte-Architektur
- Coordinator-Refactoring
- Verbesserte Sensor-Abstraktion
- Erweiterte Diagnosefunktionen
- HACS-Vorbereitung
- Options-Flow
- Code-Bereinigung und Optimierung

---

# Funktionen

## Geräteunterstützung

### Wechselrichter-Sensoren

- PV Gesamtleistung
- PV String-Leistungen
- Netzbezug / Einspeisung
- Tägliche PV-Produktion
- Täglicher Netzbezug
- Tägliche Netzeinspeisung
- Batterie Laden / Entladen
- Firmware-Version
- Gerätestatus
- Betriebsmodus
- Energiezustand

### Batterie-Sensoren

- Batterie-Ladezustand (SOC)
- Batterieleistung
- Batteriespannung
- Batteriestrom
- Batterie-SOH
- Batteriekapazität
- Tägliche Lade-/Entladeenergie

---

# Installation

## Manuelle Installation

Den Integrationsordner nach folgendem Pfad kopieren:

/config/custom_components/felicity_api/

Anschließend Home Assistant neu starten.

Konfiguration

Die Integration unterstützt:

Benutzername
Passwort
Optionale Wechselrichter-Seriennummer
Optionale Batterie-Seriennummer

Wichtig
Seriennummern sind optional.

Die Integration versucht zuerst eine automatische Geräteerkennung über die Felicity API-Geräteliste.

Manuelle Seriennummern dienen nur als Fallback.

* SSL-Hinweis

Felicity verwendet aktuell SSL-Zertifikate, die innerhalb mancher Home-Assistant-Umgebungen keine vollständige Zertifikatsvalidierung ermöglichen.

Daher verwendet die Integration derzeit bewusst einen gelockerten SSL-Kontext.

Dies ist aktuell eine Kompatibilitätslösung, bis Felicity die Zertifikatskette verbessert.

Architektur

Die Integration befindet sich aktuell im Übergang von einer festen Zwei-Geräte-Struktur zu einer vollständig dynamischen Multi-Geräte-Architektur.

Der aktuelle interne Aufbau umfasst:

zentrale API-Schicht
zentrale Request-Verarbeitung
zentrale Authentifizierungsverwaltung
zentrale SSL-Verwaltung
Coordinator-basierte Geräteverwaltung
Entwicklungsziele
Geplante Verbesserungen
Vollständig dynamische Geräteverwaltung
Unterstützung mehrerer Wechselrichter
Unterstützung mehrerer Batterien
Erweiterte Diagnosefunktionen
Sauberere Sensor-Abstraktion
Entity-Kategorien
Gerätesteuerungen
Echtzeit-/WebSocket-Unterstützung (falls möglich)
HACS-Release
Verbesserte Übersetzungen
Repair-Flow-Unterstützung
Bekannte Einschränkungen
Einige Felicity API-Felder sind undokumentiert
API-Strukturen können sich je nach Firmware-Generation unterscheiden
SSL-Validierung ist aktuell bewusst gelockert
Einige Sensoren verwenden derzeit noch Fallback-Mappings
Anforderungen

Die Integration benötigt aktuell:

"requirements": [
  "pycryptodomex"
]
Home Assistant Kompatibilität

Getestet mit aktuellen Home-Assistant-Versionen einschließlich:

2025.x
2026.x
Haftungsausschluss

Dieses Projekt steht in keiner Verbindung zu Felicity Solar und wird nicht offiziell unterstützt.

Verwendung auf eigene Verantwortung.

Danksagung
Felicity Solar Cloud Plattform
Home Assistant Community
Reverse Engineering und Tests durch die Community
Lizenz

GNU General Public License v3.0 (GPL-3.0)
