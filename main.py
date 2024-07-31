import pygame
from PIL import Image
import numpy as np
import effects.contrast
import effects.convolute
import effects.dither
import effects.hue
import effects.img_io
import effects.brightness
import effects.invert
import effects.sepia
import effects.sharpen
from ui import ui_elements
import multiprocessing as mp
import time

BACKGROUND_COLOR = (245, 255, 250)  # Use RGB tuple instead of hex color

def main():
    # Set up pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    pygame.display.set_caption('W    I    D    E')

    running = True
    frame = 0

    img = effects.img_io.open_img("test/chicken.webp")
    img_arr = effects.img_io.img_to_arr(img).astype(int)
    
    # Create the sidebar buttons
    effect_names = ["Reset","Blur","Contrast","Dither","Sharpen","Sepia","Invert","Brightness","Drawing","Hue"]
    def blur():         nonlocal img_arr; img_arr = effects.convolute.Blur.gaussian (img_arr,16,(slider.get_value()/2)+0.01 )
    def dog():          nonlocal img_arr; img_arr = effects.convolute.EdgeDetect.dog(img_arr,2,1.5,slider.get_value()/30    )
    def contrast():     nonlocal img_arr; img_arr = effects.contrast.contrast       (img_arr,   (slider.get_value()*2)      )
    def brightness():   nonlocal img_arr; img_arr = effects.brightness.brightness   (img_arr,   slider.get_value()          )
    def sharpen():      nonlocal img_arr; img_arr = effects.sharpen.sharpen         (img_arr,   slider.get_value()/50,2     )
    def dither():       nonlocal img_arr; img_arr = effects.dither.dither           (img_arr,True)
    def sepia():        nonlocal img_arr; img_arr = effects.sepia.sepia             (img_arr,   slider.get_value()          )
    def undo():         nonlocal img_arr; img_arr = effects.img_io.img_to_arr(img).astype(int)
    def invert():       nonlocal img_arr; img_arr = effects.invert.invert           (img_arr,   (-(slider.get_value()*2))   )
    def hue():          nonlocal img_arr; img_arr = effects.hue.hue                 (img_arr,   (slider.get_value()*3.6)    )
    side_bar_buttons = [ ([undo,blur,contrast,dither,sharpen,sepia,invert,brightness,dog,hue][i],
                          f"images/icons/effects/{effect_names[i].lower()}.png", effect_names[i]) for i in range(len(effect_names))]
    
    title_bar = ui_elements.ButtonGrid([0, 0], [screen.get_size()[0], 20], [0, 1])
    side_bar  = ui_elements.ButtonGrid([0, 20], [screen.get_size()[0] * 1/4, screen.get_size()[1] - 20], [2, 8], hov_col=(0, 114, 182), col=(0, 174, 239),font_size=20,buttons=side_bar_buttons)
    # Update the slider position to be within the sidebar
    slider = ui_elements.Slider((side_bar.rect.width // 2, side_bar.rect.bottom - 150), (side_bar.rect.width - 40, 20), 0, 0, 100)
    clicked = False
    def change_image(filepath:str):
        nonlocal img_arr, img, view_img, clicked
        clicked = False
        if filepath:
            img=effects.img_io.open_img(filepath)
            view_img = effects.img_io.pil_to_pyg(img)
            img_arr = effects.img_io.img_to_arr(img).astype(int)
            update_preview_area()
            return True
        return False
    def save_image(filepath:str):
        nonlocal img_arr, clicked
        clicked = False
        if filepath: effects.img_io.arr_to_img(img_arr).save(filepath)

    def update_preview_area():
        nonlocal preview_rect, screen, side_bar, title_bar, img
        img_rat = img.size[1]/img.size[0]
        img_max = (screen.get_size()[0] - side_bar.rect.right,screen.get_size()[1] -title_bar.rect.bottom)
        preview_rect = pygame.Rect(side_bar.rect.right, title_bar.rect.bottom,min(img_max[0],img_max[1]/img_rat),min(img_max[1],img_max[0]*img_rat))
        preview_rect.center = (side_bar.rect.right + (screen.get_width()-side_bar.rect.right)/2, title_bar.rect.bottom + (screen.get_height()-title_bar.rect.bottom)/2)

    # Show slider
    # Show text above slider = "Apply" + effect name
    # Show label(s) for slider(s): intensity, power, min, max, etc.
    # Show buttons to APPLY | PREVIEW | CANCEL
    # CANCEL --> stop and do nothing
    # PREVIEW --> generate effect, show preview on image BUT don't change img_arr
    # APPLY --> generate effect, change img_arr. If a preview has been generated with the current params, use said preview
 
    
    title_bar.add_button(_text="open image",_onclick=lambda:change_image(ui_elements.Prompt.get_file_open("Images (*.webp *.png *.jpg *.JPG *.jpeg *.JPEG)")))
    title_bar.add_button(_text="save image",_onclick=lambda:save_image(ui_elements.Prompt.get_file_save()))
    
    adjust = ui_elements.ButtonGrid([0, side_bar.buttons[-1].rect.bottom], [screen.get_size()[0] * 1/4, 20], [3, 1])
    adjust.add_button(_text="CANCEL",_onclick=lambda:change_image(ui_elements.Prompt.get_file_open("Images (*.webp *.png *.jpg *.JPG *.jpeg *.JPEG)")))
    adjust.add_button(_text="PREVIEW",_onclick=lambda:save_image(ui_elements.Prompt.get_file_save()))
    adjust.add_button(_text="APPLY",_onclick=lambda:save_image(ui_elements.Prompt.get_file_save()))
    adjust_bg = pygame.rect.Rect([0, side_bar.buttons[-1].rect.bottom],[screen.get_size()[0] * 1/4, screen.get_size()[1]-side_bar.buttons[-1].rect.bottom])

    preview_rect = pygame.Rect(1,1,1,1)
    update_preview_area()
    

    #getting slider value in text
    slider_font = pygame.font.SysFont("free sans",30)
    slider_text_color = (0,0,0)
    
    ui_elements.title_screen(change_image,BACKGROUND_COLOR)
    
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # Make window resizable
    rescale = False
    since_resize = 0
    # Main loop
    while running:
        clock.tick(30)
        frame += 1
        since_resize += 1

        slider_value_text = slider_font.render(f'{int(slider.get_value())}',1,slider_text_color)
        
        # Check on events
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
            if event.type == pygame.VIDEORESIZE:  # Handle window resizing
                screen = pygame.display.set_mode((max(event.w,600), max(event.h,400)), pygame.RESIZABLE)
                screen.fill(BACKGROUND_COLOR)
                pygame.display.update()
                since_resize = 0
                side_bar.rect.update(side_bar.rect.left,side_bar.rect.top,screen.get_size()[0] * 1/4, screen.get_size()[1] - title_bar.rect.bottom)
                update_preview_area()
            if event.type == pygame.MOUSEMOTION:
                moved = True

        if rescale or since_resize < 5:
            adjust.rect.update(adjust.rect.left,screen.get_size()[1]-max((screen.get_size()[1] - side_bar.buttons[-1].rect.bottom)/4,20),screen.get_size()[0] * 1/4, max((screen.get_size()[1] - side_bar.buttons[-1].rect.bottom)/4,20))
            adjust_bg.update([0, side_bar.buttons[-1].rect.bottom],[screen.get_size()[0] * 1/4, screen.get_size()[1]-side_bar.buttons[-1].rect.bottom])
            slider.rect.center = (adjust_bg.centerx,adjust_bg.centery+adjust_bg.height/8)
            slider.rect.size = (adjust_bg.width-40,20)
            view_img = pygame.transform.scale(effects.img_io.pil_to_pyg(effects.img_io.arr_to_img(img_arr)),preview_rect.size)

        # UPDATE BUTTONS
        rescale = False
        slider.update(clicked,moved)
        if slider.selected: clicked_a = False
        else: clicked_a = clicked
        if side_bar.update(clicked_a) or title_bar.update(clicked_a):
            rescale = True
        adjust.update(clicked_a)

        # DRAW EVERYTHING
        screen.fill(BACKGROUND_COLOR)
        title_bar.draw()
        side_bar.draw()
        screen.blit(view_img,preview_rect.topleft)
        pygame.draw.rect(screen,"dark gray", adjust_bg)
        adjust.draw()
        slider.draw()
        screen.blit(slider_value_text, (slider.rect.left,slider.rect.top - slider_value_text.get_height()))
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()