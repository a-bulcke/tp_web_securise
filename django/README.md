# Variante Django

Le projet minimal (`monprojet/`) est fourni : page de test + affichage des
mesures capteurs. Developpez votre application par-dessus.

Lancement : `docker compose --profile django up -d --build`
Basculer le Caddyfile sur `reverse_proxy django:8000`.
Creer avant lancement : `mkdir -p static media`
