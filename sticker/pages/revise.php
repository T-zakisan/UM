<?php
require_once __DIR__ . '/../common/db.php';

// タグ一覧取得（部品数付き）
$tags_stmt = $pdo->query("
    SELECT tags.id, tags.name, COUNT(parts_tags.part_id) AS part_count
    FROM tags
    LEFT JOIN parts_tags ON tags.id = parts_tags.tag_id
    GROUP BY tags.id, tags.name
    ORDER BY tags.name ASC
");
$tags = $tags_stmt->fetchAll(PDO::FETCH_ASSOC);

// 部品一覧取得
$parts_stmt = $pdo->query("SELECT id, description_ja, description_en FROM parts_images ORDER BY id ASC");
$parts = $parts_stmt->fetchAll(PDO::FETCH_ASSOC);

// 指定部品のタグ一覧取得
function get_tags_by_part($pdo, $part_id) {
    $stmt = $pdo->prepare("
        SELECT t.name 
        FROM tags t 
        INNER JOIN parts_tags pt ON t.id = pt.tag_id 
        WHERE pt.part_id = ? 
        ORDER BY t.name ASC
    ");
    $stmt->execute([$part_id]);
    $tags = $stmt->fetchAll(PDO::FETCH_COLUMN);
    return $tags ? implode(', ', $tags) : '';
}

// 最新版取得
function get_latest_version($pdo, $part_id) {
    $stmt = $pdo->prepare("SELECT MAX(version) FROM parts_versions WHERE part_id = ?");
    $stmt->execute([$part_id]);
    return $stmt->fetchColumn() ?: 1;
}
?>

<!-- 左エリア -->
<div class="left">
    <h2>タグ一覧</h2>

    <button id="reset-tags" style="margin-top: 10px;">クリア</button>

    <div style="margin-top: 10px;">
        <label><input type="radio" name="filter_mode" value="or" checked> OR検索</label><br>
        <label><input type="radio" name="filter_mode" value="and"> AND検索</label>
    </div>

    <ul style="list-style: none; padding: 0;">
        <?php foreach ($tags as $tag): ?>
            <li class="tag-item" 
                data-tag="<?= htmlspecialchars($tag['name']) ?>" 
                data-id="<?= htmlspecialchars($tag['id']) ?>">
                <?= htmlspecialchars($tag['name']) ?> (<?= $tag['part_count'] ?>)
            </li>
        <?php endforeach; ?>
    </ul>
</div>

<!-- 中央エリア -->
<div class="center" id="part-list">
    <h2>ステッカー</h2>

    <div id="thumbnail-view">
        <?php foreach ($parts as $part): ?>
            <?php 
                $version = get_latest_version($pdo, $part['id']);
                $tags_text = get_tags_by_part($pdo, $part['id']);
                $description = htmlspecialchars($part['description_ja']);
                $title_text = $description . "\n" . $tags_text;
            ?>
            <div class="sticker-item" 
                 data-part-id="<?= htmlspecialchars($part['id']) ?>"
                 data-description-ja="<?= htmlspecialchars($part['description_ja']) ?>"
                 data-description-en="<?= htmlspecialchars($part['description_en'] ?? '') ?>"
                 data-tags="<?= htmlspecialchars($tags_text) ?>">

                <img src="./files/<?= $part['id'] ?>-<?= $version ?>.svg"
                     alt="<?= $description ?>"
                     title="<?= $title_text ?>"
                     class="thumbnail-image">
                <br>
                <a href="./files/<?= $part['id'] ?>-<?= $version ?>.svg" download="<?= $description ?>_<?= $tags_text ?>.svg">DL</a>
            </div>
        <?php endforeach; ?>
    </div>
</div>

<!-- 右エリア -->
<div class="right" id="detail-area">
    <h2>修正登録</h2>

    <p style="color: red; font-weight: bold;">⚠画像変更のみバージョンアップ</p>

    <form action="/sticker/action/revise_action.php" method="POST" enctype="multipart/form-data" id="revise-form">
        <input type="hidden" name="part_id" id="part_id">

        <div>
            <label>説明（日本語）:</label><br>
            <input type="text" name="description_ja" id="description_ja" required maxlength="100"><br><br>
        </div>

        <div>
            <label>説明（英語）:</label><br>
            <input type="text" name="description_en" id="description_en" maxlength="100"><br><br>
        </div>

        <div>
            <label>タグ:</label><br>
            <input type="text" name="tags" id="tags" placeholder="#tag1, #tag2"><br><br>
        </div>

        <div>
            <label>修正理由（必須）:</label><br>
            <input type="text" name="reason" required maxlength="255"><br><br>
        </div>

        <div>
            <label>SVGファイル（.svg）</label><br>※変更時のみ選択:<br>
            <input type="file" name="svg_file" accept=".svg"><br><br>
        </div>

        <button type="submit">登録</button>
    </form>

    <form action="/sticker/action/revise_delete.php" method="POST" id="delete-form" style="display:none;">
        <hr>
        <input type="hidden" name="delete_part_id" id="delete_part_id">
        <button type="submit" onclick="return confirm('本当に削除しますか？');">削除</button>
    </form>
</div>

<script>
// フィルタモード
let filterMode = 'or';

// タグクリックでフィルタリング
const tagItems = document.querySelectorAll('.tag-item');
tagItems.forEach(tag => {
    tag.addEventListener('click', () => {
        tag.classList.toggle('selected-tag');
        applyFilter();
    });
});

// OR/AND切り替え
document.querySelectorAll('input[name="filter_mode"]').forEach(radio => {
    radio.addEventListener('change', () => {
        filterMode = radio.value;
        applyFilter();
    });
});

// フィルタ処理
function applyFilter() {
    const selectedTags = Array.from(document.querySelectorAll('.tag-item.selected-tag'))
        .map(tag => tag.getAttribute('data-tag'));

    document.querySelectorAll('.sticker-item').forEach(item => {
        const itemTags = item.getAttribute('data-tags').split(',').map(t => t.trim());

        if (selectedTags.length === 0) {
            item.style.display = '';
        } else if (filterMode === 'or') {
            const match = selectedTags.some(tag => itemTags.includes(tag));
            item.style.display = match ? '' : 'none';
        } else if (filterMode === 'and') {
            const match = selectedTags.every(tag => itemTags.includes(tag));
            item.style.display = match ? '' : 'none';
        }
    });
}

// リセットボタン
document.getElementById('reset-tags').addEventListener('click', () => {
    tagItems.forEach(tag => tag.classList.remove('selected-tag'));
    applyFilter();
});

// ステッカークリック → 右欄に情報セット
const stickerItems = document.querySelectorAll('.sticker-item');
const partIdInput = document.getElementById('part_id');
const descriptionJaInput = document.getElementById('description_ja');
const descriptionEnInput = document.getElementById('description_en');
const tagsInput = document.getElementById('tags');
const deleteForm = document.getElementById('delete-form');
const deletePartIdInput = document.getElementById('delete_part_id');

stickerItems.forEach(item => {
    item.addEventListener('click', () => {
        partIdInput.value = item.getAttribute('data-part-id');
        descriptionJaInput.value = item.getAttribute('data-description-ja');
        descriptionEnInput.value = item.getAttribute('data-description-en');
        tagsInput.value = item.getAttribute('data-tags');
        deletePartIdInput.value = item.getAttribute('data-part-id');
        deleteForm.style.display = 'block';
    });
});

// 送信前タグ整形
document.getElementById('revise-form').addEventListener('submit', function() {
    let tagsText = tagsInput.value.trim();
    tagsText = tagsText
        .replace(/[、。,．・\s　]+/g, ',')
        .replace(/,+/g, ',')
        .replace(/^,|,$/g, '');
    tagsInput.value = tagsText;
});
</script>
