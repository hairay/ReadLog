import os
import win32com.client

def convert_doc_to_docx(doc_path):
    """將 .doc 轉換為 .docx"""
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False  # 不顯示 Word 視窗
    doc = word.Documents.Open(doc_path)
    docx_path = doc_path + "x"  # 轉成 .docx
    doc.SaveAs(docx_path, 16)  # 16 代表 .docx 格式
    doc.Close()
    word.Quit()
    return docx_path

# 設定路徑
folder_path = r"X:\Eagle"  # 請修改為你的資料夾
search_text = "201607"

# 遍歷資料夾內的 .doc 檔案
found_files = []
for filename in os.listdir(folder_path):
    if filename.endswith(".doc") and not filename.endswith(".docx"):
        doc_path = os.path.join(folder_path, filename)
        docx_path = convert_doc_to_docx(doc_path)  # 轉換
        # 轉換後用 python-docx 搜尋（參考前面的方法）
        from docx import Document
        doc = Document(docx_path)
        for para in doc.paragraphs:
            if search_text in para.text:
                found_files.append(filename)
                break

# 輸出結果
if found_files:
    print("找到包含字串的文件:")
    for file in found_files:
        print(file)
else:
    print("沒有找到符合的文件。")
