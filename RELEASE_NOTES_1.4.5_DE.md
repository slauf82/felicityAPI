# Felicity API v1.4.5

## Neue Funktionen
- Anonymisierter Diagnoseexport über die integrierte Home-Assistant-Funktion **Diagnose herunterladen**.
- Übersicht über erkannte Gerätetypen und die Struktur verfügbarer API-/Sensorfelder.
- History-Diagnose mit Status, Datenpunktanzahl und erkannten Feldnamen, soweit verfügbar.

## Datenschutz
- Keine Übertragung der Diagnosedaten an den Entwickler oder externe Server.
- Keine Zugangsdaten, Tokens, Seriennummern, Rohmesswerte oder ungefilterten Fehlermeldungen im Export.
- Diagnose wird nur auf ausdrückliche Anforderung des Nutzers erstellt; Datei vor Veröffentlichung dennoch prüfen.

## Hinweise
- Enthält die Änderungen der v1.4.4; die Integration bleibt vollständig lesend.
- Zusätzliche Geräte können anhand freiwillig bereitgestellter Diagnosedateien besser untersucht werden.
- Ein Praxistest in Home Assistant mit echter Felicity-Cloud ist noch erforderlich.
