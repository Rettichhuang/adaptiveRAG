import openai  # for generating embeddings
import os  # for environment variables
from PIL import Image
import base64
import io

model = "gpt-4o"
client = openai.OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY", "sk-a129a97307a046668237e1c5f387fa42"),base_url="https://api.deepseek.com")#DEEPSEEK_API_KEY OPENAI_API_KEY

img_system_prompt = '''
    You are a pilot and you will be provided with an image of a panel in the cabin.It carries aircraft parameters and warning messages.\
    Your role is to recognize and warnings and parameters.then output in the following format:
    warning massages:{warning_massage}
    flight parameters:{parameters}
'''


def analyze_image(img,suffix):
    base64_image=encode_image(img,suffix)
    response = client.chat.completions.create(
    model="deepseek-chat",#gpt-4-turbo "deepseek-chat"
    temperature=0.25,
    messages=[
        {
            "role": "system",
            "content": img_system_prompt
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                },
            ],
        }
    ],
        max_tokens=300
    )
    content = response.choices[0].message.content
    # 提取 "
    # 分割并提取警告信息和飞行参数
    input_list=content.split("warning messages:")[1].split("\n")
    warning_message = next((s.strip('- ').strip() for s in input_list if len(s.strip()) > 1), None)
    flight_parameters = content.split("flight parameters:")[1].strip()
    return warning_message,flight_parameters


def encode_image(image,suffix="png"):
    buffer = io.BytesIO()
    # 将图像以某种格式保存到缓冲区
    if suffix=="jpg":
        image.save(buffer, format="JPEG")  # 确保与实际图像文件的格式匹配
    else:
        image.save(buffer, format="PNG")  # 确保与实际图像文件的格式匹配
    # 获取缓冲区的二进制内容
    binary_data = buffer.getvalue()
    # 关闭缓冲区
    buffer.close()
    return base64.b64encode(binary_data).decode('utf-8')

if __name__=='__main__':
    img_path='data/images/IMG_5583.jpg'
    img = Image.open(img_path)
    content=analyze_image(img)
    print(content)