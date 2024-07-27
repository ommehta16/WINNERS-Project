import pygame
from PIL import Image
import numpy as np
import sys
import math
import ui_elements


def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def main():
    # Set up pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('the thing')
    background_color = (120, 120, 120)

    running = True
    frame = 0
    button = ui_elements.Button([10,10],[25,25],lambda:0,_text="a")
    another_button = ui_elements.Button([100,100],[200,50],lambda:0,_text="broo")
    
    # Main loop
    while running:
        frame+=1
        prev_pos = pygame.mouse.get_pos()
        
        # Check on events
        clicked: bool = False 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:            running = False
            if event.type == pygame.MOUSEBUTTONDOWN: clicked = True
        
        # UPDATE EVERYTHING
        button.update(clicked)
        another_button.update(clicked)
        
        # DRAW EVERYTHING
        screen.fill(background_color)
        button.draw(screen)
        another_button.draw(screen)
        
        clock.tick(60)
        pygame.display.flip()
    
    pygame.quit()

if (__name__ == "__main__"):
    main()