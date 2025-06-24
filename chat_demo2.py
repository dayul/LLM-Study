import requests
import json
from dotenv import load_dotenv
import os

# .env 파일 활성화
load_dotenv()

API_KEY = os.getenv('API_KEY')

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

print("대화를 시작합니다. '/quit'을 입력하면 종료됩니다.")

while True:
    user_input = input("You: ")

    if user_input == '/quit':
        break

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 1000
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    result = response.json()
    response = result['choices'][0]['message']['content']
    
    print(f"AI: {response}")