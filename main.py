import pygame
from PIL import Image
import numpy as np
import sys
import math
from ui import ui_elements
from effects import *

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def main():
    # Set up pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)  # Make window resizable
    pygame.display.set_caption('the thing')
    background_color = (245, 255, 250)  # Use RGB tuple instead of hex color

    running = True
    frame = 0

    # TEMP --> 
    title_bar = ui_elements.ButtonGrid([0, 0], [screen.get_size()[0], 20], [0, 1])
    side_bar = ui_elements.ButtonGrid([0, 20], [screen.get_size()[0] / 6, screen.get_size()[1] - 20], [1, 9])  # Adjusted grid size for buttons

    title_bar.add_button(_text="REPRODUCE", _onclick=lambda: title_bar.add_button(_onclick=lambda: print(ui_elements.Prompt.get_file_open()), _text="open file..."))
    side_bar.add_button(_text="REPRODUCE", _onclick=lambda: 0, _minor_axis_size_spec=side_bar.size[0] / 2)
    side_bar.buttons[0].set_image("images/ex.png")

    # <-- TEMP
    slider = ui_elements.Slider((400, 500), (200, 20), 0.5, 0, 100)

    # Create the sidebar buttons
    side_bar_buttons = [
        (lambda: print("blur time"), "images/icons/effects/blur.png", "Blur"),
        (lambda: print("contrast time"), "images/icons/effects/contrast.png", "Contrast"),
        (lambda: print("dither time"), "images/icons/effects/dither.png", "Dither"),
        (lambda: print("sharpen time"), "images/icons/effects/sharpen.png", "Sharpen"),
        (lambda: print("sepia time"), "images/icons/effects/sepia.png", "Sepia"),
        (lambda: print("soften time"), "images/icons/effects/soften.png", "Soften"),
        (lambda: print("brightness time"), "images/icons/effects/brightness.png", "Brightness"),
        (lambda: print("dog time"), "images/icons/effects/dog.png", "Dog"),
        (lambda: print("hue time"), "images/icons/effects/hue.png", "Hue")
    ]
    
    for action, image_path, text in side_bar_buttons:
        side_bar.add_button(_onclick=action, _text=text, _color=(0, 174, 239))  # Use RGB tuple for color
        side_bar.buttons[-1].set_image(image_path)  # Set the image for the button

    # Create a surface for the image preview
    preview_rect = pygame.Rect(screen.get_size()[0] / 6 + 20, 20, screen.get_size()[0] * 5 / 6 - 40, screen.get_size()[1] - 40)
    preview_image = pygame.image.load("images/icons/effects/sharpen.png")  # Load your preview image here
    preview_image = pygame.transform.scale(preview_image, (preview_rect.width, preview_rect.height))

    # Main loop
    while running:
        frame += 1
        prev_pos = pygame.mouse.get_pos()

        # Check on events
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.VIDEORESIZE:  # Handle window resizing
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                preview_rect = pygame.Rect(screen.get_size()[0] / 6 + 20, 20, screen.get_size()[0] * 5 / 6 - 40, screen.get_size()[1] - 40)
                preview_image = pygame.transform.scale(preview_image, (preview_rect.width, preview_rect.height))
            slider.handle_event(event)

        # UPDATE EVERYTHING
        title_bar.update(clicked)
        side_bar.update(clicked)

        # DRAW EVERYTHING
        screen.fill(background_color)
        
        title_bar.draw()
        side_bar.draw()
        slider.draw(screen)
        
        
        # Draw the image preview
        screen.blit(preview_image, preview_rect.topleft)
        
        clock.tick(60)
        pygame.display.flip()
        

    pygame.quit()

if __name__ == "__main__":
    main()