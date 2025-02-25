import subprocess
import os
import sys
import pathlib
from tkinter import filedialog, messagebox


def Compile_tex():

    # スクリプトのあるフォルダをカレントディレクトリに設定
    script_dir = pathlib.Path( os.path.abspath(sys.argv[0]) ).parent


    # フォルダ取得
    folder_path = filedialog.askdirectory(
        title       = "main.texのあるフォルダを選択",
        initialdir  = script_dir,
        mustexist   = True )
    folder_path = pathlib.Path( folder_path ).absolute()
    os.chdir( folder_path )


    # TeXファイルの絶対パスを取得
    tex_file = folder_path / "main.tex"


    # 設定全体.sty をテキスト解析し，出力ファイル名生成
    with open( folder_path / "設定全体.sty", "r", encoding="utf-8") as ff:
        for line in ff:
            if  line[1:12] == "NewDocument" :
                line = line.rstrip()  # 改行削除

                line = line.replace("\\NewDocumentCommand","") # 先頭文字を削除
                line = line[:line.find("%")] # コメント文以降を削除

                line = line[line.find("{"):line.rfind("}")] # 主要部抽出
                if line[:line.find("}")] == "\\機種":
                    machine_type = line[line.find("{"):]
                if line[:line.find("}")] == "\\型式":
                    machine_model = line[line.find("{"):]           
                if line[:line.find("}")] == "\\BookNo":
                    book_no = line[line.find("{"):]           

         if machine_type is None or \
            machine_model is None or \
            book_no is None:
             
             break
        



    # 出力ファイル名（拡張子なしで指定）
    output_pdf = folder_path / machine_type "_" machine_model "_" book_no


    # LuaLaTeX のオプション設定（共通）
    lualatex_cmd = [
        "lualatex.exe",
        "-interaction=batchmode",  # ログを最小限に抑える
        "-halt-on-error",          # エラー発生時に即停止
        "-file-line-error",        # エラーメッセージにファイル名と行番号を含める
        f"-jobname={output_pdf}",   # 出力ファイル名を指定
        f"-output-directory={folder_path}",     # 出力フォルダ（カレントディレクトリ）
        f"{tex_file}"
    ]

    # LuaLaTeX を2回実行
    try:
        print("1回目のコンパイル...")
        #subprocess.run(lualatex_cmd, check=True)

        print("2回目のコンパイル...")
        #subprocess.run(lualatex_cmd, check=True)

        print(f"PDF 生成成功: {output_pdf}.pdf")

    except subprocess.CalledProcessError:
        print("エラーが発生しました。")

    # ウィンドウがすぐ閉じないようにする
    input("終了するには Enter キーを押してください...")



# メイン
if __name__ == "__main__":
    # messagebox.showwarning("エラー", "このスクリプトは，直接実行できません．")
    Compile_tex()