<?php
require_once __DIR__ . '/../common/db.php';

ini_set('display_errors', 1);
error_reporting(E_ALL);

// 保存先ディレクトリ
$upload_dir = __DIR__ . '/../files/';
$tmp_dir = __DIR__ . '/../tmp/';

// ★共通エラー出力用関数
function js_back($message) {
    echo "<script>alert(" . json_encode($message) . "); history.back();</script>";
    exit;
}

// POSTデータ取得
$description_ja = trim($_POST['description_ja'] ?? '');
$description_en = trim($_POST['description_en'] ?? '');
$part_no = trim($_POST['part_no'] ?? '');
$tmp_filename = $_POST['tmp_filename'] ?? '';
$new_tags_text = trim($_POST['tags'] ?? '');

// 必須チェック
if ($description_ja === '' || $tmp_filename === '') {
    js_back('説明（日本語）と仮アップロードファイルは必須です。');
}

// 仮ファイル存在確認
$tmp_path = $tmp_dir . $tmp_filename;
if (!file_exists($tmp_path)) {
    js_back('仮アップロードファイルが存在しません。');
}

// parts_imagesテーブルに登録
$stmt = $pdo->prepare("INSERT INTO parts_images (description_ja, description_en, part_no) VALUES (?, ?, ?)");
$stmt->execute([$description_ja, $description_en, $part_no]);
$part_id = $pdo->lastInsertId();

// バージョン登録（ver=1）
$stmt = $pdo->prepare("INSERT INTO parts_versions (part_id, version, reason) VALUES (?, 1, '新規登録')");
$stmt->execute([$part_id]);

// 正式保存ファイル名
$svg_path = $upload_dir . "{$part_id}-1.svg";
$pdf_path = $upload_dir . "{$part_id}-1.pdf";

// 仮ファイルを正式保存に移動
if (!rename($tmp_path, $svg_path)) {
    js_back('仮ファイルの移動に失敗しました。');
}

// PDF変換（Inkscape使用）
exec("inkscape \"$svg_path\" --export-type=pdf --export-filename=\"$pdf_path\"", $output, $return_var);
if ($return_var !== 0) {
    js_back('PDF変換に失敗しました。');
}

// タグ登録
$new_tag_list = array_filter(array_map('trim', preg_split('/[、。,．・\s　,]+/u', $new_tags_text)));
if (empty($new_tag_list)) {
    js_back('タグを選択または入力してください。');
}

$tag_ids = [];
foreach ($new_tag_list as $tag_name) {
    $stmt = $pdo->prepare("SELECT id FROM tags WHERE name = ?");
    $stmt->execute([$tag_name]);
    $tag = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$tag) {
        $stmt = $pdo->prepare("INSERT INTO tags (name) VALUES (?)");
        $stmt->execute([$tag_name]);
        $tag_id = $pdo->lastInsertId();
    } else {
        $tag_id = $tag['id'];
    }
    $tag_ids[] = $tag_id;
}

// 重複排除
$tag_ids = array_unique($tag_ids);

// parts_tagsに登録
foreach ($tag_ids as $tag_id) {
    $stmt = $pdo->prepare("INSERT INTO parts_tags (part_id, tag_id) VALUES (?, ?)");
    $stmt->execute([$part_id, $tag_id]);
}

// 完了 → uploadページへ戻す
header('Location: ../index.php?page=upload');
exit;
?>
