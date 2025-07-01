import ollama

def chat_with_ollama(model_name):
    print(f"모델: {model_name}")
    print("종료하려면 'quit'를 입력하세요.\n")
    
    conversation_history = []
    
    while True:
        user_input = input("사용자: ")
        
        if user_input.lower() == 'quit':
            break
        
        # 대화 기록에 사용자 메시지 추가
        conversation_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Ollama API 호출 (스트리밍)
        response = ollama.chat(
            model=model_name,
            messages=conversation_history,
            stream=True
        )
        
        print("AI: ", end='', flush=True)
        assistant_response = ""
        for chunk in response:
            content = chunk['message']['content']
            assistant_response += content
            print(content, end='', flush=True)
        print("\n")

        # 대화 기록에 AI 응답 추가
        conversation_history.append({
            'role': 'assistant',
            'content': assistant_response
        })


model = "gemma3:4b"
chat_with_ollama(model_name=model)
