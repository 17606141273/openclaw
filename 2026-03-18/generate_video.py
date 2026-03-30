"""
自动生成小红书视频
使用 MoviePy 将图片、音频合成为视频
"""

import os
import sys

# 检查并安装 moviepy
from moviepy import *
from moviepy import vfx

# 路径配置
ASSETS_DIR = "D:/AI_Files/xiaohongshu_video_assets"
OUTPUT_DIR = "D:/AI_Files"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "xiaohongshu_ai_video.mp4")

# 视频配置
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # 9:16 竖版
FPS = 30

def create_text_clip(text, duration, fontsize=60, color='white', bg_color=None):
    """创建文字片段"""
    # 尝试使用系统中文字体
    font_path = "C:/Windows/Fonts/msyh.ttc"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/simhei.ttf"
    if not os.path.exists(font_path):
        font_path = None
    
    txt_clip = TextClip(
        text=text,
        font_size=fontsize,
        color=color,
        font=font_path,
        size=(VIDEO_WIDTH-100, None),
        text_align='center',
        duration=duration
    )
    
    if bg_color:
        # 添加背景
        bg = ColorClip(size=(VIDEO_WIDTH, txt_clip.h + 40), color=bg_color, duration=duration)
        txt_clip = CompositeVideoClip([bg, txt_clip.with_position('center')])
    
    return txt_clip

def create_image_clip(image_path, duration, zoom_effect=False):
    """创建图片片段，带缩放效果"""
    img_clip = ImageClip(image_path).with_duration(duration)
    
    # 调整图片大小适应视频
    img_clip = img_clip.resized(height=VIDEO_HEIGHT)
    
    if img_clip.w > VIDEO_WIDTH:
        img_clip = img_clip.resized(width=VIDEO_WIDTH)
    
    # 居中裁剪
    img_clip = img_clip.with_position('center')
    
    if zoom_effect:
        # 添加缓慢放大效果
        def zoom(t):
            return 1 + 0.05 * (t / duration)
        img_clip = img_clip.resized(zoom)
    
    # 添加淡入淡出
    img_clip = img_clip.with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
    
    return img_clip

def create_background():
    """创建渐变背景"""
    # 创建深蓝渐变背景
    bg = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=(20, 25, 35), duration=1)
    return bg

