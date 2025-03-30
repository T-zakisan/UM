import pandas as pd
import os
from pathlib import Path

def generate_test_tex(excel_file, output_file="test.tex"):
	"""
	画像リスト.xlsx の内容に基づいて test.tex を生成する。

	Args:
		excel_file (str or Path): 画像リスト.xlsx のファイルパス。
		output_file (str or Path): 出力する test.tex のファイルパス。
	"""

	# Path オブジェクトに変換
	excel_file = Path(excel_file)
	output_file = Path(output_file)

	try:
		# Excel ファイルを読み込む
		df = pd.read_excel(excel_file, sheet_name="画像リスト")
	except FileNotFoundError:
		print(f"エラー: ファイル '{excel_file}' が見つかりません。")
		return
	except Exception as e:
		print(f"エラー: Excel ファイルの読み込み中にエラーが発生しました: {e}")
		return

	# 表示順をキー、画像パスを値とする辞書を作成
	image_dict = {}
	for index, row in df.iterrows():
		display_order = row["表示順"]
		if pd.isna(display_order):
			continue  # 表示順が空白の場合はスキップ

		common_path = row["共通パス"]
		individual_path = row["個別パス"]
		image_name = row["画像名"]

		if pd.isna(common_path):
			# Pathlibを使ってパスを結合
			image_path = Path(individual_path) / f"{image_name}.pdf"
			image_path_str = str(image_path)
		else:
			image_path_str = f"\\変数{{■共通パス}}{image_name}.pdf"

		if display_order not in image_dict:
			image_dict[display_order] = []
		image_dict[display_order].append(image_path_str)

	# 表示順でソート
	sorted_image_dict = dict(sorted(image_dict.items()))

	# test.tex を生成
	with open(output_file, "w", encoding="utf-8") as f:
		f.write("\\begin{enumerate}[\n")
		f.write("    leftmargin  = 0pt,\n")
		f.write("    labelwidth  = 0pt,\n")
		f.write("    itemindent  = 0pt,\n")
		f.write("  ]\n\n")

		image_count = 0
		for display_order, image_paths in sorted_image_dict.items():
			for image_path in image_paths:
				if image_count % 8 == 0 and image_count != 0:
					f.write("\\newpage\n\n")

					if image_count % 2 == 0:
						f.write("  \\begin{minipage}{0.48\\columnwidth}\n")
						f.write("    \\begin{tcolorbox}[outerBox]\n")
						f.write(f"      \\item {image_path.replace('\\変数{{■共通パス}}', '').replace('.pdf', '')}\n") #画像名を表示
						f.write("      \\vspace{-3mm}\n")
						f.write("      \\begin{tcolorbox}[innerBox]\n")
						f.write(f"        \\adjustbox{{valign=c}}{{\\includegraphics[width=70mm]{{{image_path}}}}}\n")
						f.write("      \\end{tcolorbox}\n")
						f.write("    \\end{tcolorbox}\n")
						f.write("  \\end{minipage}\n")
					else:
						f.write("  \\hfill\n")
						f.write("  \\begin{minipage}{0.48\\columnwidth}\n")
						f.write("    \\begin{tcolorbox}[outerBox]\n")
						f.write(f"      \\item {image_path.replace('\\変数{{■共通パス}}', '').replace('.pdf', '')}\n") #画像名を表示
						f.write("      \\vspace{-3mm}\n")
						f.write("      \\begin{tcolorbox}[innerBox]\n")
						f.write(f"        \\adjustbox{{valign=c}}{{\\includegraphics[width=70mm]{{{image_path}}}}}\n")
						f.write("      \\end{tcolorbox}\n")
						f.write("    \\end{tcolorbox}\n")
						f.write("  \\end{minipage}\n\n")
					image_count += 1

		# 奇数個で終わった場合、空のボックスを追加
		if image_count % 2 != 0:
				f.write("  \\hfill\n")
				f.write("  \\begin{minipage}{0.48\\columnwidth}\n")
				f.write("    \\begin{tcolorbox}[outerBox]\n")
				f.write("      \\vspace{-3mm}\n")
				f.write("      \\begin{tcolorbox}[innerBox]\n")
				f.write("      \\end{tcolorbox}\n")
				f.write("    \\end{tcolorbox}\n")
				f.write("  \\end{minipage}\n\n")

		f.write("\\end{enumerate}\n")

	print(f"'{output_file}' が生成されました。")


# 使用例
excel_file = "画像リスト.xlsx"  # 画像リスト.xlsx のファイルパスを指定
generate_test_tex(excel_file)
