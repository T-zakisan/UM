from pathlib import Path
import sys
import pikepdf
import fitz  # PyMuPDF


# PDF結合としおりの再挿入を行うスクリプト
def extract_toc(pdf_path: Path) -> list:
    """fitzからTOC（しおり）を取得（ページ番号は1始まり）"""
    with fitz.open(str(pdf_path)) as doc:
        return doc.get_toc(simple=True)

# PDFを結合する関数
def merge_pdfs(cover_pdf: Path, body_pdf: Path, output_pdf: Path) -> None:
    with (
        pikepdf.Pdf.open(cover_pdf) as pdf_cover,
        pikepdf.Pdf.open(body_pdf) as pdf_body,
        pikepdf.Pdf.new() as merged_pdf
    ):
        merged_pdf.pages.extend(pdf_cover.pages)
        merged_pdf.pages.extend(pdf_body.pages)
        merged_pdf.save(output_pdf)
        print(f"[OK] PDFを結合: {output_pdf}")


# しおりを再挿入する関数
def insert_merged_toc(output_pdf: Path, cover_toc: list, body_toc: list, offset: int) -> None:
    """結合後のPDFにしおりを再挿入"""
    # ページ番号は1始まりでオフセットを加算
    for i in range(len(body_toc)):
        body_toc[i][2] += offset

    full_toc = cover_toc + body_toc

    with fitz.open(str(output_pdf)) as doc:
        doc.set_toc(full_toc)
        doc.saveIncr()
        print(f"[OK] しおりを再挿入しました（{len(full_toc)} 項目）")


def main():
    if len(sys.argv) != 3:
        print("2つのPDFを同時にドラッグ＆ドロップしてください。")
        print("使い方: python merge_with_fitz_outline.py 表紙.pdf 本体.pdf")
        return

    path1 = Path(sys.argv[1])
    path2 = Path(sys.argv[2])

    if path1.stem.endswith("表紙"):
        cover_pdf, body_pdf = path1, path2
    elif path2.stem.endswith("表紙"):
        cover_pdf, body_pdf = path2, path1
    else:
        print("どちらかのファイル名に '_表紙' が必要です。")
        return

    output_pdf = cover_pdf.parent / f"{cover_pdf.stem.replace('_表紙', '')}_結合.pdf"

    # しおり情報を取得（結合前）
    toc_cover = extract_toc(cover_pdf)
    toc_body = extract_toc(body_pdf)

    # PDF結合
    merge_pdfs(cover_pdf, body_pdf, output_pdf)

    # ページオフセット = 表紙ページ数
    with fitz.open(str(cover_pdf)) as cover_doc:
        offset = len(cover_doc)

    # しおり再挿入
    insert_merged_toc(output_pdf, toc_cover, toc_body, offset)

if __name__ == "__main__":
    main()
