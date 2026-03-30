"""
自动生成小红书视频 - 详细版
使用 MoviePy 将图片、详细文字合成为视频
"""

import os
import sys
from moviepy import *
from moviepy import vfx

# 路径配置
ASSETS_DIR = "D:/AI_Files/xiaohongshu_video_assets"
OUTPUT_DIR = "D:/AI_Files"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "xiaohongshu_ai_video_v2.mp4")

# 视频配置
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # 9:16 竖版
FPS = 30

# 字体路径
FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/simhei.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = None

def create_background(duration, color=(20, 25, 35)):
    """创建背景"""
    return ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=color, duration=duration)

def create_title_screen():
    """创建标题画面 - 5秒"""
    duration = 5
    bg = create_background(duration)
    
    # 大标题
    title = TextClip(
        text="2024 AI发展现状",
        font_size=100,
        color='white',
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 400))
    
    # 副标题
    subtitle = TextClip(
        text="我们正在经历的历史时刻",
        font_size=50,
        color=(180, 200, 255),
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 600))
    
    # 核心主题 - 金色强调
    theme = TextClip(
        text="普通人如何抓住AI红利",
        font_size=65,
        color=(255, 200, 80),
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 900))
    
    # 装饰线
    line = ColorClip(size=(600, 4), color=(100, 150, 255), duration=duration)
    line = line.with_position(('center', 750))
    
    return CompositeVideoClip([bg, title, subtitle, line, theme])

def create_text_slide(title_text, desc_lines, duration, title_color=(100, 180, 255)):
    """创建文字说明页面"""
    bg = create_background(duration)
    clips = [bg]
    
    # 标题
    title = TextClip(
        text=title_text,
        font_size=70,
        color=title_color,
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 250))
    clips.append(title)
    
    # 描述文字（多行）
    y_pos = 450
    for line in desc_lines:
        desc = TextClip(
            text=line,
            font_size=45,
            color=(220, 220, 220),
            font=FONT_PATH,
            size=(VIDEO_WIDTH-100, None),
            text_align='center',
            duration=duration
        ).with_position(('center', y_pos))
        clips.append(desc)
        y_pos += 120
    
    return CompositeVideoClip(clips)

def create_model_slide():
    """AI模型介绍 - 8秒"""
    duration = 8
    bg = create_background(duration)
    
    title = TextClip(
        text="大模型百花齐放",
        font_size=75,
        color=(100, 200, 255),
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 200))
    
    models = [
        ("GPT-4o", "多模态王者，能看能听能说", (80, 200, 120)),
        ("Claude 3.5", "程序员福音，代码能力超强", (255, 150, 80)),
        ("Gemini 1.5", "百万级上下文，整本书都能读", (100, 150, 255)),
        ("国产模型", "文心、通义、Kimi快速崛起", (200, 100, 255)),
    ]
    
    clips = [bg, title]
    y_pos = 400
    for name, desc, color in models:
        # 模型名
        name_clip = TextClip(
            text=name,
            font_size=50,
            color=color,
            font=FONT_PATH,
            size=(VIDEO_WIDTH-80, None),
            text_align='center',
            duration=duration
        ).with_position(('center', y_pos))
        clips.append(name_clip)
        
        # 描述
        desc_clip = TextClip(
            text=desc,
            font_size=35,
            color=(180, 180, 180),
            font=FONT_PATH,
            size=(VIDEO_WIDTH-80, None),
            text_align='center',
            duration=duration
        ).with_position(('center', y_pos + 70))
        clips.append(desc_clip)
        
        y_pos += 180
    
    return CompositeVideoClip(clips)

def create_industry_slide():
    """行业改变 - 8秒"""
    duration = 8
    bg = create_background(duration)
    
    title = TextClip(
        text="AI正在改变这些行业",
        font_size=75,
        color=(100, 200, 255),
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 200))
    
    industries = [
        "设计：人人能做图",
        "写作：效率提升10倍",
        "编程：Bug更少",
        "视频：文字变大片",
        "医疗：AI诊断超人类",
        "教育：因材施教成真"
    ]
    
    clips = [bg, title]
    y_pos = 400
    for industry in industries:
        clip = TextClip(
            text=industry,
            font_size=45,
            color=(220, 220, 220),
            font=FONT_PATH,
            size=(VIDEO_WIDTH-80, None),
            text_align='center',
            duration=duration
        ).with_position(('center', y_pos))
        clips.append(clip)
        y_pos += 100
    
    return CompositeVideoClip(clips)

