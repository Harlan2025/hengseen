"""
衡简叙约 Hengseen - FastAPI 主入口（测试模式）
"""
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# 加载配置
from config import settings, is_test_mode, get_ai_service
from database import supabase

# 导入路由
from routers import auth, projects, interview, outline, contract, export, payment, custom_content, experts, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    print(f"\n{'='*60}")
    print(f"衡简叙约 Hengseen 启动")
    print(f"版本: {settings.APP_VERSION}")
    print(f"模式: {'测试' if is_test_mode() else '生产'}")
    print(f"{'='*60}\n")
    
    # 初始化测试数据库
    if is_test_mode():
        from test_db import db
        db.reset_all()
        print("✅ 测试数据库已初始化\n")
    
    yield
    
    # 关闭时清理
    print("\n🛑 衡简叙约已停止")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="衡简叙约 - AI访谈式合同生成系统",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(interview.router, prefix="/api/v1")
app.include_router(outline.router, prefix="/api/v1")
app.include_router(contract.router, prefix="/api/v1")
app.include_router(export.router, prefix="/api/v1")
app.include_router(payment.router, prefix="/api/v1")
app.include_router(custom_content.router, prefix="/api/v1")
app.include_router(experts.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "mode": "test" if is_test_mode() else "production",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "mode": "test" if is_test_mode() else "production"
    }


@app.get("/api/v1/test/reset")
async def reset_test_db():
    """重置测试数据库"""
    from test_db import db
    db.reset_all()
    return {"status": "ok", "message": "测试数据库已重置"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
