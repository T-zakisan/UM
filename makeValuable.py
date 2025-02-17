import utils

def create_variable_definitions( sheet ):
  output_file_path = "myValues.sty"
  with open(output_file_path, 'w', encoding='utf-8') as f:
    
    # コメント部分
    myStr = f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
            f"% ファイル名：{output_file_path }\n" \
            f"% 内　　　容：変数の設定(TeX制御含む)\n" \
            f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
    f.write( myStr )

    for idx, row in enumerate( sheet.iter_rows(min_row=2) ):
      col_a_value = row[0].value  # [列A]変数名
      col_b_value = row[1].value  # [列B]設定値
      col_d_value = row[3].value  # [列D]備考
      
      myVariable = f"\変数：{col_a_value}"
      sheet.cell( row=idx+2, column=3, value=myVariable )
      print( f"{idx+2} : {myVariable}" )


      if col_a_value is not None and col_b_value is not None:
        col_b_value = utils.escape_tex_string(col_b_value) # テキストチェック(エスケープ文字対応)
        f.write(f"\\newcommand{{{myVariable}}}{{{col_b_value}}} % {col_d_value }\n")

