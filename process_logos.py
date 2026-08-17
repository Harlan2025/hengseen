#!/usr/bin/env python3
"""
衡简叙约 Logo 处理脚本
保留原图案，去掉水印，文字改用隶书
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 输入输出路径
input_dir = "品牌LOGO及VI/logo"
output_dir = "品牌LOGO及VI/logo"

# 颜色定义（匹配原图）
CHARCOAL = (44, 47, 54)       # 深炭灰
BLUE = (0, 139, 139)          # 青蓝色（原图使用）
BLUE_LIGHT = (120, 180, 180)  # 浅青色
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)        # 灰色文字

# 字体路径
SIMLI_FONT = "C:/Windows/Fonts/SIMLI.TTF"  # 隶书
SIMHEI_FONT = "C:/Windows/Fonts/simhei.ttf"  # 黑体备用

def load_font(size):
    """加载字体"""
    try:
        return ImageFont.truetype(SIMLI_FONT, size)
    except:
        try:
            return ImageFont.truetype(SIMHEI_FONT, size)
        except:
            return ImageFont.load_default()

def process_logo1():
    """处理logo1：保留左侧竖条+右侧文件图标设计"""
    img = Image.open(os.path.join(input_dir, "衡简叙约logo1.png"))
    width, height = img.size
    
    # 创建新图像（白色背景）
    new_img = Image.new('RGB', (width, height), WHITE)
    draw = ImageDraw.Draw(new_img)
    
    # === 保留原图图形部分（复制上方区域）===
    # 图形部分高度约为整体的60%
    graphic_height = int(height * 0.55)
    graphic_area = img.crop((0, 0, width, graphic_height))
    new_img.paste(graphic_area, (0, 0))
    
    # === 用隶书重新绘制文字 ===
    # 中文品牌名
    cn_font = load_font(int(width * 0.08))  # 较大字体
    cn_text = "衡简叙约"
    
    # 计算文字位置（居中）
    bbox = draw.textbbox((0, 0), cn_text, font=cn_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = (width - text_w) // 2
    text_y = graphic_height + int(height * 0.05)
    
    draw.text((text_x, text_y), cn_text, fill=CHARCOAL, font=cn_font)
    
    # 英文品牌名
    en_font = load_font(int(width * 0.03))
    en_text = "HENGSEEN"
    bbox = draw.textbbox((0, 0), en_text, font=en_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = text_y + int(height * 0.08)
    
    draw.text((text_x, text_y), en_text, fill=GRAY, font=en_font)
    
    # Slogan
    slogan_font = load_font(int(width * 0.025))
    slogan = "叙清交易事实，衡简商事契约"
    bbox = draw.textbbox((0, 0), slogan, font=slogan_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = text_y + int(height * 0.06)
    
    draw.text((text_x, text_y), slogan, fill=GRAY, font=slogan_font)
    
    # 保存
    output_path = os.path.join(output_dir, "衡简叙约_logo1_隶书版.png")
    new_img.save(output_path, "PNG", quality=95)
    print(f"已保存: {output_path}")
    return output_path

def process_logo2():
    """处理logo2：保留对话气泡+天平文件设计"""
    img = Image.open(os.path.join(input_dir, "衡简叙约logo2.png"))
    width, height = img.size
    
    # 创建新图像
    new_img = Image.new('RGB', (width, height), WHITE)
    draw = ImageDraw.Draw(new_img)
    
    # 图形部分高度约为整体的65%
    graphic_height = int(height * 0.65)
    graphic_area = img.crop((0, 0, width, graphic_height))
    new_img.paste(graphic_area, (0, 0))
    
    # === 用隶书重新绘制文字 ===
    # 中文品牌名
    cn_font = load_font(int(width * 0.09))  # 较大字体
    cn_text = "衡简叙约"
    
    bbox = draw.textbbox((0, 0), cn_text, font=cn_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = (width - text_w) // 2
    text_y = graphic_height + int(height * 0.03)
    
    draw.text((text_x, text_y), cn_text, fill=CHARCOAL, font=cn_font)
    
    # 英文品牌名
    en_font = load_font(int(width * 0.035))
    en_text = "— Hengseen —"
    bbox = draw.textbbox((0, 0), en_text, font=en_font)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = text_y + int(height * 0.06)
    
    draw.text((text_x, text_y), en_text, fill=GRAY, font=en_font)
    
    # 保存
    output_path = os.path.join(output_dir, "衡简叙约_logo2_隶书版.png")
    new_img.save(output_path, "PNG", quality=95)
    print(f"已保存: {output_path}")
    return output_path

def create_svg_from_logo1():
    """创建logo1的SVG版本"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="600" viewBox="0 0 800 600" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景 -->
  <rect width="800" height="600" fill="#FFFFFF"/>
  
  <!-- 图形部分 - 参考原图设计 -->
  <g transform="translate(100, 80)">
    <!-- 左侧黑色竖条结构 -->
    <rect x="0" y="20" width="40" height="160" rx="8" fill="#2C2F36"/>
    
    <!-- 左侧声波/信号弧线 -->
    <path d="M50 60 Q70 100 50 140" stroke="#78B4B4" stroke-width="3" fill="none" stroke-linecap="round"/>
    <path d="M60 50 Q85 100 60 150" stroke="#78B4B4" stroke-width="3" fill="none" stroke-linecap="round"/>
    <path d="M70 40 Q100 100 70 160" stroke="#78B4B4" stroke-width="3" fill="none" stroke-linecap="round"/>
    
    <!-- 中间连接横线 -->
    <line x1="40" y1="100" x2="200" y2="100" stroke="#4A7C9B" stroke-width="4"/>
    
    <!-- 右侧青蓝色文件图标 -->
    <rect x="200" y="40" width="80" height="120" rx="4" fill="#4A7C9B" opacity="0.8"/>
    <rect x="200" y="40" width="80" height="120" rx="4" stroke="#4A7C9B" stroke-width="2" fill="none"/>
    <!-- 文件线条 -->
    <line x1="215" y1="60" x2="265" y2="60" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
    <line x1="215" y1="80" x2="265" y2="80" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
    <line x1="215" y1="100" x2="265" y2="100" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
    <line x1="215" y1="120" x2="250" y2="120" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
  </g>
  
  <!-- 中文品牌名 - 隶书风格 -->
  <text x="400" y="320" font-family="'SIMLI', 'LiShu', serif" font-size="56" font-weight="normal" 
        fill="#2C2F36" text-anchor="middle" letter-spacing="0.1em">衡简叙约</text>
  
  <!-- 英文品牌名 -->
  <text x="400" y="380" font-family="Arial, sans-serif" font-size="20" 
        fill="#8A919A" text-anchor="middle" letter-spacing="0.2em">HENGSEEN</text>
  
  <!-- Slogan -->
  <text x="400" y="420" font-family="'Noto Sans SC', 'Microsoft YaHei', sans-serif" font-size="16" 
        fill="#8A919A" text-anchor="middle">叙清交易事实，衡简商事契约</text>
