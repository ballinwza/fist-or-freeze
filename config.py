from dotenv import load_dotenv

load_dotenv()

import os

def get_google_token():
    api_key = os.getenv("GG_TOKEN")
    if not api_key:
        raise ValueError(
            "ไม่พบ GG_TOKEN! โปรดตรวจสอบว่าได้สร้างไฟล์ .env และระบุ GG_TOKEN= แล้วหรือยัง"
    )
    return api_key