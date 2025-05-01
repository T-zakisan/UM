<?php
// ダウンロード対象ディレクトリ
$base_dir = __DIR__ . '/../files/';  // ★統一のため "../files/" にしておきます（他ファイルに合わせる）

// エラー表示用関数
function download_error_exit($message) {
    echo "<script>alert(" . json_encode($message) . "); history.back();</script>";
    exit;
}

// パラメータ取得
$id = (int)($_GET['id'] ?? 0);
$version = (int)($_GET['version'] ?? 0);
$type = $_GET['type'] ?? '';

if ($id === 0 || $version === 0 || ($type !== 'svg' && $type !== 'pdf')) {
    download_error_exit('無効なリクエストです。');
}

// ファイル名組み立て
$filename = "{$id}-{$version}.{$type}";
$filepath = $base_dir . $filename;

if (!file_exists($filepath)) {
    download_error_exit('ファイルが存在しません。');
}

// ファイルダウンロードヘッダ送信
header('Content-Description: File Transfer');
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename="' . basename($filename) . '"');
header('Expires: 0');
header('Cache-Control: must-revalidate');
header('Pragma: public');
header('Content-Length: ' . filesize($filepath));

// ファイル送信
readfile($filepath);
exit;
?>
