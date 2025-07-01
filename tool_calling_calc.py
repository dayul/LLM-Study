import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY)

# 실제로 호출될 Python 함수들 정의
def add(a, b):
    """두 수를 더하는 실제 함수"""
    print(f"add({a}, {b}) 호출됨")
    return a + b

def multiply(a, b):
    """두 수를 곱하는 실제 함수"""
    print(f"multiply({a}, {b}) 호출됨")
    return a * b

# AI에게 알려줄 Tool 스키마 정의 (JSON Schema 형태)
# AI가 이 정보를 보고 언제, 어떻게 함수를 호출할지 결정함
tools = [
    {
        "type": "function", # Tool 타입은 function
        "function": {
            "name": "add", # 함수명 (실제 Python 함수명과 일치해야 함을 유의)
            "description": "두 숫자를 더합니다", # AI가 함수 용도를 이해할 수 있는 설명 (가장 중요!)
            "parameters": { # 함수 파라미터 스키마 (JSON Schema 형태)
                "type": "object",
                "properties": {
                    "a": {"type": "number"}, # 첫 번째 파라미터 정보
                    "b": {"type": "number"} # 두 번째 파라미터 정보
                },
                "required": ["a", "b"] # 필수 파라미터 지정
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "multiply",
            "description": "두 숫자를 곱합니다",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

# 함수명과 실제 Python 함수를 매핑하는 딕셔너리
# AI가 함수명을 알려주면 실제 함수를 찾아서 실행하기 위함
# (일반적으로는 같은 이름으로 매핑하면 됨)
functions = {"add": add, "multiply": multiply}

def chat_with_tools(user_message):
    """Tool Calling을 사용한 대화 함수"""
    
    # 대화 히스토리를 저장할 메시지 배열 (OpenAI API 형태)
    messages = [{"role": "user", "content": user_message}]
    
    # Tool Calling은 여러 번의 함수 호출이 필요할 수 있으므로 반복문 사용
    while True:
        # OpenAI API 호출 (Tool 정보 포함)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages, # 대화 히스토리 전달달
            tools=tools, # 사용 가능한 Tool 목록 전달 (전달하지 않으면 Tool Calling 자체가 불가)
            tool_choice="auto" # AI가 자동으로 Tool 사용하도록 설정
        )
        
        # AI의 응답 메시지 추출
        message = response.choices[0].message
        # 대화 히스토리에 AI 응답 추가 (다음 API 호출시 컨텍스트로 사용)
        messages.append(message.model_dump())
        
        # AI가 Tool 호출을 결정한 경우
        if message.tool_calls:
            # 각 Tool 호출을 순차적으로 처리 (여러 개일 수 있음)
            for tool_call in message.tool_calls:
                # 호출할 함수명 추출
                function_name = tool_call.function.name
                # 함수 파라미터 추출 (JSON 문자열을 파이썬 객체로 변환)
                function_args = json.loads(tool_call.function.arguments)
                
                # 실제 Python 함수 실행
                function_result = functions[function_name](**function_args)
                
                # Tool 실행 결과를 대화 히스토리에 추가
                # AI가 다음 판단을 할 때 이 결과를 참고함
                messages.append({
                    "role": "tool", # 메시지 역할: tool
                    "tool_call_id": tool_call.id, # Tool 호출 ID (추적용)
                    "content": str(function_result) # 함수 실행 결과
                })
            
            # Tool 호출 후 다시 AI에게 판단 요청 (continue로 while 루프 계속)
            continue
        else:
            # Tool 호출이 없으면 최종 답변이므로 결과 반환
            return message.content

# Tool Calling 테스트
while True:
    # 질문 예시:
    # 4 + 3은?
    # 5 * 6 =
    # 3에다가 5를 더하면?
    # (5 + 3) * 2는? <= 2번의 Tool Calling이 이루어 짐
    # (((5 * 3) + 2) * 4) = ? <= 3번의 Tool Calling이 이루어 짐 (모종의 이유로 에러도 자주 남)
    user_input = input("\n사용자: ")
    
    if user_input.lower() in ['quit', 'exit', '종료']:
        print("프로그램을 종료합니다.")
        break
        
    result = chat_with_tools(user_input)
    print(f"AI: {result}")
    print("-" * 40)