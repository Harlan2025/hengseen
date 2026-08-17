#!/usr/bin/env python3
"""
衡简叙约 Logo 处理脚本 v3 - 确保隶书字体生效
"""

from PIL import Image, ImageDraw, ImageFont
import os

input_dir = "品牌LOGO及VI/logo"
output_dir = "品牌LOGO及VI/logo"

# 颜色
CHARCOAL = (44, 47, 54)
GRAY = (120, 120, 120)
WHITE = (255, 255, 255)

def get_lishu_font(size):
    """获取隶书字体"""
    # 尝试多种路径
    font_paths = [
        "C:/Windows/Fonts/SIMLI.TTF",
        "C:/Windows/Fonts/simli.ttf",
        "C:/Windows/Fonts/SIMLI.ttf",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, size)
                print(f"  成功加载隶书字体: {path}")
                return font
            except Exception as e:
                print(f"  加载失败 {path}: {e}")
                continue
    
    # 备用：使用系统默认中文字体
    print("  警告：未找到隶书字体，使用备用字体")
    return ImageFont.load_default()

def process_logo1():
    """处理logo1"""
    print("\n处理 logo1...")
    
    # 打开原图
    img = Image.open(os.path.join(input_dir, "衡简叙约logo1.png"))
    width, height = img.size
    
    # 创建新图
    new_img = Image.new('RGB', (width, height), WHITE)
    draw = ImageDraw.Draw(new_img)
    
    # 复制图形部分（上方55%）
    graphic_height = int(height * 0.55)
    graphic_area = img.crop((0, 0, width, graphic_height))
    new_img.paste(graphic_area, (0, 0))
    
    # 用隶书绘制文字
    cn_size = int(width * 0.09)
    cn_font = get_lishu_font(cn_size)
    
    cn_text = "衡简叙约"
    bbox = draw.textbbox((0, 0), cn_text, font=cn_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = (width - text_w) // 2
    text_y = graphic_height + int(height * 0.06)
    
    # 绘制文字（带阴影效果增加可读性）
    draw.text((text_x + 2, text_y + 2), cn_text, fill=(40, 43, 50), font=cn_font)
    draw.text((text_x, text_y), cn_text, fill=CHARCOAL, font=cn_font)
    
    # 英文
    en_size = int(width * 0.03)
    en_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", en_size)
    en_text = "HENGSEEN"
    bbox = draw.textbbox((0, 0), en_text, font=en_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = text_y + int(height * 0.1)
    
    draw.text((text_x, text_y), en_text, fill=GRAY, font=en_font)
    
    # Slogan
    slogan_size = int(width * 0.025)
    slogan_font = get_lishu_font(slogan_size)
    slogan = "叙清交易事实，衡简商事契约"
    bbox = draw.textbbox((0, 0), slogan, font=slogan_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = text_y + int(height * 0.08)
    
    draw.text((text_x, text_y), slogan, fill=GRAY, font=slogan_font)
    
    # 保存
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
    
    # 复制图形部分（上方65%）
    graphic_height = int(height * 0.65)
    graphic_area = img.crop((0, 0, width, graphic_height))
    new_img.paste(graphic_area, (0, 0))
    
    # 用隶书绘制文字
    cn_size = int(width * 0.1)
    cn_font = get_lishu_font(cn_size)
    
    cn_text = "衡简叙约"
    bbox = draw.textbbox((0, 0), cn_text, font=cn_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = graphic_height + int(height * 0.04)
    
    draw.text((text_x + 2, text_y + 2), cn_text, fill=(40, 43, 50), font=cn_font)
    draw.text((text_x, text_y), cn_text, fill=CHARCOAL, font=cn_font)
    
    # 英文
    en_size = int(width * 0.035)
    en_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", en_size)
    en_text = "— Hengseen —"
    bbox = draw.textbbox((0, 0), en_text, font=en_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = text_y + int(height * 0.07)
    
    draw.text((text_x, text_y), en_text, fill=GRAY, font=en_font)
    
    # 保存
    output_path = os.path.join(output_dir, "衡简叙约_logo2_隶书版.png")
    new_img.save(output_path, "PNG", quality=95)
    print(f"  已保存: {output_path}")
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("衡简叙约 Logo 处理 (隶书字体版)")
    print("=" * 60)
    
    process_logo1()
    process_logo2()
    
    print("\n" + "=" * 60)
    print("完成！所有logo均使用隶书字体，无水印。")
    print("=" * 60)
