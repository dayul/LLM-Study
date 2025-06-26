import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {API_KEY}"
}

user_input = "고양이에 대한 재미있는 이야기를 한 문단으로 써주세요"

# temperature 값 리스트
temperatures = [0.0, 0.7, 1.5, 2.0]

# 각가의 temperature 값에 대해서 같은 질문 요청
for temp in temperatures:
    data = {
        "model": "gpt-4.1",
        "messages": [{"role": "user", "content": user_input}],
        "temperature": temp,
        "max_tokens": 200
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()
    ai_response = result['choices'][0]['message']['content']

    print(f"\n\n\ntemperature 값: {temp}")
    print(ai_response)
    print("-" * 50)