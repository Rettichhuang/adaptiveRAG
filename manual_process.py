from PIL import Image
import io
import base64
import fitz  # PyMuPDF
import pdfplumber
import os
import re


def extract_text_blocks(pdf_path):
    # 打开 PDF 文件
    pdf_document = fitz.open(pdf_path)

    # 存储文本块和行块信息
    text_blocks = []
    line_blocks = []
    all_text = ''
    Indent=''
    # 遍历 PDF 中的每一页
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)

        # 获取文本块和行块信息
        blocks = page.get_text("dict")["blocks"]
        # 合并具有相同字体的行
        current_paragraph = ""
        last_font = None
        start_indent=False
        last_sentence_x = 25.1760
        has_indent=False
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for sp in l["spans"]:
                        text = sp['text']
                        font = sp["font"]
                        x=sp["bbox"][0]
                        if text=='\ue113' or text=='\ue114':
                            current_paragraph += '\n' + text
                            start_indent=True
                            continue
                        '''   
                        if start_indent is True:
                            if x-last_sentence_x >0.01:
                                Indent +='  '
                                current_paragraph += '\n' + Indent+text
                            elif x-last_sentence_x <-0.01:
                                Indent =Indent[2:]
                                current_paragraph += '\n' + Indent+text
                            else:
                                current_paragraph += '\n' + Indent + text
                            last_sentence_x=x
                        else:
                        '''
                        current_paragraph += '\n' + text

                # 添加最后的段落
        pattern = r".*?\[QRH\] ALL ENG FAIL"
        replacement = "[QRH] ALL ENG FAIL"
        result = re.sub(pattern, replacement, current_paragraph, count=1, flags=re.DOTALL)
        if current_paragraph:
            all_text+=(result)


    # 关闭 PDF 文件
    pdf_document.close()

    return all_text


if __name__=='__main__':# 示例用法
    folder_path ='data/ALL_ENG_FAIL'
    text_blocks=''
    for filename in os.listdir(folder_path):
        pdf_path = os.path.join(folder_path, filename)
        text_blocks += extract_text_blocks(pdf_path)
    print(text_blocks)
    output_file_path = "ALL ENG FAIL.txt"
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(text_blocks)

