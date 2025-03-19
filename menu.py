import pygame
import sys
import random

# Initialize pygame and font module
pygame.init()
pygame.font.init()  # Add this line to initialize the font module

# Import the snake game - make sure the filename matches your actual file
try:
    from snake import Game, GRID_SIZE, SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR, SNAKE_EYE_COLOR
except ImportError:
    # If import fails, define constants here as fallback
    GRID_SIZE = 20
    SNAKE_HEAD_COLOR = (0, 100, 0)  # Dark green
    SNAKE_BODY_COLOR = (34, 139, 34)  # Green
    SNAKE_EYE_COLOR = (255, 255, 255)  # White
    print("Warning: Could not import snake game module. Using default values.")

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (244, 201, 127)  # Light yellow
TEXT_COLOR = (0, 100, 0)  # Dark green
BUTTON_COLOR = (50, 150, 50)
BUTTON_HOVER_COLOR = (70, 170, 70)
BUTTON_TEXT_COLOR = (255, 255, 255)
TITLE_COLOR = (139, 69, 19)  # Brown

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
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        
        # Add a border
        pygame.draw.rect(screen, (30, 100, 30), self.rect, 3, border_radius=10)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered()

class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game Menu')
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 80)
        self.button_font = pygame.font.Font(None, 40)
        self.info_font = pygame.font.Font(None, 24)
        
        # Create buttons
        button_width, button_height = 200, 60
        center_x = WINDOW_WIDTH // 2 - button_width // 2
        
        self.play_button = Button(
            center_x, 250, button_width, button_height,
            "Play Game", BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, self.button_font
        )
        
        self.ai_mode_button = Button(
            center_x, 330, button_width, button_height,
            "Play vs AI", BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, self.button_font
        )
        
        self.instructions_button = Button(
            center_x, 410, button_width, button_height,
            "Instructions", BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, self.button_font
        )
        
        self.quit_button = Button(
            center_x, 490, button_width, button_height,
            "Quit", BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, self.button_font
        )
        
        # Snake animation variables
        self.snake_positions = [(i, 5) for i in range(10, 0, -1)]
        self.snake_direction = (1, 0)
        self.snake_timer = 0
        self.snake_speed = 10  # Lower is faster
        
        # State
        self.show_instructions = False

    def draw_snake_animation(self):
        # Move snake
        self.snake_timer += 1
        if self.snake_timer >= self.snake_speed:
            self.snake_timer = 0
            
            # Get current head position
            head_x, head_y = self.snake_positions[0]
            
            # Change direction randomly or when hitting edges
            if head_x <= 0 or head_x >= WINDOW_WIDTH // GRID_SIZE - 1 or head_y <= 0 or head_y >= WINDOW_HEIGHT // GRID_SIZE - 1 or random.random() < 0.02:
                # Choose a new direction that's not opposite to current
                possible_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                opposite = (-self.snake_direction[0], -self.snake_direction[1])
                if opposite in possible_directions:
                    possible_directions.remove(opposite)
                self.snake_direction = random.choice(possible_directions)
            
            # Calculate new head position
            new_head = (head_x + self.snake_direction[0], head_y + self.snake_direction[1])
            
            # Keep snake on screen
            new_head = (
                max(0, min(new_head[0], WINDOW_WIDTH // GRID_SIZE - 1)),
                max(0, min(new_head[1], WINDOW_HEIGHT // GRID_SIZE - 1))
            )
            
            # Add new head and remove tail
            self.snake_positions.insert(0, new_head)
            self.snake_positions.pop()
        
        # Draw snake
        for i, pos in enumerate(self.snake_positions):
            x, y = pos
            center = (int(x * GRID_SIZE + GRID_SIZE / 2), 
                      int(y * GRID_SIZE + GRID_SIZE / 2))
            
            if i == 0:  # Head
                pygame.draw.circle(self.screen, SNAKE_HEAD_COLOR, center, int(GRID_SIZE / 2))
                
                # Eyes
                eye_offset = 3
                # Adjust eye position based on direction
                if self.snake_direction == (1, 0):  # Right
                    left_eye = (center[0] + eye_offset, center[1] - eye_offset)
                    right_eye = (center[0] + eye_offset, center[1] + eye_offset)
                elif self.snake_direction == (-1, 0):  # Left
                    left_eye = (center[0] - eye_offset, center[1] - eye_offset)
                    right_eye = (center[0] - eye_offset, center[1] + eye_offset)
                elif self.snake_direction == (0, -1):  # Up
                    left_eye = (center[0] - eye_offset, center[1] - eye_offset)
                    right_eye = (center[0] + eye_offset, center[1] - eye_offset)
                else:  # Down
                    left_eye = (center[0] - eye_offset, center[1] + eye_offset)
                    right_eye = (center[0] + eye_offset, center[1] + eye_offset)
                
                pygame.draw.circle(self.screen, SNAKE_EYE_COLOR, left_eye, 2)
                pygame.draw.circle(self.screen, SNAKE_EYE_COLOR, right_eye, 2)
            else:  # Body
                pygame.draw.circle(self.screen, SNAKE_BODY_COLOR, center, int(GRID_SIZE / 2) - 1)
            
            # Connect segments
            if i > 0:
                prev = self.snake_positions[i-1]
                current = pos
                pygame.draw.line(self.screen, SNAKE_BODY_COLOR, 
                                (prev[0] * GRID_SIZE + GRID_SIZE / 2, 
                                 prev[1] * GRID_SIZE + GRID_SIZE / 2),
                                (current[0] * GRID_SIZE + GRID_SIZE / 2, 
                                 current[1] * GRID_SIZE + GRID_SIZE / 2),
                                int(GRID_SIZE / 2))

    def draw_instructions(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Instructions box
        instructions_rect = pygame.Rect(WINDOW_WIDTH // 2 - 300, WINDOW_HEIGHT // 2 - 200, 600, 400)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, instructions_rect, border_radius=15)
        pygame.draw.rect(self.screen, (139, 69, 19), instructions_rect, 4, border_radius=15)
        
        # Title
        title = self.button_font.render("How to Play", True, TITLE_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 160))
        self.screen.blit(title, title_rect)
        
        # Instructions text
        instructions = [
            "• Use arrow keys to control the snake",
            "• Eat food to grow longer and earn points",
            "• Avoid hitting walls or yourself",
            "• The snake moves faster as your score increases",
            "",
            "In AI mode, you'll compete against a computer-controlled",
            "snake that uses pathfinding algorithms to find food",
            "and avoid obstacles."
        ]
        
        for i, line in enumerate(instructions):
            text = self.info_font.render(line, True, TEXT_COLOR)
            self.screen.blit(text, (WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 - 120 + i * 30))
        
        # Back button
        back_button = Button(
            WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 + 120, 120, 40,
            "Back", BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, self.info_font
        )
        back_button.draw(self.screen)
        
        return back_button

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.show_instructions:
                    back_button = self.draw_instructions()
                    if back_button.is_clicked(event):
                        self.show_instructions = False
                else:
                    if self.play_button.is_clicked(event):
                        # Start the game
                        try:
                            # Import here to avoid circular import issues
                            from snake import Game
                            game = Game()
                            game.run()
                        except ImportError:
                            print("Could not import the Game class from snake.py")
                            # Show error message on screen
                            error_font = pygame.font.Font(None, 24)
                            error_text = error_font.render("Error: Could not start game. Check console for details.", True, (255, 0, 0))
                            self.screen.blit(error_text, (WINDOW_WIDTH // 2 - 200, 550))
                            pygame.display.update()
                            pygame.time.wait(2000)  # Show error for 2 seconds
                    elif self.ai_mode_button.is_clicked(event):
                        # This would start the AI mode
                        # For now, just show a message
                        print("AI mode not implemented yet")
                    elif self.instructions_button.is_clicked(event):
                        self.show_instructions = True
                    elif self.quit_button.is_clicked(event):
                        pygame.quit()
                        sys.exit()
            
            if not self.show_instructions:
                # Draw background
                self.screen.fill(BACKGROUND_COLOR)
                
                # Draw title
                title = self.title_font.render("Snake Game", True, TITLE_COLOR)
                title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 120))
                self.screen.blit(title, title_rect)
                
                # Draw animated snake in background
                self.draw_snake_animation()
                
                # Draw buttons
                self.play_button.draw(self.screen)
                self.ai_mode_button.draw(self.screen)
                self.instructions_button.draw(self.screen)
                self.quit_button.draw(self.screen)
                
                # Draw version and credits
                version_text = self.info_font.render("Version 1.0", True, TEXT_COLOR)
                self.screen.blit(version_text, (10, WINDOW_HEIGHT - 30))
                
                credits_text = self.info_font.render("© 2025 Snake Game", True, TEXT_COLOR)
                credits_rect = credits_text.get_rect(right=WINDOW_WIDTH - 10, bottom=WINDOW_HEIGHT - 10)
                self.screen.blit(credits_text, credits_rect)
            
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    menu = Menu()
    menu.run()