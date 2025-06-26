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

user_input = "파이썬으로 간단한 계산기 프로그램을 작성하는 방법을 자세히 설명해주세요."

# max_tokens 값 리스트
# 1) 10의 경우 극단적으로 토큰 길이 제약이 심하므로, 응답이 잘림
# 2) 1000의 경우 적당한 수준의 답변이 제공됨
# 3) 32768은 최대 토큰 길이로, 이론적으로 가장 긴 답변을 받을 수 있으나, 그 정도로 긴 답변이 필요 없으므로, 적당한 수준의 답변이 제공됨
max_tokens_list = [10, 1000, 32768]

# 각각의 max_tokens 값에 대해서 같은 질문 요청
for tokens in max_tokens_list:
    data = {
        "model": "gpt-4.1",
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7,
        "max_tokens": tokens
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()
    ai_response = result['choices'][0]['message']['content']

    print(f"\n\n\nmax_tokens 길이: {tokens}")
    print(f"실제 응답 길이: 약 {len(ai_response)}자")
    print(ai_response)
    print("-" * 80)