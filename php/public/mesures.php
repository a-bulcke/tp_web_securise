<?php
// Lecture des dernieres mesures publiees par les capteurs (via MQTT).
$pdo = new PDO(
    'mysql:host=db;dbname=' . getenv('DB_NAME'),
    getenv('DB_USER'),
    getenv('DB_PASSWORD'),
    [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
);
$rows = $pdo->query(
    'SELECT capteur, valeur, ts FROM mesures ORDER BY ts DESC, id DESC LIMIT 20'
)->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Mesures capteurs</title></head>
<body>
    <h1>Dernieres mesures (20 max)</h1>
    <p><a href="index.php">Retour au test serveur</a></p>
    <?php if (!$rows): ?>
        <p>Aucune mesure pour le moment. Publiez-en une sur le broker MQTT.</p>
    <?php else: ?>
    <table border="1" cellpadding="6">
        <tr><th>Capteur</th><th>Valeur</th><th>Horodatage</th></tr>
        <?php foreach ($rows as $r): ?>
        <tr>
            <td><?= htmlspecialchars($r['capteur']) ?></td>
            <td><?= htmlspecialchars($r['valeur']) ?></td>
            <td><?= htmlspecialchars($r['ts']) ?></td>
        </tr>
        <?php endforeach ?>
    </table>
    <?php endif ?>
</body>
</html>
