


#####################################################################################
# makeVariable_version.py
#  - Excelのシート[版]から版関係のコマンド(変数)を作成
#  - 設定全体.styに版情報を追記
# [引数] sheet      シートオブジェクト
# [引数] base_path  Excelファイルの親パス
#####################################################################################
import os
import sys
import glob
from tkinter import messagebox  # ダイアログ
import openpyxl                 # Excel操作
import pathlib                  # パスの処理
import mojimoji                 # 全角半角
import datetime                 # 日付表記の変更




def create_version( sheet, base_path, lang ):
  base_path = pathlib.Path( base_path )
  output_file_path = base_path.joinpath("設定全体.sty")
  with open(output_file_path, 'a', encoding='utf-8') as ff: # 追記モード

    myStr = "" # 文字列用変数をリセット
    col_a_value = ""
    col_b_value = ""


    ############################################################
    # 版と発行日を全件取得：表紙（裏）にリスト表示
    for idx, row in enumerate( sheet.iter_rows(min_row=2)):
      col_a_value += f"{str(row[0].value)}| "   # [列A]変数名


      ## 表示言語による日付の表示切り替え
      date_object = datetime.datetime.strptime(str(row[1].value), '%Y-%m-%d %H:%M:%S') # 日付データをdatetimeオブジェクトに変換
      if lang:  # 日本語表記
        col_b_value += f"{date_object.year}年 {int(date_object.strftime('%m'))}月 {int(date_object.strftime('%d'))}日| "
      else:  # 英語表記
        col_b_value += f"{date_object.strftime('%B')} {int(date_object.strftime('%d'))}, {date_object.year}| "

    col_a_value = col_a_value[0:-2] # 版
    col_b_value = col_b_value[0:-2] # 日付
    # 版履歴を表示させない(2025.03現在)
    myStr += f"\\変数設定{{版S}}{{{col_a_value}}}     %     版の履歴(未使用だが残しておく：2025.03)\n"
    myStr += f"\\変数設定{{発行日S}}{{{col_b_value}}} % 発行日の履歴(未使用だが残しておく：2025.03)\n"
    ff.write( myStr ) # テキスト書き込み
    myStr = ""


    # 版と発行日の最新項目を取得
    col_a_value = col_a_value.split("| ") # (| )で区切り、リスト化
    col_a_value = col_a_value[-1] # 最終行取得：最新情報
    if col_a_value != "初":
      col_a_value = f"第{col_a_value}"

    myStr += f"\\変数設定{{版}}{{{col_a_value}}} % 版\n"
    col_b_value = col_b_value.split("| ") # (| )で区切り、リスト化
    col_b_value = col_b_value[-1] # 最終行取得：最新情報
    myStr += f"\\変数設定{{発行日}}{{{col_b_value}}} % 発行日\n"
    ff.write( myStr ) # テキスト書き込み

