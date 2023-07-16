import pygame
from pygame.locals import *

# Set screen size and background color
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Create snake object
class Snake():
    def __init__(self):
        self.positions = [(20, 20)]
        self.direction = (0, -1)
    
    def move(self):
        new_head = self.positions[0] + self.direction
        
        for pos in self.positions[1:]:
            if pygame.Rect(pos, 5).colliderect(pygame.Rect(new_head, 5)):
                self.positions.pop(self.positions.index(new_head))
                self.positions.append(new_head)
                
        self.positions.insert(0, new_head)
    
    def draw(self, surface):
        for pos in self.positions[:-1]:
            pygame.draw.rect(surface, (0, 0, 255), pygame.Rect(pos[0], pos[1], 5, 5))
            
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.positions[-1][0], self.positions[-1][1], 5, 5))

# Create snake game loop
run_snake_game = True
while run_snake_game:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            run_snake_game = False
        
    # Clear screen
    screen.fill((255, 255, 255))
    
    # Update snake positions and direction
    snake = Snake()
    
    # Draw snake on screen
    snake.draw(screen)
    
    # Update display
    pygame.display.flip()
    
    # Limit snake's speed
    clock.tick(30)

pygame.quit()
