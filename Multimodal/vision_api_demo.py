from openai import OpenAI
from image_util import resize_image, encode_image
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY)

def analyze_image(image_path, prompt, max_width=800):
    """Vision API로 이미지 분석 (자동 리사이즈 포함)"""
    
    print(f"📸 이미지 분석 시작: {image_path}")
    
    # 이미지를 리사이즈한 후 base64로 인코딩
    base64_image = encode_image(image_path, max_width)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Vision 지원 모델
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=16384
    )
    
    return response.choices[0].message.content

### 이미지 내용 설명
# result = analyze_image(image_path="sample_image_describe.jpg", prompt="이미지의 내용을 분석하고 묘사된 오브젝트, 색상, 화풍, 이미지의 의미가 포함되도록 최대한 자세하게 설명해주세요.", max_width=800)
# print(result)
# result = analyze_image(image_path="sample_image_describe_2.jpg", prompt="이미지의 내용을 분석하고 묘사된 오브젝트, 색상, 화풍, 이미지의 의미가 포함되도록 최대한 자세하게 설명해주세요.", max_width=800)
# print(result)

### 차트, 그래프 분석
# result = analyze_image(image_path="sample_image_explain_chart.jpg", prompt="이미지에 포함된 차트, 그래프의 내용을 분석하여 설명해주세요.", max_width=800)
# print(result)
# result = analyze_image(image_path="sample_image_explain_bar_chart.png", prompt="이미지에 포함된 차트, 그래프의 내용을 분석하여 설명해주세요.", max_width=800)
# print(result)

### 이미지 OCR (텍스트 추출)
result = analyze_image(image_path="Multimodal/img/sample_image_ocr.png", prompt="이미지에 포함된 텍스트를 추출하여 출력해주세요.", max_width=800)
print(result)