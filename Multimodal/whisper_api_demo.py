from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY)

def transcribe_audio(audio_file_path):
    """음성 파일을 텍스트로 변환하는 함수"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            # Whisper API를 사용하여 음성을 텍스트로 변환
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ko" # 한국어 설정 (생략 가능, 자동 감지됨)
            )
            return transcript.text
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def translate_audio(audio_file_path):
    """음성 파일을 영어로 번역하는 함수"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            # Whisper API를 사용하여 음성을 영어로 번역
            translation = client.audio.translations.create(
                model="whisper-1",
                file=audio_file
            )
            return translation.text
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

# 사용 예시
audio_file = "./audio/news.mp3"

# 음성을 텍스트로 변환
print("음성 인식 중...")
transcription = transcribe_audio(audio_file)
if transcription:
    print(f"인식된 텍스트: {transcription}")

# 음성을 영어로 번역
print("\n음성 번역 중...")
translation = translate_audio(audio_file)
if translation:
    print(f"영어 번역: {translation}")