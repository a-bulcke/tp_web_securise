<?php
// Page de test : verifie PHP + extension MySQL + connexion a la base.
$pdo = new PDO(
    'mysql:host=db;dbname=' . getenv('DB_NAME'),
    getenv('DB_USER'),
    getenv('DB_PASSWORD'),
    [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
);
$stmt = $pdo->query('SELECT VERSION() AS v');
$version = $stmt->fetch()['v'];
?>
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Test serveur</title></head>
<body>
    <h1>Serveur operationnel</h1>
    <p>PHP <?= PHP_VERSION ?> — MySQL <?= htmlspecialchars($version) ?></p>
    <p style="color:green">Connexion a la base <code><?= htmlspecialchars(getenv('DB_NAME')) ?></code> : OK</p>
    <p><a href="mesures.php">Voir les dernieres mesures capteurs</a></p>
</body>
</html>