</svg>'''
    
    svg_path = os.path.join(output_dir, "衡简叙约_logo1.svg")
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"已保存: {svg_path}")
    return svg_path

def create_svg_from_logo2():
    """创建logo2的SVG版本"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="800" viewBox="0 0 600 800" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景 -->
  <rect width="600" height="800" fill="#FFFFFF"/>
  
  <!-- 图形部分 - 对话气泡 + 天平文件组合 -->
  <g transform="translate(100, 50)">
    <!-- 对话气泡外框 -->
    <path d="M100 0 H400 C411 0 420 9 420 20 V180 C420 191 411 200 400 200 H350 L300 250 L250 200 H100 C89 200 80 191 80 180 V20 C80 9 89 0 100 0 Z" 
          fill="#F7F8FA" stroke="#2C2F36" stroke-width="3"/>
    
    <!-- 内部圆形背景 -->
    <circle cx="250" cy="100" r="60" fill="#2C2F36"/>
    
    <!-- 文件图标（左） -->
    <rect x="190" y="70" width="40" height="50" rx="2" fill="#FFFFFF"/>
    <line x1="198" y1="82" x2="222" y2="82" stroke="#4A7C9B" stroke-width="2"/>
    <line x1="198" y1="92" x2="222" y2="92" stroke="#4A7C9B" stroke-width="2"/>
    <line x1="198" y1="102" x2="222" y2="102" stroke="#4A7C9B" stroke-width="2"/>
    
    <!-- 天平图标（右） -->
    <line x1="280" y1="60" x2="280" y2="140" stroke="#FFFFFF" stroke-width="3"/>
    <line x1="260" y1="75" x2="300" y2="75" stroke="#FFFFFF" stroke-width="3"/>
    <path d="M260 75 L250 95 H270 Z" fill="#4A7C9B"/>
    <path d="M300 75 L310 95 H290 Z" fill="#4A7C9B"/>
    
    <!-- 文件与天平的连接线 -->
    <line x1="230" y1="100" x2="260" y2="100" stroke="#FFFFFF" stroke-width="2"/>
  </g>
  
  <!-- 中文品牌名 - 隶书风格 -->
  <text x="300" y="420" font-family="'SIMLI', 'LiShu', serif" font-size="64" font-weight="normal" 
        fill="#2C2F36" text-anchor="middle" letter-spacing="0.15em">衡简叙约</text>
  
  <!-- 英文品牌名 -->
  <text x="300" y="480" font-family="Arial, sans-serif" font-size="24" 
        fill="#8A919A" text-anchor="middle" letter-spacing="0.1em">— Hengseen —</text>
</svg>'''
    
    svg_path = os.path.join(output_dir, "衡简叙约_logo2.svg")
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"已保存: {svg_path}")
    return svg_path

if __name__ == "__main__":
    print("正在处理 Logo...")
    print()
    
    print("处理 logo1...")
    process_logo1()
    
    print()
    print("处理 logo2...")
    process_logo2()
    
    print()
    print("生成 SVG 版本...")
    create_svg_from_logo1()
    create_svg_from_logo2()
    
    print()
    print("完成！所有logo均使用隶书字体，无水印。")
