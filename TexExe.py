import sys
import subprocess
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_folder_and_compile():
    """フォルダを選択し、LuaLaTeX でコンパイル"""
    folder_path = filedialog.askdirectory(title="TeXファイルのあるフォルダを選択")

    if not folder_path:  # キャンセル時
        return

    tex_file = os.path.join(folder_path, "main.tex")

    if not os.path.exists(tex_file):
        messagebox.showerror("エラー", "main.tex が見つかりません。")
        return

    output_pdf = "output"
    
    # LuaLaTeX コマンド
    lualatex_cmd = [
        "lualatex.exe",
        "--shell-escape",  # 制限解除
        "-interaction=batchmode",  # ログを最小限に抑える
        "-halt-on-error",          # エラー発生時に即停止
        "-file-line-error",        # エラーメッセージにファイル名と行番号を含める
        f"-jobname={output_pdf}",   # 出力ファイル名
        f"-output-directory={folder_path}",  # 出力先を選択フォルダ
        tex_file
    ]

    try:
        messagebox.showinfo("処理開始", "1回目のコンパイルを開始します。")
        subprocess.run(lualatex_cmd, check=True)

        messagebox.showinfo("処理中", "2回目のコンパイルを開始します。")
        subprocess.run(lualatex_cmd, check=True)

        messagebox.showinfo("完了", f"PDF 生成成功: {os.path.join(folder_path, output_pdf)}.pdf")

    except subprocess.CalledProcessError:
        messagebox.showerror("エラー", "コンパイル中にエラーが発生しました。")

# GUI 設定
root = tk.Tk()
root.title("LuaLaTeX コンパイル")
root.geometry("500x150")
root.resizable(False, False)

# フォント設定
FONT_TITLE = ("IPAゴシック", 14, "bold")
FONT_BUTTON = ("IPAゴシック", 12, "bold")

# ラベル
tk.Label(root, text="コンパイルするフォルダを選択してください", font=FONT_TITLE).pack(pady=10)

# ボタン
tk.Button(root, text="フォルダを選択", font=FONT_BUTTON, command=select_folder_and_compile).pack(pady=20)

root.mainloop()