def create_tips_slide():
    """三个建议 - 10秒"""
    duration = 10
    bg = create_background(duration)
    
    title = TextClip(
        text="普通人抓住AI红利的3件事",
        font_size=70,
        color=(255, 200, 80),
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 200))
    
    tips = [
        ("1. 用起来", "每天30分钟和AI对话", "尝试ChatGPT/Claude/文心一言"),
        ("2. 学提示词", "提示词=AI时代的编程语言", "好的提示词让输出质量翻倍"),
        ("3. 结合专业", "AI+你的专业=王炸", "律师/医生/老师+AI"),
    ]
    
    clips = [bg, title]
    y_pos = 400
    for tip_title, line1, line2 in tips:
        # 标题
        tip_title_clip = TextClip(
            text=tip_title,
            font_size=50,
            color=(100, 200, 255),
            font=FONT_PATH,
            size=(VIDEO_WIDTH-80, None),
            text_align='center',
            duration=duration
        ).with_position(('center', y_pos))
        clips.append(tip_title_clip)
        
        # 描述1
        line1_clip = TextClip(
            text=line1,
            font_size=35,
            color=(200, 200, 200),
            font=FONT_PATH,
            size=(VIDEO_WIDTH-80, None),
            text_align='center',
            duration=duration
        ).with_position(('center', y_pos + 70))
        clips.append(line1_clip)
        
        # 描述2
        line2_clip = TextClip(
            text=line2,
            font_size=35,
            color=(180, 180, 180),
            font=FONT_PATH,
            size=(VIDEO_WIDTH-80, None),
            text_align='center',
            duration=duration
        ).with_position(('center', y_pos + 115))
        clips.append(line2_clip)
        
        y_pos += 220
    
    return CompositeVideoClip(clips)

def create_future_slide():
    """未来发展 - 8秒"""
    duration = 8
    bg = create_background(duration)
    
    title = TextClip(
        text="未来3年AI发展预测",
        font_size=75,
        color=(100, 200, 255),
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 200))
    
    futures = [
        ("2024-2025", "AI助手普及", "人人有AI助理"),
        ("2025-2026", "AI Agent爆发", "能自主完成任务"),
        ("2026-2027", "具身智能成熟", "机器人走进家庭"),
    ]
    
    clips = [bg, title]
    y_pos = 420
    for year, event, desc in futures:
        # 年份
        year_clip = TextClip(
            text=year,
            font_size=45,
            color=(255, 200, 80),
            font=FONT_PATH,
            size=(VIDEO_WIDTH-80, None),
            text_align='center',
            duration=duration
        ).with_position(('center', y_pos))
        clips.append(year_clip)
        
        # 事件
        event_clip = TextClip(
            text=event,
            font_size=40,
            color=(220, 220, 220),
            font=FONT_PATH,
            size=(VIDEO_WIDTH-80, None),
            text_align='center',
            duration=duration
        ).with_position(('center', y_pos + 60))
        clips.append(event_clip)
        
        # 描述
        desc_clip = TextClip(
            text=desc,
            font_size=35,
            color=(180, 180, 180),
            font=FONT_PATH,
            size=(VIDEO_WIDTH-80, None),
            text_align='center',
            duration=duration
        ).with_position(('center', y_pos + 105))
        clips.append(desc_clip)
        
        y_pos += 200
    
    return CompositeVideoClip(clips)

def create_ending_slide():
    """结尾画面 - 5秒"""
    duration = 5
    bg = create_background(duration)
    
    # 主标语
    slogan = TextClip(
        text="未来的你",
        font_size=90,
        color=(255, 200, 80),
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 500))
    
    slogan2 = TextClip(
        text="会感谢今天开始的自己",
        font_size=80,
        color=(255, 200, 80),
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 650))
    
    # 互动提示
    cta = TextClip(
        text="你觉得AI对你影响最大的是什么？",
        font_size=45,
        color=(200, 200, 200),
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 1000))
    
    cta2 = TextClip(
        text="评论区聊聊~",
        font_size=45,
        color=(100, 200, 255),
        font=FONT_PATH,
        size=(VIDEO_WIDTH-80, None),
        text_align='center',
        duration=duration
    ).with_position(('center', 1080))
    
    return CompositeVideoClip([bg, slogan, slogan2, cta, cta2])

def generate_video():
    """生成完整视频"""
    print("开始生成详细版视频...")
    
    clips = []
    
    # 1. 开场标题
    print("制作开场...")
    clips.append(create_title_screen())
    
    # 2. AI模型介绍
    print("添加AI模型介绍...")
    clips.append(create_model_slide())
    
    # 3. 行业改变
    print("添加行业改变...")
    clips.append(create_industry_slide())
    
    # 4. 三个建议
    print("添加三个建议...")
    clips.append(create_tips_slide())
    
    # 5. 未来发展
    print("添加未来发展...")
    clips.append(create_future_slide())
    
    # 6. 结尾
    print("制作结尾...")
    clips.append(create_ending_slide())
    
    # 合并
    print("合并视频...")
    final = concatenate_videoclips(clips)
    
    # 确保尺寸
    final = final.resized((VIDEO_WIDTH, VIDEO_HEIGHT))
    
    # 导出
    print(f"导出视频: {OUTPUT_FILE}")
    final.write_videofile(
        OUTPUT_FILE,
        fps=FPS,
        codec='libx264',
        audio=False,
        threads=4,
        preset='medium',
        logger=None
    )
    
    print(f"视频生成完成！时长: {final.duration:.1f}秒")
    return OUTPUT_FILE

if __name__ == "__main__":
    try:
        video_path = generate_video()
        print(f"视频已保存: {video_path}")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()