import os
import argparse
from docx import Document
try:
    import win32com.client
except ImportError:
    win32com = None

def convert_doc_to_docx(word, doc_path):
    """將 .doc 轉換為 .docx"""
    doc = None
    try:
        doc = word.Documents.Open(os.path.abspath(doc_path))
        docx_path = doc_path + "x"
        doc.SaveAs(os.path.abspath(docx_path), 16)  # 16 代表 .docx 格式
        return docx_path
    finally:
        if doc is not None:
            doc.Close()

def main():
    parser = argparse.ArgumentParser(description="在 .doc 檔案中搜尋指定字串（透過 Word 轉為 .docx）")
    parser.add_argument("-d", "--dir", default=r"X:\Eagle", help="搜尋資料夾路徑 (預設: X:\\Eagle)")
    parser.add_argument("-k", "--keyword", default="201607", help="搜尋目標關鍵字 (預設: 201607)")
    args = parser.parse_args()

    folder_path = args.dir
    search_text = args.keyword

    if not os.path.exists(folder_path):
        print(f"錯誤：資料夾不存在: {folder_path}")
        return

    if win32com is None:
        print("錯誤：請先安裝 pywin32 (`pip install pywin32`)")
        return

    word = None
    found_files = []
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".doc") and not filename.lower().endswith(".docx"):
                doc_path = os.path.join(folder_path, filename)
                docx_path = None
                try:
                    docx_path = convert_doc_to_docx(word, doc_path)
                    doc = Document(docx_path)
                    for para in doc.paragraphs:
                        if search_text in para.text:
                            found_files.append(filename)
                            break
                except Exception as e:
                    print(f"處理檔案 {filename} 時發生錯誤: {e}")
                finally:
                    if docx_path and os.path.exists(docx_path):
                        try:
                            os.remove(docx_path)
                        except OSError:
                            pass
    finally:
        if word is not None:
            word.Quit()

    if found_files:
        print(f"找到包含 '{search_text}' 的文件:")
        for file in found_files:
            print(f"  - {file}")
    else:
        print(f"沒有找到包含 '{search_text}' 的文件。")

if __name__ == "__main__":
    main()