def generate_video():
    """生成完整视频"""
    print("开始生成视频...")
    
    clips = []
    
    # 1. 开场标题 (4秒)
    print("制作开场...")
    title_bg = create_background().with_duration(4)
    
    # 字体路径
    font_file = "C:/Windows/Fonts/msyh.ttc"
    if not os.path.exists(font_file):
        font_file = "C:/Windows/Fonts/simhei.ttf"
    if not os.path.exists(font_file):
        font_file = None
    
    # 主标题 - 更大更醒目
    title_text = TextClip(
        text="2024 AI发展现状",
        font_size=90,
        color='white',
        font=font_file,
        size=(VIDEO_WIDTH-100, None),
        text_align='center',
        duration=4
    ).with_position(('center', VIDEO_HEIGHT * 0.35))
    
    # 副标题1
    subtitle1 = TextClip(
        text="我们正在经历的历史时刻",
        font_size=55,
        color=(200, 220, 255),
        font=font_file,
        size=(VIDEO_WIDTH-100, None),
        text_align='center',
        duration=4
    ).with_position(('center', VIDEO_HEIGHT * 0.5))
    
    # 副标题2 - 核心主题
    subtitle2 = TextClip(
        text="普通人如何抓住AI红利",
        font_size=60,
        color=(255, 200, 100),
        font=font_file,
        size=(VIDEO_WIDTH-100, None),
        text_align='center',
        duration=4
    ).with_position(('center', VIDEO_HEIGHT * 0.65))
    
    opening = CompositeVideoClip([title_bg, title_text, subtitle1, subtitle2])
    clips.append(opening)
    
    # 2. 模型对比 (8秒)
    print("添加模型对比...")
    if os.path.exists(f"{ASSETS_DIR}/03_model_comparison.png"):
        model_clip = create_image_clip(
            f"{ASSETS_DIR}/03_model_comparison.png",
            8,
            zoom_effect=True
        )
        clips.append(model_clip)
    
    # 3. 过渡文字 (2秒)
    transition = create_text_clip(
        "AI正在重塑各行各业...",
        2,
        fontsize=60
    ).with_position('center')
    transition_bg = create_background().with_duration(2)
    clips.append(CompositeVideoClip([transition_bg, transition]))
    
    # 4. 行业网格 (8秒)
    print("添加行业网格...")
    if os.path.exists(f"{ASSETS_DIR}/04_industry_grid.png"):
        industry_clip = create_image_clip(
            f"{ASSETS_DIR}/04_industry_grid.png",
            8,
            zoom_effect=True
        )
        clips.append(industry_clip)
    
    # 5. 过渡文字 (2秒)
    transition2 = create_text_clip(
        "普通人如何抓住这波红利？",
        2,
        fontsize=60,
        color=(100, 200, 255)
    ).with_position('center')
    transition2_bg = create_background().with_duration(2)
    clips.append(CompositeVideoClip([transition2_bg, transition2]))
    
    # 6. 三个建议 (10秒)
    print("添加三个建议...")
    if os.path.exists(f"{ASSETS_DIR}/05_three_tips.png"):
        tips_clip = create_image_clip(
            f"{ASSETS_DIR}/05_three_tips.png",
            10,
            zoom_effect=True
        )
        clips.append(tips_clip)
    
    # 7. 过渡文字 (2秒)
    transition3 = create_text_clip(
        "未来3年，AI将如何发展？",
        2,
        fontsize=60,
        color=(255, 150, 100)
    ).with_position('center')
    transition3_bg = create_background().with_duration(2)
    clips.append(CompositeVideoClip([transition3_bg, transition3]))
    
    # 8. 未来时间线 (8秒)
    print("添加未来时间线...")
    if os.path.exists(f"{ASSETS_DIR}/06_future_timeline.png"):
        future_clip = create_image_clip(
            f"{ASSETS_DIR}/06_future_timeline.png",
            8,
            zoom_effect=True
        )
        clips.append(future_clip)
    
    # 9. 结尾号召 (4秒)
    print("制作结尾...")
    ending_bg = create_background().with_duration(4)
    ending_text = create_text_clip(
        "未来的你\n会感谢今天开始的自己",
        4,
        fontsize=70,
        color=(255, 200, 100)
    ).with_position('center')
    
    # 添加互动提示
    cta = create_text_clip(
        "你觉得AI对你影响最大的是什么？\n评论区聊聊~",
        4,
        fontsize=40,
        color=(200, 200, 200)
    ).with_position(('center', VIDEO_HEIGHT * 0.75))
    
    ending = CompositeVideoClip([ending_bg, ending_text, cta])
    clips.append(ending)
    
    # 合并所有片段
    print("合并视频片段...")
    final_video = concatenate_videoclips(clips)
    
    # 添加背景音乐（如果有的话）
    # 这里可以添加轻快的BGM
    
    # 导出视频
    print(f"导出视频到: {OUTPUT_FILE}")
    
    # 确保所有片段尺寸一致
    final_video = final_video.resized((VIDEO_WIDTH, VIDEO_HEIGHT))
    
    final_video.write_videofile(
        OUTPUT_FILE,
        fps=FPS,
        codec='libx264',
        audio=False,  # 暂时没有音频
        threads=4,
        preset='medium',
        logger=None
    )
    
    print(f"✅ 视频生成完成！")
    print(f"📁 文件位置: {OUTPUT_FILE}")
    print(f"⏱️ 视频时长: {final_video.duration:.1f}秒")
    
    return OUTPUT_FILE

if __name__ == "__main__":
    try:
        video_path = generate_video()
        print(f"\n视频已生成: {video_path}")
    except Exception as e:
        print(f"生成视频时出错: {e}")
        import traceback
        traceback.print_exc()