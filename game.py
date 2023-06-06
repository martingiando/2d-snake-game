import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Define the snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.positions = [(width // 2, height // 2)]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])  # noqa: E501
    
    def get_head_position(self):
        return self.positions[0]
    
    def move(self):
        cur = self.get_head_position()
        x, y = cur

        if self.direction == pygame.K_UP:
            y -= 10
        elif self.direction == pygame.K_DOWN:
            y += 10
        elif self.direction == pygame.K_LEFT:
            x -= 10
        elif self.direction == pygame.K_RIGHT:
            x += 10
        
        self.positions.insert(0, (x, y))
        
        if len(self.positions) > self.size:
            self.positions.pop()
    
    def change_direction(self, direction):
        if direction == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.direction = direction
        elif direction == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.direction = direction
        elif direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.direction = direction
        elif direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.direction = direction
    
    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, GREEN, (p[0], p[1], 10, 10))
    
    def check_collision(self):
        if self.get_head_position() in self.positions[1:]:
            return True
        
        if self.get_head_position()[0] < 0 or self.get_head_position()[0] >= width:
            return True
        
        if self.get_head_position()[1] < 0 or self.get_head_position()[1] >= height:
            return True
        
        return False

# Define the food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, (width // 10) - 1) * 10, random.randint(0, (height // 10) - 1) * 10)  # noqa: E501
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], 10, 10))  # noqa: E501

# Create the snake and food objects
snake = Snake()
food = Food()

# Set up the game clock
clock = pygame.time.Clock()

# Define fonts
font = pygame.font.SysFont(None, 36)

# Define game states
GAME_OVER = 0
PLAYING = 1

game_state = PLAYING
score = 0

# Function to display the score on the screen
def show_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

# Function to display the game over screen
def show_game_over_screen():
    game_over_text = font.render("Game Over", True, WHITE)
    restart_text = font.render("Press SPACE to restart or ESC to quit", True, WHITE)
    window.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))  # noqa: E501
    window.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + restart_text.get_height() // 2))  # noqa: E501

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == PLAYING:
                snake.change_direction(event.key)
            elif game_state == GAME_OVER:
                if event.key == pygame.K_SPACE:
                    game_state = PLAYING
                    snake = Snake()
                    food = Food()
                    score = 0
                elif event.key == pygame.K_ESCAPE:
                    running = False
    
    if game_state == PLAYING:
        # Move the snake
        snake.move()
        
        # Check for collision with food
        if snake.get_head_position() == food.position:
            snake.size += 1
            food.randomize_position()
            score += 1
        
        # Check for collision with boundaries or itself
        if snake.check_collision():
            game_state = GAME_OVER
    
    # Draw the game window
    window.fill(BLACK)
    snake.draw(window)
    food.draw(window)
    show_score()
    
    if game_state == GAME_OVER:
        show_game_over_screen()
    
    pygame.display.update()
    
    # Set the frame rate
    clock.tick(15)

# Quit the game
pygame.quit()
