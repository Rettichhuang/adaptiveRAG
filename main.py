import os.path

from image_process import analyze_image
from rag import retrieval
from generate import generate_ess
import pandas as pd
from ast import literal_eval
from PIL import Image
import numpy as np
from eval import *
from text_process import *
import re
import shutil
import os

# Optional: load data from saved file
data_path = r'merged0104.csv'
df = pd.read_csv(data_path, encoding='ISO-8859-1')
df["embedding_emergency"] = df.embedding_emergency.apply(literal_eval).apply(np.array)
df["embedding_actions"] = df.embedding_actions.apply(literal_eval).apply(np.array)

EVAL=True
SAVE_PATH='result.csv'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    table = pd.DataFrame()
    # 目标文件夹路径
    img_root = "data/images"
    i=0
    img_ls=os.listdir(img_root)
    for img_name in img_ls:
            img_path=os.path.join(img_root,img_name)
            #shutil.copy(img_path, destination_folder)
            img = Image.open(img_path)
            suffix=img_path[-3:]
            #perception
            warning, params = analyze_image(img, suffix)
            #retrieval
            checklist,token_num=retrieval(df,warning)
            ess_steps=generate_ess(warning,params,checklist)
            if EVAL:#evaluate
                score=llm_eval(ess_steps,checklist,warning)#gpt4_eval
                # 正则表达式提取每段文字中的最近数字
                numbers = re.findall(r': (\d+)', score)
                # 转换为整数，并仅输出前四个数字
                score_array = [int(num) for num in numbers[:4]]
                # 将分数转换为整数并存储在数组中
                score_rag = llm_eval(checklist, checklist, warning)
                rag_numbers = re.findall(r': (\d+)', score_rag)

                checklist=remove_punctuation(checklist)
                ess_steps = remove_punctuation(ess_steps)
                # entropy_eval
                entropy_before = calculate_entropy(text=checklist)
                entropy_after=calculate_entropy(text=ess_steps)
                #save
                df1 = pd.DataFrame(
                    {"img_name":img_name,"ess_steps": ess_steps,"score_text":score, "score_num":  " ".join(numbers[:4]), "entropy_before": entropy_before, \
                     "entropy_after": entropy_after,"token_num":token_num,"retrieval_score": " ".join(rag_numbers[:4])}, index=[i])
                i+=1
                table = pd.concat([table, df1], ignore_index=True)
            if i%10==0:
                table.to_csv(SAVE_PATH, index=False)
    # 最后一次保存
    if i % 10 != 0:
        print(f"已添加 {i} 条数据，保存中...")
        table.to_csv(SAVE_PATH, index=False)
        print("数据已保存。")













