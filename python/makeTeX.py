#####################################################################################
# makeTeX.py
#  2025.03.07
#  - ExcelファイルからTeX関係の各種ファイルを出力
#  - TeXコマンド(変数として、文章制御等に利用)を***.styファイルとして出力
#  - 各種表を*.texファイルとして出力
#####################################################################################

import os, sys
import glob
from tkinter import messagebox  # ダイアログ
import openpyxl                 # Excel操作
import pathlib                  # パスの処理
import mojimoji                 # 全角半角
import datetime                 # 日付表記の変更


#####################################################################################
# create_sty_and_tex_files
#  - Excelのシートによる分岐とシート種ごとの処理関数呼び出し
# [引数] base_path  Excelファイルの親パス
#####################################################################################
def create_sty_and_tex_files(excel_file_path):

  # 既存の出力ファイル削除
  ff = [ '*.pdf', '*.toc', '*.out', '*.aux', '*.log', 'main.tex' ]
  for pattern in ff:
    for filepath in pathlib.Path('.').glob( pattern ):
      try:
        os.remove(filepath)
      except FileNotFoundError:
        print(f"ファイル {filepath} は存在しません。")
      except Exception as e:
        print(f"ファイル {filepath} の削除中にエラーが発生しました: {e}")


  try:
    # workbook = openpyxl.load_workbook(excel_file_path, read_only=True)
    workbook = openpyxl.load_workbook(excel_file_path)
    sheet = workbook["ReadMe"]

    for sheet_index, sheet_name in enumerate(workbook.sheetnames):
      sheet = workbook[sheet_name]

      # 変数設定ファイル出力
      if "変数" in sheet_name:
        lang = create_variable(sheet, os.path.dirname(excel_file_path))  # 関数を呼び出す

      ## elif "安全上の…b" in sheet_name:
      ##   create_variable_definitions(sheet, os.path.dirname(excel_file_path))  # 関数を呼び出す

      # 各表ファイル出力
      elif sheet_index >= 5:  # 6番目(0スタート)以降のシート
        create_table_code(sheet, pathlib.Path(excel_file_path).parent )  # 関数を呼び出す


    # [版]を後から追記したいので、もうひとサイクル！
    for sheet_index, sheet_name in enumerate(workbook.sheetnames):
      sheet = workbook[sheet_name]

      # 変数設定ファイル出力
      if "版" in sheet_name:
        create_version(sheet, pathlib.Path(excel_file_path).parent, lang )  # 関数を呼び出す


    # workbook.save(excel_file_path)
    workbook.close()
    return 0

  except FileNotFoundError:
    print(f"エラー: ファイル '{excel_file_path}' が見つかりません。")
    return -1
  except Exception as e:
    print(f"エラー: 予期せぬエラーが発生しました: {e}")
    return -1




#####################################################################################
# create_version
#  - Excelのシート[版]から版関係のコマンド(変数)を作成
# [引数] sheet      シートオブジェクト
# [引数] base_path  Excelファイルの親パス
#####################################################################################
def create_version( sheet, base_path, lang ):
  base_path = pathlib.Path( base_path )
  output_file_path = base_path.joinpath("設定全体.sty")
  with open(output_file_path, 'a', encoding='utf-8') as ff:

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
    myStr += f"\\変数設定{{版S}}{{{col_a_value}}} % 版の履歴(未使用：2025.03)\n"
    myStr += f"\\変数設定{{発行日S}}{{{col_b_value}}} % 発行日の履歴(未使用：2025.03)\n"
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




