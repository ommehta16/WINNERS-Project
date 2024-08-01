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
    edit_img_arr = effects.img_io.img_to_arr(img).astype(int)
    preview_img_arr = edit_img_arr

    #loading text function

    
    
    def get_options(func):
        nonlocal edit_img_arr, preview_img_arr, preview_rect, rescale, screen, side_bar
        # IT'S WAR CRIME TIME
        preview_img_arr = edit_img_arr
        clicked = False
        rescale = True
        callerID = ""
        tmp_font = pygame.font.SysFont("Calibri",30)
        for button in side_bar.buttons:
            if button.is_hovered:
                callerID = button.text
                break
        callerText = tmp_font.render(f"{callerID} Settings",True,(0,0,0))

        while True:
            moved = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN: clicked = True
                if event.type == pygame.MOUSEBUTTONUP: clicked = False
                if event.type == pygame.MOUSEMOTION: moved = True
                if event.type == pygame.VIDEORESIZE: screen = pygame.display.set_mode(screen.get_size(), pygame.RESIZABLE)
            adjust_block.update(clicked,moved)
            adjust_block.draw()
            if adjust_block.adjust.buttons[0].update(clicked):
                preview_img_arr = edit_img_arr
                screen = pygame.display.set_mode(screen.get_size(),pygame.RESIZABLE)
                return
            if adjust_block.adjust.buttons[1].update(clicked):
                preview_img_arr = edit_img_arr
                loadingtext(func)
                view_img = pygame.transform.scale(effects.img_io.pil_to_pyg(effects.img_io.arr_to_img(preview_img_arr)),preview_rect.size)
                screen.blit(view_img,preview_rect.topleft)
                pygame.display.set_caption("W    I    D    E • Previewing Image")
            if adjust_block.adjust.buttons[2].update(clicked):
                loadingtext(func)
                screen = pygame.display.set_mode(screen.get_size(),pygame.RESIZABLE)
                return
            
            screen.blit(callerText,(screen.get_width()/8 - callerText.get_width()/2,13.5/16*screen.get_height()-callerText.get_width()/2))
            pygame.display.update()
            clock.tick(30)

    def loadingtext(func):
        nonlocal screen, adjust_block
        loading_font = pygame.font.SysFont("free sans",min(30,screen.get_width()/20))
        loading_text_color = (0,0,0)
        loading_text = loading_font.render('Processing...',1,loading_text_color)
        screen.blit(loading_text,(screen.get_width()/8,adjust_block.adjust_bg.top))
        print((screen.get_width()/8,side_bar.rect.bottom))
        print((screen.get_width(),screen.get_height()))
        pygame.display.set_caption("W    I    D    E • Processing Image...")
        pygame.event.pump()
        pygame.display.update()
        func()
        pygame.display.set_caption('W    I    D    E')

    
    def blur():
        nonlocal preview_img_arr
        preview_img_arr = effects.convolute.Blur.gaussian(preview_img_arr,16,(adjust_block.get_slider_val()/2)+0.01)
        
    def dog():
        nonlocal preview_img_arr
        preview_img_arr = effects.convolute.EdgeDetect.dog(preview_img_arr,2,1.5,adjust_block.get_slider_val()/30)
        
    def contrast():
        nonlocal preview_img_arr
        preview_img_arr = effects.contrast.contrast(preview_img_arr,(adjust_block.get_slider_val()*2))
        
    def brightness():
        nonlocal preview_img_arr
        preview_img_arr = effects.brightness.brightness(preview_img_arr,adjust_block.get_slider_val())
        
    def sharpen():
        nonlocal preview_img_arr
        preview_img_arr = effects.sharpen.sharpen(preview_img_arr,adjust_block.get_slider_val()/50,2)
        
    def dither():
        nonlocal preview_img_arr
        preview_img_arr = effects.dither.dither(preview_img_arr,True)
        
    def sepia():
        nonlocal preview_img_arr
        preview_img_arr = effects.sepia.sepia(preview_img_arr,adjust_block.get_slider_val())
        
    def undo():
        nonlocal preview_img_arr
        preview_img_arr = effects.img_io.img_to_arr(img).astype(int)
        
    def invert():
        nonlocal preview_img_arr
        preview_img_arr = effects.invert.invert(preview_img_arr,(-(adjust_block.get_slider_val()*2)))
        
    def hue():
        nonlocal preview_img_arr
        preview_img_arr = effects.hue.hue_nine(preview_img_arr,int(adjust_block.get_slider_val()*3.6))
        

    clicked = False
    def change_image():
        nonlocal preview_img_arr, img, view_img, clicked
        clicked = False
        filepath = ui_elements.Prompt.get_file_open("Images (*.webp *.png *.jpg *.JPG *.jpeg *.JPEG)")
        if filepath:
            img=effects.img_io.open_img(filepath)
            view_img = effects.img_io.pil_to_pyg(img)
            preview_img_arr = effects.img_io.img_to_arr(img).astype(int)
            update_preview_area()
            return True
        return False
    
    def save_image():
        nonlocal preview_img_arr, clicked
        clicked = False
        filepath = ui_elements.Prompt.get_file_save()
        if filepath: effects.img_io.arr_to_img(preview_img_arr).save(filepath)

    def mul_image():
        nonlocal preview_img_arr, img, clicked
        clicked = False
        tmp_img_arr = effects.img_io.img_to_arr(img).astype(int)
        if tmp_img_arr.shape == preview_img_arr.shape: preview_img_arr = (preview_img_arr.astype(float)/255 * tmp_img_arr).astype(int)
    
    def add_image():
        nonlocal preview_img_arr, img, clicked
        clicked = False
        tmp_img_arr = effects.img_io.img_to_arr(img).astype(int)
        if tmp_img_arr.shape == preview_img_arr.shape: preview_img_arr = preview_img_arr + tmp_img_arr

    wrapped = [undo, lambda: get_options(blur), lambda: get_options(contrast), lambda: get_options(dither), lambda: get_options(sharpen), lambda: get_options(sepia), lambda: get_options(invert), lambda: get_options(brightness), lambda: get_options(dog), lambda: get_options(hue)]
    side_bar_buttons = [ (wrapped[i],
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
            edit_img_arr = preview_img_arr
            view_img = pygame.transform.scale(effects.img_io.pil_to_pyg(effects.img_io.arr_to_img(preview_img_arr)),preview_rect.size)

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