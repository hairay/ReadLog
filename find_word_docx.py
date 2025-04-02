import os
from docx import Document

# 設定要搜尋的資料夾和目標字串
folder_path = "X:\Eagle"  # 替換成你的 Word 檔案所在資料夾
search_text = "201607"

# 搜尋函數
def search_in_docx(file_path, search_text):
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            if search_text in para.text:
                return True  # 找到即回傳 True
    except Exception as e:
        print(f"無法讀取 {file_path}: {e}")
    return False

# 遍歷資料夾中的所有 .docx 文件
found_files = []
for filename in os.listdir(folder_path):
    if filename.endswith(".docx"):
        file_path = os.path.join(folder_path, filename)
        if search_in_docx(file_path, search_text):
            found_files.append(filename)

# 輸出搜尋結果
if found_files:
    print("找到包含字串的文件:")
    for file in found_files:
        print(file)
else:
    print("沒有找到符合的文件。")

