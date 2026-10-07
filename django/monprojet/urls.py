from django.db import connection
from django.http import HttpResponse
from django.urls import path


def home(request):
    """Page de test : verifie la connexion MySQL."""
    with connection.cursor() as cursor:
        cursor.execute('SELECT VERSION()')
        version = cursor.fetchone()[0]
    html = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<title>Serveur Django operationnel</title></head>
<body>
<h1>Serveur Django operationnel</h1>
<p>Python + Django — MySQL {version}</p>
<p style="color:green">Connexion a la base OK</p>
<p><a href="/mesures">Voir les dernieres mesures capteurs</a></p>
</body></html>"""
    return HttpResponse(html)


def mesures(request):
    """Affiche les dernieres mesures collectees via MQTT par le bridge."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT capteur, valeur, ts FROM mesures '
                'ORDER BY ts DESC, id DESC LIMIT 20')
            rows = cursor.fetchall()
    except Exception:
        return HttpResponse(
            '<h1>Mesures indisponibles</h1>'
            '<p>La table mesures n\'existe pas encore '
            '(le bridge ne s\'est pas encore execute).</p>', status=503)
    lignes = ''.join(
        f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>'
        for r in rows) or '<tr><td colspan="3">Aucune mesure</td></tr>'
    html = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>Mesures</title></head>
<body><h1>Dernieres mesures (20 max)</h1>
<p><a href="/">Retour</a></p>
<table border="1" cellpadding="6">
<tr><th>Capteur</th><th>Valeur</th><th>Horodatage</th></tr>
{lignes}
</table></body></html>"""
    return HttpResponse(html)


urlpatterns = [
    path('', home),
    path('mesures', mesures),
]
