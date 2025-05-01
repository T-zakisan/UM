<?php
$page = $_GET['page'] ?? 'tag'; // 今のページ取得
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ステッカー管理システム</title>
    <link rel="stylesheet" href="/sticker/common/style.css">
</head>
<body>

<div class="header">
    <div class="header-title">Sticker</div>
    <nav class="header-nav">
        <a href="index.php?page=tag" class="<?= $page === 'tag' ? 'active' : '' ?>">タグ管理</a>
        <a href="index.php?page=revise" class="<?= $page === 'revise' ? 'active' : '' ?>">修正・版管理</a>
        <a href="index.php?page=upload" class="<?= $page === 'upload' ? 'active' : '' ?>">新規登録</a>
        <a href="index.php?page=export" class="<?= $page === 'export' ? 'active' : '' ?>">ファイル出力</a>
    </nav>
</div>
