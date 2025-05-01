<?php
require_once '../common/db.php'; // DB接続ファイル

// POSTデータからアクション取得
$action = $_POST['action'] ?? '';

function js_back($message) {
    echo "<script>alert(" . json_encode($message) . "); history.back();</script>";
    exit;
}

if ($action === 'add') {
    // タグ新規追加
    $new_tag_name = trim($_POST['new_tag_name'] ?? '');

    if ($new_tag_name === '') {
        js_back('タグ名が入力されていません。');
    }

    // 同名タグが存在しないか確認
    $stmt = $pdo->prepare("SELECT id FROM tags WHERE name = ?");
    $stmt->execute([$new_tag_name]);
    if ($stmt->fetch()) {
        js_back('同じタグ名がすでに存在します！');
    }

    // タグ追加
    $stmt = $pdo->prepare("INSERT INTO tags (name) VALUES (?)");
    $stmt->execute([$new_tag_name]);

    header('Location: ../index.php?page=tag');
    exit;

} elseif ($action === 'rename') {
    // タグ改名
    $rename_tag_id = (int)($_POST['rename_tag_id'] ?? 0);
    $new_tag_name_rename = trim($_POST['new_tag_name_rename'] ?? '');

    if ($rename_tag_id === 0 || $new_tag_name_rename === '') {
        js_back('改名対象または新しいタグ名が入力されていません。');
    }

    // 同名タグがすでに存在しないかチェック
    $stmt = $pdo->prepare("SELECT id FROM tags WHERE name = ?");
    $stmt->execute([$new_tag_name_rename]);
    if ($stmt->fetch()) {
        js_back('同じタグ名がすでに存在します！');
    }

    // タグ名更新
    $stmt = $pdo->prepare("UPDATE tags SET name = ? WHERE id = ?");
    $stmt->execute([$new_tag_name_rename, $rename_tag_id]);

    header('Location: ../index.php?page=tag');
    exit;

} elseif ($action === 'delete') {
    // タグ削除
    $delete_tag_id = (int)($_POST['delete_tag_id'] ?? 0);

    if ($delete_tag_id === 0) {
        js_back('削除対象が指定されていません。');
    }

    // タグ削除
    $stmt = $pdo->prepare("DELETE FROM tags WHERE id = ?");
    $stmt->execute([$delete_tag_id]);

    header('Location: ../index.php?page=tag');
    exit;

} else {
    js_back('不正な操作です。');
}
?>
