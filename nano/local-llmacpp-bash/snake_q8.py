import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the window dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
DISPLAYSURFACE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Create a surface to draw on
SCREEN = pygame.display.set_mode(DISPLAYSURFACE)

# Set the background color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN.fill(WHITE)

# Create a snake object
class Snake:
    def __init__(self):
        self.positions = [(10, 10)]
        self.direction = "right"
        self.speed = 2
    
    def move(self):
        if not self.positions[0] in self:
            raise ValueError("Snake is moving into itself!")
        
        new_head = (self.positions[-1][0], self.positions[-1][1])
        new_tail = (self.positions[0][0], self.positions[0][1])
        
        if self.direction == "right":
            new_head += (0, -1)
            new_tail -= (0, 1)
        elif self.direction == "left":
            new_head -= (0, 1)
            new_tail += (0, -1)
        elif self.direction == "up":
            new_head = (self.positions[-1][0], self.positions[0][1])
            new_tail = (self.positions[0][0], self.positions[-1][1])
        else:
            new_head = (self.positions[0][0], self.positions[0][1])
            new_tail = (self.positions[-1][0], self.positions[-1][1])
        
        self.positions[:] = [new_head, new_tail]
    
    def draw(self):
        for pos in self.positions:
            pygame.draw.rect(SCREEN, BLACK)
            SCREEN.fill((255, 0, 0, 0))
            
            pygame.draw.rect(SCREEN, (0, 0, 0), pos[0], (self.speed, self.direction))


snake = Snake()
snake.draw()            


game_over = False
snake_speed = 60

while not game_over:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            game_over = True
    snake = Snake()
    snake.draw()  
        
    pygame.display.update()
