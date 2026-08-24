import os
import argparse
from docx import Document

def search_in_docx(file_path, search_text):
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            if search_text in para.text:
                return True
    except Exception as e:
        print(f"無法讀取 {file_path}: {e}")
    return False

def main():
    parser = argparse.ArgumentParser(description="在 .docx 檔案中搜尋指定字串")
    parser.add_argument("-d", "--dir", default=r"X:\Eagle", help="搜尋資料夾路徑 (預設: X:\\Eagle)")
    parser.add_argument("-k", "--keyword", default="201607", help="搜尋目標關鍵字 (預設: 201607)")
    args = parser.parse_args()

    folder_path = args.dir
    search_text = args.keyword

    if not os.path.exists(folder_path):
        print(f"錯誤：資料夾不存在: {folder_path}")
        return

    found_files = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".docx"):
            file_path = os.path.join(folder_path, filename)
            if search_in_docx(file_path, search_text):
                found_files.append(filename)

    if found_files:
        print(f"找到包含 '{search_text}' 的文件:")
        for file in found_files:
            print(f"  - {file}")
    else:
        print(f"沒有找到包含 '{search_text}' 的文件。")

if __name__ == "__main__":
    main()
