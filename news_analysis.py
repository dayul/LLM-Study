from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

client = OpenAI(api_key=API_KEY)

# 분석할 뉴스 기사
news_article = """
치솟는 전셋값에…서울 아파트 재계약 절반이 갱신권 사용

서울 아파트 전셋값 상승세가 지속되면서 올해 2분기 계약갱신요구권을 사용한 임차인의 비중이 절반에 달했다. 전문가는 당분간 계약갱신요구권을 행사하는 임차인이 늘 것이라고 내다봤다.
24일 부동산R114가 국토교통부 실거래가시스템에 신고된 서울 아파트 전월세 계약(전월세신고제가 도입된 2021년 6월 이후분)을 분석한 자료를 보면, 올해 2분기 서울 아파트 전월세 갱신계약 가운데 갱신권을 사용한 비중은 49.7%로 절반에 육박했다. 이는 2022년 3분기 60.4% 이후 최대 비중이다. 주택임대차보호법에 따라 임차인은 1회에 한해 계약갱신을 청구할 수 있으며, 이 경우 임대료 증액률은 5%로 제한된다.
전월세 계약갱신권 사용 비중은 전셋값 하락 여파로 지난해 2분기 27.9%까지 감소했다가 3분기 30.3%로 늘어났고 4분기 42.0%를 기록했다. 올해 1분기 48.1%, 2분기 49.7%로 증가세가 지속되고 있다.
임차인의 계약갱신요구권 사용 증가의 원인으로 전셋값 상승이 꼽힌다. 전셋값이 오르면서 임차인들이 기존 계약을 유지하려는 움직임이 늘고 있는 것이다. 한국부동산원에 따르면 6월 둘째주 서울 아파트 전셋값은 전주보다 0.07% 올랐다. 2월 첫째 주를 기점으로 서울 아파트 전셋값은 꾸준히 상승 중이다. 전세 가격 지수는 2023년 1월 이후 최고치다.
전세 매물 감소도 계약갱신요구권을 유도하는 요인 중 하나다. 부동산 빅데이터 업체 아실에 따르면 지난 4월 기준 서울 아파트 전세 매물은 2만7550개로 집계됐다. 지난 3월 전달(2만 8110개) 대비 560개가 줄었으며 전년(3만 578건) 대비 3028개가 감소한 것이다.
반면 전세 수요는 계속 증가하면서 전세난에 대한 우려가 커지고 있다. KB부동산에 따르면 지난 5월 서울 전세수급지수는 139.5로 전월(136.4)보다 3.1 상승했다. 전세수급지수는 0~200 범위에서 100을 넘기면 수요가 공급보다 많은 시장임을 의미한다.
전문가는 전셋값 상승과 매물 부족이 맞물리면서 당분간 이런 흐름이 이어질 것으로 내다봤다. 심형석 우대빵연구소 소장(미국 IAU 교수)은 “전셋값이 계속 오르고 있고 매물도 없다”며 “전세 시장의 핵심 변수는 입주 물량인데, 입주가 적은 상황에서는 계약갱신요구권을 행사하는 임차인이 늘어날 수밖에 없다”고 말했다.
송승현 도시와 경제 대표는 “아파트 매매 가격이 비싸다 보니 매매하지 못하고 전세로 머무르려는 임차인이 늘고 있다”며 “매매 가격과 더불어 전셋값도 오르면서 계약갱신요구권을 행사하는 사례도 많아질 것”이라고 언급했다.
"""

def analyze_news(article_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": """뉴스 기사를 분석해서 다음 JSON 형태로 응답해주세요.

반드시 다음 구조를 정확히 따라주세요:
- title: 기사의 핵심 제목 (간결하게)
- summary: 기사 요약 (2-3문장으로)
- sentiment: "positive", "negative", "neutral" 중 하나
- category: "정치", "경제", "사회", "국제", "스포츠", "연예", "기술" 중 하나
- key_facts: 중요한 사실들의 배열 (3-5개 정도)

다른 필드는 추가하지 마세요."""
            },
            {"role": "user", "content": f"다음 뉴스 기사를 분석해주세요:\n\n{article_text}"}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "news_analysis",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string"
                        },
                        "summary": {
                            "type": "string"
                        },
                        "sentiment": {
                            "type": "string",
                            "enum": ["positive", "negative", "neutral"]
                        },
                        "category": {
                            "type": "string",
                            "enum": ["정치", "경제", "사회", "국제", "스포츠", "연예", "기술"]
                        },
                        "key_facts": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["title", "summary", "sentiment", "category", "key_facts"],
                    "additionalProperties": False
                }
            }
        }
    )
    
    return response.choices[0].message.content

# 뉴스 기사 분석 실행
print("뉴스 기사 분석 중...")
result = analyze_news(news_article)

# JSON 파싱해서 활용
import json
from pprint import pprint
data = json.loads(result)

print("\n=== JSON 구조 확인 ===")
pprint(data)

print("\n=== 분석 결과 요약 ===")
print(f"제목: {data['title']}")
print(f"카테고리: {data['category']}")
print(f"감정: {data['sentiment']}")
print(f"요약: {data['summary']}")
print("\n주요 사실들:")
for i, fact in enumerate(data['key_facts'], 1):
    print(f"{i}. {fact}")