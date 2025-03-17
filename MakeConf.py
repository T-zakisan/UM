#####################################################################################
# TeX.py
#  2025.03.10
#  - LuaLaTeXのコンパイルを行うスクリプト
#####################################################################################
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pathlib                  # パスの処理
import sys
import os


# 自作スクリプト
import makeMain # makeMain.py
import makeTeX  # makeTeX.py

os.system('cls' if os.name == 'nt' else 'clear') # コンソールの表示を初期化

print( f"\n指定ディレクトリ(機種)の各種ファイルを生成します．" )
print( f"--------------------------------------------------" )
print( f"■設定ファイル\n  ・設定全体.sty\n  ・設定変数.sty" )
print( f"■基本texファイル\n  ・main.tex" )
print( f"■コンパイルファイル\n  ・_Compile(機種_号機_BookNo).py" )
print( f"--------------------------------------------------" )
print( f"対象をダイアログで選択してください．\n\n" )
print( f"終了するべき場合" )
print( f"  ※ 対象ディレクトリ がない / 作成していない" )
print( f"  ※ 対象ディレクトリ に \"変数・表生成.xlsm\" がない" )
print( f"  ※ 対象ディレクトリ の \"変数・表生成.xlsm\" のシート[変数]の赤文字部(全体設定)が適切でない" )
print( f"ダイアログ > [キャンセル]" )



try:  # 正常時
  path2 = filedialog.askdirectory(
                          # initialdir = path1,
                          title     = "対象フォルダを選択",
                          mustexist = True) # ダイアログで対象機種のパス取得
except ValueError:  # 一応
  os.system('cls' if os.name == 'nt' else 'clear') # コンソールの表示を初期化


# [キャンセル]選択時
if path2 == "." or path2 == "": sys.exit()

print( f"\n\n" )
print( f"--------------------------------------------------" )
print( f"対象パス取得 完了", end = "\n" )
print( f"相対パス取得 ", end = "" )

path1 = pathlib.Path(sys.argv[0]) # script.path取得
path1 = path1.parent.parent.parent # "■共通の親"を取得
path2 = pathlib.Path( path2 )
# print( f"path1 : {path1}" )
# print( f"path2 : {path2}" )
relative_path = path2.relative_to( path1 ) # 相対パス取得
relative_path = pathlib.Path("../../").joinpath( relative_path ) # 相対パス取得

print( f"完了", end = "\n" )
print( f"変数・表生成.xlsm ", end = "" )


# print( f"relative_path : {relative_path}")
excel_path = relative_path.joinpath( "変数・表生成.xlsm" ) # エクセルファイルの相対パス生成
if not excel_path.exists():
  print( "存在しません！\n" )
  print( "処理終了" )
  sys.exit
print( f"ok", end = "\n" )


print( f"styファイル生成 ", end = "" )
makeTeX.create_sty_and_tex_files( excel_path ) # 各種設定(sty)とtexファイル生成
print( f"ok", end = "\n" )

print( f"main.tex, コンパイルファイル生成 ", end = "" )
makeMain.make_Main( relative_path ) # main.tex生成
print( f"ok", end = "\n" )


print( f"--------------------------------------------------" )
print( f"処理終了 : 何か入力 > [Enter]" )
input()

