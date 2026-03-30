"""
生成小红书视频配图
使用 PIL 创建精美的封面和关键画面
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 创建输出目录
output_dir = "D:/AI_Files/xiaohongshu_video_assets"
os.makedirs(output_dir, exist_ok=True)

# 颜色配置
COLORS = {
    'bg_dark': (20, 25, 35),
    'bg_gradient_top': (45, 55, 80),
    'bg_gradient_bottom': (20, 25, 35),
    'accent_blue': (100, 180, 255),
    'accent_orange': (255, 150, 80),
    'accent_green': (80, 200, 120),
    'text_white': (255, 255, 255),
    'text_gray': (180, 190, 210),
}

def create_gradient_background(width, height, color_top, color_bottom):
    """创建渐变背景"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def create_cover_image():
    """创建视频封面"""
    width, height = 1080, 1440  # 小红书竖版比例 3:4
    
    # 创建渐变背景
    img = create_gradient_background(width, height, 
                                     COLORS['bg_gradient_top'], 
                                     COLORS['bg_gradient_bottom'])
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 80)
        font_subtitle = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 48)
        font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 36)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = font_title
        font_small = font_title
    
    # 绘制装饰元素 - 科技感圆环
    center_x, center_y = width // 2, height // 3
    
    # 外圈发光效果
    for i in range(5):
        alpha = 100 - i * 15
        color = (100, 180, 255, alpha)
        draw.ellipse([center_x - 200 - i*10, center_y - 200 - i*10, 
                     center_x + 200 + i*10, center_y + 200 + i*10], 
                    outline=(100, 180, 255), width=2)
    
    # 主圆环
    draw.ellipse([center_x - 180, center_y - 180, center_x + 180, center_y + 180], 
                outline=COLORS['accent_blue'], width=4)
    draw.ellipse([center_x - 150, center_y - 150, center_x + 150, center_y + 150], 
                outline=COLORS['accent_orange'], width=3)
    
    # AI 图标文字
    draw.text((center_x, center_y), "🤖", font=font_title, anchor="mm", 
             fill=COLORS['text_white'])
    
    # 主标题
    title_y = height // 2 + 50
    draw.text((center_x, title_y), "2024 AI发展现状", 
             font=font_title, anchor="mm", fill=COLORS['text_white'])
    
    # 副标题背景
    subtitle_bg = [center_x - 350, title_y + 100, center_x + 350, title_y + 180]
    draw_rounded_rect(draw, subtitle_bg, 20, (255, 150, 80, 100))
    
    # 副标题
    draw.text((center_x, title_y + 140), "普通人如何抓住AI红利", 
             font=font_subtitle, anchor="mm", fill=COLORS['text_white'])
    
    # 底部要点
    points = ["✓ 大模型百花齐放", "✓ AI重塑各行业", "✓ 3招抓住红利"]
    point_y = height - 250
    for i, point in enumerate(points):
        draw.text((center_x, point_y + i * 60), point, 
                 font=font_small, anchor="mm", fill=COLORS['text_gray'])
    
    # 保存
    img.save(f"{output_dir}/01_cover.png")
    print("封面图已生成")
    return img

def create_title_card(title, subtitle, filename):
    """创建标题卡片"""
    width, height = 1080, 608  # 16:9 横版，适合视频转竖版
    
    img = create_gradient_background(width, height,
                                     COLORS['bg_gradient_top'],
                                     COLORS['bg_gradient_bottom'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 64)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 36)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title
    
    center_x, center_y = width // 2, height // 2
    
    # 装饰线
    draw.line([(center_x - 200, center_y - 80), (center_x + 200, center_y - 80)],
             fill=COLORS['accent_blue'], width=4)
    
    # 标题
    draw.text((center_x, center_y - 20), title, 
             font=font_title, anchor="mm", fill=COLORS['text_white'])
    
    # 副标题
    draw.text((center_x, center_y + 60), subtitle, 
             font=font_sub, anchor="mm", fill=COLORS['text_gray'])
    
    # 装饰线
    draw.line([(center_x - 200, center_y + 120), (center_x + 200, center_y + 120)],
             fill=COLORS['accent_orange'], width=4)
    
    img.save(f"{output_dir}/{filename}")
    print(f"{filename} 已生成")

