"""
苹果蛇小游戏 (Apple Snake)
一条爱吃苹果的可爱小蛇冒险记
"""

import pygame
import random
import sys
import math

# 初始化 Pygame
pygame.init()

# 游戏常量
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
GRID_SIZE = 25
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义 - 温馨可爱的配色
COLOR_BACKGROUND = (34, 45, 56)        # 深蓝灰背景
COLOR_GRID = (45, 58, 72)              # 网格线
COLOR_SNAKE_HEAD = (76, 175, 80)       # 草绿色蛇头
COLOR_SNAKE_BODY = (129, 199, 132)     # 浅绿色蛇身
COLOR_SNAKE_OUTLINE = (46, 125, 50)    # 深绿轮廓
COLOR_APPLE = (239, 83, 80)            # 红苹果
COLOR_APPLE_STEM = (121, 85, 72)       # 苹果梗
COLOR_LEAF = (104, 159, 56)            # 绿叶
COLOR_GOLDEN_APPLE = (255, 193, 7)     # 金苹果
COLOR_TEXT = (255, 255, 255)           # 白色文字
COLOR_SCORE = (255, 241, 118)          # 淡黄色分数
COLOR_GAME_OVER = (255, 112, 67)       # 橙红色游戏结束
COLOR_PAUSE = (100, 181, 246)          # 浅蓝暂停

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Particle:
    """粒子效果类 - 吃苹果时的特效"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(3, 8)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = 30
        self.max_life = 30
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += 0.1  # 重力
        self.life -= 1
        return self.life > 0
    
    def draw(self, screen):
        alpha = self.life / self.max_life
        size = int(self.size * alpha)
        if size > 0:
            color = tuple(int(c * alpha + 255 * (1 - alpha)) for c in self.color[:3])
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), size)


class FloatingText:
    """浮动文字 - 显示得分"""
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 40
        self.max_life = 40
        self.speed_y = -1
    
    def update(self):
        self.y += self.speed_y
        self.life -= 1
        return self.life > 0
    
    def draw(self, screen, font):
        alpha = self.life / self.max_life
        text_surface = font.render(self.text, True, self.color)
        text_surface.set_alpha(int(255 * alpha))
        screen.blit(text_surface, (self.x, self.y))


class Apple:
    """苹果类 - 普通苹果和金苹果"""
    def __init__(self):
        self.position = (0, 0)
        self.is_golden = False
        self.golden_timer = 0
        self.animation_offset = 0
        self.randomize()
    
    def randomize(self, snake_body=None):
        """随机生成苹果位置"""
        while True:
            pos = (random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3))
            if snake_body is None or pos not in snake_body:
                self.position = pos
                break
        # 10% 概率生成金苹果
        self.is_golden = random.random() < 0.1
        self.golden_timer = 300 if self.is_golden else 0  # 金苹果5秒后消失
    
    def update(self):
        """更新动画"""
        self.animation_offset = math.sin(pygame.time.get_ticks() / 200) * 3
        if self.is_golden and self.golden_timer > 0:
            self.golden_timer -= 1
            if self.golden_timer <= 0:
                self.is_golden = False
    
    def draw(self, screen):
        """绘制苹果"""
        x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        y = self.position[1] * GRID_SIZE + GRID_SIZE // 2 + self.animation_offset
        
        color = COLOR_GOLDEN_APPLE if self.is_golden else COLOR_APPLE
        
        # 苹果主体（圆形）
        radius = GRID_SIZE // 2 - 2
        pygame.draw.circle(screen, color, (int(x), int(y)), radius)
        pygame.draw.circle(screen, (200, 50, 50), (int(x), int(y)), radius, 2)
        
        # 苹果梗
        stem_rect = pygame.Rect(x - 2, y - radius - 4, 4, 6)
        pygame.draw.rect(screen, COLOR_APPLE_STEM, stem_rect)
        
        # 叶子
        leaf_points = [
            (x, y - radius - 2),
            (x + 8, y - radius - 8),
            (x + 2, y - radius)
        ]
        pygame.draw.polygon(screen, COLOR_LEAF, leaf_points)
        
        # 金苹果闪烁效果
        if self.is_golden:
            glow_radius = radius + 4 + math.sin(pygame.time.get_ticks() / 100) * 2
            glow_surface = pygame.Surface((int(glow_radius * 2), int(glow_radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 215, 0, 100), (int(glow_radius), int(glow_radius)), int(glow_radius))
            screen.blit(glow_surface, (int(x - glow_radius), int(y - glow_radius)))
            
            # 倒计时条
            bar_width = GRID_SIZE
            bar_height = 4
            progress = self.golden_timer / 300
            pygame.draw.rect(screen, (100, 100, 100), (x - bar_width//2, y + radius + 5, bar_width, bar_height))
            pygame.draw.rect(screen, COLOR_GOLDEN_APPLE, (x - bar_width//2, y + radius + 5, int(bar_width * progress), bar_height))


class Snake:
    """蛇类 - 可爱的苹果蛇"""
    def __init__(self):
        self.reset()
        self.blink_timer = 0
        self.is_blinking = False
    
    def reset(self):
        """重置蛇的状态"""
        center_x, center_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.body = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False
        self.ate_apple = False
        self.ate_golden = False
    
    def move(self):
        """移动蛇"""
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        
        # 穿墙逻辑
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        
        # 检查撞到自己
        if new_head in self.body:
            return False
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        return True
    
    def grow_snake(self, is_golden=False):
        """让蛇变长"""
        self.grow = True
        self.ate_apple = True
        self.ate_golden = is_golden
        # 金苹果长3格，普通苹果长1格
        if is_golden:
            self.grow_count = 3
        else:
            self.grow_count = 1
    
    def change_direction(self, new_direction):
        """改变方向"""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.next_direction = new_direction
    
    def update(self):
        """更新动画状态"""
        self.blink_timer += 1
        if self.blink_timer > 150:  # 每2.5秒眨眼
            self.is_blinking = True
            if self.blink_timer > 160:
                self.blink_timer = 0
                self.is_blinking = False
    
    def draw(self, screen):
        """绘制可爱的蛇"""
        for i, segment in enumerate(self.body):
            x = segment[0] * GRID_SIZE + GRID_SIZE // 2
            y = segment[1] * GRID_SIZE + GRID_SIZE // 2
            
            if i == 0:  # 蛇头
                self._draw_head(screen, x, y)
            else:  # 蛇身
                self._draw_body(screen, x, y, i)
    
    def _draw_head(self, screen, x, y):
        """绘制蛇头 - 带可爱表情"""
        radius = GRID_SIZE // 2 - 2
        
        # 头部主体
        pygame.draw.circle(screen, COLOR_SNAKE_HEAD, (x, y), radius)
        pygame.draw.circle(screen, COLOR_SNAKE_OUTLINE, (x, y), radius, 2)
        
        # 眼睛位置（根据方向调整）
        eye_offset = 6
        eye_y_offset = -2
        
        if self.direction == UP:
            left_eye = (x - eye_offset, y - eye_offset + eye_y_offset)
            right_eye = (x + eye_offset, y - eye_offset + eye_y_offset)
        elif self.direction == DOWN:
            left_eye = (x - eye_offset, y + eye_offset + eye_y_offset)
            right_eye = (x + eye_offset, y + eye_offset + eye_y_offset)
        elif self.direction == LEFT:
            left_eye = (x - eye_offset, y + eye_y_offset)
            right_eye = (x - eye_offset + 3, y + eye_y_offset)
        else:  # RIGHT
            left_eye = (x + eye_offset - 3, y + eye_y_offset)
            right_eye = (x + eye_offset, y + eye_y_offset)
        
        # 眨眼动画
        if self.is_blinking:
            pygame.draw.line(screen, (0, 0, 0), (left_eye[0] - 4, left_eye[1]), (left_eye[0] + 4, left_eye[1]), 2)
            pygame.draw.line(screen, (0, 0, 0), (right_eye[0] - 4, right_eye[1]), (right_eye[0] + 4, right_eye[1]), 2)
        else:
            # 眼睛
            pygame.draw.circle(screen, (255, 255, 255), left_eye, 5)
            pygame.draw.circle(screen, (255, 255, 255), right_eye, 5)
            # 瞳孔
            pygame.draw.circle(screen, (0, 0, 0), (left_eye[0] + 1, left_eye[1] + 1), 3)
            pygame.draw.circle(screen, (0, 0, 0), (right_eye[0] + 1, right_eye[1] + 1), 3)
            # 高光
            pygame.draw.circle(screen, (255, 255, 255), (left_eye[0] - 1, left_eye[1] - 1), 1)
            pygame.draw.circle(screen, (255, 255, 255), (right_eye[0] - 1, right_eye[1] - 1), 1)
        
        # 腮红
        pygame.draw.circle(screen, (255, 182, 193), (x - 8, y + 5), 3)
        pygame.draw.circle(screen, (255, 182, 193), (x + 8, y + 5), 3)
        
        # 微笑
        smile_rect = pygame.Rect(x - 5, y + 2, 10, 6)
        pygame.draw.arc(screen, (0, 0, 0), smile_rect, 0, math.pi, 2)
    
    def _draw_body(self, screen, x, y, index):
        """绘制蛇身"""
        radius = GRID_SIZE // 2 - 3
        
        # 身体渐变效果
        green_value = max(129 - index * 3, 80)
        body_color = (76, green_value, 80 + index * 2)
        
        pygame.draw.circle(screen, body_color, (x, y), radius)
        pygame.draw.circle(screen, COLOR_SNAKE_OUTLINE, (x, y), radius, 1)
        
        # 身上的花纹
        if index % 2 == 0:
            pygame.draw.circle(screen, (200, 230, 201), (x, y), radius // 2)


class Game:
    """游戏主类"""
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🍎 苹果蛇 - Apple Snake")
        self.clock = pygame.time.Clock()
        
        # 字体
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 28)
        
        # 游戏对象
        self.snake = Snake()
        self.apple = Apple()
        self.particles = []
        self.floating_texts = []
        
        # 游戏状态
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.paused = False
        self.speed = 8
        self.apples_eaten = 0
        self.golden_apples_eaten = 0
    
    def spawn_particles(self, x, y, color, count=10):
        """生成粒子特效"""
        pixel_x = x * GRID_SIZE + GRID_SIZE // 2
        pixel_y = y * GRID_SIZE + GRID_SIZE // 2
        for _ in range(count):
            self.particles.append(Particle(pixel_x, pixel_y, color))
    
    def handle_events(self):
        """处理输入事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.paused = not self.paused
                
                elif event.key == pygame.K_ESCAPE:
                    return False
                
                elif not self.game_over and not self.paused:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(RIGHT)
        
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_over or self.paused:
            return
        
        # 更新蛇
        self.snake.update()
        if not self.snake.move():
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return
        
        # 更新苹果
        self.apple.update()
        
        # 检查是否吃到苹果
        if self.snake.body[0] == self.apple.position:
            is_golden = self.apple.is_golden
            points = 50 if is_golden else 10
            
            self.score += points
            self.apples_eaten += 1
            if is_golden:
                self.golden_apples_eaten += 1
            
            # 蛇变长
            grow_amount = 3 if is_golden else 1
            for _ in range(grow_amount):
                self.snake.grow_snake(is_golden)
            
            # 特效
            color = COLOR_GOLDEN_APPLE if is_golden else COLOR_APPLE
            self.spawn_particles(self.apple.position[0], self.apple.position[1], color, 15 if is_golden else 8)
            
            # 浮动文字
            pixel_x = self.apple.position[0] * GRID_SIZE
            pixel_y = self.apple.position[1] * GRID_SIZE
            text = f"+{points}!" if is_golden else f"+{points}"
            self.floating_texts.append(FloatingText(pixel_x, pixel_y, text, COLOR_GOLDEN_APPLE if is_golden else COLOR_SCORE))
            
            # 速度提升
            self.speed = min(8 + self.score // 100, 15)
            
            # 生成新苹果
            self.apple.randomize(self.snake.body)
        
        # 更新粒子
        self.particles = [p for p in self.particles if p.update()]
        
        # 更新浮动文字
        self.floating_texts = [t for t in self.floating_texts if t.update()]
    
    def draw(self):
        """绘制游戏画面"""
        # 背景
        self.screen.fill(COLOR_BACKGROUND)
        
        # 网格
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (WINDOW_WIDTH, y))
        
        # 游戏元素
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)
        
        # 粒子特效
        for particle in self.particles:
            particle.draw(self.screen)
        
        # 浮动文字
        for text in self.floating_texts:
            text.draw(self.screen, self.font_small)
        
        # UI - 分数面板
        self._draw_ui()
        
        # 暂停画面
        if self.paused and not self.game_over:
            self._draw_pause_screen()
        
        # 游戏结束画面
        if self.game_over:
            self._draw_game_over_screen()
        
        pygame.display.flip()
    
    def _draw_ui(self):
        """绘制用户界面"""
        # 分数
        score_text = self.font_medium.render(f"🍎 {self.score}", True, COLOR_SCORE)
        self.screen.blit(score_text, (15, 15))
        
        # 最高分
        high_score_text = self.font_small.render(f"最高分: {self.high_score}", True, (200, 200, 200))
        self.screen.blit(high_score_text, (15, 55))
        
        # 统计信息
        stats_text = self.font_tiny.render(f"苹果: {self.apples_eaten} | 金苹果: {self.golden_apples_eaten}", True, (180, 180, 180))
        self.screen.blit(stats_text, (15, 85))
        
        # 速度
        speed_text = self.font_tiny.render(f"速度: {self.speed}", True, (180, 180, 180))
        self.screen.blit(speed_text, (WINDOW_WIDTH - 100, 15))
        
        # 操作提示
        if not self.game_over and not self.paused:
            help_text = self.font_tiny.render("WASD/方向键移动 | 空格暂停 | ESC退出", True, (120, 120, 120))
            text_rect = help_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
            self.screen.blit(help_text, text_rect)
    
    def _draw_pause_screen(self):
        """绘制暂停画面"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font_large.render("⏸ 暂停", True, COLOR_PAUSE)
        text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, text_rect)
        
        hint_text = self.font_small.render("按空格键继续", True, (200, 200, 200))
        text_rect = hint_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(hint_text, text_rect)
    
    def _draw_game_over_screen(self):
        """绘制游戏结束画面"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束
        game_over_text = self.font_large.render("💀 游戏结束", True, COLOR_GAME_OVER)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, text_rect)
        
        # 最终分数
        final_score_text = self.font_medium.render(f"最终得分: {self.score}", True, COLOR_SCORE)
        text_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 10))
        self.screen.blit(final_score_text, text_rect)
        
        # 统计
        stats_text = self.font_small.render(f"吃了 {self.apples_eaten} 个苹果 ({self.golden_apples_eaten} 个金苹果)", True, (200, 200, 200))
        text_rect = stats_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
        self.screen.blit(stats_text, text_rect)
        
        # 新纪录
        if self.score > 0 and self.score == self.high_score:
            record_text = self.font_medium.render("🎉 新纪录!", True, COLOR_GOLDEN_APPLE)
            text_rect = record_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90))
            self.screen.blit(record_text, text_rect)
        
        # 提示
        restart_text = self.font_small.render("空格键重新开始 | ESC退出", True, (180, 180, 180))
        text_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
        self.screen.blit(restart_text, text_rect)
    
    def reset_game(self):
        """重置游戏"""
        self.snake.reset()
        self.apple.randomize()
        self.particles = []
        self.floating_texts = []
        self.score = 0
        self.speed = 8
        self.apples_eaten = 0
        self.golden_apples_eaten = 0
        self.game_over = False
        self.paused = False
    
    def run(self):
        """游戏主循环"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed)
        
        pygame.quit()
        sys.exit()


def main():
    """主函数"""
    print("=" * 60)
    print("🍎 苹果蛇 - Apple Snake 🐍")
    print("=" * 60)
    print("\n🎮 操作说明:")
    print("   ↑ 或 W - 向上移动")
    print("   ↓ 或 S - 向下移动")
    print("   ← 或 A - 向左移动")
    print("   → 或 D - 向右移动")
    print("   空格   - 暂停/继续")
    print("   ESC    - 退出游戏")
    print("\n🍎 游戏规则:")
    print("   • 控制可爱的苹果蛇吃红色苹果 (+10分)")
    print("   • 金苹果出现时赶紧吃 (+50分，限时5秒)")
    print("   • 每吃一个苹果蛇会变长")
    print("   • 撞到自己的身体游戏结束")
    print("   • 蛇可以穿墙哦！")
    print("\n✨ 特色:")
    print("   • 可爱的表情动画（会眨眼！）")
    print("   • 吃苹果粒子特效")
    print("   • 分数浮动动画")
    print("   • 速度逐渐加快")
    print("\n" + "=" * 60)
    
    game = Game()
    game.run()


if __name__ == "__main__":
    main()