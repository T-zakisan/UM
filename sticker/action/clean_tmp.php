<?php
// 必須エラー表示
ini_set('display_errors', 1);
error_reporting(E_ALL);

// 仮ファイル保存先
$tmp_dir = __DIR__ . '/../tmp/';

// パラメータ確認
if (!isset($_GET['file']) || trim($_GET['file']) === '') {
    http_response_code(400);
    echo 'ファイル名が指定されていません。';
    exit;
}

$file = basename($_GET['file']); // パストラバーサル対策
$file_path = $tmp_dir . $file;

// 存在チェックして削除
if (is_file($file_path)) {
    if (unlink($file_path)) {
        echo '仮ファイルを削除しました。';
    } else {
        http_response_code(500);
        echo '仮ファイルの削除に失敗しました。';
    }
} else {
    http_response_code(404);
    echo '指定された仮ファイルが存在しません。';
}
?>
