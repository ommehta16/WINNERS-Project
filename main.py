import pygame
from PIL import Image
import numpy as np
import sys
import math
import ui_elements


def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    # Set up display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('the thing')
    color = (0, 128, 255)
    # Main loop
    running = True
    frame = 0
    button = ui_elements.Button([0,0],[10,10])
    while running:
        
        prev_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                color = "red"
        
        
        # Fill the screen with a color
        screen.fill(color)
        
        pygame.draw.circle(screen,"red",pygame.mouse.get_pos(),
                           dist(pygame.mouse.get_pos(),prev_pos)+2)
        # DELETE THIS ^^^
        button.draw(screen)
        clock.tick(60)
        pygame.display.flip()
        frame+=1
        
        
        
    pygame.quit()

if (__name__ == "__main__"):
    main()