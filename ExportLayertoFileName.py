import inkex
import os
import re
import subprocess
from urllib.parse import urlparse
import tkinter as tk
from tkinter import filedialog

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
            VERSION = 1 # 増分（バージョン1って意味ではない）

        # 全レイヤーで繰り返し
        for layer in self.svg.xpath("//svg:g[@inkscape:groupmode='layer']", namespaces=inkex.NSS):
            layer_name = layer.get("inkscape:label", "") # レイヤー名取得

            # バージョンアップ
            match = re.search(r"バージョン：(\d+)", layer_name)
            if match:
                VERSION = int(match.group(1)) + VERSION # カウントアップ
                layer.set("inkscape:label", "バージョン：" + str( VERSION ) ) 

            # 非表示に変更
            if "：出力" in layer_name:
                layer.set("visibility", "hidden")
                layer.set("style", "display:none")


        # 保存先フォルダの選択
        root = tk.Tk()
        root.withdraw()  # メインウィンドウを非表示にする
        root.title("保存先フォルダの選択")  # タイトルを変更
        folder_path = os.path.abspath(filedialog.askdirectory() ) + "\\"


        # svgファイル名の取得
        svg_full_path = self.document.getroot().get("sodipodi:docname")
        if svg_full_path:
            svg_full_path = os.path.abspath(svg_full_path) # 絶対パスに変換
            svg_file_name = os.path.splitext(os.path.basename(svg_full_path))[0] # 拡張子なしファイル名


        # 全レイヤーで繰り返し：ファイル出力
        for layer in self.svg.xpath("//svg:g[@inkscape:groupmode='layer']", namespaces=inkex.NSS):
            layer_name = layer.get("inkscape:label", "") # レイヤー名取得

            # ：出力を含む場合：ファイル出力へ
            if "：出力" in layer_name:

                # 非表示の場合のみ表示状態にする
                layer.set("visibility", "visible")
                layer.set("style", "display:inline")  # 表示状態にする

                # 今の表示をSVGに反映
                with open(svg_full_path, "w", encoding="utf-8") as f:
                    f.write(inkex.etree.tostring(self.document.getroot(), encoding="unicode"))

                # ファイル名生成
                svg_base_name =  f"{svg_file_name}{layer_name.replace('：出力', '')}_{str(VERSION).zfill(2)}" # バージョン追加
                pdf_path = os.path.join( folder_path, svg_base_name + ".pdf") # 拡張子追加

                # PDF出力 (subprocessでInkscapeを呼び出す)
                try:
                    subprocess.run(["inkscape", "--export-filename=" + pdf_path, self.svg.get("sodipodi:docname")], check=True)
                    inkex.errormsg(f"出力：{pdf_path}") # ないとそれはそれで不安なため表示
                except subprocess.CalledProcessError as e:
                    inkex.errormsg(f"PDFエクスポート中にエラーが発生しました: {e}")

                # 非表示状態にする
                layer.set("visibility", "hidden")
                layer.set("style", "display:none")


if __name__ == '__main__':
    ExportLayertoFileName().run()
