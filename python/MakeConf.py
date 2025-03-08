#####################################################################################
# TeX.py
#   2025.03.07
#   LuaLaTeXのコンパイルを行うスクリプト
#####################################################################################
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pathlib                  # パスの処理
import subprocess
import sys
import os


# 自作スクリプト
import makeMain # makeMain.py
import makeTeX  # makeTeX.py    


def run_selected_script():
    global ARGV # scrippt.path

    """ラジオボタンとチェックボックスの選択に応じてスクリプトを実行"""
    selected_option = radio_var.get()

    print( f"cwd : {pathlib.Path.cwd()}" )
    print( f"ARGV : {ARGV}" )
    # tk.Message( ARGV )

    script_path = pathlib.Path(ARGV).parent # Python置き場のパス
    path1 = pathlib.Path(ARGV) # script.path取得
    path1 = path1.parent.parent.parent # ■共通の親を取得
    path2 = pathlib.Path( filedialog.askdirectory(
                            # initialdir = path1,
                            title     = "対象フォルダを選択",
                            mustexist = True))
    # print( f"path1 : {path1}" )
    # print( f"path2 : {path2}" )

    try:
        relative_path = path2.relative_to( path1 ) # 相対パス取得
        # print( f"relative_path : {relative_path}")
        relative_path = pathlib.Path("../../").joinpath( relative_path ) # 相対パス取得
        print( f"relative_path : {relative_path}")
    except ValueError:
        print("相対パスを生成できません。")
        # input()


    if selected_option == 1:  # 個別実行
        if var_table_check.get():
            excel_path = relative_path.joinpath( "変数・表生成.xlsm" )
            makeTeX.create_sty_and_tex_files( excel_path )
            input()
        if main_code_check.get():
            makeMain.make_main( relative_path )
            input()

    elif selected_option == 2:  # まとめて実行
            excel_path = relative_path.joinpath( "変数・表生成.xlsm" )
            makeTeX.create_sty_and_tex_files( excel_path )
            makeMain.make_main( relative_path )

    else:
        messagebox.showwarning("エラー", "オプションを選択してください。")
        return

    root.destroy()




def toggle_checkboxes():
    """ラジオボタンの状態に応じてチェックボックスの有効/無効を切り替える"""
    if radio_var.get() == 1:
        var_table_checkbox.config(state="normal")
        main_code_checkbox.config(state="normal")
    else:
        var_table_checkbox.config(state="disabled")
        main_code_checkbox.config(state="disabled")


# GUIの設定
root = tk.Tk()
root.title("処理選択")
root.geometry("400x250")
root.resizable(False, False)

# フォント設定
FONT_TITLE =  ("BIZ UDゴシック", 14, "bold")
FONT_OPTION = ("BIZ UDゴシック", 13)
FONT_BUTTON = ("BIZ UDゴシック", 12, "bold")

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

var_table_checkbox = tk.Checkbutton(root, text="変数・表生成", variable=var_table_check, font=FONT_OPTION)
main_code_checkbox = tk.Checkbutton(root, text="メインコード生成", variable=main_code_check, font=FONT_OPTION)

var_table_checkbox.pack(anchor="w", padx=50)
main_code_checkbox.pack(anchor="w", padx=50)

# 初期状態でチェックボックスの状態を更新
toggle_checkboxes()

# ボタンフレーム
frame = tk.Frame(root)
frame.pack(pady=0)

# print( sys.argv[0] )
ARGV = sys.argv[0]

btn_cancel = tk.Button(frame, text="キャンセル\n(Esc)", font=FONT_BUTTON, width=10, command=root.quit)
btn_cancel.pack(side="left", padx=20, pady=(10, 0))


btn_ok = tk.Button(frame, text="実行\n(Enter)", font=FONT_BUTTON, width=10, command=run_selected_script)
btn_ok.pack(side="right", padx=20, pady=(10, 0))

# キーボードショートカットの割り当て
root.bind("<Return>", lambda event: run_selected_script())  # Enterキーで実行
root.bind("<Escape>", lambda event: root.quit())  # Escapeキーでキャンセル


root.mainloop()
