import tkinter as tk
from tkinter import messagebox
import subprocess

# 実行するスクリプトのパス
SCRIPT_TEX_GEN = "generate_tex.py"
SCRIPT_LUALATEX = "compile_lualatex.py"

def run_selected_script():
    """ラジオボタンの選択に応じてスクリプトを実行"""
    selected_option = var.get()
    
    if selected_option == 1:
        script = SCRIPT_TEX_GEN
    elif selected_option == 2:
        script = SCRIPT_LUALATEX
    else:
        messagebox.showwarning("エラー", "オプションを選択してください。")
        return
    
    try:
        subprocess.run(["python", script], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("エラー", f"スクリプトの実行に失敗しました:\n{e}")

    root.destroy()

# GUIの設定
root = tk.Tk()
root.title("処理選択")
root.geometry("400x220")  # ウィンドウサイズを指定（高さを少し増やす）
root.resizable(False, False)  # ウィンドウサイズを固定

# ラジオボタンの選択状態を管理する変数（デフォルトは1: TeXファイル生成）
var = tk.IntVar(value=1)

# フォント設定（IPAゴシック）
FONT_TITLE = ("IPAゴシック", 14, "bold")
FONT_OPTION = ("IPAゴシック", 13)  # ラジオボタンのフォントを大きめに
FONT_BUTTON = ("IPAゴシック", 12, "bold")

# ラベル
tk.Label(root, text="処理を選択してください", font=FONT_TITLE).pack(pady=10)

# ラジオボタン
radio1 = tk.Radiobutton(root, text="TeXファイル生成（Excel選択）", variable=var, value=1, font=FONT_OPTION)
radio2 = tk.Radiobutton(root, text="Lualatexのコンパイルを開始", variable=var, value=2, font=FONT_OPTION)

# ラジオボタンのサイズを調整（パディングを増やす）
radio1.pack(anchor="w", padx=30, pady=8, ipadx=5, ipady=3)
radio2.pack(anchor="w", padx=30, pady=8, ipadx=5, ipady=3)

# ボタンフレーム
frame = tk.Frame(root)
frame.pack(pady=15)

tk.Button(frame, text="中断", font=FONT_BUTTON, width=10, command=root.quit).pack(side="left", padx=20)
tk.Button(frame, text="実行", font=FONT_BUTTON, width=10, command=run_selected_script).pack(side="right", padx=20)

root.mainloop()

