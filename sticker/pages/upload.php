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
    ORDER BY tags.name ASC
");
$tags = $tags_stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!-- 左エリア -->
<div class="left">
    <h2>タグ一覧</h2>

    <button id="reset-tags" style="margin-top: 10px;">クリア</button>

    <ul style="list-style: none; padding: 0;">
        <?php foreach ($tags as $tag): ?>
            <li class="tag-item" data-tag="<?= htmlspecialchars($tag['name']) ?>">
                <?= htmlspecialchars($tag['name']) ?> (<?= $tag['part_count'] ?>)
            </li>
        <?php endforeach; ?>
    </ul>
</div>

<!-- 中央エリア -->
<div class="center">
    <h2>新規登録</h2>

    <form id="upload-form" method="POST" enctype="multipart/form-data" action="/sticker/action/upload_action.php">

        <input type="hidden" name="tmp_filename" id="tmp_filename">

        <div>
            <label>説明（日本語）:</label><br>
            <input type="text" name="description_ja" required><br><br>
        </div>

        <div>
            <label>説明（英語）:</label><br>
            <input type="text" name="description_en"><br><br>
        </div>

        <div>
            <label>部品番号：</label><br>
            <input type="text" name="part_no"><br><br>
        </div>

        <div>
            <label>タグ:</label><br>
            <textarea name="tags" id="tags" rows="3" style="resize: vertical; width: 90%;"></textarea><br><br>
        </div>

        <div>
            <label>SVGファイル (.svg):</label><br>
            <input type="file" name="svg_file" id="svg_file" accept=".svg" required><br><br>
        </div>

        <button type="button" id="pre-upload-btn">登録</button>
    </form>
</div>

<!-- 右エリア -->
<div class="right">
    <h2>補足エリア</h2>
    <div><label>説明（日本語）</label></div>
    <div>必須</div>
    <p></p>
    <div><label>タグ</label></div>
		<div>リストクリックで追加</div>
    <div>スペース区切り</div>
    <div>複数行対応</div>
</div>

<!-- スクリプト -->
<script>
// タグクリック
const tagItems = document.querySelectorAll('.tag-item');
const tagsInput = document.getElementById('tags');

tagItems.forEach(tag => {
    tag.addEventListener('click', () => {
        const selectedTag = tag.getAttribute('data-tag').trim();
        let currentTags = tagsInput.value.split(',').map(t => t.trim()).filter(t => t);

        if (tag.classList.contains('selected-tag')) {
            currentTags = currentTags.filter(t => t !== selectedTag);
            tag.classList.remove('selected-tag');
        } else {
            if (!currentTags.includes(selectedTag)) {
                currentTags.push(selectedTag);
            }
            tag.classList.add('selected-tag');
        }

        tagsInput.value = currentTags.join(', ');
    });
});

// リセットボタン
document.getElementById('reset-tags').addEventListener('click', () => {
    tagItems.forEach(tag => tag.classList.remove('selected-tag'));
    tagsInput.value = '';
});

// 登録ボタン押下 → 仮アップロード＆プレビュー確認
document.getElementById('pre-upload-btn').addEventListener('click', () => {
    const svgInput = document.getElementById('svg_file');
    if (!svgInput.files.length) {
        alert('SVGファイルを選択してください。');
        return;
    }

    const formData = new FormData();
    formData.append('svg_file', svgInput.files[0]);

    fetch('/sticker/action/tmp_upload.php', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(tmpFilename => {
        if (!tmpFilename.endsWith('.svg')) {
            alert('仮アップロード失敗：' + tmpFilename);
            return;
        }

        document.getElementById('tmp_filename').value = tmpFilename;

        // 仮ファイルをプレビュー表示
        showPreview(tmpFilename);
    })
    .catch(error => {
        console.error('通信エラー:', error);
        alert('通信エラーが発生しました。');
    });
});

// 仮ファイルプレビュー表示
function showPreview(tmpFilename) {

	const width = 500;
	const height = 600;
	const left = (screen.width - width) / 2;
	const top = (screen.height - height) / 2;
	const previewWindow = window.open('', '_blank', `width=${width},height=${height},left=${left},top=${top}`);


    if (!previewWindow) {
        alert('ポップアップブロックを解除してください。');
        return;
    }

    previewWindow.document.write(`
        <html>
        <head><title>仮アップロードファイル確認</title></head>
        <body style="text-align: center;">
            <h2>プレビュー確認</h2>
            <img src="/sticker/tmp/${tmpFilename}" style="max-width:90%; max-height:500px; border:1px solid #ccc;"><br><br>
            <button onclick="window.opener.confirmAndSubmit('${tmpFilename}'); window.close();">このファイルで登録</button>
            <button onclick="window.opener.cancelAndDelete('${tmpFilename}'); window.close();">キャンセル</button>
        </body>
        </html>
    `);
}

// 登録送信
function confirmAndSubmit(tmpFilename) {
    document.getElementById('upload-form').submit();
}

// 仮ファイル削除
function cancelAndDelete(tmpFilename) {
    fetch('/sticker/action/clean_tmp.php?file=' + encodeURIComponent(tmpFilename))
    .then(() => {
        alert('仮ファイルを削除しました。');
        document.getElementById('tmp_filename').value = '';
    });
}
</script>
