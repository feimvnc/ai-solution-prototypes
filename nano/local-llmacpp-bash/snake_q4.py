import pygame
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 640, 480
FPS = 30
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
snake = {"x": 320, "y": 240}
direction = {"up": False, "down": False, "left": False, "right": False}
food = {"x": WIDTH // 2 - 15, "y": HEIGHT // 2 + 15}
game_over = False
snake_speed = 60

while not game_over:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            game_over = True
        
    keys = pygame.key.get_pressed()
    
    if keys[K_LEFT]:
        snake["x"] -= snake_speed
    elif keys[K_RIGHT]:
        snake["x"] += snake_speed
    elif keys[K_UP]:
        snake["y"] -= snake_speed
    elif keys[K_DOWN]:
        snake["y"] += snake_speed
    
    if direction["up"] and snake["y"] > 0:
        snake["y"] = 0
        food["y"] += snake_speed // 2
        
    if direction["down"] and snake["y"] < HEIGHT:
        snake["y"] = HEIGHT - 1
    
    if direction["left"] and snake["x"] > 0:
        snake["x"] = 0
        food["x"] -= snake_speed // 2
        
    if direction["right"] and snake["x"] < WIDTH - 15:
        snake["x"] += snake_speed // 2
    
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (snake["x"], snake["y"], 30, 30))
    pygame.draw.rect(screen, RED, (food["x"], food["y"], 15, 15))
    
    if game_over:
        screen.fill(BLACK)
       #  text = font.render("Game Over! Press Q to Quit.", True, BLACK)
        text = "Game Over! Press Q to Quit."
        
        screen.blit(text, (200, 200))
        
    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()