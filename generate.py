from prompt import *
import openai  # for generating embeddings
import os


model = "gpt-4o"
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))


def generate_ess_func(prompts):
    response = client.chat.completions.create(
    model=model,
    temperature=0.5,
    messages=[
        {
            "role": "system",
            "content": prompts
        },
    ],
        max_tokens=300
    )
    content = response.choices[0].message.content
    # 提取 "
    return content


def generate_ess(warning,data,checklist):
    template=PROMPTS["generation_ess"]
    # 使用 format 方法将参数插入模板
    filled_template = template.format(input_warning=warning, input_params=data, input_checklist=checklist)
    ess_steps=generate_ess_func(filled_template)
    return ess_steps