#####################################################################################
# create_variable
#  - ExcelのシートからTeXコマンドの定義文をstyファイルで出力
# [引数] sheet      シートオブジェクト
# [引数] base_path  Excelファイルの親パス
#####################################################################################
def create_variable( sheet, base_path ):
  
  # セル[A3]が空白なら終了：■共通フォルダ対策
  value = sheet.cell(3,1).value
  if value is None or str(value).strip() == "":
    return


  # 相対パスのstyファイル(設定パス.sty)出力処理
  base_path = pathlib.Path( base_path )
  output_file_path = base_path.joinpath("設定全体.sty")
  with open(output_file_path, 'w', encoding='utf-8') as ff:

    # ファイルコメント
    myStr = f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
            f"% ファイル名：{output_file_path.name}\n" \
            f"% made by makeTeX.py\n" \
            f"% 内　　　容：日本語名コマンド用コマンド\n" \
            f"%           ：■共通への相対パス（変数・表生成.xlsmを完成のこと！）\n" \
            f"%           ：本文制御用コマンド定義\n" \
            f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
    ff.write( myStr )

    # 日本語コマンド定義
    myStr = f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
            f"% コマンドの定義チェックからの表示\n" \
            f"%  (これだけ例外的にHANTA.styから独立)\n" \
            f"%  通常の変数（コマンド）と同じように展開され、使える\n" \
            f"%  未定義の変数は未表示\n" \
            f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
            f"\\usepackage{{xparse}} % 限りない引数\n" \
            f"\\usepackage{{expl3}} % スクリプト用\n" \
            f"\\NewExpandableDocumentCommand{{\\変数}}{{m}}{{\\csname 変数:#1\\endcsname}}\n" \
            f"\\NewDocumentCommand{{\\変数設定}}{{mm}}{{\\global\\expandafter\\def\\csname 変数:#1\\endcsname{{#2}}}}\n\n"
    ff.write( myStr )

    myStr = "" # 文字列用変数をリセット
    flag_lang = False # 表示言語用のフラグリセット
    flag_end = False
    flag_directions = False
    for idx, row in enumerate( sheet.iter_rows(min_row=1)):
      col_a_value = row[0].value  # [列A]変数名
      col_b_value = row[1].value  # [列B]設定値
      col_c_value = row[2].value  # [列C]備考

      # １行目：パス
      if idx == 0 :
        col_b_value = col_b_value.replace( "/", "\\" )
        relative_path = base_path.replace( col_b_value.replace("■共通",""), "" ) # 差分
        dir_depth = relative_path.split("\\")  # /区切り
        relative_path = "../" * (len(dir_depth))# 相対パス生成
        myStr += f"\\変数設定{{■共通パス}}{{{relative_path}■共通}} % 共通パーツにアクセスするためのパス \n\n"
        myStr += f"% 主に，表紙 ＆ PDFの文書プロパティ\n"

      # ３行目以降 & 文字色が青
      if idx >= 2 and row[0].font.color.rgb == "FF0070C0" : # 色縛り：青
        # 表示言語による機種名の全角/半角切り替え
        ## 表示言語の行でフラグセット
        if (col_a_value == "表示言語") and (col_b_value == "Jpn") :
          flag_lang  = True

        ##################################################
        ## 表示言語による機種名の全/半角切り替え
        if flag_lang  == True:
          if  col_a_value == "機種名" or \
              col_a_value == "機種" :
            col_b_value = mojimoji.han_to_zen( col_b_value ) # 日本語表記[Jpn]：全角化
        else:
          pass
          # col_b_value = mojimoji.han_to_zen( col_b_value ) # 基本的には半角表記

        ##################################################
        if col_a_value != "号機":
          # 号機以外の青文字
          myStr += f"\\変数設定{{{col_a_value}}}{{{col_b_value}}} % {col_c_value }\n"
        else:
          # 号機
          if row[0].offset(1,0).value == "号機": # 次行の列Aの値が号機か確認
            # 次行も号機：表形式で表示させるためのデータ生成
            ## 号機の範囲取得
            result = {} # 表用データ格納用
            types = [] # 号機一時格納配列
            num = 0 # "号機"の行数カウント
            while 1 : # 無限ループ
              if row[0].offset(num,0).value == "号機": # 号機縛り
                types.append( row[1].offset(num,0).value ) # 型式号機
                num += 1
              else:
                break # "号機"でない行となったら終了
            for type in types: # 取得した号機sで繰り返し
              print( type.find("；") )
              if type.find("；") == -1:
                result.setdefault("辞書",[]).append(type) # ；区切以降を辞書登録
              else:
                result.setdefault(type[:type.find("；")],[]).append(type[type.find("；")+1:]) # ；区切以降を辞書登録

            flag_end = True # 終了フラグ
          else:
            # 次行号機ではない
            myStr += f"\\変数設定{{{col_a_value}}}{{{col_b_value}以降}} % {col_c_value }\n"


        # ここから"前後左右の方向"用の値取得
        if col_a_value == "機種名":
          machine_type = col_b_value
        if col_a_value == "機種" :
          machine_model = col_b_value
        if col_a_value == "BookNo":
          book_no = col_b_value

      if col_a_value == "前後左右の方向の有無" and col_b_value == "あり":
        flag_directions = True

      if flag_end == True:
        break


    if flag_end == True:
      # 号機を表形式表示するためのデータ整形
      keys_str = ', '.join(result.keys()) # キーを結合
      values_str = ''
      for ii in range( max(map(len, result.values())) ):
        temp_values = []
        for key in result:
          if ii < len(result[key]):
            temp_values.append(result[key][ii])
          else:
            temp_values.append('')
        values_str += ','.join(temp_values) + ' ;'
      result_str = keys_str + ' ;' + values_str
      if result_str.find("辞書") != -1: # 複数行、小型用ではない場合
        result_str = f"{result_str[result_str.find(";")+1:-1].replace(";","・")}以降"
        myStr += f"\\変数設定{{号機}}{{{result_str}}} % 複数号機\n"
      elif  result_str.find("辞書") != -1: # 複数行、小型(;区切り)の場合
        myStr += f"\\変数設定{{号機s}}{{{result_str}}} % 複数号機\n"

    myStr += f"\n\n% 版/発行日\n"
    ff.write( myStr ) # テキスト書き込み


  # "前後左右の方向"ありの場合：ファイル作成（ヘッダのみ作成）
  if flag_directions == True:
    filename = base_path.joinpath( "11_前後左右の方向.tex" )
    if not( os.path.exists( filename )):
      with open(filename, 'w', encoding='utf-8') as ff:
        myStr = f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
                f"% made by makeTeX.py\n" \
                f"% 機　種：{machine_type}\n" \
                f"% 型　式：{machine_model}\n" \
                f"% BookNo：{book_no}\n" \
                f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n\n" \
                f"% ※'ファイル名'が'方向.pdf'ではない場合は，状況に応じて変更すること！\n" \
                f"% ■前後左右方向の画像作成ルール■■■■■■■■■■■■■\n" \
                f"% 1.画像ファイル名\n" \
                f"%     各機種フォルダの'図/方向.pdf'とすること！\n" \
                f"%       →以下コード変更の工数削減\n" \
                f"% 2.画像サイズ\n" \
                f"%     幅×高＝mm×mmの寸法に収まる画像を作成すること！\n" \
                f"%       →縮尺変更時に文字が拡大/縮小防止のため\n" \
                f"% 3.画像の向き\n" \
                f"%     掲載時の向きで作成すること！\n" \
                f"%       →以下コード変更の工数削減\n" \
                f"%       ※Inkscape : 回転が必要な場合は，右下のR値を90/-90とし画像を事前に逆回転させておくこと！\n" \
                f"\n\n"\
                f"\\begin{{figure}}[h]\n" \
                f"\\centering\n" \
                f"\\includepraphic[scale=1.0, angle=0, keepaspectratio]{{./図/方向.pdf}} % 画像サイズのまま，回転なし　※原則コレを使用！\n" \
                f"%\\includepraphic[scale=1.0, angle=90, keepaspectratio]{{./図/方向.pdf}} % 画像サイズのまま，90度回転(CCW)\n" \
                f"%\\includepraphic[width=\\textwidth, angle=0, keepaspectratio]{{./図/方向.pdf}} % 用紙幅にフィット，回転なし\n" \
                f"%\\includepraphic[height=\\textwidth, angle=90, keepaspectratio]{{./図/方向.pdf}}% 用紙幅にフィット後に90度回転(CCW)\n" \
                f"\\end{{figure}}\n"
        ff.write( myStr ) # テキスト書き込み



  # 自作変数のstyファイル(設定変数.sty)出力処理
  output_file_path = base_path.joinpath( "設定変数.sty")
  with open(output_file_path, 'w', encoding='utf-8') as ff:

    # コメント部分
    myStr = f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
            f"% ファイル名：{output_file_path.name}\n" \
            f"% 内　　　容：自作変数の設定(TeX制御含む、変数・表生成.xlsmを完成のこと！）\n" \
            f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
    ff.write( myStr )

    for idx, row in enumerate( sheet.iter_rows(min_row=3) ):
      col_a_value = row[0].value  # [列A]変数名
      col_b_value = row[1].value  # [列B]設定値
      col_c_value = row[2].value  # [列C]備考
      if (col_a_value is not None) and (col_b_value is not None) and row[0].font.color.rgb != "FF0070C0": # 色縛：青以外
        ff.write(f"\\変数設定{{{col_a_value}}}{{{col_b_value}}} % {col_c_value }\n")

  return flag_lang  # 表示言語フラグ