def create_model_comparison():
    """创建AI模型对比图"""
    width, height = 1080, 1440
    
    img = create_gradient_background(width, height,
                                     COLORS['bg_gradient_top'],
                                     COLORS['bg_gradient_bottom'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 56)
        font_text = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 40)
    except:
        font_title = ImageFont.load_default()
        font_text = font_title
    
    center_x = width // 2
    
    # 标题
    draw.text((center_x, 100), "🚀 大模型百花齐放", 
             font=font_title, anchor="mm", fill=COLORS['text_white'])
    
    # 模型卡片
    models = [
        ("GPT-4o", "多模态王者\n能看能听能说", COLORS['accent_green']),
        ("Claude 3.5", "程序员福音\n代码能力超强", COLORS['accent_orange']),
        ("Gemini 1.5", "百万级上下文\n整本书都能读", COLORS['accent_blue']),
        ("国产模型", "文心、通义、Kimi\n紧追不舍", (200, 100, 255)),
    ]
    
    card_y = 250
    card_height = 220
    for i, (name, desc, color) in enumerate(models):
        # 卡片背景
        card_rect = [80, card_y + i * (card_height + 30), width - 80, 
                    card_y + i * (card_height + 30) + card_height]
        draw_rounded_rect(draw, card_rect, 20, (40, 50, 70), color, 3)
        
        # 模型名
        draw.text((card_rect[0] + 40, card_rect[1] + 40), name,
                 font=font_title, fill=color)
        
        # 描述
        for j, line in enumerate(desc.split('\n')):
            draw.text((card_rect[0] + 40, card_rect[1] + 110 + j * 50), line,
                     font=font_text, fill=COLORS['text_gray'])
    
    # 金句
    quote_y = height - 150
    draw.text((center_x, quote_y), "💬 以前觉得AI是科幻，现在觉得AI是日常",
             font=font_text, anchor="mm", fill=COLORS['accent_orange'])
    
    img.save(f"{output_dir}/03_model_comparison.png")
    print("模型对比图已生成")

