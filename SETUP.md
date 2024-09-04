## Design choices

### Broker

Ein Broker für alle UC und Regionen in denen pro Region-UC-Kombination ein "Postfach" generiert wird.

### Blaze

FHIR Server zur Ablage und Verarbeitung von strukturierten Daten.

### Beam File Exchange 

-> Link zum Repo von Patrick

## Tutorial

- Server für jeden Bridgehead und jedne Broker aufsetzen (16GB RAM)
- Domain für den Broker festlegen broker-test.health-innovation-lab.eu
- In jedem Server git, docker und docker compose installieren (Broker + Bridgeheads)

### Broker aufsetzen:
- Im Verzeichnis /srv/docker folgenden command ausführen
  ``` git clone https://github.com/samply/beam-deploy```
- In der docker compose /srv/docker/beam-deploy die networks auskommentieren und die BIND-ADDR: 0.0.0.0:8080 setzen (traefic wird hier nicht benutzt)
- Template env-datei in /srv/docker/beam-deploy kopieren und anpassen (Anzupassen PROJECT, BROKER_ID, BROKER_URL)
- Command ausführen ``` source .env ```
- Installieren von jq (sudo apt install jq -y)
- Ausführen des initial vault setup scripts (sudo /srv/docker/beam-deploy/pki-scripts/initial_vault_setup.sh)
- Command susführen: ```sudo /srv/docker/beam-deploy/pki-scripts/create_privkey_and_cert.sh broker``` (Funktioniert nur bei korrekten Versionen https://github.com/samply/bridgehead?tab=readme-ov-file#software)
- Unseal key bekommen und abspeichern (Wenn der Broker down ist kann man mit Hilfe des Keys den Vault unsealen. Command steht im Readme.md vom geklonten Repo)
- ```sudo docker compose up -d```
- Checken ob der Broker läuft ```curl -v localhost:80```

### Broker unsealen:
- ```sudo docker compose up -d```
- ```sudo docker compose exec -it -e VAULT_ADDR=http://localhost:8200/ vault vault operator unseal```
- Unseal-Key: JEt4Jhpr86+q6qhTmYIuAFxr807tA9Aw/Ws3qP5XFOg=

### Bridgehead aufsetzen:
- ```sudo mkdir -p /srv/docker```
- Im Verzeichnis /srv/docker folgenden command ausführen
  ``` sudo git clone --branch pro/lemedart https://github.com/ae25-medma/bridgehead.git```
- ```cd /srv/docker/bridgehead```
- ```sudo git checkout pro/lemedart``` (Anschließend den angezeigten command ausführen ```git config --global --add safe.directory /srv/docker/bridgehead```)
- ```sudo mkdir /etc/bridgehead```
- ```sudo echo SITE_ID=<Name> > leme.conf``` (Erstellen der leme.conf ```sudo su``` wird für den Command benötigt)
- ```sudo ./bridgehead install leme``` (Troubleshooting, wenn leme.conf nicht funkt: Enter region name)
- ```sudo ./bridgehead enroll leme```
- Kopieren des Zertifikats in den Broker /srv/docker/beam-deploy/csr/<Name>.csr
- ```sudo /srv/docker/beam-deploy/pki-scripts/managepki sign --csr-file csr/<name>.csr --common-name=<name>.broker-test.health-innovation-lab.eu```
- Bridgehead starten ```sudo systemctl start bridgehead@leme``` (command zum starten des Bridgeheads)
- ```sudo journalctl -u bridgehead@leme -f``` (Um zu sehen was der bridgehead macht)
- Bridgehead Passwort in "/etc/bridgehead/leme.local.conf"

### Bridgehead troubleshooting
- curl Befehl auf den Broker um zu schauen welche Standorte aktiv sind: ```curl broker-test.health-innovation-lab.eu/v1/health/proxies```
- root.crt.pem in den ordner leme hizufügen
- ```sudo systemctl restart bridgehead@leme```

### Broker Zertifikate erneurn
- ```sudo /srv/docker/beam-deploy/pki-scripts/managepki list``` (Liste von den Zertifikaten und wann sie auslaufen)
- ```sudo /srv/docker/beam-deploy/pki-scripts/managepki sign --csr-file csr/<name>.csr --common-name=<name>.broker-test.health-innovation-lab.eu``` (Erneuern der Zertifikate)



### Upload Data to bridgehead

- ```sudo docker compose enroll get-root-cert --no-log-prefix```
- Kopieren des Zertifikats in den Broker /srv/docker/beam-deploy/csr/<Name>.csr
- execute in Broker no underscores ('_')!: ```sudo /srv/docker/beam-deploy/pki-scripts/managepki sign --csr-file csr/<name>.csr --common-name=<name>.broker-test.health-innovation-lab.eu```
Back to Standort
- ```sudo docker compose beam-proxy```
- In uploader unter command `command: ["send", "--to", "downloader.<other_proxy>"]`  `<other_proxy>` add bridgehead name
- ```sudo docker compose run -v ./<fileToTransfere>:/Data/<savingFileName> uploader /Data/<savingFileName>```
- add to docker compose in receiving Instance /srv/docker/bridgehead/leme/docker-compose.yaml to check for avalible data requests:

``` yaml
 beam-proxy:
    image: docker.verbis.dkfz.de/cache/samply/beam-proxy:develop-sockets      # <-- CHANGED
    container_name: bridgehead-beam-proxy
    environment:
      BROKER_URL: ${BROKER_URL}
      PROXY_ID: ${PROXY_ID}
      APP_focus_KEY: ${FOCUS_BEAM_SECRET_SHORT}
      APP_downloader_KEY: "SUPERSECRETAPIKEY"                                 # <-- ADDED
      PRIVKEY_FILE: /run/secrets/proxy.pem
      ALL_PROXY: http://forward_proxy:3128
      TLS_CA_CERTIFICATES_DIR: /conf/trusted-ca-certs
      ROOTCERT_FILE: /conf/root.crt.pem

    secrets:
      - proxy.pem
    depends_on:
      - "forward_proxy"
    volumes:
      - /etc/bridgehead/trusted-ca-certs:/conf/trusted-ca-certs:ro
      - /srv/docker/bridgehead/leme/root.crt.pem:/conf/root.crt.pem:ro

  downloader:
    image: samply/beam-file:task-based-files
    environment:
      BEAM_ID: "downloader.${PROXY_ID}"
      BEAM_SECRET: "SUPERSECRETAPIKEY"
      BEAM_URL: "http://beam-proxy:8081"
    command: ["receive", "save", "-o", "/Data", "-p", "%f_%n_%t"]
             # L-> can be changet to ["receive", "callback", "INPUT_URL"]
    volumes:
      - /home/ubuntu/Data:/Data                                               # <-- CHANGE TO DESIRED DIRECTORY
```

- restart bridghead : `sudo systemctl restart bridgehead@leme.service`
