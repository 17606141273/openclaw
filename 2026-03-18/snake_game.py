"""
贪吃蛇小游戏 (Snake Game)
使用 Pygame 实现
"""

import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 游戏常量
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
COLOR_BACKGROUND = (20, 20, 20)
COLOR_GRID = (40, 40, 40)
COLOR_SNAKE_HEAD = (0, 255, 100)
COLOR_SNAKE_BODY = (0, 200, 80)
COLOR_FOOD = (255, 80, 80)
COLOR_TEXT = (255, 255, 255)
COLOR_GAME_OVER = (255, 100, 100)

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    """蛇类"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        """重置蛇的状态"""
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
    
    def move(self):
        """移动蛇"""
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        
        # 检查是否撞到自己
        if new_head in self.body:
            return False
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        return True
    
    def grow_snake(self):
        """让蛇变长"""
        self.grow = True
    
    def change_direction(self, new_direction):
        """改变方向（防止180度掉头）"""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction
    
    def draw(self, screen):
        """绘制蛇"""
        for i, segment in enumerate(self.body):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            rect = pygame.Rect(
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE - 1,
                GRID_SIZE - 1
            )
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)


class Food:
    """食物类"""
    def __init__(self):
        self.position = (0, 0)
        self.randomize()
    
    def randomize(self, snake_body=None):
        """随机生成食物位置"""
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if snake_body is None or pos not in snake_body:
                self.position = pos
                break
    
    def draw(self, screen):
        """绘制食物"""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE - 1,
            GRID_SIZE - 1
        )
        pygame.draw.rect(screen, COLOR_FOOD, rect)
        pygame.draw.rect(screen, (200, 50, 50), rect, 2)


class Game:
    """游戏主类"""
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 贪吃蛇小游戏")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.speed = 8
    
    def handle_events(self):
        """处理输入事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        return False
        
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_over:
            return
        
        # 移动蛇
        if not self.snake.move():
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return
        
        # 检查是否吃到食物
        if self.snake.body[0] == self.food.position:
            self.snake.grow_snake()
            self.score += 10
            self.speed = min(8 + self.score // 50, 20)  # 速度随分数增加
            self.food.randomize(self.snake.body)
    
    def draw(self):
        """绘制游戏画面"""
        # 清空屏幕
        self.screen.fill(COLOR_BACKGROUND)
        
        # 绘制网格（可选）
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (WINDOW_WIDTH, y))
        
        # 绘制游戏元素
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        
        # 绘制分数
        score_text = self.font_small.render(f"分数: {self.score}", True, COLOR_TEXT)
        self.screen.blit(score_text, (10, 10))
        
        high_score_text = self.font_small.render(f"最高分: {self.high_score}", True, COLOR_TEXT)
        self.screen.blit(high_score_text, (10, 45))
        
        # 绘制游戏结束画面
        if self.game_over:
            # 半透明遮罩
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # 游戏结束文字
            game_over_text = self.font_large.render("游戏结束!", True, COLOR_GAME_OVER)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
            # 最终分数
            final_score_text = self.font_medium.render(f"最终分数: {self.score}", True, COLOR_TEXT)
            text_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(final_score_text, text_rect)
            
            # 提示文字
            restart_text = self.font_small.render("按空格键重新开始 | 按 ESC 退出", True, COLOR_TEXT)
            text_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            self.screen.blit(restart_text, text_rect)
        
        # 绘制操作说明
        if not self.game_over:
            help_text = self.font_small.render("WASD 或方向键移动 | ESC 退出", True, (150, 150, 150))
            text_rect = help_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
            self.screen.blit(help_text, text_rect)
        
        pygame.display.flip()
    
    def reset_game(self):
        """重置游戏"""
        self.snake.reset()
        self.food.randomize()
        self.score = 0
        self.speed = 8
        self.game_over = False
    
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
    print("=" * 50)
    print("🐍 贪吃蛇小游戏")
    print("=" * 50)
    print("\n操作说明:")
    print("  ↑ 或 W - 向上移动")
    print("  ↓ 或 S - 向下移动")
    print("  ← 或 A - 向左移动")
    print("  → 或 D - 向右移动")
    print("  ESC    - 退出游戏")
    print("  空格   - 游戏结束后重新开始")
    print("\n游戏规则:")
    print("  • 控制蛇吃红色食物")
    print("  • 每吃一个食物得10分，蛇会变长")
    print("  • 撞到自己的身体游戏结束")
    print("  • 速度会随着分数增加而变快")
    print("\n" + "=" * 50)
    
    game = Game()
    game.run()


if __name__ == "__main__":
    main()