def create_industry_grid():
    """创建行业改变网格图"""
    width, height = 1080, 1440
    
    img = create_gradient_background(width, height,
                                     COLORS['bg_gradient_top'],
                                     COLORS['bg_gradient_bottom'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 52)
        font_text = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 32)
    except:
        font_title = ImageFont.load_default()
        font_text = font_title
    
    center_x = width // 2
    
    # 标题
    draw.text((center_x, 100), "🌍 AI正在改变这些行业", 
             font=font_title, anchor="mm", fill=COLORS['text_white'])
    
    # 行业网格
    industries = [
        ("🎨", "设计", "人人能做图"),
        ("📝", "写作", "效率10倍"),
        ("💻", "编程", "Bug更少"),
        ("🎬", "视频", "文字变大片"),
        ("🏥", "医疗", "AI诊断超人类"),
        ("📚", "教育", "因材施教成真"),
    ]
    
    cols = 2
    rows = 3
    card_width = 450
    card_height = 280
    start_x = (width - cols * card_width - (cols - 1) * 30) // 2
    start_y = 220
    
    colors = [COLORS['accent_blue'], COLORS['accent_orange'], COLORS['accent_green'],
              (255, 100, 150), (150, 100, 255), (100, 220, 180)]
    
    for i, (emoji, name, desc) in enumerate(industries):
        row = i // cols
        col = i % cols
        x = start_x + col * (card_width + 30)
        y = start_y + row * (card_height + 30)
        
        # 卡片背景
        card_rect = [x, y, x + card_width, y + card_height]
        draw_rounded_rect(draw, card_rect, 20, (40, 50, 70), colors[i], 2)
        
        # Emoji
        draw.text((x + card_width // 2, y + 50), emoji,
                 font=font_title, anchor="mm", fill=colors[i])
        
        # 行业名
        draw.text((x + card_width // 2, y + 130), name,
                 font=font_title, anchor="mm", fill=COLORS['text_white'])
        
        # 描述
        draw.text((x + card_width // 2, y + 200), desc,
                 font=font_text, anchor="mm", fill=COLORS['text_gray'])
    
    img.save(f"{output_dir}/04_industry_grid.png")
    print("行业网格图已生成")

def create_three_tips():
    """创建3个建议图"""
    width, height = 1080, 1440
    
    img = create_gradient_background(width, height,
                                     COLORS['bg_gradient_top'],
                                     COLORS['bg_gradient_bottom'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 56)
        font_tip = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 48)
        font_text = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 36)
    except:
        font_title = ImageFont.load_default()
        font_tip = font_title
        font_text = font_title
    
    center_x = width // 2
    
    # 标题
    draw.text((center_x, 100), "✅ 普通人抓住AI红利的3件事", 
             font=font_title, anchor="mm", fill=COLORS['text_white'])
    
    # 3个建议
    tips = [
        ("1️⃣", "用起来", "每天30分钟和AI对话\n尝试ChatGPT/Claude/文心一言", COLORS['accent_green']),
        ("2️⃣", "学提示词", "提示词=AI时代的编程语言\n好的提示词让输出翻倍", COLORS['accent_orange']),
        ("3️⃣", "结合专业", "AI+你的专业=王炸\n律师/医生/老师+AI", COLORS['accent_blue']),
    ]
    
    tip_y = 220
    tip_height = 320
    for i, (num, title, desc, color) in enumerate(tips):
        # 卡片背景
        card_rect = [60, tip_y + i * (tip_height + 40), width - 60, 
                    tip_y + i * (tip_height + 40) + tip_height]
        draw_rounded_rect(draw, card_rect, 25, (40, 50, 70), color, 3)
        
        # 序号
        draw.text((card_rect[0] + 60, card_rect[1] + 50), num,
                 font=font_tip, fill=color)
        
        # 标题
        draw.text((card_rect[0] + 150, card_rect[1] + 50), title,
                 font=font_tip, fill=COLORS['text_white'])
        
        # 描述
        for j, line in enumerate(desc.split('\n')):
            draw.text((card_rect[0] + 60, card_rect[1] + 140 + j * 55), line,
                     font=font_text, fill=COLORS['text_gray'])
    
    img.save(f"{output_dir}/05_three_tips.png")
    print("3个建议图已生成")

def create_future_timeline():
    """创建未来时间线图"""
    width, height = 1080, 1440
    
    img = create_gradient_background(width, height,
                                     COLORS['bg_gradient_top'],
                                     COLORS['bg_gradient_bottom'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 52)
        font_year = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 44)
        font_text = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 36)
    except:
        font_title = ImageFont.load_default()
        font_year = font_title
        font_text = font_title
    
    center_x = width // 2
    
    # 标题
    draw.text((center_x, 100), "🔮 未来3年AI发展预测", 
             font=font_title, anchor="mm", fill=COLORS['text_white'])
    
    # 时间线
    timeline = [
        ("2024-2025", "AI助手普及", "人人有AI助理", COLORS['accent_green']),
        ("2025-2026", "AI Agent爆发", "能自主完成任务", COLORS['accent_orange']),
        ("2026-2027", "具身智能成熟", "机器人走进家庭", COLORS['accent_blue']),
    ]
    
    line_x = center_x
    start_y = 280
    node_radius = 30
    spacing = 320
    
    # 画时间线
    draw.line([(line_x, start_y), (line_x, start_y + 2 * spacing)],
             fill=(100, 100, 120), width=4)
    
    for i, (year, title, desc, color) in enumerate(timeline):
        y = start_y + i * spacing
        
        # 节点
        draw.ellipse([line_x - node_radius, y - node_radius, 
                     line_x + node_radius, y + node_radius],
                    fill=color, outline=COLORS['text_white'], width=3)
        
        # 年份
        draw.text((line_x + 60, y), year, font=font_year, 
                 anchor="lm", fill=color)
        
        # 标题
        draw.text((line_x + 60, y + 50), title, font=font_text,
                 anchor="lm", fill=COLORS['text_white'])
        
        # 描述
        draw.text((line_x + 60, y + 95), desc, font=font_text,
                 anchor="lm", fill=COLORS['text_gray'])
    
    # 底部号召
    call_y = height - 180
    draw.text((center_x, call_y), "✨ 未来的你，会感谢今天开始的自己",
             font=font_title, anchor="mm", fill=COLORS['accent_orange'])
    
    img.save(f"{output_dir}/06_future_timeline.png")
    print("未来时间线图已生成")

def main():
    """生成所有素材"""
    print("开始生成小红书视频配图...")
    print()
    
    # 1. 封面
    create_cover_image()
    
    # 2. 标题卡片
    create_title_card("🤖 AI发展现状", "我们正在经历的历史时刻", "02_title_opener.png")
    
    # 3. 模型对比
    create_model_comparison()
    
    # 4. 行业网格
    create_industry_grid()
    
    # 5. 3个建议
    create_three_tips()
    
    # 6. 未来时间线
    create_future_timeline()
    
    print(f"\n所有素材已生成到: {output_dir}")
    print("\n生成的文件:")
    for f in sorted(os.listdir(output_dir)):
        print(f"   - {f}")

if __name__ == "__main__":
    main()