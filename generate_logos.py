#!/usr/bin/env python3
"""
衡简叙约 Logo 生成脚本
使用隶书字体，无水印版本
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 创建输出目录
output_dir = "品牌LOGO及VI/logo"
os.makedirs(output_dir, exist_ok=True)

# 颜色定义
CHARCOAL = (44, 47, 54)       # 深炭灰 #2C2F36
BLUE = (74, 124, 155)         # 静谧青蓝 #4A7C9B
BLUE_LIGHT = (91, 141, 181)   # 浅青蓝 #5B8DB5
PALE_BLUE = (232, 241, 245)   # 极浅青 #E8F1F5
GRAY = (138, 145, 154)        # 次要灰 #8A919A
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 字体路径
SIMLI_FONT = "C:/Windows/Fonts/SIMLI.TTF"  # 隶书
SIMHEI_FONT = "C:/Windows/Fonts/simhei.ttf"  # 黑体（备用）

def load_font(size):
    """加载字体，失败则使用备用"""
    try:
        return ImageFont.truetype(SIMLI_FONT, size)
    except:
        try:
            return ImageFont.truetype(SIMHEI_FONT, size)
        except:
            return ImageFont.load_default()

def create_logo_v1(size=2048):
    """
    Logo 版本1：对话气泡 + 平衡标尺 + 契约书页
    参考原logo1的设计思路，使用隶书字体
    """
    img = Image.new('RGB', (size, size), WHITE)
    draw = ImageDraw.Draw(img)
    
    # 居中计算
    center_x = size // 2
    center_y = size // 2
    
    # === 图形部分 ===
    # 对话气泡（左侧）
    bubble_w = size // 4
    bubble_h = size // 5
    bubble_x = center_x - bubble_w - size // 20
    bubble_y = center_y - bubble_h // 2 - size // 10
    
    # 绘制对话气泡
    draw.rounded_rectangle(
        [bubble_x, bubble_y, bubble_x + bubble_w, bubble_y + bubble_h],
        radius=bubble_h // 4,
        fill=BLUE,
        outline=WHITE,
        width=3
    )
    # 气泡尾巴
    tail_points = [
        (bubble_x + 20, bubble_y + bubble_h),
        (bubble_x - 20, bubble_y + bubble_h + 30),
        (bubble_x + 40, bubble_y + bubble_h)
    ]
    draw.polygon(tail_points, fill=BLUE)
    
    # 对话点（代表访谈）
    dot_r = size // 80
    for i in range(3):
        draw.ellipse(
            [bubble_x + bubble_w//3 - dot_r, bubble_y + bubble_h//3 + i * dot_r * 3,
             bubble_x + bubble_w//3 + dot_r, bubble_y + bubble_h//3 + i * dot_r * 3 + dot_r*2],
            fill=WHITE
        )
    
    # 平衡标尺（中央）
    scale_w = size // 8
    scale_h = size // 3
    scale_x = center_x - scale_w // 2
    scale_y = center_y - scale_h // 2
    
    # 竖线
    draw.line([(center_x, scale_y), (center_x, scale_y + scale_h)], 
              fill=CHARCOAL, width=size // 40)
    # 横线
    draw.line([(scale_x, scale_y + scale_h//3), (scale_x + scale_w, scale_y + scale_h//3)], 
              fill=CHARCOAL, width=size // 40)
    # 砝码
    weight_r = size // 30
    draw.ellipse([center_x - scale_w//2 - weight_r, scale_y + scale_h//3 - weight_r,
                  center_x - scale_w//2 + weight_r, scale_y + scale_h//3 + weight_r], 
                 fill=BLUE)
    draw.ellipse([center_x + scale_w//2 - weight_r, scale_y + scale_h//3 - weight_r,
                  center_x + scale_w//2 + weight_r, scale_y + scale_h//3 + weight_r], 
                 fill=BLUE)
    # 基座
    base_points = [
        (center_x - size//20, scale_y + scale_h),
        (center_x, scale_y + scale_h + size//15),
        (center_x + size//20, scale_y + scale_h)
    ]
    draw.polygon(base_points, fill=CHARCOAL)
    
    # === 文字部分 ===
    # 中文品牌名（隶书）
    cn_font = load_font(size // 10)  # 较大的字体
    cn_text = "衡简叙约"
    bbox = draw.textbbox((0, 0), cn_text, font=cn_font)
    text_w = bbox[2] - bbox[0]
    text_x = center_x - text_w // 2
    text_y = center_y + size // 4
    
    draw.text((text_x, text_y), cn_text, fill=CHARCOAL, font=cn_font)
    
    # 英文品牌名
    en_font = load_font(size // 25)
    en_text = "HENGSEEN"
    bbox = draw.textbbox((0, 0), en_text, font=en_font)
    text_w = bbox[2] - bbox[0]
    text_x = center_x - text_w // 2
    text_y = text_y + size // 8
    
    draw.text((text_x, text_y), en_text, fill=GRAY, font=en_font)
    
    # Slogan
    slogan_font = load_font(size // 35)
    slogan = "叙清交易事实，衡简商事契约"
    bbox = draw.textbbox((0, 0), slogan, font=slogan_font)
    text_w = bbox[2] - bbox[0]
    text_x = center_x - text_w // 2
    text_y = text_y + size // 15
    
    draw.text((text_x, text_y), slogan, fill=GRAY, font=slogan_font)
    
    return img

def create_logo_v2(size=2048):
    """
    Logo 版本2：圆形平衡设计
    参考原logo2的设计思路，使用隶书字体
    """
    img = Image.new('RGB', (size, size), WHITE)
    draw = ImageDraw.Draw(img)
    
    center_x = size // 2
    center_y = size // 2 - size // 10  # 稍微偏上
    
    # === 图形部分 ===
    # 外圆环
    outer_r = size // 4
    draw.ellipse([center_x - outer_r, center_y - outer_r, 
                  center_x + outer_r, center_y + outer_r],
                 outline=CHARCOAL, width=size // 50)
    
    # 左对话气泡（使用半透明蓝色）
    bubble_r = size // 8
    left_bubble_x = center_x - outer_r // 2
    left_bubble_y = center_y
    # 创建半透明图层
    semi_blue = (*BLUE, 128)  # RGBA with alpha
    left_bubble_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    left_draw = ImageDraw.Draw(left_bubble_img)
    left_draw.rounded_rectangle(
        [left_bubble_x - bubble_r, left_bubble_y - bubble_r//2,
         left_bubble_x + bubble_r, left_bubble_y + bubble_r//2],
        radius=bubble_r//4,
        fill=semi_blue
    )
    img = img.convert('RGBA')
    img.paste(Image.alpha_composite(img, left_bubble_img), (0, 0))
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # 右对话气泡
    right_bubble_x = center_x + outer_r // 2
    right_bubble_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    right_draw = ImageDraw.Draw(right_bubble_img)
    right_draw.rounded_rectangle(
        [right_bubble_x - bubble_r, left_bubble_y - bubble_r//2,
         right_bubble_x + bubble_r, left_bubble_y + bubble_r//2],
        radius=bubble_r//4,
        fill=semi_blue
    )
    img = img.convert('RGBA')
    img.paste(Image.alpha_composite(img, right_bubble_img), (0, 0))
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # 中心平衡圆
    center_r = size // 12
    draw.ellipse([center_x - center_r, center_y - center_r,
                  center_x + center_r, center_y + center_r],
                 fill=BLUE)
    
    # 连接线
    draw.line([(left_bubble_x + bubble_r, center_y), 
               (center_x - center_r, center_y)],
              fill=CHARCOAL, width=size // 60)
    draw.line([(center_x + center_r, center_y),
               (right_bubble_x - bubble_r, center_y)],
              fill=CHARCOAL, width=size // 60)
    
    # === 文字部分 ===
    # 中文品牌名（隶书）
    cn_font = load_font(size // 10)
    cn_text = "衡简叙约"
    bbox = draw.textbbox((0, 0), cn_text, font=cn_font)
    text_w = bbox[2] - bbox[0]
    text_x = center_x - text_w // 2
    text_y = center_y + outer_r + size // 15
    
    draw.text((text_x, text_y), cn_text, fill=CHARCOAL, font=cn_font)
    
    # 英文品牌名
    en_font = load_font(size // 25)
    en_text = "— Hengseen —"
    bbox = draw.textbbox((0, 0), en_text, font=en_font)
    text_w = bbox[2] - bbox[0]
    text_x = center_x - text_w // 2
    text_y = text_y + size // 10
    
    draw.text((text_x, text_y), en_text, fill=GRAY, font=en_font)
    
    return img

def create_logo_v3(size=2048):
    """
    Logo 版本3：简约抽象版
    更简洁的设计，突出核心元素
    """
    img = Image.new('RGB', (size, size), WHITE)
    draw = ImageDraw.Draw(img)
    
    center_x = size // 2
    center_y = size // 2 - size // 8
    
    # === 图形部分 ===
    # 外框
    frame_size = size // 3
    frame_x = center_x - frame_size // 2
    frame_y = center_y - frame_size // 2
    
    draw.rounded_rectangle(
        [frame_x, frame_y, frame_x + frame_size, frame_y + frame_size],
        radius=size // 20,
        outline=CHARCOAL,
        width=size // 40
    )
    
    # 对话气泡（左）
    bubble_size = frame_size // 3
    left_bubble_x = frame_x + frame_size // 6
    left_bubble_y = frame_y + frame_size // 3
    draw.rounded_rectangle(
        [left_bubble_x, left_bubble_y, 
         left_bubble_x + bubble_size, left_bubble_y + bubble_size // 2],
        radius=bubble_size // 6,
        fill=BLUE
    )
    
    # 平衡标尺（右）
    scale_x = left_bubble_x + bubble_size + frame_size // 10
    scale_y = frame_y + frame_size // 3
    scale_h = bubble_size
    draw.line([(scale_x, scale_y), (scale_x, scale_y + scale_h)], 
              fill=CHARCOAL, width=size // 60)
    draw.line([(scale_x - bubble_size//4, scale_y + scale_h//3),
               (scale_x + bubble_size//4, scale_y + scale_h//3)],
              fill=CHARCOAL, width=size // 60)
    # 砝码
    weight_r = size // 50
    draw.ellipse([scale_x - bubble_size//4 - weight_r, scale_y + scale_h//3 - weight_r,
                  scale_x - bubble_size//4 + weight_r, scale_y + scale_h//3 + weight_r],
                 fill=BLUE)
    draw.ellipse([scale_x + bubble_size//4 - weight_r, scale_y + scale_h//3 - weight_r,
                  scale_x + bubble_size//4 + weight_r, scale_y + scale_h//3 + weight_r],
                 fill=BLUE)
    
    # === 文字部分 ===
    cn_font = load_font(size // 12)
    cn_text = "衡简叙约"
    bbox = draw.textbbox((0, 0), cn_text, font=cn_font)
    text_w = bbox[2] - bbox[0]
    text_x = center_x - text_w // 2
    text_y = frame_y + frame_size + size // 15
    
    draw.text((text_x, text_y), cn_text, fill=CHARCOAL, font=cn_font)
    
    en_font = load_font(size // 30)
    en_text = "HENGSEEN"
    bbox = draw.textbbox((0, 0), en_text, font=en_font)
    text_w = bbox[2] - bbox[0]
    text_x = center_x - text_w // 2
    text_y = text_y + size // 12
    
    draw.text((text_x, text_y), en_text, fill=GRAY, font=en_font)
    
    return img

# 生成所有版本
print("正在生成 Logo...")

print("生成版本1...")
logo1 = create_logo_v1()
logo1.save(os.path.join(output_dir, "衡简叙约_logo1_隶书版.png"), "PNG", quality=95)
print(f"  已保存: {os.path.join(output_dir, '衡简叙约_logo1_隶书版.png')}")

print("生成版本2...")
logo2 = create_logo_v2()
logo2.save(os.path.join(output_dir, "衡简叙约_logo2_隶书版.png"), "PNG", quality=95)
print(f"  已保存: {os.path.join(output_dir, '衡简叙约_logo2_隶书版.png')}")

print("生成版本3...")
logo3 = create_logo_v3()
logo3.save(os.path.join(output_dir, "衡简叙约_logo3_隶书版.png"), "PNG", quality=95)
print(f"  已保存: {os.path.join(output_dir, '衡简叙约_logo3_隶书版.png')}")

print("\n完成！所有logo均使用隶书字体，无水印。")