#####################################################################################
# escape_tex_string
#  - TeXで安全な文字列に変換する
# [引数] s 文字列
#####################################################################################
def escape_tex_string(s):
    if isinstance(s, (int, float)):
        s = str(s)
    s = s.replace("\\", "\\\\")
    s = s.replace("{", "\\{")
    s = s.replace("}", "\\}")
    s = s.replace("%", "\\%")
    s = s.replace("$", "\\$")
    s = s.replace("&", "\\&")
    s = s.replace("#", "\\#")
    s = s.replace("~", "\\~")
    s = s.replace("^", "\\^")
    s = s.replace("_", "\\_")
    return s




##############################################################
# create_table_code
#  - Excelの表をTeX(longtable)形式に変換
# [引数] sheet      シートオブジェクト
# [引数] base_path  Excelファイルの親パス
##############################################################
def create_table_code(sheet, base_path):


  tex_file_name = sheet['A1'].value  # A2セルにファイル名(拡張子なし)が記述されている前提
  if not tex_file_name:
    print(f"シート '{sheet['A1'].value}' のセル[A2]にファイル名が記述されていません。")
    exit

  base_path = pathlib.Path( base_path )
  output_dir = base_path.joinpath("表")
  if not os.path.exists( output_dir ):
    os.makedirs( output_dir ) # なければディレクトリ生成

  output_file_path = output_dir.joinpath("{tex_file_name}.tex") # ファイル名
  with open(output_file_path, 'w', encoding='utf-8') as f:

##########################################################
    # コメント部分出力
    myStr = f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
            f"% ファイル名：{output_file_path.stem}\n" \
            f"% made by makeTeX.py\n" \
            f"% 内　　　容：{sheet['A1'].value}\n" \
            f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
    f.write( myStr ) # テキスト出力

    # 表の設定：インデント含む
    indent = "0mm" # 初期値：インデントなし
    if "あり" in sheet['A2'].value:
      indent = f"\\myLEFTSKIP" # インデントあり時
    myStr = f"\\setlength{{\\tabcolsep}}{{2mm}} % セルの余白\n" \
            f"\\setlength{{\\LTleft}}{{{ indent }}} % 字下げ\n" \
            f"\\setlength{{\\LTright}}{{0pt}} % 右側余白設定\n" \
            f"\\setlength{{\\LTpre}}{{2mm}} % 表前の余白\n" \
            f"\\setlength{{\\LTpost}}{{0mm}} % 表後の余白\n\n\n"
    # f.write( myStr ) # テキスト出力


    # ヘッダ部
    NumRule = 0 # 罫線(垂線)の本数：表幅補正に使用
    myLength = 0 # 表幅用：インデントの有無による変動算出
    NumColumn = 0 # 最大列数：なにかしらの処理で空白セルが発生しうるため、列数をこれで制限


    if "ボルト締付" in sheet['A1'].value:
      myStr = f"{{\\ttfamily % [ボルト締付トルク] など等幅フォントを使用する場合は、先頭の[%]を省く\n\n"

    myStr += f"\\begin{{longtable}}"
    myStr += "{"

    for row in sheet.iter_rows(min_row=3, max_row=3):
      for idx, cell in enumerate( row[2:] ): #

        # 列数：空白行が入り込みやすいため、ココで制限をかける
        if cell.value is None:
          break
        else:
          NumColumn = idx


        # 幅と寄せの設定
        if str(cell.offset(0,0).value).isdigit(): # 幅が数値の場合（*ではない）
          if "S" in cell.offset(1,0).value: # 寄せ：小数点
            tmp = f">{{}}S[table-column-width={cell.offset(0,0).value}mm]" # 寄せ：なし　幅：数値のまま
            myLength += int( cell.offset(0,0).value ) + 4
          else:# 寄せ：S以外（lcr）
            tmp = f"p{{{cell.offset(0,0).value}mm}}" # 幅：数値のまま
            myLength += int( cell.offset(0,0).value ) + 4
        else:
          tmp = f"p{{\\myTableWidth}}" # 修正必要

        if not( "S" in cell.offset(1,0).value ) :
          if "l" in cell.offset(1,0).value: # 寄せ:左
            tmp = f">{{\\raggedright\\arraybackslash}}" + tmp
          elif "c" in cell.offset(1,0).value:# 寄せ:中央
            tmp = f">{{\\centering\\arraybackslash}}" + tmp
          elif "r" in cell.offset(1,0).value:# 寄せ:右
            tmp = f">{{\\raggedleft\\arraybackslash}}" + tmp


        # 罫線
        if cell.offset(1,0).value.replace(" ","")[0:1] == "|": # 左側に罫線
          tmp = f" |{tmp}"
          NumRule += 1 # 罫線数を加算
        if cell.offset(1,0).value.replace(" ","")[-1:] == "|": # 右側に罫線
          tmp = f" {tmp}|"
          NumRule += 1 # 罫線数を加算
        myStr = f"{myStr}{tmp} "

    myStr += "}\n"

    tmp = f"\\setlength{{\\myTableWidth}}{{\\dimexpr 166mm - {myLength}mm - {indent} - {NumRule}\\arrayrulewidth }}\n"
    f.write( tmp ) # テキス出力
    f.write( myStr )

    # print( f"{NumColumn} : {sheet['A1'].value}" )
