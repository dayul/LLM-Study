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

# 대화 기록을 저장할 리스트 추가
messages = []

print("대화를 시작합니다. '/quit'을 입력하면 종료됩니다.")
while True:
   user_input = input("You: ")
   if user_input == '/quit':
       break
   
   print("이전 대화기록\n", messages, "\n")

   # 사용자 메시지를 대화 기록에 추가
   messages.append({"role": "user", "content": user_input})
   
   data = {
       "model": "gpt-4.1",
       "messages": messages, # 전체 대화 기록 전송
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
   
   # AI 응답을 대화 기록에 추가하여 대화 내용이 유지되도록 함 
   # (role은 assistant로 설정)
   messages.append({"role": "assistant", "content": response})