import requests
from dotenv import load_dotenv
import os

# .env 파일 활성화
load_dotenv()

API_KEY = os.getenv('API_KEY')

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

# 요청 데이터
data = {
    "model": "gpt-3.5-turbo-instruct",  # 유일하게 남은 completion 모델
    "max_tokens": 1000,
    "temperature": 0.7,
}
# data["prompt"] = "파리는 프랑스의 "
# data["prompt"] = "셰익스피어는 영국의 "
data["prompt"] = "1 + 1 = "

# API 호출
response = requests.post(
    "https://api.openai.com/v1/completions",  # 구형 엔드포인트nai.com/v1/chat/completions",
    headers=headers,
    json=data,
)

result = response.json()
completion_text = result["choices"][0]["text"]
print(f"응답:\n{completion_text.strip()}")
