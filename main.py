import pygame
from PIL import Image
import numpy as np
import sys

def main():
    pygame.init()


# Set up display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('the thing')
    color = (0, 128, 255)
# Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                

        # Fill the screen with a color
        screen.fill(color)
    pygame.quit()

if (__name__ == "__main__"):
    main()