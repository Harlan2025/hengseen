#!/usr/bin/env python
"""安装依赖脚本"""
import subprocess
import sys

packages = [
    "python-jose",
    "fastapi", 
    "uvicorn",
    "httpx",
    "pydantic-settings",
    "supabase",
    "python-docx",
    "markdown",
    "qrcode",
    "Pillow"
]

print("正在安装依赖...")
for pkg in packages:
    print(f"安装 {pkg}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])
    print(f"✓ {pkg} 安装完成")

print("\n所有依赖安装完成!")
