import pandas as pd  # for DataFrames to store article sections and embeddings
from ast import literal_eval
import numpy as np
import openai  # for generating embeddings
import os  # for environment variables
from sklearn.metrics.pairwise import cosine_similarity
import tiktoken
import re
import time


model="gpt-4o"
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))


def count_tokens_in_message(message: str) -> int:
    # 加载 GPT-4 Turbo 模型的编码器
    encoding = tiktoken.encoding_for_model("gpt-4-turbo")
    # 将消息编码为 tokens
    tokens = encoding.encode(message)
    # 返回 token 的数量
    return len(tokens)

def get_embeddings(text):
    embeddings = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        encoding_format="float"
    )
    return embeddings.data[0].embedding


def search_content(df, input_text, top_k, obj_name='embedding_emergency'):
    embedded_value = get_embeddings(input_text)
    if obj_name == 'embedding_actions':
        df["similarity"] = df.embedding_actions.apply(
            lambda x: cosine_similarity(np.array(x).reshape(1, -1),
                                        np.array(embedded_value).reshape(1, -1)))  # embedding_emergency
    else:
        df["similarity"] = df.embedding_emergency.apply(
            lambda x: cosine_similarity(np.array(x).reshape(1, -1),
                                        np.array(embedded_value).reshape(1, -1)))  # embedding_emergency
    res = df.sort_values('similarity', ascending=False).head(top_k)
    return res


def get_similarity(row):
    similarity_score = row['similarity']
    if isinstance(similarity_score, np.ndarray):
        similarity_score = similarity_score[0][0]
    return similarity_score


def find_last_number(sentence):
    # Use regex to find all numbers in the sentence
    numbers = re.findall(r'\d+', sentence)

    # Check if there are any numbers found
    if numbers:
        # Return the last number in the list
        return numbers[-1]
    else:
        return None


def cal_token(prompt_str,model_name):
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(prompt_str))
    return num_tokens


def generate_output(input_prompt, similar_content, threshold=0.99, retrieval_type='RSG'):
    n = 0
    token_num=0
    if similar_content.iloc[0]['similarity'] > threshold:
        content = similar_content.iloc[0]['actions']
        emergency = similar_content.iloc[0]['emergency']
    # Adding more matching content if the similarity is above threshold
    else:
        emergency = ""
        for i, row in similar_content.iterrows():
            emergency += f"\n\n{n + 1}:{row['emergency']}"
            n = n + 1
        prompt1 = (f"Analyze each operational title below {emergency} ,\ "
                   f" then identify the one that most closely matches the warning scene {input_prompt} ."
                   f"Finally,return the reason and corresponding serial number,for example 1")
        start_time = time.time()
        completion1 = client.chat.completions.create(
            model=model,
            temperature=1,
            messages=[

                {
                    "role": "user",
                    "content": prompt1
                }
            ]
        )
        id = completion1.choices[0].message.content[-1]
        if not id.isdigit():
            id = find_last_number(completion1.choices[0].message.content)
        content = similar_content.iloc[int(id) - 1]['actions']
        token_num=cal_token(prompt1,model)
    return content,token_num


def format_string(input_string):
    # 去除字符串两端的空白字符并按换行符分割字符串
    lines = input_string.strip().split('\n')

    # 遍历每一行并去除两端的空白字符
    formatted_lines = [line.strip() for line in lines]

    return formatted_lines


def extract_brace_content(text):
    # 使用正则表达式提取花括号中的内容
    pattern = re.compile(r'\{([^}]*)\}')
    matches = pattern.findall(text)
    return matches


def contains_when_or_if(input_string):
    # Convert the string to uppercase to ensure case-insensitive search
    input_string_upper = input_string.upper()

    # Check if 'WHEN' or 'IF' is in the string
    if 'WHEN' in input_string_upper or 'IF' in input_string_upper:
        return True
    else:
        return False


def retrieval(df,exs):
    # Running the RAG pipeline on each example
    matching_content3 = search_content(df, exs, 3)
    check_list,token_num = generate_output(exs, matching_content3)

    return check_list,token_num








