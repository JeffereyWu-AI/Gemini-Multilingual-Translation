# Making sure the data coming from the frontend is valid
from pydantic import BaseModel

class TranslationRequestSchema(BaseModel):
    text: str
    languages: str

    class Config:
        schema_extra = {
            "example": {
                "text": "Hello, world!",
                "languages": "english, german, russian"
            }
        }
        # schema_extra：为 FastAPI 的自动文档（如 Swagger UI）提供示例数据。
        # 效果：在 API 文档中会显示这个示例，帮助开发者理解如何构造请求体。