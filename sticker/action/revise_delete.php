<?php
require_once __DIR__ . '/../common/db.php';

ini_set('display_errors', 1);
error_reporting(E_ALL);

// ★エラー表示用関数
function js_back($message) {
    echo "<script>alert(" . json_encode($message) . "); history.back();</script>";
    exit;
}

// POSTから部品ID取得
$part_id = (int)($_POST['delete_part_id'] ?? 0);

// 必須チェック
if ($part_id <= 0) {
    js_back('不正なIDです。');
}

// 1. データベースから削除
try {
    $pdo->beginTransaction();

    // parts_tags削除
    $stmt = $pdo->prepare("DELETE FROM parts_tags WHERE part_id = ?");
    $stmt->execute([$part_id]);

    // parts_versions削除
    $stmt = $pdo->prepare("DELETE FROM parts_versions WHERE part_id = ?");
    $stmt->execute([$part_id]);

    // parts_images削除
    $stmt = $pdo->prepare("DELETE FROM parts_images WHERE id = ?");
    $stmt->execute([$part_id]);

    $pdo->commit();
} catch (Exception $e) {
    $pdo->rollBack();
    js_back('データベース削除中にエラーが発生しました。');
}

// 2. ファイル削除
$upload_dir = __DIR__ . '/../files/';

// SVGとPDFを削除
foreach (glob($upload_dir . "{$part_id}-*.svg") as $file) {
    @unlink($file);
}
foreach (glob($upload_dir . "{$part_id}-*.pdf") as $file) {
    @unlink($file);
}

// 3. 完了後リダイレクト
header('Location: ../index.php?page=revise');
exit;
?>
