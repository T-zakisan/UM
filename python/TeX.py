#####################################################################################
# TeX.py
#  LuaLaTeXのコンパイルを行うスクリプト
# [ 2025.02.26 ]
#####################################################################################
import tkinter as tk
from tkinter import messagebox
import subprocess

# 実行するスクリプトのパス
SCRIPT_VAR_TABLE_GEN = "makeTeX.py"
SCRIPT_MAIN_CODE_GEN = "makeMain.py"
SCRIPT_COMPILE = "compile_project.py" # 未実装

def run_selected_script():
    """ラジオボタンとチェックボックスの選択に応じてスクリプトを実行"""
    selected_option = radio_var.get()

    if selected_option == 1:  # 個別実行
        if var_table_check.get():
            subprocess.run(["python", SCRIPT_VAR_TABLE_GEN], check=True)
        if main_code_check.get():
            subprocess.run(["python", SCRIPT_MAIN_CODE_GEN], check=True)
        if compile_check.get():
            # subprocess.run(["python", SCRIPT_COMPILE], check=True)
            pass
    elif selected_option == 2:  # まとめて実行
        scripts = [ SCRIPT_VAR_TABLE_GEN, SCRIPT_MAIN_CODE_GEN, SCRIPT_COMPILE]
        subprocess.run(["python", SCRIPT_ALL], check=True)
    else:
        messagebox.showwarning("エラー", "オプションを選択してください。")
        return

    root.destroy()

def toggle_checkboxes():
    """ラジオボタンの状態に応じてチェックボックスの有効/無効を切り替える"""
    if radio_var.get() == 1:
        var_table_checkbox.config(state="normal")
        main_code_checkbox.config(state="normal")
        compile_checkbox.config(state="normal")
    else:
        var_table_checkbox.config(state="disabled")
        main_code_checkbox.config(state="disabled")
        compile_checkbox.config(state="disabled")

# GUIの設定
root = tk.Tk()
root.title("処理選択")
root.geometry("400x280")
root.resizable(False, False)

# フォント設定
FONT_TITLE = ("IPAゴシック", 14, "bold")
FONT_OPTION = ("IPAゴシック", 13)
FONT_BUTTON = ("IPAゴシック", 12, "bold")

# ラベル
tk.Label(root, text="処理を選択してください", font=FONT_TITLE).pack(pady=10)

# ラジオボタン
radio_var = tk.IntVar(value=1)
radio1 = tk.Radiobutton(root, text="まとめて実行", variable=radio_var, value=2, font=FONT_OPTION, command=toggle_checkboxes)
radio2 = tk.Radiobutton(root, text="個別で実行", variable=radio_var, value=1, font=FONT_OPTION, command=toggle_checkboxes)

radio1.pack(anchor="w", padx=30, pady=5)
radio2.pack(anchor="w", padx=30, pady=5)

# チェックボックス
var_table_check = tk.IntVar()
main_code_check = tk.IntVar()
compile_check = tk.IntVar()

var_table_checkbox = tk.Checkbutton(root, text="変数・表生成", variable=var_table_check, font=FONT_OPTION)
main_code_checkbox = tk.Checkbutton(root, text="メインコード生成", variable=main_code_check, font=FONT_OPTION)
compile_checkbox = tk.Checkbutton(root, text="コンパイル", variable=compile_check, font=FONT_OPTION)

var_table_checkbox.pack(anchor="w", padx=50)
main_code_checkbox.pack(anchor="w", padx=50)
compile_checkbox.pack(anchor="w", padx=50)

# 初期状態でチェックボックスの状態を更新
toggle_checkboxes()

# ボタンフレーム
frame = tk.Frame(root)
frame.pack(pady=0)

tk.Button(frame, text="キャンセル", font=FONT_BUTTON, width=10, command=root.quit).pack(side="left", padx=20, pady=(10, 0))
tk.Button(frame, text="実行", font=FONT_BUTTON, width=10, command=run_selected_script).pack(side="right", padx=20, pady=(10, 0))

root.mainloop()