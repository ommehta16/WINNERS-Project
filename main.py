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

BACKGROUND_COLOR = (245, 255, 250)
EFFECT_NAMES = ["Reset","Blur","Contrast","Dither","Sharpen","Sepia","Invert","Brightness","Drawing","Hue"]
TITLE_NAMES = ["OPEN","SAVE","MULTIPLY","ADD"]
NAME = "W    I    D    E"

def main():
    # General variable initialization work
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    pygame.display.set_caption(NAME)
    img = effects.img_io.open_img("test/chicken.webp")
    preview_img_arr = effects.img_io.img_to_arr(img).astype(int)
    clicked = False
    pygame.display.set_icon(pygame.image.load("images/icons/icon512.png"))

    # Wrapper for the functions that apply effects: allows for the preview/tweaking mode
    def get_options(effect):
        nonlocal preview_img_arr, preview_rect, screen, side_bar, since_resize
        bg = screen.copy()
        edit_img_arr = preview_img_arr # edit_img_arr lags behind preview_img_arr: the former is the final/saved state, the latter is our 'test'/reversible changes
        clicked = False
        callerID = ""
        for button in side_bar.buttons:
            if button.is_hovered:
                callerID = button.text
                break
        if callerID == "Hue": adjust_block.unit = "°"
        else: adjust_block.unit = "%"
        callerText = pygame.font.SysFont("Calibri",30).render(f"{callerID} Settings",True,(0,0,0)) # Create the label text for the effect being used
        view_img = pygame.transform.scale(effects.img_io.pil_to_pyg(effects.img_io.arr_to_img(preview_img_arr)),preview_rect.size)
        while True:
            screen.blit(bg,(0,0)) # Fix to some screen-filling issues
            clicked, moved, running, _, _ = handle_events(clicked,0)
            if not running: quit()
            adjust_block.update(clicked,moved)
            adjust_block.draw()

            # (I really should've replaced these with _onclick actions)
            # We check if each button has been pressed, then take the corresponding action
            if adjust_block.adjust.buttons[0].update(clicked): # Cancel
                preview_img_arr = edit_img_arr
                since_resize = 0
                return
            if adjust_block.adjust.buttons[1].update(clicked): # Preview
                preview_img_arr = edit_img_arr
                loadingtext(effect, adjust_block)
                view_img = pygame.transform.scale(effects.img_io.pil_to_pyg(effects.img_io.arr_to_img(preview_img_arr)),preview_rect.size)
                pygame.display.set_caption(f"{NAME} • Previewing Image")
            if adjust_block.adjust.buttons[2].update(clicked): # Apply
                preview_img_arr = edit_img_arr
                loadingtext(effect, adjust_block)
                edit_img_arr = preview_img_arr
                since_resize = 0
                return
            screen.blit(view_img,preview_rect.topleft)
            screen.blit(callerText,(screen.get_width()/8 - callerText.get_width()/2,13.5/16*screen.get_height()-callerText.get_width()/2))
            pygame.display.update()
            clock.tick(30)

    # Define 0-arg functions that change the image array
    def blur():      nonlocal preview_img_arr; preview_img_arr = effects.convolute.Blur.gaussian(preview_img_arr,16,(adjust_block.get_slider_val()/2)+0.01)
    def dog():       nonlocal preview_img_arr; preview_img_arr = effects.convolute.EdgeDetect.dog(preview_img_arr,2,1.5,adjust_block.get_slider_val()/30)
    def contrast():  nonlocal preview_img_arr; preview_img_arr = effects.contrast.contrast(preview_img_arr,(adjust_block.get_slider_val()*2))
    def brightness():nonlocal preview_img_arr; preview_img_arr = effects.brightness.brightness(preview_img_arr,adjust_block.get_slider_val())
    def sharpen():   nonlocal preview_img_arr; preview_img_arr = effects.sharpen.sharpen(preview_img_arr,adjust_block.get_slider_val()/50,2)
    def dither():    nonlocal preview_img_arr; preview_img_arr = effects.dither.dither(preview_img_arr,bool(round(adjust_block.get_slider_val()/100)))
    def sepia():     nonlocal preview_img_arr; preview_img_arr = effects.sepia.sepia(preview_img_arr,adjust_block.get_slider_val())
    def undo():      nonlocal preview_img_arr; preview_img_arr = effects.img_io.img_to_arr(img).astype(int)
    def invert():    nonlocal preview_img_arr; preview_img_arr = effects.invert.invert(preview_img_arr,(-(adjust_block.get_slider_val()*2)))
    def hue():       nonlocal preview_img_arr; preview_img_arr = effects.hue.hue_nine(preview_img_arr,int(adjust_block.get_slider_val()*3.6))
        
    # Completely restart editing, and open up a new image
    def change_image():
        nonlocal preview_img_arr, img, view_img
        filepath = ui_elements.Prompt.get_file_open("Images (*.webp *.png *.jpg *.JPG *.jpeg *.JPEG)")
        if not filepath: return False
        img=effects.img_io.open_img(filepath)
        view_img = effects.img_io.pil_to_pyg(img)
        preview_img_arr = effects.img_io.img_to_arr(img).astype(int)
        update_preview_area(img,title_bar.rect.bottom,side_bar.rect.right,preview_rect)
        return True

    # Multiplies the current (edited) image array by the original (imported) image
    def mul_image():
        nonlocal preview_img_arr, img
        tmp_img_arr = effects.img_io.img_to_arr(img).astype(int)
        preview_img_arr = (preview_img_arr * tmp_img_arr/255).astype(int)
    
    # Add the current (edited) image array to the original (imported) image
    def add_image():
        nonlocal preview_img_arr, img
        tmp_img_arr = effects.img_io.img_to_arr(img).astype(int)
        preview_img_arr = np.clip(preview_img_arr + tmp_img_arr,0,255)

    # We make a list of all the wrapped functions to make side bar's initialization easier
    wrapped = [ undo,
        lambda: get_options(blur),
        lambda: get_options(contrast),
        lambda: get_options(dither),
        lambda: get_options(sharpen),
        lambda: get_options(sepia),
        lambda: get_options(invert),
        lambda: get_options(brightness),
        lambda: get_options(dog),
        lambda: get_options(hue)]
    
    side_bar_buttons = [ (wrapped[i], # in format (function, image path, text)
                          f"images/icons/effects/{EFFECT_NAMES[i].lower()}.png", EFFECT_NAMES[i]) for i in range(len(EFFECT_NAMES))]
    
    title_bar_buttons = [ ([change_image,lambda:save_image(preview_img_arr),mul_image,add_image][i], "", TITLE_NAMES[i]) for i in range(len(TITLE_NAMES))]

    title_bar = ui_elements.ButtonGrid([0, 0], [screen.get_size()[0], 20], [0, 1],buttons=title_bar_buttons)
    side_bar  = ui_elements.ButtonGrid([0, 20], [screen.get_size()[0] * 1/4, screen.get_size()[1] - 20], [2, 8], hov_col=(0, 114, 182), col=(0, 174, 239),font_size=20,buttons=side_bar_buttons)

    adjust_block = ui_elements.adjustmentTile(side_bar.buttons[-1].rect.bottom,lambda:0,lambda:0) # Creates the block at the bottom left that performs adjustments

    preview_rect = pygame.Rect(1,1,1,1) # This contains the image preview
    update_preview_area(img,title_bar.rect.bottom,side_bar.rect.right,preview_rect)
    
    ui_elements.title_screen(change_image,BACKGROUND_COLOR) # Runs the entire title screen

    def handle_resize(size, side_bar:ui_elements.ButtonGrid): # Resizes the screen, and resizes critical elements accordingly
        nonlocal screen, img, title_bar
        screen = pygame.display.set_mode((max(size[0],600), max(size[1],400)), pygame.RESIZABLE)
        screen.fill(BACKGROUND_COLOR)
        pygame.display.update()

        side_bar.rect.update(side_bar.rect.left,side_bar.rect.top,screen.get_size()[0] * 1/4, screen.get_size()[1] - title_bar.rect.bottom)
        update_preview_area(img,title_bar.rect.bottom,side_bar.rect.right,preview_rect)

    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    rescale = False
    since_resize = 0
    running = True
    while running: # The main loop is very short and sweet
        clock.tick(30)
        since_resize += 1
        
        clicked, moved, running, since_resize, resize_size = handle_events(clicked, since_resize)
        if resize_size != (0,0): handle_resize(resize_size,side_bar)
        if rescale or since_resize < 5: # Resize more finnicky elements - this also means that resizes cascade (vs happen all at once)
            adjust_block.update_size(screen,side_bar.buttons[-1].rect.bottom)
            view_img = pygame.transform.scale(effects.img_io.pil_to_pyg(effects.img_io.arr_to_img(preview_img_arr)),preview_rect.size)

        rescale = False
        clicked_a = adjust_block.update(clicked,moved)
        if side_bar.update(clicked_a) or title_bar.update(clicked_a): # We update everything if a button on the side- or title- bar is clicked
            rescale = True
            clicked = False
        draw_all(title_bar,side_bar,view_img,preview_rect)
    pygame.quit()

