from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
client = OpenAI(api_key = API_KEY)

messages = []
print("대화를 시작합니다. '/quit'을 입력하면 종료됩니다.")

while True:
    user_input = input("You: ")
    if user_input == '/quit':
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        stream=True # SSE를 이용한 Streaming 응답 활성화
    )

    # 응답이 chunk 단위로 스트리밍되므로
    for chunk in response:
        content = chunk.choices[0].delta.content
        # 일부 응답 chunk를 매번 출력
        if content:
            print(content, end='', flush=True)
    print() # 줄바꿈 추가