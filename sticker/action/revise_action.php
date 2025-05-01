<?php
require_once __DIR__ . '/../common/db.php';

ini_set('display_errors', 1);
error_reporting(E_ALL);

// ★共通エラー出力用関数
function js_back($message) {
    echo "<script>alert(" . json_encode($message) . "); history.back();</script>";
    exit;
}

// POSTデータ取得
$part_id = (int)($_POST['part_id'] ?? 0);
$description_ja = trim($_POST['description_ja'] ?? '');
$description_en = trim($_POST['description_en'] ?? '');
$tags_text = trim($_POST['tags'] ?? '');
$reason = trim($_POST['reason'] ?? '');

// 必須チェック
if ($part_id === 0 || $reason === '') {
    js_back('部品IDまたは修正理由が入力されていません。');
}

// 1. 説明（日本語・英語）更新
$stmt = $pdo->prepare("UPDATE parts_images SET description_ja = ?, description_en = ? WHERE id = ?");
$stmt->execute([$description_ja, $description_en, $part_id]);

// 2. タグ更新
if ($tags_text !== '') {
    // 一旦すべてのタグ解除
    $pdo->prepare("DELETE FROM parts_tags WHERE part_id = ?")->execute([$part_id]);

    // タグ再登録（区切り文字を統一）
    $tag_list = array_filter(array_map('trim', preg_split('/[、。,．・\s　,]+/u', $tags_text)));
    foreach ($tag_list as $tag_name) {
        if ($tag_name === '') continue;

        // タグID取得（なければ新規登録）
        $stmt = $pdo->prepare("SELECT id FROM tags WHERE name = ?");
        $stmt->execute([$tag_name]);
        $tag = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($tag) {
            $tag_id = $tag['id'];
        } else {
            $stmt = $pdo->prepare("INSERT INTO tags (name) VALUES (?)");
            $stmt->execute([$tag_name]);
            $tag_id = $pdo->lastInsertId();
        }

        // 部品とタグの紐付け
        $stmt = $pdo->prepare("INSERT INTO parts_tags (part_id, tag_id) VALUES (?, ?)");
        $stmt->execute([$part_id, $tag_id]);
    }
}

// 3. 画像ファイル修正時のみ、版アップ＋ファイル保存
$has_new_svg = isset($_FILES['svg_file']) && $_FILES['svg_file']['error'] === UPLOAD_ERR_OK;
$has_new_pdf = isset($_FILES['pdf_file']) && $_FILES['pdf_file']['error'] === UPLOAD_ERR_OK;

if ($has_new_svg) {
    // 最新版取得
    $stmt = $pdo->prepare("SELECT MAX(version) FROM parts_versions WHERE part_id = ?");
    $stmt->execute([$part_id]);
    $current_version = (int)($stmt->fetchColumn() ?? 1);
    $new_version = $current_version + 1;

    // parts_versionsに登録
    $stmt = $pdo->prepare("INSERT INTO parts_versions (part_id, version, reason) VALUES (?, ?, ?)");
    $stmt->execute([$part_id, $new_version, $reason]);

    // ファイル保存
    $upload_dir = __DIR__ . '/../files/';
    $svg_path = $upload_dir . "{$part_id}-{$new_version}.svg";
    move_uploaded_file($_FILES['svg_file']['tmp_name'], $svg_path);

    // PDF変換（SVGから自動生成）
    $pdf_path = $upload_dir . "{$part_id}-{$new_version}.pdf";
    exec("inkscape \"$svg_path\" --export-type=pdf --export-filename=\"$pdf_path\"", $output, $return_var);
    if ($return_var !== 0) {
        js_back('PDF変換に失敗しました。');
    }
}

// 完了後リダイレクト
header('Location: ../index.php?page=revise');
exit;
?>
