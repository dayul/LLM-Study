from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

client = OpenAI(api_key=API_KEY)

# 분석할 텍스트들
texts = [
    "이 제품 정말 최고예요! 강력 추천합니다.",
    "배송이 너무 늦고 품질도 별로네요. 실망입니다.",
    "그냥 평범한 것 같아요."
]

def analyze_sentiment(text):
    response = client.chat.completions.create(
        model="gpt-4.1",
        # 시스템 프롬프트를 통해서 응답할 JSON 구조를 설명
        messages=[
            {
                "role": "system",
                "content": """다음 텍스트의 감정을 분석해주세요.
                
                반드시 JSON 형태로 응답하며, 다음 구조를 정확히 따라주세요:
                - sentiment: "positive", "negative", "neutral" 중 하나

                다른 필드는 추가하지 마세요."""
            },
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"} # JSON 출력 강제
    )
    
    return response.choices[0].message.content

# 각 텍스트의 감정 분석
for i, text in enumerate(texts, 1):
    print(f"분석 텍스트: {text}")
    
    result = analyze_sentiment(text)
    print(f"결과:\n{result}")
    
    # JSON 문자열을 파싱해서 파이썬 딕셔너리로 변환하여 활용 가능
    import json
    data = json.loads(result)
    sentiment = data['sentiment']
    
    print(f"감정: {sentiment}")   