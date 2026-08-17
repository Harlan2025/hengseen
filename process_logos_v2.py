#!/usr/bin/env python3
"""
衡简叙约 Logo 处理脚本 v2
保留原图案，去掉水印，文字改用隶书
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# 输入输出路径
input_dir = "品牌LOGO及VI/logo"
output_dir = "品牌LOGO及VI/logo"

# 颜色定义
CHARCOAL = (44, 47, 54)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

def load_chinese_font(size, font_name="SIMLI"):
    """加载中文字体，优先隶书"""
    font_paths = [
        f"C:/Windows/Fonts/{font_name}.TTF",
        f"C:/Windows/Fonts/{font_name}.ttf",
        "C:/Windows/Fonts/simli.ttf",
        "C:/Windows/Fonts/SIMLI.TTF",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, size)
                print(f"  使用字体: {path}")
                return font
            except Exception as e:
                print(f"  加载失败 {path}: {e}")
                continue
    
    # 尝试系统字体
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", size)
        print(f"  使用备用字体: simhei.ttf")
        return font
    except:
        return ImageFont.load_default()

def process_logo1():
    """处理logo1"""
    print("\n处理 logo1...")
    img = Image.open(os.path.join(input_dir, "衡简叙约logo1.png"))
    width, height = img.size
    
    # 创建新图像
    new_img = Image.new('RGB', (width, height), WHITE)
    draw = ImageDraw.Draw(new_img)
    
    # 复制原图图形部分（去除下方文字区域）
    graphic_height = int(height * 0.55)
    graphic_area = img.crop((0, 0, width, graphic_height))
    new_img.paste(graphic_area, (0, 0))
    
    # 用隶书绘制文字
    font_size = int(width * 0.08)
    cn_font = load_chinese_font(font_size, "SIMLI")
    
    cn_text = "衡简叙约"
    bbox = draw.textbbox((0, 0), cn_text, font=cn_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = graphic_height + int(height * 0.05)
    
    draw.text((text_x, text_y), cn_text, fill=CHARCOAL, font=cn_font)
    
    # 英文
    en_font = load_chinese_font(int(width * 0.03), "Arial")
    en_text = "HENGSEEN"
    bbox = draw.textbbox((0, 0), en_text, font=en_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = text_y + int(height * 0.08)
    
    draw.text((text_x, text_y), en_text, fill=GRAY, font=en_font)
    
    # Slogan
    slogan_font = load_chinese_font(int(width * 0.025), "SIMLI")
    slogan = "叙清交易事实，衡简商事契约"
    bbox = draw.textbbox((0, 0), slogan, font=slogan_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = text_y + int(height * 0.06)
    
    draw.text((text_x, text_y), slogan, fill=GRAY, font=slogan_font)
    
    output_path = os.path.join(output_dir, "衡简叙约_logo1_隶书版.png")
    new_img.save(output_path, "PNG", quality=95)
    print(f"  已保存: {output_path}")
    return output_path

def process_logo2():
    """处理logo2"""
    print("\n处理 logo2...")
    img = Image.open(os.path.join(input_dir, "衡简叙约logo2.png"))
    width, height = img.size
    
    new_img = Image.new('RGB', (width, height), WHITE)
    draw = ImageDraw.Draw(new_img)
    
    # 复制原图图形部分
    graphic_height = int(height * 0.65)
    graphic_area = img.crop((0, 0, width, graphic_height))
    new_img.paste(graphic_area, (0, 0))
    
    # 用隶书绘制文字
    font_size = int(width * 0.09)
    cn_font = load_chinese_font(font_size, "SIMLI")
    
    cn_text = "衡简叙约"
    bbox = draw.textbbox((0, 0), cn_text, font=cn_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = graphic_height + int(height * 0.03)
    
    draw.text((text_x, text_y), cn_text, fill=CHARCOAL, font=cn_font)
    
    # 英文
    en_font = load_chinese_font(int(width * 0.035), "Arial")
    en_text = "— Hengseen —"
    bbox = draw.textbbox((0, 0), en_text, font=en_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = text_y + int(height * 0.06)
    
    draw.text((text_x, text_y), en_text, fill=GRAY, font=en_font)
    
    output_path = os.path.join(output_dir, "衡简叙约_logo2_隶书版.png")
    new_img.save(output_path, "PNG", quality=95)
    print(f"  已保存: {output_path}")
    return output_path

if __name__ == "__main__":
    print("=" * 50)
    print("衡简叙约 Logo 处理 (隶书字体版)")
    print("=" * 50)
    
    process_logo1()
    process_logo2()
    
    print("\n完成！")
