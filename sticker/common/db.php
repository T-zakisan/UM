<?php
// db.php （共通DB接続ファイル）

$host = 'localhost';
$dbname = 'sticker_db';
$username = 'sticker_user';
$password = 'sticker_pass';

// エラー表示関数（共通化）
function db_error_exit($message) {
    echo "<script>alert(" . json_encode($message) . ");</script>";
    exit;
}

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    db_error_exit('データベース接続失敗: ' . $e->getMessage());
}
?>
