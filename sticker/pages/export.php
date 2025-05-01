<?php
require_once __DIR__ . '/../common/db.php';

// タグ一覧取得
$tags_stmt = $pdo->query("
    SELECT tags.id, tags.name, COUNT(parts_tags.part_id) AS part_count
    FROM tags
    LEFT JOIN parts_tags ON tags.id = parts_tags.tag_id
    GROUP BY tags.id, tags.name
    ORDER BY tags.name ASC
");
$tags = $tags_stmt->fetchAll(PDO::FETCH_ASSOC);

// 部品一覧取得
$parts_stmt = $pdo->query("SELECT id, description_ja FROM parts_images ORDER BY id ASC");
$parts = $parts_stmt->fetchAll(PDO::FETCH_ASSOC);

// 部品ごとのタグ取得
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


<div class="left">
  <h2>タグ一覧</h2>
  <button id="reset-tags" style="margin-top: 10px;">クリア</button>
  <div style="margin-top: 10px;">
    <label><input type="radio" name="filter_mode" value="or" checked> OR検索</label><br>
    <label><input type="radio" name="filter_mode" value="and"> AND検索</label>
  </div>
  <ul style="list-style: none; padding: 0;">
    <?php foreach ($tags as $tag): ?>
      <li class="tag-item" data-tag="<?= htmlspecialchars($tag['name']) ?>">
        <?= htmlspecialchars($tag['name']) ?> (<?= $tag['part_count'] ?>)
      </li>
    <?php endforeach; ?>
  </ul>
</div>


<div class="center">
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
           data-tags="<?= htmlspecialchars($tags_text) ?>">

        <img src="./files/<?= $part['id'] ?>-<?= $version ?>.svg"
             alt="<?= $description ?>"
             title="<?= $title_text ?>"
             class="thumbnail-image">
      </div>
    <?php endforeach; ?>
  </div>
</div>


<div class="right">
  <h2>ストック</h2>
  <button id="export-tex">TeX出力</button>
  <button id="export-txt">サムネイル出力</button>
  <br>
  <div><strong>追加</strong>：Ｄ＆Ｄ</div>
  <div><strong>削除</strong>：Ｗクリック</div> 
  <div id="stock-list"></div>
</div>



<script>

let filterMode = 'or';
const stockList = document.getElementById('stock-list');
let draggedItem = null; // ★ドラッグ中のアイテムを保持


// ★ サムネイルをダブルクリックで拡大・縮小
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


// タグクリック → フィルタリング
const tagItems = document.querySelectorAll('.tag-item');
tagItems.forEach(tag => {
  tag.addEventListener('click', () => {
    tag.classList.toggle('selected-tag');
    applyFilter();
  });
});

document.querySelectorAll('input[name="filter_mode"]').forEach(radio => {
  radio.addEventListener('change', () => {
    filterMode = radio.value;
    applyFilter();
  });
});

// フィルタ処理
function applyFilter() {
  const selectedTags = Array.from(document.querySelectorAll('.tag-item.selected-tag')).map(tag => tag.getAttribute('data-tag'));
  document.querySelectorAll('.sticker-item').forEach(item => {
    const itemTags = item.getAttribute('data-tags').split(',').map(t => t.trim());
    if (selectedTags.length === 0) {
      item.style.display = '';
    } else if (filterMode === 'or') {
      item.style.display = selectedTags.some(tag => itemTags.includes(tag)) ? '' : 'none';
    } else {
      item.style.display = selectedTags.every(tag => itemTags.includes(tag)) ? '' : 'none';
    }
  });
}

// クリア（リセット）
document.getElementById('reset-tags').addEventListener('click', () => {
  tagItems.forEach(tag => tag.classList.remove('selected-tag'));
  applyFilter();
});

// 中央のステッカー → ドラッグ設定
document.querySelectorAll('.sticker-item').forEach(item => {
  item.draggable = true;
  item.addEventListener('dragstart', e => {
    const partId = item.getAttribute('data-part-id');
    const description = item.getAttribute('data-description-ja') || '';
    e.dataTransfer.setData('application/json', JSON.stringify({ partId, description }));
    draggedItem = null; // 中央からの場合、ストックではないので null
  });
});

// ストック内アイテム → ドラッグ設定
function makeStockItemDraggable(item) {
  item.draggable = true;
  item.addEventListener('dragstart', e => {
    draggedItem = item; // ★ドラッグ開始時に自分を覚える
  });
}

// ストックリストへのドロップ設定
stockList.addEventListener('dragover', e => e.preventDefault());

stockList.addEventListener('drop', e => {
  e.preventDefault();

  if (draggedItem) {
    const target = e.target.closest('.sticker-item');

    if (target && target !== draggedItem) {
      const children = Array.from(stockList.children);
      const draggedIndex = children.indexOf(draggedItem);
      const targetIndex = children.indexOf(target);

      if (draggedIndex < targetIndex) {
        // 自分より下にドロップ → targetの次に挿入
        stockList.insertBefore(draggedItem, target.nextSibling);
      } else {
        // 自分より上にドロップ → targetの前に挿入
        stockList.insertBefore(draggedItem, target);
      }
    }

    draggedItem = null;
    return;
  }

  // 中央から新規ドロップの場合
  const json = e.dataTransfer.getData('application/json');
  if (!json) return;
  const data = JSON.parse(json);

  // すでに同じIDがあれば追加しない
  if ([...stockList.children].some(el => el.getAttribute('data-part-id') === data.partId)) {
    return;
  }

  const newItem = document.createElement('div');
  newItem.className = 'sticker-item';
  newItem.setAttribute('data-part-id', data.partId);
  newItem.setAttribute('data-description-ja', data.description);
  newItem.innerHTML = `<img src="./files/${data.partId}-1.svg" alt="${data.description}" title="${data.description}">`;

  makeStockItemDraggable(newItem);

  stockList.appendChild(newItem);
});


//右欄Wクリックで削除
stockList.addEventListener('dblclick', e => {
  if (e.target.closest('.sticker-item')) {
    e.target.closest('.sticker-item').remove();
  }
});


// TeX出力
document.getElementById('export-tex').addEventListener('click', () => {
  const lines = Array.from(stockList.children).map(item => {
    const partId = item.getAttribute('data-part-id');
    const description = item.getAttribute('data-description-ja') || '';
    return `\\includegraphics{./files/${partId}-1.svg} % ${description}`;
  });
  download('hoge.tex', lines.join('\n'));
});

// サムネイル出力
document.getElementById('export-txt').addEventListener('click', () => {
  const lines = Array.from(stockList.children).map(item => {
    const partId = item.getAttribute('data-part-id');
    return `./files/${partId}-1.svg`;
  });
  download('hoge.txt', lines.join('\n'));
});

// ファイルダウンロード処理
function download(filename, text) {
  const blob = new Blob([text], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}


</script>


<style>
/* .center {
    flex: 1 1 50%;
    background: #fafafa;
}
.right {
    flex: 1 1 50%;
    background: #ffffff;
    border-left: 1px solid #ccc;
} */
#thumbnail-view {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}
#stock-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
    min-height: 300px;
    border: 1px dashed #ccc;
    padding: 10px;
    background: #f9f9f9;
}
.sticker-item img {
    width: 100px;
    height: 100px;
    object-fit: contain;
    border: 1px solid #ccc;
    background: white;
}
</style>
