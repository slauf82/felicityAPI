# felicityAPI
Version 1.0.0

Es werden im Moment 2 feste Geräte, Inverter und Batterie erzeugt, so wie das auch in der App ist. Eine flexible Geräteerkennung ist die nächste geplante Erweiterung. Ich habe mich für die wichtigsten Sensoren für Inverter (25) und Batterie (18) entschieden. Die API liefert über 600 mögliche Sensoren, wovon über 200 mit Werten gefüllt sind. Ich werde mir noch was einfallen lassen, wie ich die gefüllten Sensoren alle sichtbar machen kann, ohne euch mit Sensoren zu überfluten und zu nerven. Entweder als separates Gerät oder irgendwie abgetrennt vom Rest in einer Art extra Gruppe. Aber das muss ich noch mit ChatGPT erkunden. Diese Erweiterung wurde auch komplett mit Hilfe von ChatGPT erstellt. Aber keine Sorge, das ist so sehr getestet, dass es sehr flexibel erweiterbar ist und zudem hat mir ChatGPT bescheinigt, dass es etwa auf Herstellerniveau von der Qualität her schon ist.

Viel Spaß beim Testen !

Manual Installation : 
1. Download the latest release into config/custom_components/felicityAPI
2. Restart Home Assistant
3. Add the integration from Devices & services
4. Search for "Felicity API" and add it.

You are asked about username and password (use the same data as you entered in the FSolar App) ! The serial numbers of inverter and battery can be entered, but are optional.

Manuelle Installation :
1. Download die neueste Version nach config/custom_components/felicityAPI
2. Home Assistant neu starten
3. Füge die Integration über Geräte & Dienste hinzu
4. Suche dabei nach Felicity API und akzeptiere

Es wird nach Benutzername und Kennwort gefragt (dieselben Zugangsdaten wie in der FSolar App angeben) ! Die Seriennummern für Wechselrichter und Batterie kann angegeben werden, ist aber optional.
