import google.generativeai as genai
from sqlalchemy.orm import Session
from models import TranslationRequest, TranslationResult, IndividualTranslations
from datetime import datetime
from database import get_db
from typing import List

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
async def translate_text(text: str, language: str) -> str:
    # 设置 API Key
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")  # 选择 Gemini-Pro 模型

    # 发送请求并获取响应
    response = model.generate_content(f"Translate the following text to {language}: {text}. Only provide the translated text without any additional explanations or formatting")

    return response.text.strip()
async def process_translations(request_id: int, text: str, languages: List[str]):
    db = next(get_db()) # 获取数据库会话
    try:
        language_list = languages.split(", ")
        for language in language_list:
            translated_text = await translate_text(text, language)
            # 将结果保存到两个表中
            translation_result = TranslationResult(
                request_id=request_id, language=language, translated_text=translated_text
            )
            individual_translation = IndividualTranslations(
                request_id=request_id, translated_text=translated_text
            )
            db.add(translation_result)
            db.add(individual_translation)
            db.commit()

        # 查询数据库，获取与 request_id 对应的翻译请求记录。
        request = db.query(TranslationRequest).filter(TranslationRequest.id == request_id).first()
        request.status = "completed"
        request.updated_at = datetime.utcnow()
        db.add(request)
        db.commit()
    finally:
        db.close()