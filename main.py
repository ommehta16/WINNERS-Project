import pygame
from PIL import Image
import numpy as np
import sys


def dist_squared(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def main():
    pygame.init()


    # Set up display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('the thing')
    color = (0, 128, 255)
    # Main loop
    running = True
    frame = 0
    while running:
        prev_time = pygame.time.get_ticks()
        
        prev_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                color = "red"
        
        
        # Fill the screen with a color
        screen.fill(color)
        pygame.draw.circle(screen,"red",pygame.mouse.get_pos(),dist_squared(pygame.mouse.get_pos(),prev_pos)/100+10)
        pygame.time.delay(max(0,pygame.time.get_ticks() + 16 - prev_time))
        pygame.display.flip()
        frame+=1
        
        
        
    pygame.quit()

if (__name__ == "__main__"):
    main()