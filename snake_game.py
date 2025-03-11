import pygame
import random
import sys
import math

# Khởi tạo pygame
pygame.init()

# Các thông số cơ bản
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Màu sắc
BACKGROUND_COLOR = (244, 201, 127)  # Màu vàng nhạt
BORDER_COLOR = (139, 90, 43)  # Màu nâu
SNAKE_BODY_COLOR = (34, 139, 34)  # Xanh lá đậm
SNAKE_HEAD_COLOR = (0, 100, 0)  # Xanh lá đậm hơn
SNAKE_EYE_COLOR = (255, 255, 255)  # Trắng
FOOD_COLOR = (255, 69, 0)  
GRID_COLOR = (232, 178, 108)  
TEXT_COLOR = (255, 255, 255) 
BUTTON_COLOR = (50, 150, 50)
BUTTON_HOVER_COLOR = (70, 170, 70)

# Hướng di chuyển
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.length = 1
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)

        if new[0] < 0 or new[0] >= GRID_WIDTH or new[1] < 0 or new[1] >= GRID_HEIGHT:
            return False

        if new in self.positions[2:]:
            return False

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

class Food:
    def __init__(self, snake):
        self.snake = snake
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake.positions:
                self.position = pos
                break

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font

    def draw(self, screen):
        current_color = self.hover_color if self.is_hovered() else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.is_running = True
        self.reset_game()
        self.restart_button = Button(
            WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 + 50, 150, 50,
            "Restart", BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR, self.font
        )

    def reset_game(self):
        self.snake = Snake()
        self.food = Food(self.snake)
        self.is_running = True

    def draw_grid(self):
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            for x in range(0, WINDOW_WIDTH, GRID_SIZE):
                rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

    def draw_score(self):
        score_text = self.font.render(f'Score: {self.snake.score}', True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))

    def draw_snake(self):
        for i, pos in enumerate(self.snake.positions):
            x, y = pos
            center = (int(x * GRID_SIZE + GRID_SIZE / 2), int(y * GRID_SIZE + GRID_SIZE / 2))
            
            if i == 0:  # Head
                pygame.draw.circle(self.screen, SNAKE_HEAD_COLOR, center, int(GRID_SIZE / 2))
                
                # Eyes
                eye_offset = 3
                left_eye = (center[0] - eye_offset, center[1] - eye_offset)
                right_eye = (center[0] + eye_offset, center[1] - eye_offset)
                pygame.draw.circle(self.screen, SNAKE_EYE_COLOR, left_eye, 2)
                pygame.draw.circle(self.screen, SNAKE_EYE_COLOR, right_eye, 2)
                
            else:  # Body
                pygame.draw.circle(self.screen, SNAKE_BODY_COLOR, center, int(GRID_SIZE / 2) - 1)
            
            # Connect segments
            if i > 0:
                prev = self.snake.positions[i-1]
                current = pos
                pygame.draw.line(self.screen, SNAKE_BODY_COLOR, 
                                 (prev[0] * GRID_SIZE + GRID_SIZE / 2, prev[1] * GRID_SIZE + GRID_SIZE / 2),
                                 (current[0] * GRID_SIZE + GRID_SIZE / 2, current[1] * GRID_SIZE + GRID_SIZE / 2),
                                 int(GRID_SIZE / 2))

    def game_over_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        text = self.font.render("Game Over!", True, TEXT_COLOR)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        self.restart_button.draw(self.screen)
        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.is_running:
                        if event.key == pygame.K_UP:
                            self.snake.change_direction(UP)
                        elif event.key == pygame.K_DOWN:
                            self.snake.change_direction(DOWN)
                        elif event.key == pygame.K_LEFT:
                            self.snake.change_direction(LEFT)
                        elif event.key == pygame.K_RIGHT:
                            self.snake.change_direction(RIGHT)
                elif not self.is_running and self.restart_button.is_clicked(event):
                    self.reset_game()

            if self.is_running:
                if not self.snake.update():
                    self.is_running = False
                    continue

                if self.snake.get_head_position() == self.food.position:
                    self.snake.length += 1
                    self.snake.score += 10
                    self.food.randomize_position()

                self.screen.fill(BACKGROUND_COLOR)
                self.draw_grid()
                self.draw_snake()

                food_center = (int(self.food.position[0] * GRID_SIZE + GRID_SIZE / 2),
                               int(self.food.position[1] * GRID_SIZE + GRID_SIZE / 2))
                pygame.draw.circle(self.screen, FOOD_COLOR, food_center, int(GRID_SIZE / 2))

                self.draw_score()
                pygame.display.update()
                self.clock.tick(10 + self.snake.score // 20)
            else:
                self.game_over_screen()

if __name__ == "__main__":
    game = Game()
    game.run()