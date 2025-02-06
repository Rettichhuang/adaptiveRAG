import openai  # for generating embeddings
import os


model = "gpt-4o"
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))
