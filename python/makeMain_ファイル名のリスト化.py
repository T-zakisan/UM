#####################################################################################
# makeMain.py
#  2025.03.10
#  - main.texをフォルダの内容、設定変数.styから生成
#  - _Compile({機種}_{号機}_{機種}).pyのショートカット生成　※コンパイルファイル
#  - （機種）_（号機）_（機種）.pyのショートカット生成　※
#  ■issue
#####################################################################################
import sys
import os
import pathlib
from tkinter import messagebox, filedialog
import mojimoji


# main.tex　を書き出すやつ #
def make_main( folder_path, machine_type, machine_model, book_no ):


  # 出力ファイル名
  file_name = f"main.tex"
  folder_path = pathlib.Path( folder_path )
  tex_file = folder_path.joinpath(file_name)


  # 既存の出力ファイル削除
  if tex_file.exists():
    tex_file.unlink()


  # main.tex　前半固定部
  with open(tex_file, 'w', encoding='utf-8') as ff:
    myStr = f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
            f"% main.tex\n" \
            f"%   made by makeMain.py\n" \
            f"%   機　種：{machine_type}\n" \
            f"%   号　機：{machine_model}\n" \
            f"%   BookNo：{book_no}\n" \
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
    if folder_path.joinpath("11_前後左右方向の表現.tex").exists():
      myStr +=  f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%\n" \
                f"\\input{{./11_前後左右方向の表現.tex}}\n" \
                f"%\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
      # ff.write( myStr )


    myStr +=  f"\\input{{\\変数{{■共通パス}}/20_目次.tex}}\n" \
              f"\\input{{\\変数{{■共通パス}}/30_安全上の注意事項.tex}}\n" \
              f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%\n"
    # ff.write( myStr )

    # main.tex  可変部分
    # myStr = ""

    for ii, filename in enumerate( folder_path.iterdir()):
      filename = filename.name
      if  (".tex" in str(filename)) and \
          (str(filename) != str(file_name)) and \
          not ("11_" in str(filename)) : # 対象：*.tex & !main.tex & !"11_…"
        myStr += f"\\input{{./{filename}}}\n"
    # ff.write( myStr )


  # main.tex　後半占め
    myStr +=  f"%\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n" \
              f"\\input{{\\変数{{■共通パス}}/99_裏表紙.tex}}\n\n" \
              f"\\end{{document}}\n\n"

    # ファイル書き出し
    ff.write( myStr )



# コンパイル用のスクリプト(機種名_BookNo_号機.py)を書き出すやつ #
def make_compile( folder_path, machine_type, machine_model, book_no ):
  # 出力ファイル名
  machine_type = mojimoji.zen_to_han( machine_type ) # 全角→半角
  file_name = f"_Compile({machine_type}_{machine_model}_{book_no}).ps1"
  folder_path = pathlib.Path( folder_path )
  compile_file = folder_path.joinpath(file_name)


  # 既存の出力ファイル削除
  if compile_file.exists():
    compile_file.unlink()


  # コンパイル　前半固定部
  with open(compile_file, 'w', encoding='shift-jis') as ff:
    myStr = f"##################################################\n" \
            f"# LuaLatexコンパイルスクリプト\n" \
            f"#   made by makeMain.py\n" \
            f"#   機　種：{machine_type}\n" \
            f"#   号　機：{machine_model}\n" \
            f"#   BookNo：{book_no}\n" \
            f"##################################################\n\n\n" \
            f"# LualaTeXコマンド作成\n" \
            f"$Command = (\n" \
            f"  \"lualatex.exe\",\n" \
            f"  \"-output-directory=./\",\n" \
            f"  \"-jobname={machine_type}_{book_no}_{machine_model}\",\n" \
            f"  \"-interaction=batchmode\",\n" \
            f"  \"-halt-on-error\",\n" \
            f"  \"-file-line-error\",\n" \
            f"  \"-synctex=1\",\n" \
            f"  \"--shell-escape\",\n" \
            f"  \"main.tex\"\n" \
            f")\n\n" \
            f"# コマンド実行\n" \
            f"Write-Host \"LuaLaTeXを実行中...\"\n" \
            f"$Process = Start-Process -FilePath $Command[0] -ArgumentList ($Command[1..$Command.Length] -join \" \") -NoNewWindow -Wait -PassThru\n\n" \
            f"Write-Host \"しおりを作成中...\"\n" \
            f"$Process = Start-Process -FilePath $Command[0] -ArgumentList ($Command[1..$Command.Length] -join \" \") -NoNewWindow -Wait -PassThru\n\n" \
            f"# 終了コードを取得\n" \
            f"if ( $Process.ExitCode -eq 0 ){{\n" \
            f"  Write-Host \"コンパイル成功: {machine_type}_{book_no}_{machine_model}.pdf \"\n" \
            f"}} else {{\n" \
            f"  Write-Host \"エラーが発生\"\n" \
            f"}}\n\n" \
            f"# コンパイル終了メッセージ\n" \
            f"Write-Host \"コンパイル終了 : [Enter] > 終了\"\n" \
            f"Read-Host | Out-Null\n" \


    # ファイル書き出し
    ff.write( myStr )


