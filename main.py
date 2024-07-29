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
    screen = pygame.display.set_mode((1920, 1080))
    screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)
    pygame.display.set_caption('the thing')
    background_color = ('#F5FFFA')

    running = True
    frame = 0
    
    # TEMP --> 
    button = ui_elements.Button([300,300],[25,25],lambda:0,_text="a")
    another_button = ui_elements.Button([100,100],[200,50],lambda:0,_text="broo")
    title_bar = ui_elements.ButtonGrid([0,0],[screen.get_size()[0],20],[0,1])
    side_bar = ui_elements.ButtonGrid([0,20],[screen.get_size()[0]/20,screen.get_size()[1]-20],[2,0])
    
    title_bar.add_button(_text="REPRODUCE",_onclick = lambda: title_bar.add_button(_onclick=lambda:print(ui_elements.Prompt.get_file_open()),_text="open file..."))
    side_bar.add_button(_text="REPRODUCE",_onclick = lambda: 0,_minor_axis_size_spec=side_bar.size[0]/2)
    side_bar.buttons[0].set_image("images/ex.png")
    
    # <-- TEMP
    slider = ui_elements.Slider((400, 500), (200, 20), 0.5, 0, 100)
    
    side_bar_buttons = [
        (lambda:print("blur time")      ,"images/icons/effects/blur.png"),
        (lambda:print("contrast time")  ,"images/icons/effects/contrast.png"),
        (lambda:print("dither time")    ,"images/icons/effects/dither.png"),
        (lambda:print("sharpen time")   ,"images/icons/effects/sharpen.png"),
        (lambda:print("sepia time")   ,"images/icons/effects/sepia.png"),
        (lambda:print("soften time")   ,"images/icons/effects/soften.png"),
        (lambda:print("brightness time")   ,"images/icons/effects/brightness.png"),
        (lambda:print("dog time")   ,"images/icons/effects/dog.png"),
        (lambda:print("hue time")   ,"images/icons/effects/hue.png")
    ]
    for i in range(len(side_bar_buttons)):
        side_bar.add_button(_onclick=side_bar_buttons[i][0])
        side_bar.buttons[i+1].set_image(side_bar_buttons[i][1])


    # Main loop
    while running:
        frame+=1
        prev_pos = pygame.mouse.get_pos()
        
        # Check on events
        clicked: bool = False 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:            running = False
            if event.type == pygame.MOUSEBUTTONDOWN: clicked = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((min(event.w,600),min(event.h,400)), pygame.RESIZABLE)
            slider.handle_event(event)
            
        # UPDATE EVERYTHING
        button.update(clicked)
        another_button.update(clicked)
        title_bar.update(clicked)
        side_bar.update(clicked)
        
        # DRAW EVERYTHING
        screen.fill(background_color)
        
        title_bar.draw()
        button.draw()
        another_button.draw()
        side_bar.draw()
        slider.draw(screen)
        clock.tick(60)
        pygame.display.flip()
    
    pygame.quit()

if (__name__ == "__main__"):
    main()