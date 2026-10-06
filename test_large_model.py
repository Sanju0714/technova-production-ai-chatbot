from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

start = time.perf_counter()

response = client.chat.completions.create(
    model="nvidia/nemotron-3-super-120b-a12b",
    messages=[
        {
            "role": "user",
            "content": "Where is my order TN1001?"
        }
    ],
    temperature=0,
    max_tokens=256,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    }
)

elapsed = time.perf_counter() - start

print(f"Latency: {elapsed:.2f}s")
print("Answer:", response.choices[0].message.content)