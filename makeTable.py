##############################################################
# makeTable.py
#   Excelの表をTeX(longtable)形式に変換
#   2025.02.17
#   <issu>
#    - 関数で小分け（ヘッダ，リスト＆フッタ）程度に小分けにしたいかな
##############################################################

import utils 

"""表シートの処理"""
def create_table_code(sheet):

  tex_file_name = sheet['A2'].value  # A2セルにファイル名(拡張子なし)が記述されている前提
  if not tex_file_name:
    print(f"シート '{sheet['A1'].value}' のセル[A2]にファイル名が記述されていません。")
    exit

  output_file_path = tex_file_name + ".tex" # ファイル名
  with open(output_file_path, 'w', encoding='utf-8') as f:


##########################################################

    # コメント部分出力
    myStr = "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" + \
            "% ファイル名：" + output_file_path + "\n" \
            "% 内　　　容：" + sheet['A1'].value + "\n" \
            "% 製　　　作：2025.02.18\n" \
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
    f.write( myStr ) # テキスト出力

    # 表の設定：インデント含む
    indent = "0mm" # 初期値：インデントなし
    if "あり" in sheet['A3'].value:
      indent = f"\\myLEFTSKIP" # インデントあり時
    myStr = f"\\setlength{{\\tabcolsep}}{{2mm}} % セルの余白\n" \
            f"\\setlength\\LTleft{{{ indent }}} % 字下げ\n" \
            f"\\setlength\\LTright{{0pt}} % 右側余白設定\n" \
            f"\\setlength\\LTpre{{2mm}} % 表前の余白\n" \
            f"\\setlength\\LTpost{{0mm}} % 表後の余白\n"
    f.write( myStr ) # テキスト出力


    # ヘッダ部
    myLength = 0
    myStr = f"\\begin{{longtable}}"
    myStr += "{"
    for row in sheet.iter_rows(min_row=4, max_row=4): #
      for idx, cell in enumerate( row[0:] ): # 
        if idx>=2 :

          # 背景色
          tmp = cell.offset(2,0).value # 背景値取得
          myStr += " >{"
          if not( tmp is None ): # 背景色（濃度）：入力あり
            myStr += f"\\columncolor{{gray!{tmp}}}"

          # 寄せ
          tmp = cell.offset(1,0).value # 寄せ取得
          if tmp == "l": # 左寄せ
            myStr += f"\\raggedright\\arraybackslash"
          elif tmp == "c" or tmp == "": # 中央寄せ：未記入
            myStr += f"\\centering\\arraybackslash"
          elif tmp == "r": # 右寄せ
            myStr += f"\\raggedleft\\arraybackslash"
          myStr += "}"

          # 列幅
          tmp = f"{cell.offset(0,0).value}" # 列幅取得
          if tmp.isdigit(): # 数値の場合
            myStr += f"p{{{tmp}mm}}" # 数値をそのまま反映
            myLength += int( tmp ) + 4 
          else:
            myStr += f"p{{\\myTableWidth}}" # 修正必要
            pass
    myStr += "}\n"

    tmp = f"\\newlength{{\\myTableWidth}}\n" \
          f"\\setlength{{\\myTableWidth}}{{166mm - {myLength}mm - {indent} }}\n"
    f.write( tmp ) # テキス出力
    f.write( myStr ) # テキス出力

##########################################################


    # リスト＆環境の締め部
    myStr = "" # テキストの一時保管用
    count_row = 0 # 行カウンタ：偶/奇数処理用
    for row in sheet.iter_rows(min_row=7): # 行で繰り返し
      list = [] # 行項目リスト
      count_row += 1 # 行カウンタの加算
      flag_merge = False # 結合フラグ
      flag_header = False # ヘッダ用フラグ
      flag_hline = "" # 罫線用フラグ（文字列）
      for ii, cell in enumerate( row[0:] ): # 各行の列で繰り返し(列Aスタート)
        
        # 罫線チェック
        if ii == 0:
          if cell.value == "太線":
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

      for ii, ll in enumerate( list ):
        if ll[1] == 1: # セル結合なし(1=1セル) 
          if ll[0] is None: # セル値：なし
            myStr += f" & " # 空白表示
          else: # セル値：あり
            if not( row[1].value is None): # 行背景色：あり
              myStr += f"\\textbf{{{ll[0]}}} & " # 太文字
            else:# 行背景色：なし
              myStr += f"{ll[0]} & " # そのまま表示

        else: # セル結合あり
          if ii == 0: # 列C
            align = "l" # B列：左寄＆太文字
            myStr += f"\\multicolumn{{{ll[1]}}}{{{align}}}{{\\textbf{{{ll[0]}}}}} & " # セル値：太文字
            count_row = 0 # 行カウンタの初期化
          else: # 列D以降
            align = "c" # 中央寄せ
            myStr += f"\\multicolumn{{{ll[1]}}}{{{align}}}{{{ll[0]}}} & " # セル値


      myStr = myStr[:-2] + f"\\\\ {flag_hline}\n" # 最後の&除去と改行
      flag_hline = ""

      if flag_header == True:
        flag_header = False
        tmp = myStr
        myStr = f"{tmp} \\endfirsthead  \\hline\\hline \n" \
                f"{tmp} \\endhead       \\hline\\hline \n" 

    myStr += f"\\hline\\hline \n" # 最後の罫線と改行
    myStr += f"\\end{{longtable}}" # 環境の締め
    f.write( myStr )
