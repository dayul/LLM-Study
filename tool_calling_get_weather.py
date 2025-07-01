import json
import random
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY)

# Mock 날씨 데이터
MOCK_WEATHER_DATA = {
    "서울": {"temperature": 15, "condition": "맑음", "humidity": 60},
    "부산": {"temperature": 18, "condition": "흐림", "humidity": 70},
    "대구": {"temperature": 16, "condition": "비", "humidity": 80},
}

def get_weather(city):
    """특정 도시의 날씨 정보를 조회하는 Mock 함수"""
    print(f"get_weather('{city}') 호출됨")
    
    if city in MOCK_WEATHER_DATA:
        return MOCK_WEATHER_DATA[city]
    else:
        # 모르는 도시는 랜덤한 날씨 정보 생성
        conditions = ["맑음", "흐림", "비", "눈", "안개"]
        return {
            "temperature": random.randint(10, 30),
            "condition": random.choice(conditions), 
            "humidity": random.randint(40, 90),
            "note": f"{city}의 상세 정보는 없지만 예상 날씨입니다"
        }

# AI에게 알려줄 Tool 스키마 정의
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "특정 도시의 현재 날씨 정보를 조회합니다",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "날씨를 조회할 도시명"}
                },
                "required": ["city"]
            }
        }
    }
]

# 함수명과 실제 Python 함수를 매핑하는 딕셔너리
functions = {"get_weather": get_weather}

def chat_with_tools(user_message):
    """Tool Calling을 사용한 대화 함수"""
    messages = [{"role": "user", "content": user_message}]
    
    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        messages.append(message.model_dump())
        
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function_result = functions[function_name](**function_args)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(function_result)
                })
            continue
        else:
            return message.content

# 테스트
# 서울의 날씨가 어떻게 되지?
# 대구쪽 날씨가 궁금하네
# 뉴욕의 온도가 궁금해
while True:
    user_input = input("\n사용자: ")
    if user_input.lower() in ['quit', 'exit', '종료']:
        break
    result = chat_with_tools(user_input)
    print(f"AI: {result}")
    print("-" * 40)