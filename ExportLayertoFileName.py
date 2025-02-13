import inkex
import os
import re
import subprocess

class ExportLayertoFileName( inkex.EffectExtension ):

    def __init__(self):
        super().__init__()

    # パラメータ取得
    def add_arguments( self, parser ):  # 引数パーサーを設定
        parser.add_argument("--radio", type=str, dest="radio", default="0", help="バージョンアップする？ (0 or 1)")


    def effect( self ):

        # バージョン加算量
        VERSION = 0
        if self.options.radio == '1':
            VERSION = 1

        # 元のSVGファイル名を取得
        file_path = self.document.getroot().get("sodipodi:docname")
        if not file_path:
            inkex.errormsg("元のSVGファイル名が取得できませんでした。")
            return

        # 全レイヤーで繰り返し
        for layer in self.svg.xpath("//svg:g[@inkscape:groupmode='layer']", namespaces=inkex.NSS):
            layer_name = layer.get("inkscape:label", "") # レイヤー名取得

            # バージョンアップ
            match = re.search(r"バージョン：(\d+)", layer_name)
            if match:
                VERSION = int(match.group(1)) + VERSION
                layer.set("inkscape:label", "バージョン：" + str( VERSION ) )
            
            # 非表示に変更
            if "：出力" in layer_name:
                layer.set("visibility", "hidden")
                layer.set("style", "display:none")
            

        # 全レイヤーで繰り返し：ファイル出力
        for layer in self.svg.xpath("//svg:g[@inkscape:groupmode='layer']", namespaces=inkex.NSS):
            layer_name = layer.get("inkscape:label", "") # レイヤー名取得
            
            # ：出力を含む場合：ファイル出力へ
            if "：出力" in layer_name:

                # 非表示の場合のみ表示状態にする
                layer.set("visibility", "visible")
                layer.set("style", "display:inline")  # 表示状態にする

                # **SVGを保存**
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(inkex.etree.tostring(self.document.getroot(), encoding="unicode"))
                inkex.errormsg(f"出力：{file_path}")

                # ファイル名生成
                base_name = os.path.splitext(self.document.getroot().get("sodipodi:docname"))[0]
                file_name = f"{base_name}_{layer_name.replace('：出力', '')}_{str(VERSION).zfill(2)}.pdf"
                out_path = os.path.join(os.path.dirname(self.document.getroot().get("sodipodi:docname")), file_name)

                # PDF出力 (subprocessでInkscapeを呼び出す)
                try:
                    subprocess.run(["inkscape", "--export-filename=" + out_path, self.svg.get("sodipodi:docname")], check=True)
                    inkex.errormsg(f"出力：{out_path}")
                except subprocess.CalledProcessError as e:
                    inkex.errormsg(f"PDFエクスポート中にエラーが発生しました: {e}")

                # 非表示状態にする
                layer.set("visibility", "hidden")
                layer.set("style", "display:none")


if __name__ == '__main__':
    ExportLayertoFileName().run()
