import pygame
from PIL import Image
import numpy as np
import sys
import math
import effects.img_io
from ui import ui_elements
import effects

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

    title_bar = ui_elements.ButtonGrid([0, 0], [screen.get_size()[0], 20], [0, 1])
    side_bar = ui_elements.ButtonGrid([0, 20], [screen.get_size()[0] * 1/4, screen.get_size()[1] - 20], [2, 5], hov_col=(0,114,182),col=(0,174,239))

    title_bar.add_button(_text="REPRODUCE", _onclick=lambda: title_bar.add_button(_onclick=lambda: print(ui_elements.Prompt.get_file_open()), _text="open file..."))

    slider = ui_elements.Slider((800, 500), (200, 20), 0.5, 0, 100)
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
        side_bar.add_button(_onclick=action, _text=text, _font_size=20)  # Use RGB tuple for color
        side_bar.buttons[-1].set_image(image_path)  # Set the image for the button

    img = effects.img_io.open_img("test/mountain.jpeg")
    img_arr = effects.img_io.img_to_arr(img)
    
    img_rat = img.size[1]/img.size[0]
    img_max = (screen.get_size()[0] - side_bar.rect.right,screen.get_size()[1] -title_bar.rect.bottom)
    preview_rect = pygame.Rect(side_bar.rect.right, title_bar.rect.bottom,
                            min(img_max[0],img_max[1]/img_rat),
                            min(img_max[1],img_max[0]*img_rat)
                            )
    preview_rect.center = (side_bar.rect.right + (screen.get_width()-side_bar.rect.right)/2, title_bar.rect.bottom + (screen.get_height()-title_bar.rect.bottom)/2)
    # Main loop
    while running:
        frame += 1
        prev_pos = pygame.mouse.get_pos()
        skip_frame = False

        # Check on events
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.VIDEORESIZE:  # Handle window resizing

                squished = pygame.transform.scale(screen,(max(event.w,600), max(event.h,400)))
                screen = pygame.display.set_mode((max(event.w,600), max(event.h,400)), pygame.RESIZABLE)
                screen.fill(background_color)
                pygame.display.update()
                side_bar.rect.update(side_bar.rect.left,side_bar.rect.top,screen.get_size()[0] * 1/4, screen.get_size()[1] - title_bar.rect.bottom)
                
                
                img_rat = img.size[1]/img.size[0]
                img_max = (screen.get_size()[0] - side_bar.rect.right,screen.get_size()[1] -title_bar.rect.bottom)
                preview_rect = pygame.Rect(side_bar.rect.right, title_bar.rect.bottom,
                                        min(img_max[0],img_max[1]/img_rat),
                                        min(img_max[1],img_max[0]*img_rat)
                                        )
                preview_rect.center = (side_bar.rect.right + (screen.get_width()-side_bar.rect.right)/2, title_bar.rect.bottom + (screen.get_height()-title_bar.rect.bottom)/2)
                view_img = pygame.transform.scale(effects.img_io.pil_to_pyg(img),preview_rect.size)
                skip_frame = True
            slider.handle_event(event)
        
        if skip_frame:
            continue
        # UPDATE EVERYTHING
        title_bar.update(clicked)
        side_bar.update(clicked)

        # DRAW EVERYTHING
        screen.fill(background_color)
        
        title_bar.draw()
        side_bar.draw()
        slider.draw(screen)
        
        
        # Draw the image preview
        screen.blit(view_img,preview_rect.topleft)
        
        clock.tick(60)
        pygame.display.flip()
        

    pygame.quit()

if __name__ == "__main__":
    main()