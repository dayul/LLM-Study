from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY)

def generate_image(prompt, size="1024x1024", quality="standard", n=1):
    """DALL-E를 사용하여 이미지 생성하는 함수"""
    try:
        response = client.images.generate(
            model="dall-e-3", # dall-e-2 또는 dall-e-3
            prompt=prompt,
            size=size, # "1024x1024", "1792x1024", "1024x1792"
            quality=quality, # "standard" 또는 "hd"
            n=n # 생성할 이미지 개수 (dall-e-3은 1개만 가능)
        )
        
        # 생성된 이미지 URL 반환
        image_url = response.data[0].url
        print(f"이미지가 생성되었습니다: {image_url}")
        return image_url
        
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def download_and_save_image(image_url, filename="generated_image.png"):
    """생성된 이미지를 다운로드하고 저장하는 함수"""
    try:
        # 이미지 다운로드
        response = requests.get(image_url)
        response.raise_for_status()
        
        # PIL로 이미지 열기
        image = Image.open(BytesIO(response.content))
        
        # 이미지 저장
        image.save(filename)
        print(f"이미지가 저장되었습니다: {filename}")
        
        return filename
        
    except Exception as e:
        print(f"이미지 저장 중 오류 발생: {e}")
        return None

# 이미지 생성 프롬프트 모음과 파일명 쌍
prompts_and_filenames = [
    ("고양이가 우주복을 입고 달 위에서 춤추는 모습, 디지털 아트 스타일", "cat_on_moon.png"),
    ("마법사가 거대한 도서관에서 빛나는 책을 읽고 있는 모습, 판타지 아트", "wizard_library.png"),
    ("벚꽃이 만개한 호수 위에 떠있는 작은 섬, 일본 전통 건축물, 수채화 스타일", "cherry_blossom_island.png"),
    ("네온사인이 빛나는 사이버펑크 도시의 밤거리를 걷는 로봇, 디지털 아트", "cyberpunk_robot.png"),
    ("파스텔 색상의 구름 위에서 무지개를 타고 있는 유니콘, 귀여운 만화 스타일", "unicorn_rainbow.png"),
    ("음표들이 춤추며 색깔로 변하는 추상적인 음악의 시각화, 현대 미술", "music_visualization.png"),
    ("1950년대 아메리칸 다이너에서 밀크셰이크를 마시는 사람들, 빈티지 포스터 스타일", "retro_diner.png"),
    ("황금빛 크루아상과 커피가 있는 프랑스 카페의 아침 풍경, 따뜻한 조명", "french_cafe.png")
]

# 인덱스 변경해서 사용 (0~7)
index = 2
prompt, filename = prompts_and_filenames[index]

print(f"선택된 프롬프트: {prompt}")
print("이미지 생성 중...")
image_url = generate_image(prompt)

if image_url:
    print("이미지 다운로드 중...")
    saved_file = download_and_save_image(image_url, filename)
    
    if saved_file:
        print(f"완료! {saved_file}에서 이미지를 확인하세요.")