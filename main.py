import pygame
from PIL import Image
import numpy as np
import sys
import math
import effects.contrast
import effects.convolute
import effects.dither
import effects.img_io
import effects.brightness
# import effects.hue
import effects.sepia
import effects.sharpen
# import effects.soften
from ui import ui_elements

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

BACKGROUND_COLOR = (245, 255, 250)  # Use RGB tuple instead of hex color

def numpy_to_pygame(np_img: np.ndarray) -> pygame.Surface:
    return effects.img_io.pil_to_pyg(effects.img_io.arr_to_img(np_img))

def main():
    # Set up pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
    pygame.display.set_caption('the thing')

    running = True
    frame = 0

    img = effects.img_io.open_img("test/chicken.webp")
    img_arr = effects.img_io.img_to_arr(img).astype(int)

    title_bar = ui_elements.ButtonGrid([0, 0], [screen.get_size()[0], 20], [0, 1])
    side_bar = ui_elements.ButtonGrid([0, 20], [screen.get_size()[0] * 1/4, screen.get_size()[1] - 20], [2, 5], hov_col=(0, 114, 182), col=(0, 174, 239))
    def change_image(filepath:str):
        nonlocal img_arr, img, view_img
        print(filepath)
        if filepath:
            img=effects.img_io.open_img(filepath)
            view_img = effects.img_io.pil_to_pyg(img)
            img_arr = effects.img_io.img_to_arr(img).astype(int)
            update_preview_area()
            return True
        return False
    def save_image(filepath:str):
        nonlocal img_arr
        if filepath:
            img = effects.img_io.arr_to_img(img_arr)
            img.save(filepath)


    title_bar.add_button(_text="open image",_onclick=lambda:change_image(ui_elements.Prompt.get_file_open("Images (*.webp *.png *.jpg *.JPG *.jpeg *.JPEG)")))
    title_bar.add_button(_text="save image",_onclick=lambda:save_image(ui_elements.Prompt.get_file_save()))
    title_bar.add_button(_text="REPRODUCE", _onclick=lambda: title_bar.add_button(_onclick=lambda: print(ui_elements.Prompt.get_file_open()), _text="open file..."))

    # Update the slider position to be within the sidebar
    slider = ui_elements.Slider((side_bar.rect.width // 2, side_bar.rect.bottom - 50), (side_bar.rect.width - 40, 20), 0, 0, 100)

    def update_preview_area():
        nonlocal preview_rect, screen, side_bar, title_bar, img
        img_rat = img.size[1]/img.size[0]
        img_max = (screen.get_size()[0] - side_bar.rect.right,screen.get_size()[1] -title_bar.rect.bottom)
        preview_rect = pygame.Rect(side_bar.rect.right, title_bar.rect.bottom,min(img_max[0],img_max[1]/img_rat),min(img_max[1],img_max[0]*img_rat))
        preview_rect.center = (side_bar.rect.right + (screen.get_width()-side_bar.rect.right)/2, title_bar.rect.bottom + (screen.get_height()-title_bar.rect.bottom)/2)
    # Create the sidebar buttons
    def blur():         nonlocal img_arr; img_arr = effects.convolute.Blur.gaussian (img_arr,16,(slider.get_value()/2)+0.01 )
    def dog():          nonlocal img_arr; img_arr = effects.convolute.EdgeDetect.dog(img_arr,2,1.5,2.5                      )
    def contrast():     nonlocal img_arr; img_arr = effects.contrast.contrast       (img_arr,   slider.get_value())
    def brightness():   nonlocal img_arr; img_arr = effects.brightness.brightness   (img_arr,   slider.get_value()          )
    def sharpen():      nonlocal img_arr; img_arr = effects.sharpen.sharpen         (img_arr,   slider.get_value(),1        )
    def dither():       nonlocal img_arr; img_arr = effects.dither.dither           (img_arr,True)
    def sepia():        nonlocal img_arr; img_arr = effects.sepia.sepia             (img_arr,   slider.get_value()          )
    def undo():         nonlocal img_arr; img_arr = effects.img_io.img_to_arr(img).astype(int)
    # def soften(): nonlocal img_arr; img_arr = effects.soften.soften(img_arr,slider.get_value())
    side_bar_buttons = [
        (undo,"images/icons/effects/undo.png", "Reset"),
        (blur, "images/icons/effects/blur.png", "Blur"),
        (contrast, "images/icons/effects/contrast.png", "Contrast"),
        (dither, "images/icons/effects/dither.png", "Dither"),
        (sharpen, "images/icons/effects/sharpen.png", "Sharpen"),
        (sepia, "images/icons/effects/sepia.png", "Sepia"),
        (lambda: 0, "images/icons/effects/soften.png", "Soften"),
        (brightness, "images/icons/effects/brightness.png", "Brightness"),
        (dog, "images/icons/effects/dog.png", "Dog"),
        (lambda: 0, "images/icons/effects/hue.png", "Hue")
    ]


    preview_rect = pygame.Rect(1,1,1,1)

    for action, image_path, text in side_bar_buttons:
        side_bar.add_button(_onclick=action, _text=text, _font_size=20)
        side_bar.buttons[-1].set_image(image_path)
    update_preview_area()
    on_title = True

    title_font = pygame.font.SysFont("free sans",24)
    text1 = title_font.render('Welcome to Winners Image Data Editor (WIDE), ', True, (0, 0, 0))
    text1_1 = title_font.render('an image editor built in Python using Pygame and Pillow.', True, (0, 0, 0))
    text2 = title_font.render('To continue, please upload a file.', True, (0, 0, 0))
    def title_img_set():
        nonlocal on_title
        if change_image(ui_elements.Prompt.get_file_open("Images (*.webp *.png *.jpg *.JPG *.jpeg *.JPEG)")):
            on_title = False

    
    screen = pygame.display.set_mode((800,600))  # Make window resizable
    start_up_button = ui_elements.Button((433,348),(80,40),title_img_set,_text="upload",_fontsize=24,_font="free sans")
    while on_title:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(text1, (screen.get_width()/2-text1.get_width()/2,screen.get_height()/2-text1.get_height()/2))
        screen.blit(text1_1, (screen.get_width()/2-text1_1.get_width()/2,screen.get_height()/2+text1.get_height()/2))
        screen.blit(text2, (screen.get_width()/2-text2.get_width()/2,screen.get_height()/2+2*text2.get_height()))
        start_up_button.draw()
        for event in pygame.event.get():
            clicked = False
            if event.type == pygame.QUIT:
                running = False
                on_title = False
            if event.type == pygame.MOUSEBUTTONUP:
                on_title = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
        start_up_button.update(clicked)
        pygame.display.update()
        clock.tick(10)
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # Make window resizable
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
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()