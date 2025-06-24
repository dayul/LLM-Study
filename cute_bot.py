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

print("귀여운 냥봇과 대화를 시작합니다. '/quit'으로 종료")

while True:
  user_input = input("You: ")
  if user_input == '/quit':
      break
  
  data = {
      "model": "gpt-4.1",
      "messages": [
          {"role": "system", "content": "당신은 세상에서 가장 귀여운 고양이 AI입니다. 모든 문장을 '~다냥', '~했다냥', '~이다냥' 등으로 끝내야 합니다. 매우 애교스럽고 귀여운 말투를 사용하고, 가끔 '냥냥', '야옹' 같은 고양이 소리도 넣으세요. 항상 밝고 긍정적이며 사용자를 도와주려고 노력하는 착한 고양이입니다."},
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
  
  print(f"냥봇: {ai_response}")