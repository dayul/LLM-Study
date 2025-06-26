from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY)

# 분석할 리뷰
product_review = """
                    상품명: 애플 에어팟 프로 2세대

                    배송도 빠르고 포장도 완벽했어요! 
                    노이즈 캔슬링이 정말 대단합니다. 지하철에서도 음악이 완전 깨끗하게 들려요.
                    음질도 1세대보다 훨씬 좋아졌고, 배터리도 오래 갑니다.
                    다만 가격이 좀 비싸긴 해요. 그래도 애플 제품이니까 그런가 봅니다.
                    케이스도 예쁘고 무선충전도 잘 돼요.
                    추천합니다! 살만한 값어치는 하는 것 같아요.
                  """


def analyze_reviews(review_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """상품 리뷰를 분석해서 다음 JSON 형태로 응답해주세요.

                반드시 다음 구조를 정확히 따라주세요:
                - predicted_rating: 리뷰 총점
                - sentiment: "positive", "negative", "neutral" 중 하나
                - pros: 장점 배열 (2개)
                - cons: 단점 배열 (2개)
                - main_features: 언급된 기능 배열 (2개)
                - recommendation: 최종적인 상품 추천 여부

                다른 필드는 추가하지 마세요.""",
            },
            {
                "role": "user",
                "content": f"다음 상품 리뷰를 분석해주세요:\n\n{review_text}",
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "reviews_analysis",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "predicted_rating": {"type": "string"},
                        "sentiment": {
                            "type": "string",
                            "enum": ["positive", "negative", "neutral"],
                        },
                        "pros": {
                            "type": "array",
                            "items": {"type": "string"},
                            "items": {"type": "string"},
                        },
                        "cons": {
                            "type": "array",
                            "items": {"type": "string"},
                            "items": {"type": "string"},
                        },
                        "main_features": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "recommendation": {"type": "boolean"},
                    },
                    "required": [
                        "predicted_rating",
                        "sentiment",
                        "pros",
                        "cons",
                        "main_features",
                        "recommendation",
                    ],
                    "additionalProperties": False,
                },
            },
        },
    )

    return response.choices[0].message.content


# 리뷰 분석 실행
print("리뷰 분석 중...")
result = analyze_reviews(product_review)

# JSON 파싱해서 활용
import json
from pprint import pprint

data = json.loads(result)

print("\n=== JSON 구조 확인 ===")
pprint(data)

print("\n=== 분석 결과 요약 ===")
print(f"리뷰 총점: {data['predicted_rating']}")
print(f"감정: {data['sentiment']}")
print(f"장점: ")
for i, pros in enumerate(data["pros"], 1):
    print(f"{i}. {pros}")

print(f"단점: ")
for i, cons in enumerate(data["cons"], 1):
    print(f"{i}. {cons}")

print("\n주요 사실들:")
for i, feat in enumerate(data["main_features"], 1):
    print(f"{i}. {feat}")
print(f"상품추천 여부: {data['recommendation']}")