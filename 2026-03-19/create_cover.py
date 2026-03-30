from PIL import Image, ImageDraw, ImageFont
import os

# 创建小红书封面图片 (3:4比例，900x1200)
width, height = 900, 1200
img = Image.new('RGB', (width, height), color='#f093fb')

# 创建渐变背景
draw = ImageDraw.Draw(img)
for y in range(height):
    # 从粉色渐变到红色
    r = int(240 - (240 - 245) * y / height)
    g = int(147 - (147 - 87) * y / height)
    b = int(251 - (251 - 108) * y / height)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 尝试加载字体
try:
    # Windows字体路径
    title_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 72)
    subtitle_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 42)
    tag_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 28)
    footer_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 20)
except:
    # 使用默认字体
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    tag_font = ImageFont.load_default()
    footer_font = ImageFont.load_default()

# 绘制图标
draw.text((width//2 - 80, 200), "🤖", font=title_font, fill="white")
draw.text((width//2 + 10, 200), "🎨", font=title_font, fill="white")

# 绘制标题
title = "AI绘画工具"
bbox = draw.textbbox((0, 0), title, font=title_font)
title_width = bbox[2] - bbox[0]
draw.text(((width - title_width) // 2, 350), title, font=title_font, fill="white")

# 绘制副标题
subtitle = "2024最全测评对比"
bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = bbox[2] - bbox[0]
draw.text(((width - subtitle_width) // 2, 460), subtitle, font=subtitle_font, fill=(255, 255, 255, 230))

# 绘制标签
tags = ["Midjourney", "Stable Diffusion", "DALL·E 3", "文心一格"]
tag_y = 600
for i, tag in enumerate(tags):
    bbox = draw.textbbox((0, 0), tag, font=tag_font)
    tag_width = bbox[2] - bbox[0]
    tag_x = (width - tag_width) // 2
    
    # 绘制标签背景（圆角矩形效果）
    padding = 20
    draw.rounded_rectangle([tag_x - padding, tag_y - 10, tag_x + tag_width + padding, tag_y + 40], 
                           radius=20, fill=(255, 255, 255, 80))
    draw.text((tag_x, tag_y), tag, font=tag_font, fill="white")
    tag_y += 70

# 绘制底部
draw.text((width//2 - 100, height - 100), "小红书 @AI探索者", font=footer_font, fill=(255, 255, 255, 180))

# 保存图片
output_path = "C:/Users/29210/.openclaw/workspace/xiaohongshu_cover.png"
img.save(output_path, "PNG")
print(f"封面图片已保存到: {output_path}")
