<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// ページ指定（デフォルトはtag）
$page = $_GET['page'] ?? 'tag';

// ヘッダー読み込み
require_once 'common/header.php';

// コンテンツエリア開始
echo '<div class="container">';

// ページ切り替え
$page_file = '';

if ($page === 'tag') {
    require_once 'pages/tag.php';
} elseif ($page === 'revise') {
    require_once 'pages/revise.php';
} elseif ($page === 'upload') {
    require_once 'pages/upload.php';
} elseif ($page === 'export') {
    require_once 'pages/export.php';
} else {
    echo "<p>ページが存在しません。</p>";
}

// コンテンツエリア終了
echo '</div>';

// body, html閉じタグは各ページで！
?>
