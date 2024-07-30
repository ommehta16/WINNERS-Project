import pygame
from PIL import Image
import numpy as np
import sys
import math
import effects.convolute
import effects.dither
import effects.img_io
import effects.brightness
import effects.hue
from ui import ui_elements


def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

BACKGROUND_COLOR = (245, 255, 250)  # Use RGB tuple instead of hex color

def numpy_to_pygame(np_img:np.ndarray) -> pygame.Surface:
    return effects.img_io.pil_to_pyg(effects.img_io.arr_to_img(np_img))

def main():
    # Set up pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)  # Make window resizable
    pygame.display.set_caption('the thing')

    running = True
    frame = 0

    title_bar = ui_elements.ButtonGrid([0, 0], [screen.get_size()[0], 20], [0, 1])
    side_bar = ui_elements.ButtonGrid([0, 20], [screen.get_size()[0] * 1/4, screen.get_size()[1] - 20], [2, 5], hov_col=(0, 114, 182), col=(0, 174, 239))
    title_bar.add_button(_text="REPRODUCE", _onclick=lambda: title_bar.add_button(_onclick=lambda: print(ui_elements.Prompt.get_file_open()), _text="open file..."))

    # Update the slider position to be within the sidebar
    slider = ui_elements.Slider((side_bar.rect.width // 2, side_bar.rect.bottom - 50), (side_bar.rect.width - 40, 20), 0, 0, 100)
    
    img = effects.img_io.open_img("test/time-transfixed.jpg")
    img_arr = effects.img_io.img_to_arr(img).astype(int)
    def update_preview_area():
        nonlocal preview_rect, screen, side_bar, title_bar
        img_rat = img.size[1]/img.size[0]
        img_max = (screen.get_size()[0] - side_bar.rect.right,screen.get_size()[1] -title_bar.rect.bottom)
        preview_rect = pygame.Rect(side_bar.rect.right, title_bar.rect.bottom,min(img_max[0],img_max[1]/img_rat),min(img_max[1],img_max[0]*img_rat))
        preview_rect.center = (side_bar.rect.right + (screen.get_width()-side_bar.rect.right)/2, title_bar.rect.bottom + (screen.get_height()-title_bar.rect.bottom)/2)
    # Create the sidebar buttons

    def blur():
        nonlocal img_arr
        img_arr = effects.convolute.Blur.gaussian(img_arr,16,(slider.get_value()/2)+0.01)
    
    def dog():
        nonlocal img_arr
        img_arr = effects.convolute.EdgeDetect.dog(img_arr,2,1.5,2.5)

    side_bar_buttons = [
        (blur, "images/icons/effects/blur.png", "Blur"),
        (lambda: 0, "images/icons/effects/contrast.png", "Contrast"),
        (lambda: 0, "images/icons/effects/dither.png", "Dither"),
        (lambda: 0, "images/icons/effects/sharpen.png", "Sharpen"),
        (lambda: 0, "images/icons/effects/sepia.png", "Sepia"),
        (lambda: 0, "images/icons/effects/soften.png", "Soften"),
        (lambda: 0, "images/icons/effects/brightness.png", "Brightness"),
        (dog, "images/icons/effects/dog.png", "Dog"),
        (lambda: 0, "images/icons/effects/hue.png", "Hue")
    ]
    preview_rect = pygame.Rect(1,1,1,1)

    for action, image_path, text in side_bar_buttons:
        side_bar.add_button(_onclick=action, _text=text, _font_size=20)
        side_bar.buttons[-1].set_image(image_path)
    update_preview_area()

    # Main loop
    while running:
        frame += 1
        skip_frame = False

        # Check on events
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.VIDEORESIZE:  # Handle window resizing
                screen = pygame.display.set_mode((max(event.w,600), max(event.h,400)), pygame.RESIZABLE)
                screen.fill(BACKGROUND_COLOR)
                pygame.display.update()
                
                side_bar.rect.update(side_bar.rect.left,side_bar.rect.top,screen.get_size()[0] * 1/4, screen.get_size()[1] - title_bar.rect.bottom)
                update_preview_area()
                skip_frame = True
            slider.handle_event(event)
        if skip_frame: continue

        view_img = pygame.transform.scale(effects.img_io.pil_to_pyg(effects.img_io.arr_to_img(img_arr)),preview_rect.size)
        
        # UPDATE BUTTONS
        title_bar.update(clicked)
        side_bar.update(clicked)

        # DRAW EVERYTHING
        screen.fill(BACKGROUND_COLOR)
        title_bar.draw()
        side_bar.draw()
        slider.draw(screen)
        screen.blit(view_img,preview_rect.topleft)
        
        clock.tick(30)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()