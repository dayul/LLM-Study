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
        # structured output을 지원하는 gpt-4o 모델 사용 (다른 모델에서는 json_schema가 지원되지 않음)
        model="gpt-4o",
        # confidence 속성도 포함하도록 시스템 프롬프트 수정
        messages=[
            {
                "role": "system", 
                "content": """다음 텍스트의 감정을 분석해주세요.
                
반드시 JSON 형태로 응답하며, 다음 구조를 정확히 따라주세요:
- sentiment: "positive", "negative", "neutral" 중 하나
- confidence: 0.0~1.0 사이의 숫자 (얼마나 확신하는지)

다른 필드는 추가하지 마세요."""
            },
            {"role": "user", "content": text}
        ],
        # JSON Schema를 사용해서 구체적인 구조 지정
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "sentiment_analysis",
                "strict": True,
                # schema 필드를 통해서 JSON 구조를 명확히 정의
                "schema": {
                    "type": "object",
                    # 필요한 속성들의 타입과 값의 제한 조건을 정의
                    "properties": {
                        "sentiment": {
                            "type": "string",
                            "enum": ["positive", "negative", "neutral"]
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0
                        }
                    },
                    "required": ["sentiment", "confidence"],
                    "additionalProperties": False
                }
            }
        }
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
    confidence = data['confidence']
    
    print(f"감정: {sentiment}")
    print(f"신뢰도: {confidence}")
    print("-" * 50)