##########################################################
    # リスト＆環境の締め部
    myStr = "" # テキストの一時保管用
    count_row = 0 # 行カウンタ：偶/奇数処理用
    for row in sheet.iter_rows(min_row=6): # 行で繰り返し(7行目以降)
      list = [] # 行項目リスト
      count_row += 1 # 行カウンタの加算
      flag_merge = False # 結合フラグ
      flag_header = False # ヘッダ用フラグ
      flag_hline = "" # 罫線用フラグ（文字列）
      for ii, cell in enumerate( row[0:NumColumn+3] ): # 各行の列で繰り返し(列Aスタート)

        # 罫線チェック
        if ii == 0:
          if cell.value == "改ページ":
            flag_hline = "\\hline \\pagebreak"
          elif cell.value == "太線":
            flag_hline = "\\hline \\hline"
          elif cell.value == "細線":
            flag_hline = "\\hline"
          else:
            flag_hline = ""

        # 行指定の背景色
        if ii == 1: # 列A @ Excel
          if cell.value is None: # 列Bの値が空白の場合
            if ( count_row % 2 ) == 0: # 偶奇数判定
              myStr += f"\\rowcolor{{gray!10}}\t" # 偶数行
            else:
              myStr += f"\\rowcolor{{white}}\t" # 奇数行
          else:
            if str(cell.value).isdigit(): # 数値判定
              myStr += f"\\rowcolor{{gray!{cell.value}}}\t" # 背景色
              if cell.value == 60: # ヘッダフラグ
                if cell.offset(1,0).value != 60: # 次行が60(タイトル：濃背景)の場合
                  flag_header = True #

        # 結合チェック
        if (ii > 1) and (ii<len(row)): # 不要項目除去
          flag_merge = False # 結合フラグ
          for jj in range( len(list) ): # 既存リストで繰り返し
            if cell.value == list[jj][0] and not(list[jj][0] is None): # 結合判定
              flag_merge = True # 結合（隣セルと同値）：あり

          if flag_merge == True: # 結合（隣セルと同値）：あり
            list[jj][1] += 1 # 結合数をカウントアップ
          else: # 結合：なし
            list.append([cell.value,1]) # リストにセル値，数量(1)を追記

      for ii, ll in enumerate( list ): # リスト部の処理
        if ll[1] == 1: # セル結合なし(1=1セル)
          if ll[0] is None: # セル値：なし
            myStr += f" & " # 空白表示
          else: # セル値：あり
            if not( row[1].value is None): # 行背景色：あり
              myStr += f"\\textbf{{{ll[0]}}} & " # 太文字
            else:# 行背景色：なし
              myStr += f"{ll[0]} & " # そのまま表示

        else: # セル結合あり

          if sheet.cell(4,ii+3).value == "S"   : # 寄せがS(小数点)
            align = "c" #
            tmp = f"\\textbf{{{ll[0]}}}"
          elif ii == 0: # 列C
            align = "l" # B列：左寄＆太文字
            tmp = f"\\textbf{{{ll[0]}}}"

          elif not( row[1].value is None) : # 背景色あり(=タイトル)
            align = "l" # 左寄＆太文字
            tmp = f"\\textbf{{{ll[0]}}}"
          else: # 列D以降
            align = "c" # 中央寄せ
            tmp = f"{ll[0]}"
          myStr += f"\\multicolumn{{{ll[1]}}}{{{align}}}{{{tmp}}} & " # セル値

        # 行カウンタの初期か
        if not( row[1].value is None):
          count_row = 0 # 行カウンタの初期化

      myStr = myStr[:-2] + f"\\\\ {flag_hline}\n"
      # if flag_hline in "改ページ":
      #   myStr += f"\\hline\\pagebreak\n" # 罫線＋改ページ
      # else:
      #   myStr +=  # 最後の&除去と改行
      flag_hline = ""

      if flag_header == True:
        flag_header = False
        tmp = myStr
        myStr = f"{tmp} \\endfirsthead\n" \
                f"{tmp} \\endhead\n"

    myStr += f"\n\\end{{longtable}}\n\n" # 環境の締め

    if "ボルト締付" in sheet['A1'].value:
      myStr += f"}} % [ボルト締付トルク] など等幅フォントを使用する場合は、先頭の[%]を省く\n\n"

    f.write( myStr )





# メイン
if __name__ == "__main__":
  
  ret = messagebox.askyesno('確認', '［は　い］：誤動作⇒終了！ \n\n［いいえ］：■共通の表作成')   #「はい」、「いいえ」を選択
  if not ret:
    script_dir = pathlib.Path( sys.argv[0] ).parent.parent
    excel_file_path = script_dir.joinpath("変数・表生成.xlsm")


  # # フォルダ取得
  # folder_path = filedialog.askdirectory(
  #   title       = "変数・表生成.xlsm のあるフォルダを選択",
  #   initialdir  = "./",
  #   mustexist   = True )
  # folder_path = pathlib.Path( folder_path ).absolute()
  # os.chdir(folder_path)  # カレントディレクトリ変更

  # excel_file_path = folder_path / "変数・表生成.xlsm"

  # if excel_file_path:
  #   result = create_sty_and_tex_files(excel_file_path)
  #   # print( result )
  #   if result == 0:
  #     print("処理終了！")
  #   else:
  #     print("処理中にエラー発生！")
  # else:
  #   print("ファイルが選択されませんでした。")
