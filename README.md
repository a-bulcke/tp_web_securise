# Site web sécurisé + collecte de capteurs (MQTT)

Site **PHP** ou **Django** + MySQL en HTTPS, broker **Mosquitto**
(MQTT sur TLS) et un service *bridge* qui recopie les messages MQTT en base.

## 0. Installer Docker
```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER   # puis se déconnecter/reconnecter
docker run hello-world          # test
```

## 1. Préparer les secrets

```bash
cp .env.example .env
nano .env
```
Pour générer une clé secrète pour Django :
```bash
openssl rand -base64 50
```

## 2. Créer les certificats et comptes MQTT (une seule fois)

```bash
chmod +x mosquitto/generate.sh
bash mosquitto/generate.sh
```

Voir mosquitto/README.md.

## 3. Lancer

```bash
docker compose --profile php up -d --build       # site PHP
docker compose --profile django up -d --build    # site Django
```

## 4. Tester sans capteurs (sans carte qui envoie les mesures capteurs)

```bash
mosquitto_pub -h <IP_SERVEUR> -p 8883 \
  -u capteur -P "$MQTT_DEVICE_PASSWORD" \
  --cafile mosquitto/certs/server.crt \
  -t capteurs/temp -m '{"capteur":"temp","valeur":21.5}'
```

Puis ouvrir `https://localhost/mesures.php` (PHP) ou `https://localhost/mesures`
(Django) : la mesure doit apparaître.

## Accéder au serveur depuis un autre poste (VM/Pi sans interface graphique)

⚠️ On n'accède pas au site par son IP : TLS interdit une IP dans le SNI,
donc Caddy ne peut présenter aucun certificat (`SSL_ERROR_INTERNAL_ERROR_ALERT`).
On utilise un **nom** :

1. `.env` : `DOMAIN=tpweb.local` puis `docker compose up -d --force-recreate caddy`
2. Utiliser mDNS :
    Sur le réseau local, le protocole mDNS permet à une machine de répondre elle-même
    à son nom machine.local, sans aucun fichier hosts ni serveur DNS (natif sur RasPi OS,
    et ça s'ajoute sur Debian) :
    ```bash
    sudo hostnamectl set-hostname tpweb
    sudo apt install avahi-daemon
    sudo systemctl enable --now avahi-daemon
    ```
    puis ajouter "127.0.1.1  tpweb" dans /etc/hosts :
    ```bash
    #
    sudo nano /etc/hosts
    ```
3. Ouvrir `https://tpweb.local` et accepter le certificat local (auto-signé).

En production avec un vrai domaine : enregistrement DNS type A → Caddy obtient
un certificat Let's Encrypt automatiquement, aucune entrée hosts nécessaire.

## Sécurité — rappels

- `.env`, `mosquitto/passwd` et `mosquitto/certs/` ne sont **jamais** commités.
- La carte n'a accès qu'au broker (TLS + compte `capteur`), jamais à la bdd.
- Le bridge est le seul service autorisé à écrire dans la bdd (moindre privilège).