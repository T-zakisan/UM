import inkex
import os
import re
import tkinter.messagebox as messagebox

class LayerNameToFileName(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
        # 現在のファイル名を取得
        filename = self.options.output
        base_filename = os.path.splitext(filename)[0]

        # バージョン番号と出力レイヤー名を格納する変数を初期化
        version = None
        output_layer_names = []



        # バージョンアップするかダイアログを表示
        if version is not None:
            result = messagebox.askyesno("バージョンアップ", f"バージョンを{version + 1}に更新しますか？")

            if result:
                # バージョン番号をカウントアップ
                version += 1



        # レイヤーをループ処理
        for layer in self.document.layers:
            if layer.visible:
                layer_name = layer.label

                # バージョン番号を取得
                match = re.search(r"バージョン：(\d+)", layer_name)
                if match:
                    version = int(match.group(1))

                # 出力レイヤー名を格納
                if ":出力" in layer_name:
                    output_layer_names.append(layer_name)

                #バージョン番号を更新
                match = re.search(r"バージョン：(\d+)", layer_name)
                if match:
                　　layer.label = layer_name.replace(f"バージョン：{match.group(1)}", f"バージョン：{version}")

        # 出力レイヤーをループ処理
        for layer_name in output_layer_names:
            # ファイル名を作成
            new_filename = f"{base_filename}_{layer_name.replace(':出力', '')}_v{version if version is not None else '1'}.pdf"

            # PDF形式でエクスポート
            # self.document.save(new_filename) # ドキュメント全体をPDFでエクスポートする場合
            self.document.export_to_file(new_filename, "pdf", area="page") # ページ全体をPDFでエクスポートする場合

            print(f"{layer_name} を {new_filename} にエクスポートしました。")

if __name__ == '__main__':
    effect = LayerNameToFileName()
    effect.run()