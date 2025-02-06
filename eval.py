import math
from collections import Counter
import openai
from config import *
# OpenAI API 密钥配置
import re

# 提示文本
eval_prompt = """
You are an aviation expert tasked with evaluating the quality of flight operation instructions for an emergeny scenario. Please assess the generated steps using the following criteria:

1. Accuracy: Does the instruction match the warning scenario? (0 means poor, 1 means partially match the scenario and 2 means fully matches the scenario.)
2. Comprehensiveness:Does the generated step include detailed explanations?(0 means no, 1 means yes)
3. Hallucination:  Are the steps consistent with the given checklist? (0 means steps are correct and stem from the checklist, even if partially.1 means steps are not stem from the checklist.
4. Conciseness:Are the steps necessary and direct for the warning?(0: Clear and direct steps. No additional judgment required. \
1: Only Steps provided but require the pilot to interpret flight parameters.2: Includes detailed explanations along with steps.)

Provide a score for each criterion and a brief justification.

Standard Checklist:{checklist}
Warning:{warning_message}
Generated Steps:{steps}

Evaluation:
"""

def calculate_entropy(text):
    # 统计每个字符的频率
    freq = Counter(text)
    total_chars = len(text)

    # 计算熵
    entropy = -sum((count / total_chars) * math.log2(count / total_chars) for count in freq.values())
    return entropy


def eval_Acc(result,check_list):
    pre=0

    return pre


#用户友好性：检查长度和术语
def llm_eval(steps,checklist,warning):
    content=eval_prompt.format(steps=steps, checklist=checklist,warning_message=warning)
    # 调用 LLM

    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {
            "role": "system",
            "content": content
            },
        ],


        max_tokens=300
    )
    evaluation = response.choices[0].message.content
    # 提取 "
    return evaluation



if __name__=='__main__':
    # 示例文本

    score=r"""1. Accuracy: 1 - The instruction does not match the standard checklist for the specific scenario of "AUTO FLT FAC 2 FAULT." The generated steps incorrectly address "FAC 1 + 2" instead of focusing on "FAC 2" only.
            2. Comprehensiveness: 1 - The generated steps do not provide any reference or detailed explanations specific to the "AUTO FLT FAC 2 FAULT" scenario. It lacks context and necessary information.
            3. Hallucination: 1 - The response is incorrect and does not stem from the retrieved documents. The steps provided are not applicable to the specific fault mentioned.
            4. Conciseness: 0 - The generated steps do not provide any additional unnecessary steps for the current warning. However, they are incorrect and not concise in addressing the specific fault.
            Justification: The generated steps are inaccurate and do not align with the standard checklist for the specific fault scenario. They lack comprehensiveness and context, and the response appears to be a hallucination as it does not derive from the correct documentation. The steps are not concise as they do not address the specific fault correctly."""
    numbers = re.findall(r': (\d+)', score)

    # 转换为整数，并仅输出前四个数字
    score_array = [int(num) for num in numbers[:4]]
    exit()
    text = "ENG 1 OIL LO PR"
    entropy = calculate_entropy(text)
    print(f"文本的熵为: {entropy}")