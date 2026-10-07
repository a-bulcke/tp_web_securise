"""Pont MQTT -> MySQL : s'abonne au broker et insere chaque mesure.

Format attendu d'un message (JSON) :
    {"capteur": "temp_salon", "valeur": 21.5}
Si le champ "capteur" est absent, le dernier segment du topic est utilise.
"""
import json
import logging
import os
import time

import paho.mqtt.client as mqtt
import pymysql

log = logging.getLogger("bridge")
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

MQTT_HOST = os.environ.get("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_USER = os.environ.get("MQTT_USER", "bridge")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "")
TOPIC = os.environ.get("MQTT_TOPIC", "capteurs/#")

DB = dict(
    host=os.environ.get("DB_HOST", "db"),
    user=os.environ.get("DB_USER", "projet"),
    password=os.environ.get("DB_PASSWORD", ""),
    database=os.environ.get("DB_NAME", "projet"),
)


def ensure_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mesures (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                capteur VARCHAR(64) NOT NULL,
                valeur DECIMAL(12,3) NOT NULL,
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
    conn.commit()


def insert_mesure(conn, capteur, valeur):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO mesures (capteur, valeur) VALUES (%s, %s)",
            (capteur, valeur),
        )
    conn.commit()


def on_connect(client, userdata, flags, reason_code, properties):
    log.info("Connecte au broker (%s), abonnement a '%s'", reason_code, TOPIC)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    conn = userdata["conn"]
    try:
        data = json.loads(msg.payload.decode())
        capteur = str(data.get("capteur") or msg.topic.split("/")[-1])[:64]
        valeur = float(data["valeur"])
        insert_mesure(conn, capteur, valeur)
        log.info("mesure inseree : %s = %s (topic %s)",
                 capteur, valeur, msg.topic)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        log.warning("message invalide sur %s : %s", msg.topic, exc)


def main():
    conn = None
    while conn is None:
        try:
            conn = pymysql.connect(**DB)
            ensure_table(conn)
        except pymysql.MySQLError as exc:
            log.warning("base pas prete (%s), nouvelle tentative...", exc)
            time.sleep(5)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.user_data_set({"conn": conn})
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    main()
