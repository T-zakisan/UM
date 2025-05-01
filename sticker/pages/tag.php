<?php
require_once __DIR__ . '/../common/db.php';

// タグ一覧取得
$tags_stmt = $pdo->query("
    SELECT 
        tags.id, 
        tags.name, 
        COUNT(parts_tags.part_id) AS part_count
    FROM 
        tags
    LEFT JOIN 
        parts_tags ON tags.id = parts_tags.tag_id
    GROUP BY 
        tags.id, tags.name
    ORDER BY 
        tags.name ASC
");
$tags = $tags_stmt->fetchAll(PDO::FETCH_ASSOC);

// 部品一覧取得
$parts_stmt = $pdo->query("SELECT id, description_ja, description_en FROM parts_images ORDER BY id ASC");
$parts = $parts_stmt->fetchAll(PDO::FETCH_ASSOC);

// 部品ごとのタグ取得関数
function get_tags_by_part($pdo, $part_id) {
    $stmt = $pdo->prepare("SELECT t.name FROM tags t INNER JOIN parts_tags pt ON t.id = pt.tag_id WHERE pt.part_id = ? ORDER BY t.name ASC");
    $stmt->execute([$part_id]);
    $tags = $stmt->fetchAll(PDO::FETCH_COLUMN);
    return $tags ? implode(', ', $tags) : '';
}

function get_latest_version($pdo, $part_id) {
    $stmt = $pdo->prepare("SELECT MAX(version) FROM parts_versions WHERE part_id = ?");
    $stmt->execute([$part_id]);
    return $stmt->fetchColumn() ?: 1;
}
?>

<!-- 左エリア：タグ一覧 -->
<div class="left">
    <h2>タグ一覧</h2>
    <button id="reset-tags">クリア</button>
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

<!-- 中央エリア：ステッカー -->
<div class="center" id="part-list">
    <h2>ステッカー</h2>

    <div style="margin-bottom: 10px;">
        <label><input type="radio" name="view_mode" value="thumbnail" checked>サムネイル</label>
        <label><input type="radio" name="view_mode" value="list">リスト</label>
    </div>

    <!-- サムネイル表示 -->
    <div id="thumbnail-view">
        <?php foreach ($parts as $part): ?>
            <?php 
                $version = get_latest_version($pdo, $part['id']);
                $tags_text = get_tags_by_part($pdo, $part['id']);
                $description = htmlspecialchars($part['description_ja']);
                $title_text = $description . "\n" . $tags_text; // ← タグも含めてtitleを作成
            ?>
            <div class="sticker-item" data-tags="<?= htmlspecialchars($tags_text) ?>">
                <img src="./files/<?= $part['id'] ?>-<?= $version ?>.svg"
                    alt="<?= $description ?>"
                    title="<?= $title_text ?>"
                    class="thumbnail-image">
            </div>
        <?php endforeach; ?>
    </div>

    <!-- リスト表示 -->
    <div id="list-view" style="display: none;">
        <table border="1" cellpadding="5" cellspacing="0" style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>説明（日本語）</th>
                    <th>説明（英語）</th>
                    <th>タグ</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($parts as $part): ?>
                    <tr class="list-item" data-tags="<?= htmlspecialchars(get_tags_by_part($pdo, $part['id'])) ?>">
                        <td><?= htmlspecialchars($part['id']) ?></td>
                        <td><?= htmlspecialchars($part['description_ja']) ?></td>
                        <td><?= htmlspecialchars($part['description_en'] ?? '') ?></td>
                        <td><?= htmlspecialchars(get_tags_by_part($pdo, $part['id'])) ?></td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
</div>

<!-- 右エリア：部品詳細・操作 -->
<div class="right" id="detail-area">
    <h2>タグ管理</h2>

    <form action="/sticker/action/tag_action.php" method="POST" id="add-form">
        <h3>新規タグ追加</h3>
        <input type="text" name="new_tag_name" required maxlength="50" placeholder="#新規タグ">
        <button type="submit" name="action" value="add">追加</button>
    </form>

    <hr>

    <form action="/sticker/action/tag_action.php" method="POST" id="rename-form">
        <h3>タグ改名</h3>
        <div>対象タグ: <strong id="current_tag_name_rename">（未選択）</strong></div>
        <input type="text" name="new_tag_name_rename" required maxlength="50" placeholder="新しいタグ名">
        <input type="hidden" name="rename_tag_id" id="rename_tag_id">
        <button type="submit" name="action" value="rename">改名</button>
    </form>

    <hr>

    <form action="/sticker/action/tag_action.php" method="POST" id="delete-form">
        <h3>タグ削除</h3>
        <div>対象タグ: <strong id="current_tag_name_delete">（未選択）</strong></div>
        <input type="hidden" name="delete_tag_id" id="delete_tag_id">
        <button type="submit" name="action" value="delete" onclick="return confirm('本当に削除しますか？')">削除</button>
    </form>
</div>

<script>
// サムネイル拡大・縮小
document.querySelectorAll('.thumbnail-image').forEach(img => {
    img.addEventListener('dblclick', () => {
        if (img.classList.contains('expanded')) {
            // すでに拡大されていたら縮小
            img.classList.remove('expanded');
        } else {
            // 拡大されていなかったら一旦全て縮小し、自分だけ拡大
            document.querySelectorAll('.thumbnail-image.expanded').forEach(expandedImg => {
                expandedImg.classList.remove('expanded');
            });
            img.classList.add('expanded');
        }
    });
});


// サムネイル/リスト切り替え
const viewRadios = document.getElementsByName('view_mode');
const thumbnailView = document.getElementById('thumbnail-view');
const listView = document.getElementById('list-view');

viewRadios.forEach(radio => {
    radio.addEventListener('change', () => {
        thumbnailView.style.display = (radio.value === 'thumbnail') ? '' : 'none';
        listView.style.display = (radio.value === 'list') ? '' : 'none';
    });
});

// タグクリック → フィルタ＆右欄に反映
const tagItems = document.querySelectorAll('.tag-item');
tagItems.forEach(tag => {
    tag.addEventListener('click', () => {
        const selectedTag = tag.getAttribute('data-tag');
        const selectedTagId = tag.getAttribute('data-id');

        tagItems.forEach(t => t.classList.remove('selected-tag'));
        tag.classList.add('selected-tag');

        document.querySelectorAll('.sticker-item, .list-item').forEach(item => {
            const itemTags = item.getAttribute('data-tags').split(',').map(t => t.trim());
            item.style.display = itemTags.includes(selectedTag) ? '' : 'none';
        });

        document.getElementById('current_tag_name_delete').textContent = selectedTag;
        document.getElementById('current_tag_name_rename').textContent = selectedTag;
        document.getElementById('delete_tag_id').value = selectedTagId;
        document.getElementById('rename_tag_id').value = selectedTagId;
    });
});

// リセットボタン
document.getElementById('reset-tags').addEventListener('click', () => {
    tagItems.forEach(t => t.classList.remove('selected-tag'));
    document.querySelectorAll('.sticker-item, .list-item').forEach(item => {
        item.style.display = '';
    });
    document.getElementById('current_tag_name_delete').textContent = '（未選択）';
    document.getElementById('current_tag_name_rename').textContent = '（未選択）';
});
</script>
