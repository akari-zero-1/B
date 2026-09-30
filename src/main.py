import sys
import asyncio

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.routes import chat_router, products_router, link_parser_router, alerts_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Hệ thống Backend Multi-Agent thông minh (Hỗ trợ Groq / OpenRouter & LangSmith Tracing)",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI tại http://localhost:8000/docs
    redoc_url="/redoc"    # Redoc UI tại http://localhost:8000/redoc
)

# Cấu hình CORS để Frontend G (React/Next.js tại port 3000) có thể gọi trực tiếp
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router API
app.include_router(chat_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(link_parser_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "ShopAI Agent Backend is running!",
        "docs_url": "http://localhost:8000/docs",
        "llm_provider": settings.LLM_PROVIDER,
        "langsmith_tracing": settings.LANGCHAIN_TRACING_V2.lower() in ("true", "1") and bool(settings.LANGCHAIN_API_KEY)
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "provider": settings.LLM_PROVIDER,
        "langsmith_project": settings.LANGCHAIN_PROJECT,
        "langsmith_tracing_enabled": settings.LANGCHAIN_TRACING_V2.lower() in ("true", "1")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=True)
