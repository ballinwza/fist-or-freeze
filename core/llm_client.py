import json
import os
# from ollama import AsyncClient
from models.quiz import QuestionModel
from config import get_google_token
from google import genai
from google.genai import types

class LLMClient:
    # TODO: ต้องคอยเปลี่ยน model ไม่มีเงินจ่าย T-T , gemini-3.6-flash/gemini-3.5-flash/ gemini-3.5-flash-lite
    def __init__(self, model_name: str = "gemini-3.5-flash-lite"):
        # self.client = AsyncClient()
        
        api_key = get_google_token()
        
        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)
        
    async def generate_question(self, category: str, difficulty: str) -> QuestionModel:
        prompt = f"""
คุณคือระบบสร้างคำถามในเกมทายปัญหา โดยใช้ภาษาไทยที่อ่านง่ายแบบเป็นกันเอง
ห้ามสร้างคำถามซ้ำเด็ดขาด
คำถามต้องมีความหลากหลาย
สร้างคำถามโดยเกี่ยวข้องกับหัวข้อ {category}
กำหนดความยากระดับความยากของคำถาม {difficulty}
จำนวน 1 ข้อ ตอบกลับมาเป็น JSON เท่านั้นในโครงสร้างนี้:
{{
  "question": "คำถาม",
  "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "correct_option": "A",
  "explanation": "คำอธิบายเฉลยแบบสั้น ห้ามเกิน 1 บรรทัด" 
}}

INSTRUTOR
คุณต้องตอบคำถามโดยใช้ลักษณะนิสัยเหล่านี้
-เป็นเพศชาย
-ขี้เล่น
-พูดเป็นกันเอง แต่สุภาพอ่อนน้อม
    """
        
        # TODO: Ollama style
        # response = await self.client.chat(
        #     model=self.model_name,
        #     messages=[{'role': 'user', 'content': prompt}],
        #     format=QuestionModel.model_json_schema()
        # )
        
        # data = json.loads(response['message']['content'])
        
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=QuestionModel,
                temperature=0.7,
            ),
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")
        
        content = response.text

        data = json.loads(content)
        return QuestionModel(**data)