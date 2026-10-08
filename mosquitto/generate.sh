#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Charger les mots de passe depuis ../.env
set -a; source ../.env; set +a

# 1. Certificat auto-signe pour MQTT/TLS (un an, CN=mosquitto)
mkdir -p certs
openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
  -keyout certs/server.key -out certs/server.crt \
  -subj "/CN=mosquitto" \
  -addext "subjectAltName=DNS:mosquitto,IP:127.0.0.1"

# 2. Comptes MQTT : le bridge + les cartes
docker run --rm -v "$PWD:/mosquitto" eclipse-mosquitto:2 \
  sh -c "mosquitto_passwd -c -b /mosquitto/passwd '$MQTT_BRIDGE_USER' '$MQTT_BRIDGE_PASSWORD' \
      && mosquitto_passwd -b /mosquitto/passwd '$MQTT_DEVICE_USER' '$MQTT_DEVICE_PASSWORD'"

# 3. Permissions : dans le conteneur, mosquitto tourne sous l'uid 1883
sudo chown 1883:1883 passwd certs/server.key
sudo chmod 700 passwd
sudo chmod 600 certs/server.key
sudo chmod 644 certs/server.crt

echo "OK : certs/ et passwd crees avec les bonnes permissions."