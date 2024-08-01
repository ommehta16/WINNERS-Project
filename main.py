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

BACKGROUND_COLOR = (245, 255, 250)
EFFECT_NAMES = ["Reset","Blur","Contrast","Dither","Sharpen","Sepia","Invert","Brightness","Drawing","Hue"]
TITLE_NAMES = ["OPEN","SAVE","MULTIPLY","ADD"]

def main():
    # Set up pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    pygame.display.set_caption('W    I    D    E')

    img = effects.img_io.open_img("test/chicken.webp")
    img_arr = effects.img_io.img_to_arr(img).astype(int)
    
    def blur():         nonlocal img_arr; img_arr = effects.convolute.Blur.gaussian (img_arr,16,(adjust_block.get_slider_val()/2)+0.01 )
    def dog():          nonlocal img_arr; img_arr = effects.convolute.EdgeDetect.dog(img_arr,2,1.5,adjust_block.get_slider_val()/30    )
    def contrast():     nonlocal img_arr; img_arr = effects.contrast.contrast       (img_arr,   (adjust_block.get_slider_val()*2)      )
    def brightness():   nonlocal img_arr; img_arr = effects.brightness.brightness   (img_arr,   adjust_block.get_slider_val()          )
    def sharpen():      nonlocal img_arr; img_arr = effects.sharpen.sharpen         (img_arr,   adjust_block.get_slider_val()/50,2     )
    def dither():       nonlocal img_arr; img_arr = effects.dither.dither           (img_arr,True)
    def sepia():        nonlocal img_arr; img_arr = effects.sepia.sepia             (img_arr,   adjust_block.get_slider_val()          )
    def undo():         nonlocal img_arr; img_arr = effects.img_io.img_to_arr(img).astype(int)
    def invert():       nonlocal img_arr; img_arr = effects.invert.invert           (img_arr,   (-(adjust_block.get_slider_val()*2))   )
    def hue():          nonlocal img_arr; img_arr = effects.hue.hue_nine         (img_arr,   int(adjust_block.get_slider_val()*3.6)    )

    clicked = False
    def change_image():
        nonlocal img_arr, img, view_img, clicked
        clicked = False
        filepath = ui_elements.Prompt.get_file_open("Images (*.webp *.png *.jpg *.JPG *.jpeg *.JPEG)")
        if filepath:
            img=effects.img_io.open_img(filepath)
            view_img = effects.img_io.pil_to_pyg(img)
            img_arr = effects.img_io.img_to_arr(img).astype(int)
            update_preview_area()
    
    def save_image():
        nonlocal img_arr, clicked
        clicked = False
        filepath = ui_elements.Prompt.get_file_save()
        if filepath: effects.img_io.arr_to_img(img_arr).save(filepath)

    def mul_image():
        nonlocal img_arr, img, clicked
        clicked = False
        tmp_img_arr = effects.img_io.img_to_arr(img).astype(int)
        if tmp_img_arr.shape == img_arr.shape: img_arr = (img_arr.astype(float)/255 * tmp_img_arr).astype(int)
    
    def add_image():
        nonlocal img_arr, img, clicked
        clicked = False
        tmp_img_arr = effects.img_io.img_to_arr(img).astype(int)
        if tmp_img_arr.shape == img_arr.shape: img_arr = img_arr + tmp_img_arr

    side_bar_buttons = [ ([undo,blur,contrast,dither,sharpen,sepia,invert,brightness,dog,hue][i],
                          f"images/icons/effects/{EFFECT_NAMES[i].lower()}.png", EFFECT_NAMES[i]) for i in range(len(EFFECT_NAMES))]
    
    title_bar_buttons = [ ([change_image,save_image,mul_image,add_image][i], "", TITLE_NAMES[i]) for i in range(len(TITLE_NAMES))]

    title_bar = ui_elements.ButtonGrid([0, 0], [screen.get_size()[0], 20], [0, 1],buttons=title_bar_buttons)
    side_bar  = ui_elements.ButtonGrid([0, 20], [screen.get_size()[0] * 1/4, screen.get_size()[1] - 20], [2, 8], hov_col=(0, 114, 182), col=(0, 174, 239),font_size=20,buttons=side_bar_buttons)

    def update_preview_area():
        nonlocal preview_rect, screen, side_bar, title_bar, img
        img_rat = img.size[1]/img.size[0]
        img_max = (screen.get_size()[0] - side_bar.rect.right,screen.get_size()[1] -title_bar.rect.bottom)
        preview_rect = pygame.Rect(side_bar.rect.right, title_bar.rect.bottom,min(img_max[0],img_max[1]/img_rat),min(img_max[1],img_max[0]*img_rat))
        preview_rect.center = (side_bar.rect.right + (screen.get_width()-side_bar.rect.right)/2, title_bar.rect.bottom + (screen.get_height()-title_bar.rect.bottom)/2) 
    
    adjust_block = ui_elements.adjustmentTile(screen,side_bar.buttons[-1].rect.bottom,lambda:0,lambda:0)

    preview_rect = pygame.Rect(1,1,1,1)
    update_preview_area()
    
    ui_elements.title_screen(change_image,BACKGROUND_COLOR)
    
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    rescale = False
    since_resize = 0
    running = True
    while running:
        clock.tick(30)
        since_resize += 1
        
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.MOUSEBUTTONDOWN: clicked = True
            if event.type == pygame.MOUSEBUTTONUP: clicked = False
            if event.type == pygame.MOUSEMOTION: moved = True
            
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((max(event.w,600), max(event.h,400)), pygame.RESIZABLE)
                screen.fill(BACKGROUND_COLOR)
                pygame.display.update()

                since_resize = 0
                side_bar.rect.update(side_bar.rect.left,side_bar.rect.top,screen.get_size()[0] * 1/4, screen.get_size()[1] - title_bar.rect.bottom)
                update_preview_area()

        if rescale or since_resize < 5:
            adjust_block.update_size(screen,side_bar.buttons[-1].rect.bottom)
            view_img = pygame.transform.scale(effects.img_io.pil_to_pyg(effects.img_io.arr_to_img(img_arr)),preview_rect.size)

        rescale = False
        clicked_a = adjust_block.update(clicked,moved)
        if side_bar.update(clicked_a) or title_bar.update(clicked_a):
            rescale = True
        adjust_block.adjust.update(clicked_a)

        screen.fill(BACKGROUND_COLOR)
        title_bar.draw()
        side_bar.draw()
        screen.blit(view_img,preview_rect.topleft)
        
        adjust_block.draw()
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()