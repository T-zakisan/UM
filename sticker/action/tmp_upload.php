<?php
// エラー表示を有効化
ini_set('display_errors', 1);
error_reporting(E_ALL);

// 仮アップロード先ディレクトリ
$tmp_dir = __DIR__ . '/../tmp/';

// フォルダがなければ作成
if (!is_dir($tmp_dir)) {
    mkdir($tmp_dir, 0777, true);
}

// ファイルが送信されていない場合
if (!isset($_FILES['svg_file']) || $_FILES['svg_file']['error'] !== UPLOAD_ERR_OK) {
    http_response_code(400);
    echo 'ファイルが送信されていません。';
    exit;
}

// ファイル名と仮保存パス
$original_name = basename($_FILES['svg_file']['name']);
$timestamp = time();
$tmp_filename = $timestamp . '_' . $original_name;
$tmp_path = $tmp_dir . $tmp_filename;

// move_uploaded_fileで仮保存
if (!move_uploaded_file($_FILES['svg_file']['tmp_name'], $tmp_path)) {
    http_response_code(500);
    echo '仮アップロードに失敗しました。';
    exit;
}

// 成功時：仮ファイル名だけ返す
echo $tmp_filename;
?>