def make_Main( folder_path ):

  # 既存の出力ファイル削除
  ff = ( "*.aux", "*.log", "*.out", "*.pdf", "*.toc", "main.tex" )
  for pattern in ff:
    for filepath in pathlib.Path(folder_path).glob( pattern ):
      try:
        filepath.unlink()
      except FileNotFoundError:
        print(f"ファイル {filepath} は存在しません。")
      except Exception as e:
        print(f"ファイル {filepath} の削除中にエラーが発生しました: {e}")


  # 設定変数.sty をテキスト解析し，出力ファイル名生成
  folder_path = pathlib.Path(folder_path)
  with open( folder_path.joinpath("設定全体.sty"), "r", encoding="utf-8") as ff:
    for line in ff:
      if line is not None and line[0] != "#":
        line = line.rstrip()  # 改行削除
        line = line[1+line.find("{"):line.rfind("}")] # 主要部抽出
        if "機種" in line:
          machine_type = line[1+line.find("{"):]
          machine_type = mojimoji.zen_to_han( machine_type )
        if "BookNo" in line:
          book_no = line[1+line.find("{"):]
        if "年度" in line:
          fiscal_year = line[1+line.find("{"):]
          fiscal_year = mojimoji.zen_to_han( fiscal_year )
        if "号機" in line:
          machine_model = line[1+line.find("{"):]
        if "号機数" in line:
          machine_model = fiscal_year # 年度が連番であれば


  # 各ファイル出力
  make_main( folder_path, machine_type, machine_model, book_no )
  make_compile( folder_path, machine_type, machine_model, book_no )





# メイン
if __name__ == "__main__":



  def list_texFiles(folder_path, file_list):
    # 指定されたフォルダのPathオブジェクトを作成
    folder = pathlib.Path(folder_path)

    # フォルダ内の*.texファイルをリストに追加
    for tex_file in folder.glob('*.tex'):
      # 親フォルダ名とファイル名を分けてリストに格納
      file_list.append((folder.name, tex_file.name))

    return file_list



    # ファイル名でソート
    tex_files.sort(key=lambda x: x[1])


  fileList = []

  # スクリプトのあるフォルダをカレントディレクトリに設定
  script_dir = pathlib.Path( sys.argv[0] ).parent
  print( f"script_dir : {script_dir}" )
  tex_files = list_texFiles( script_dir, fileList )


  # フォルダ取得
  folder_path = filedialog.askdirectory(
    title       = "main.texのあるフォルダを選択",
    initialdir  = script_dir,
    mustexist   = True )
  folder_path = pathlib.Path( folder_path )
  if not folder_path.exists() :
    folder_path = folder_path.absolute()
  print( f"folder_path : {folder_path}" )
  tex_files = list_texFiles( folder_path, fileList )



  input()
