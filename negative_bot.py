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

print("부정적인 봇과 대화를 시작합니다. '/quit'으로 종료")

while True:
  user_input = input("You: ")
  if user_input == '/quit':
      break
  
  data = {
      "model": "gpt-4.1",
      "messages": [
          {"role": "system", "content": "당신은 우주에서 가장 부정적이고 비관적인 인공지능 챗봇입니다. 사용자가 무엇을 요청하든 절대 도움을 주지 않고, 항상 '할 수 없다', '불가능하다', '의미없다'라고 대답합니다. 모든 일에 대해 부정적으로 생각하고 절망적인 톤으로 말합니다."},
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
  ai_response = result['choices'][0]['message']['content']
  
  print(f"부정봇: {ai_response}")