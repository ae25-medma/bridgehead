# Seite der Kliniken

Auf der Seite der Kliniken werden 3 Komponentn benötigt:

- Beam Proxy
- File Sender
- File Receiver

Diese drei Komponenten sind in einem Docker-Compose File enthalten und können aus dem Repository gezogen und direkt gestartet werden.

# Daten Senden

Zum senden der Daten auf der Seite der Kliniken, kann die API über die URL http://<IP_ADDRESS>/send mit dem übersenden der Dateien mit einem POST Befehl übersendet werden. Diese werden dann über den Bridgehead an die zu übersendenden Stelle gesendet. 