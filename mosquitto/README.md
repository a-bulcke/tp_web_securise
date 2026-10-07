# Broker MQTT — préparation

    bash generate.sh

Le script crée :
- `certs/server.crt` + `certs/server.key` : certificat TLS du broker ;
- `passwd` : comptes `bridge` (ingestion) et `capteur` (cartes).

Ces fichiers sont **ignorés par Git** (secrets). Le `server.crt` doit être
copié sur les cartes capteurs pour qu'elles vérifient le broker (anti-MITM).

## Publication (test ou depuis une carte)

    mosquitto_pub -h <IP_SERVEUR> -p 8883 \
      -u capteur -P "$MQTT_DEVICE_PASSWORD" \
      --cafile certs/server.crt \
      -t capteurs/temp -m '{"capteur":"temp","valeur":21.5}'

## Écoute (debug)

    mosquitto_sub -h <IP_SERVEUR> -p 8883 \
      -u capteur -P "$MQTT_DEVICE_PASSWORD" \
      --cafile certs/server.crt -t 'capteurs/#' -v
