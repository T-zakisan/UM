##############################################################
# makeTable.py
#   Excelの表をTeX(longtable)形式に変換
#   2025.02.17
#   <issu>
#    - インデントの有無に対して，p{長さ}の処理が未実装 
#    - |で\hlineが未実装
#    - コメントがおおよそつけていない（勢いで作ったので・・・）
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
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
    f.write( myStr )


    # 表の設定：インデント含む
    indent = [ "0mm", 156.1 ] # 初期値：インデントなし
    if "あり" in sheet['A3'].value:
      indent = [ "\\myLEFTSKIP", 140.0 ] # インデントあり時
    myStr = f"\\setlength{{\\tabcolsep}}{{2mm}} % セルの余白\n" \
            f"\\setlength\\LTleft{{{ indent[0] }}} % 字下げ\n" \
            f"\\setlength\\LTright{{0pt}} % 右側余白設定\n" \
            f"\\setlength\\LTpre{{2mm}} % 表前の余白\n" \
            f"\\setlength\\LTpost{{0mm}} % 表後の余白\n"
    f.write( myStr )


    # ヘッダ部
    myLength = 0
    myStr = f"\\begin{{longtable}}"
    myStr += "{"
    for row in sheet.iter_rows(min_row=4, max_row=4):
      for idx, cell in enumerate( row[0:] ): 
        if idx>=2 :

          # 背景色
          tmp = cell.offset(2,0).value
          myStr += " >{"
          if tmp != None:
            myStr += f"\\columncolor{{gray!{tmp}}}"

          # 寄せ
          tmp = cell.offset(1,0).value
          if tmp == "l":
            myStr += f"\\raggedright\\arraybackslash"
          elif tmp == "c" or tmp == "":
            myStr += f"\\centering\\arraybackslash"
          elif tmp == "r":
            myStr += f"\\raggedleft\\arraybackslash"
          myStr += "}"

          # 列幅
          tmp = f"{cell.offset(0,0).value}"
          if tmp != "*":
            myStr += f"p{{{tmp}mm}}"
            # myLength += tmp
          else:
            if "あり" in sheet['A3'].value:
              pass
              # mystr += f"p{{{tmp}}}" # 修正必要
            else:
              pass
              # mystr += f"p{{{tmp}}}" # 修正必要
    myStr += "}\n"
    f.write( myStr )

##########################################################


    # リスト部分
    myStr = ""
    count_row = 0
    for row in sheet.iter_rows(min_row=7): # 行で繰り返し
      list = []
      # list.clear
      count_row += 1
      flag = False
      for ii, cell in enumerate( row[1:] ): # 各行の列で繰り返し(列Bスタート)
        
        # 行指定の背景色
        if ii == 0:
          if cell.value is None:
            if ( count_row % 2 ) == 0:
              myStr += f"\\rowcolor{{gray!10}}\t" # 偶数行
            else:
              myStr += f"\\rowcolor{{white}}\t" # 奇数行
          else:
            if str(cell.value).isdigit():
              myStr += f"\\rowcolor{{gray!{cell.value}}}\t" # 値がある場合
            else:
              pass

        # 結合チェック
        if (ii > 0) and (ii<len(row)):
          flag = False
          for jj in range( len(list) ):
            if cell.value == list[jj][0] and not(list[jj][0] is None):
              flag = True

          if flag == True:
            list[jj][1] += 1              
          else:
            list.append([cell.value,1])

      for ii, ll in enumerate( list ):
        if ll[1] == 1: # セル結合なし
          if ll[0] is None:
            myStr += f" & "
          else:
            if not( row[0].value is None): # 色あり
              myStr += f"\\textbf{{{ll[0]}}} & "
            else:
              myStr += f"{ll[0]} & "
        
        else: # セル結合あり
          if ii == 0: # 列C
            align = "l" # B列：左寄＆太文字
            myStr += f"\\multicolumn{{{ll[1]}}}{{{align}}}{{\\textbf{{{ll[0]}}}}} & " # セル値：太文字
          else: # 列D以降
            align = "c" # 中央寄せ
            myStr += f"\\multicolumn{{{ll[1]}}}{{{align}}}{{{ll[0]}}} & " # セル値



      myStr = myStr[:-2]  # 最後の&除去
      myStr += f"\\\\ \n" # 改行


    myStr += f"\\hline\\hline \n"
    myStr += f"\\end{{longtable}}"
    f.write( myStr )
