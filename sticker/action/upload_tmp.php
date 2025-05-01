<?php
// 必須
ini_set('display_errors', 1);
error_reporting(E_ALL);

// 保存先（仮）
$tmp_dir = __DIR__ . '/../tmp/';

// フォルダがなければ作成
if (!is_dir($tmp_dir)) {
    mkdir($tmp_dir, 0777, true);
}

// ファイルチェック
if (!isset($_FILES['svg_file'])) {
    http_response_code(400);
    echo 'ファイルが送信されていません。';
    exit;
}

$svg_tmp = $_FILES['svg_file']['tmp_name'];
$svg_name = basename($_FILES['svg_file']['name']);

// 仮ファイル名（タイムスタンプ＋元のファイル名）
$timestamp = time();
$tmp_filename = $timestamp . '_' . $svg_name;
$tmp_path = $tmp_dir . $tmp_filename;

// アップロード
if (!move_uploaded_file($svg_tmp, $tmp_path)) {
    http_response_code(500);
    echo '仮アップロードに失敗しました。';
    exit;
}

// 成功時：仮ファイル名だけ返す
echo $tmp_filename;
?>