def save_image(img_arr): # Saves the image to a user-specified path
        filepath = ui_elements.Prompt.get_file_save()
        if filepath: effects.img_io.arr_to_img(img_arr).save(filepath)

def draw_all(title_bar:ui_elements.ButtonGrid,side_bar:ui_elements.ButtonGrid,view_img:pygame.Surface,preview_rect:pygame.Rect):
    screen = pygame.display.get_surface()
    screen.fill(BACKGROUND_COLOR)
    title_bar.draw()
    side_bar.draw()
    screen.blit(view_img,preview_rect.topleft)
    pygame.display.update()

def update_preview_area(img:Image.Image,top:int,left:int,preview_rect:pygame.Rect):
    screen = pygame.display.get_surface()
    img_rat = img.size[1]/img.size[0]
    img_max = (screen.get_size()[0] - left,screen.get_size()[1] -top)
    preview_rect.update(left, top,min(img_max[0],img_max[1]/img_rat),min(img_max[1],img_max[0]*img_rat))
    preview_rect.center = (left + (screen.get_width()-left)/2, top + (screen.get_height()-top)/2)

def handle_events(clicked:bool, since_resize:int):
        resize_size = (0,0)
        moved = False
        running = True
        for event in pygame.event.get(): # Handles the event loop for us, because events are kinda annoying
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.MOUSEBUTTONDOWN: clicked = True
            if event.type == pygame.MOUSEBUTTONUP: clicked = False
            if event.type == pygame.MOUSEMOTION: moved = True
            if event.type == pygame.VIDEORESIZE:
                since_resize = 0
                resize_size = (event.w,event.h)
        
        return clicked, moved, running, since_resize, resize_size
def loadingtext(effect, adjust_block): # Change the window name and add text to the screen when doing effects
        screen = pygame.display.get_surface()
        loading_font = pygame.font.SysFont("free sans",min(30,int(screen.get_width()/40)))
        loading_text = loading_font.render('Processing...',True,(0,0,0)) # We use static text here (rather than a fun animation/game) because of complexity+time limitations (adding mp processes can get complicated fast)
        screen.blit(loading_text,(0,adjust_block.adjust_bg.top))
        pygame.display.set_caption(f"{NAME}  •  Processing Image...")
        pygame.event.pump() # Sends the caption change to the OS
        pygame.display.update()
        effect()
        pygame.display.set_caption(NAME)
if __name__ == "__main__": # python boilerplate. hooray!
    main()