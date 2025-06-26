import base64
from PIL import Image
import io

def resize_image(image_path, max_width=800):
    """이미지를 지정된 최대 너비로 리사이즈"""
    with Image.open(image_path) as img:
        # RGB로 변환 (JPEG 저장을 위해)
        if img.mode in ('RGBA', 'P', 'L'):
            img = img.convert('RGB')
            
        # 원본 크기
        original_width, original_height = img.size
        print(f"원본 크기: {original_width}x{original_height}")
        
        # 리사이즈가 필요한지 확인
        if original_width <= max_width:
            print("리사이즈 불필요")
            return img.copy() # 복사본 반환
        
        # 비율 유지하면서 리사이즈
        ratio = max_width / original_width
        new_height = int(original_height * ratio)
        
        resized_img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        print(f"리사이즈 후: {max_width}x{new_height}")
        
        return resized_img.copy() # 복사본 반환

def encode_image(image_path, max_width=800):
    """이미지를 리사이즈한 후 base64로 인코딩"""
    
    # 이미지 리사이즈
    resized_img = resize_image(image_path, max_width)
    
    # 메모리에서 JPEG로 변환
    img_byte_arr = io.BytesIO()
    resized_img.save(img_byte_arr, format='JPEG', quality=85)
    img_byte_arr = img_byte_arr.getvalue()
    
    # base64 인코딩
    return base64.b64encode(img_byte_arr).decode('utf-8')