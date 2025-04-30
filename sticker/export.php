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

// タグ取得関数
function get_tags_by_part($pdo, $part_id) {
    $stmt = $pdo->prepare("SELECT t.name FROM tags t INNER JOIN parts_tags pt ON t.id = pt.tag_id WHERE pt.part_id = ? ORDER BY t.name ASC");
    $stmt->execute([$part_id]);
    return implode(', ', $stmt->fetchAll(PDO::FETCH_COLUMN));
}

// バージョン取得関数
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
           data-version="<?= $version ?>"
           data-description-ja="<?= $description ?>"
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
  <div id="stock-list"></div>
</div>

<script>
let filterMode = 'or';
const stockList = document.getElementById('stock-list');

// タグフィルタ
document.querySelectorAll('.tag-item').forEach(tag => {
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
function applyFilter() {
  const selected = Array.from(document.querySelectorAll('.tag-item.selected-tag')).map(t => t.getAttribute('data-tag'));
  document.querySelectorAll('.sticker-item').forEach(item => {
    const tags = item.getAttribute('data-tags').split(',').map(t => t.trim());
    item.style.display = selected.length === 0 ? '' :
      (filterMode === 'or'
        ? selected.some(tag => tags.includes(tag))
        : selected.every(tag => tags.includes(tag)));
  });
}
document.getElementById('reset-tags').addEventListener('click', () => {
  document.querySelectorAll('.tag-item').forEach(tag => tag.classList.remove('selected-tag'));
  applyFilter();
});

// D&D ステッカー → ストック
document.querySelectorAll('.sticker-item').forEach(item => {
  item.draggable = true;
  item.addEventListener('dragstart', e => {
    const data = {
      id: item.getAttribute('data-part-id'),
      version: item.getAttribute('data-version'),
      description: item.getAttribute('data-description-ja')
    };
    e.dataTransfer.setData('application/json', JSON.stringify(data));
  });
});

// ストックへのドロップ
stockList.addEventListener('dragover', e => e.preventDefault());
stockList.addEventListener('drop', e => {
  e.preventDefault();
  const json = e.dataTransfer.getData('application/json');
  if (!json) return;
  const data = JSON.parse(json);
  if ([...stockList.children].some(el => el.getAttribute('data-part-id') === data.id)) return;

  const div = document.createElement('div');
  div.className = 'sticker-item';
  div.setAttribute('data-part-id', data.id);
  div.setAttribute('data-version', data.version);
  div.setAttribute('data-description-ja', data.description);
  div.draggable = true;
  div.innerHTML = `<img src="./files/${data.id}-${data.version}.svg" alt="${data.description}" title="${data.description}">`;

  // 再ドラッグ対応
  div.addEventListener('dragstart', ev => {
    ev.dataTransfer.setData('application/json', JSON.stringify({
      id: data.id,
      version: data.version,
      description: data.description
    }));
    div.remove();  // 移動扱い
  });

  div.addEventListener('dblclick', () => {
    div.remove();  // Wクリックで削除
  });

  stockList.appendChild(div);
});

// TeX出力
document.getElementById('export-tex').addEventListener('click', () => {
  const lines = Array.from(stockList.children).map(item => {
    const id = item.getAttribute('data-part-id');
    const version = item.getAttribute('data-version');
    const description = item.getAttribute('data-description-ja');
    return `\\includegraphics{./files/${id}-${version}.svg} % ${description}`;
  });
  download('hoge.tex', lines.join('\n'));
});

// サムネイル出力（PDF）
document.getElementById('export-txt').addEventListener('click', () => {
  const lines = Array.from(stockList.children).map(item => {
    const id = item.getAttribute('data-part-id');
    const version = item.getAttribute('data-version');
    return `./files/${id}-${version}.pdf`;
  });
  download('hoge.txt', lines.join('\n'));
});

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
.center { flex: 1 1 50%; background: #fafafa; }
.right  { flex: 1 1 50%; background: #fff; border-left: 1px solid #ccc; }
#thumbnail-view {
  display: flex; flex-wrap: wrap; gap: 5px;
}
#stock-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
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
