
import inkex
from lxml import etree
from pathlib import Path

def all_bboxes(element, svg):
    bboxes = []
    for node in element.iter():
        if node.tag.endswith(('rect', 'circle', 'ellipse', 'path', 'polygon', 'polyline', 'line')):
            try:
                b = inkex.BoundingBox(node, svg)
                if b.width != 0 and b.height != 0:
                    bboxes.append(b)
            except Exception:
                pass
    return bboxes

def union_bbox(bboxes):
    if not bboxes:
        return None
    bbox = bboxes[0]
    for b in bboxes[1:]:
        bbox += b
    return bbox

class AddObject(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--radio", default="kaku", help="ID of object to insert")

    def effect(self):
        svg_path = Path(__file__).parent / "parts.svg"
        if not svg_path.exists():
            inkex.errormsg(f"parts.svgが見つかりません: {svg_path}")
            return

        doc = etree.parse(str(svg_path))
        svg = doc.getroot()
        obj_id = self.options.radio
        elems = svg.xpath(f'//*[@id=\"{obj_id}\"]')
        if not elems:
            inkex.errormsg(f"ID={obj_id} のオブジェクトが parts.svg に見つかりません")
            return
        elem = elems[0]
        new_elem = etree.fromstring(etree.tostring(elem))

        # まず仮追加
        layer = self.svg.get_current_layer()
        layer.append(new_elem)

        # 挿入後にbbox計算
        bboxes = all_bboxes(new_elem, self.svg)
        bbox = union_bbox(bboxes)

        # スケール・位置補正
        if bbox is None or bbox.height == 0:
            scale = 1
            min_x, min_y = 0, 0
        else:
            target_height_mm = 10
            px_per_mm = 3.7795275591
            target_height_px = target_height_mm * px_per_mm
            scale = target_height_px / bbox.height
            min_x, min_y = bbox.left, bbox.top

            # transform属性を新規にセット
            new_elem.attrib["transform"] = f"translate({-min_x},{-min_y}) scale({scale})"

        # ※すでに追加済みなのでreturnのみ

if __name__ == '__main__':
    AddObject().run()
