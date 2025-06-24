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

# messages 키를 통해 전달한 리스트의 구조 살펴보기
content = "안녕하세요!"
# content = "당신은 누구인가요?"
data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": content}
    ],
    "max_tokens": 1000
}

response = requests.post(
    "https://api.openai.com/v1/chat/completions", # 달라진 엔드포인트 확인 (채팅 API)
    headers=headers,
    json=data
)

result = response.json()
completion_text = result['choices'][0]['message']['content'] # 답변 JSON 데이터의 구조가 조금 달라졌음을 유의
print(f"응답:\n{completion_text.strip()}")