from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
# Depends 的作用，依赖注入：FastAPI 的核心特性之一，允许你声明某个参数（如 db）需要由其他函数（如 get_db）提供。
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session # 表示数据库会话对象，通过这个会话，可以执行数据库操作（如查询、插入、更新等）。

from schemas import TranslationRequestSchema
from typing import List
from utils import translate_text, process_translations

# db related
from database import engine, SessionLocal, get_db
import models 
from models import TranslationRequest, TranslationResult, IndividualTranslations

# 创建数据库中所有定义的表结构
models.Base.metadata.create_all(engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# 指定模板文件存放的目录（通常是项目下的 `templates` 文件夹）
templates = Jinja2Templates(directory="templates")

# 返回一个 HTML 页面 (index.html)
@app.get("/index", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", # 模板文件名（位于 `templates/` 下）
        {"request": request} # 传递给模板的上下文数据
    )
# FastAPI 的 TemplateResponse 要求上下文必须包含 request 对象，用于生成 URL

# 接收 POST 请求
@app.post("/translate")
async def translate(request: TranslationRequestSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    print(request.text)
    print(request.languages)

    # 创建并保存翻译请求到数据库
    request_data = models.TranslationRequest(
        text=request.text,
        languages=request.languages)
    
    db.add(request_data)
    db.commit()
    db.refresh(request_data)

    # print(f"Translation request submitted. ID: {request_data.id}")  # 打印 ID 以确认是否正确生成

    # 添加后台任务处理翻译
    background_tasks.add_task(process_translations, request_data.id, request.text, request.languages)
    # print("request_data: ", request_data)
    return {"payload": request_data}

# 根据 request_id 查询翻译请求
@app.get("/translate/{request_id}")
async def get_translation_status(request_id: int, request: Request, db: Session = Depends(get_db)):
    # 根据 request_id 从 TranslationRequest 表中获取一条记录
    request_obj = db.query(TranslationRequest).filter(TranslationRequest.id == request_id).first() # 执行查询并返回第一条结果
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")
    if request_obj.status == "in progress":
        return {"status": request_obj.status}
    translations = db.query(TranslationResult).filter(TranslationResult.request_id == request_id).all()
    return templates.TemplateResponse(
        "results.html", 
        {"request": request, "translations": translations}
    )