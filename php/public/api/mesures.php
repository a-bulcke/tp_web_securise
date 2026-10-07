<?php
// Ingestion HTTP optionnelle : POST JSON {"capteur":"temp","valeur":21.5}
// avec en-tete X-API-KEY. Necessite API_KEY dans .env + environment php-fpm.
$cle = getenv('API_KEY');
if ($cle === false || !isset($_SERVER['HTTP_X_API_KEY'])
    || !hash_equals($cle, $_SERVER['HTTP_X_API_KEY'])) {
    http_response_code(401);
    exit('Non autorise');
}
$data = json_decode(file_get_contents('php://input'), true);
if (!is_array($data) || !isset($data['valeur'])) {
    http_response_code(400);
    exit('JSON invalide');
}
$pdo = new PDO(
    'mysql:host=db;dbname=' . getenv('DB_NAME'),
    getenv('DB_USER'), getenv('DB_PASSWORD'),
    [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
);
$stmt = $pdo->prepare('INSERT INTO mesures (capteur, valeur) VALUES (?, ?)');
$stmt->execute([
    substr(strval($data['capteur'] ?? 'anonyme'), 0, 64),
    (float) $data['valeur'],
]);
header('Content-Type: application/json');
echo json_encode(['status' => 'ok']);
