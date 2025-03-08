#####################################################################################
# makeMain.py
# [ 2025.03.07 ]
#  main.texをフォルダの内容、設定変数.styから生成
#  ■issue
#####################################################################################

import pathlib
from tkinter import messagebox

def make_main( folder_path ):

  # 既存の出力ファイル削除
  ff = [ '*.pdf', '*.toc', '*.out', '*.aux', '*.log', 'main.tex' ]
  for pattern in ff:
    for filepath in pathlib.Path('.').glob( pattern ):
      try:
        filepath.unlink()
      except FileNotFoundError:
        print(f"ファイル {filepath} は存在しません。")
      except Exception as e:
        print(f"ファイル {filepath} の削除中にエラーが発生しました: {e}")


  # 設定変数.sty をテキスト解析し，出力ファイル名生成
  with open( folder_path.joinpath("設定全体.sty"), "r", encoding="utf-8") as ff:
    for line in ff:
      if line is not None and line[0] != "%":
        line = line.rstrip()  # 改行削除
        line = line[1+line.find("{"):line.rfind("}")] # 主要部抽出
        if "機種" in line:
          machine_type = line[1+line.find("{"):]
        if "号機" in line:
          machine_model = line[1+line.find("{"):]
        if "BookNo" in line:
          book_no = line[1+line.find("{"):]


    # 出力ファイル名
    file_name = f"main.tex"
    tex_file = folder_path.joinpath(file_name)


    # 既存の出力ファイル削除
    if tex_file.exists():
      tex_file.unlink()


  # main.tex　前半固定部
  with open(tex_file, 'w', encoding='utf-8') as ff:
    myStr = f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
            f"% 機　種：{machine_type}\n" \
            f"% 型　式：{machine_model}\n" \
            f"% BookNo：{book_no}\n" \
            f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
            f"\\documentclass[11pt, a4paper]{{ltjsarticle}}\n\n" \
            f"\\usepackage{{設定全体}}          % 設定全体.sty\n" \
            f"\\usepackage{{\\変数{{■共通パス}}/HANTA}} % 共通書式設定\n" \
            f"\\usepackage{{設定変数}}          % 設定変数.sty\n\n\n" \
            f"\\begin{{document}}\n\n" \
            f"\\input{{\\変数{{■共通パス}}/00_表紙.tex}}\n" \
            f"\\input{{\\変数{{■共通パス}}/10_まえがき.tex}}\n"
    # ff.write( myStr )



    # 前後左右の方向の有無
    if folder_path.joinpath("11_前後左右の方向.tex").exists():
      myStr +=  f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%¥n" \
                f"\\input{{./11_前後左右の方向.tex}}\n" \
                f"%\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
      # ff.write( myStr )


    myStr +=  f"\\input{{\\変数{{■共通パス}}/20_目次.tex}}\n" \
              f"\\input{{\\変数{{■共通パス}}/30_安全上の注意事項.tex}}\n" \
              f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%\n"
    # ff.write( myStr )


    # main.tex  可変部分
    # myStr = ""
    for filename in folder_path.iterdir():
      if ".tex" in filename and filename != file_name:
        myStr += f"\\input{{./{filename}}}\n"
    # ff.write( myStr )

  # main.tex　後半占め
    myStr +=  f"%\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
              f"\\input{{\\変数{{■共通パス}}/99_裏表紙.tex}}\n\n" \
              f"\\end{{document}}\n\n"
    
    # ファイル書き出し
    ff.write( myStr )


# メイン
if __name__ == "__main__":
  
  messagebox.showinfo('注意', '単独起動はできません．') 

  # # スクリプトのあるフォルダをカレントディレクトリに設定
  # script_dir = pathlib.Path( os.path.abspath(sys.argv[0]) ).parent

  # # フォルダ取得
  # folder_path = filedialog.askdirectory(
  #   title       = "main.texのあるフォルダを選択",
  #   initialdir  = script_dir,
  #   mustexist   = True )
  # if not os.path.exists( folder_path ):
  #   folder_path = pathlib.Path( folder_path ).absolute()
  #   os.chdir(folder_path)  # カレントディレクトリ変更

  #   make_main( folder_path )


