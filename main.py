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

# Define functions for each button action
def blur_action(img: np.ndarray, slider: ui_elements.Slider) -> np.ndarray:
    img = effects.convolute.Blur.gaussian(img, 16, slider.get_value())
    return img

def contrast_action(img: np.ndarray, slider: ui_elements.Slider) -> np.ndarray:
    pass # Implement contrast effect
    return img

def dither_action(img: np.ndarray, slider: ui_elements.Slider) -> np.ndarray:
    img = effects.dither.dither(img, bool(slider.get_value()))
    return img

def sharpen_action(img: np.ndarray, slider: ui_elements.Slider, slider2: ui_elements.Slider) -> np.ndarray:
    effects.sharpen.sharpen(img, slider.get_value(), slider2.get_value())
    return img

def sepia_action(img: np.ndarray, slider: ui_elements.Slider) -> np.ndarray:
    effects.sepia.sepia(img, slider.get_value())
    return img

def soften_action(img: np.ndarray, slider: ui_elements.Slider) -> np.ndarray:
    pass
    return img

def brightness_action(img, slider: ui_elements.Slider):
    change = slider.get_value()
    img = effects.brightness.brightness(img, change)
    return img

def dog_action(img: np.ndarray, slider: ui_elements.Slider, slider2: ui_elements.Slider, slider3: ui_elements.Slider) -> np.ndarray:
    effects.convolute.EdgeDetect.dog(img, slider.get_value(), slider2.get_value(), slider3.get_value())
    return img

def hue_action(img: np.ndarray, slider: ui_elements.Slider) -> np.ndarray:
    effects.hue.hue(img, slider.get_value())
    return img

def numpy_to_pygame(np_img: np.ndarray) -> pygame.Surface:
    return effects.img_io.pil_to_pyg(effects.img_io.arr_to_img(np_img))

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
    side_bar = ui_elements.ButtonGrid([0, 20], [screen.get_size()[0] * 1/4, screen.get_size()[1] - 20], [2, 5], hov_col=(0, 114, 182), col=(0, 174, 239))

    title_bar.add_button(_text="REPRODUCE", _onclick=lambda: title_bar.add_button(_onclick=lambda: print(ui_elements.Prompt.get_file_open()), _text="open file..."))

    # Update the slider position to be within the sidebar
    slider = ui_elements.Slider((side_bar.rect.width // 2, side_bar.rect.bottom - 50), (side_bar.rect.width - 40, 20), 0, 0, 100)

    # Load original image and convert to numpy array
    original_image = np.array(Image.open("/Users/armaanthadani/Desktop/Work/Tufts/Final_Project/WINNERS-Project/test/mountain.JPEG"))
    preview_image = original_image.copy()

    # Variable to store the currently active effect function
    active_effect_function = None

    def set_active_effect(effect_function):
        nonlocal active_effect_function
        active_effect_function = effect_function
        update_preview()  # Update the preview immediately when the effect is selected

    # Create the sidebar buttons
    side_bar_buttons = [
        (lambda: set_active_effect(lambda img, slider: blur_action(img, slider)), "images/icons/effects/blur.png", "Blur"),
        (lambda: set_active_effect(lambda img, slider: contrast_action(img, slider)), "images/icons/effects/contrast.png", "Contrast"),
        (lambda: set_active_effect(lambda img, slider: dither_action(img, slider)), "images/icons/effects/dither.png", "Dither"),
        (lambda: set_active_effect(lambda img, slider: sharpen_action(img, slider, slider)), "images/icons/effects/sharpen.png", "Sharpen"),
        (lambda: set_active_effect(lambda img, slider: sepia_action(img, slider)), "images/icons/effects/sepia.png", "Sepia"),
        (lambda: set_active_effect(lambda img, slider: soften_action(img, slider)), "images/icons/effects/soften.png", "Soften"),
        (lambda: set_active_effect(lambda img, slider: brightness_action(img, slider)), "images/icons/effects/brightness.png", "Brightness"),
        (lambda: set_active_effect(lambda img, slider: dog_action(img, slider, slider, slider)), "images/icons/effects/dog.png", "Dog"),
        (lambda: set_active_effect(lambda img, slider: hue_action(img, slider)), "images/icons/effects/hue.png", "Hue")
    ]

    for action, image_path, text in side_bar_buttons:
        side_bar.add_button(_onclick=action, _text=text, _font_size=20)
        side_bar.buttons[-1].set_image(image_path)

    img = effects.img_io.open_img("test/mountain.jpeg")
    img_arr = effects.img_io.img_to_arr(img)
    
    img_rat = img.size[1] / img.size[0]
    img_max = (screen.get_size()[0] - side_bar.rect.right, screen.get_size()[1] - title_bar.rect.bottom)
    preview_rect = pygame.Rect(side_bar.rect.right, title_bar.rect.bottom,
                               min(img_max[0], img_max[1] / img_rat),
                               min(img_max[1], img_max[0] * img_rat)
                              )
    preview_rect.center = (side_bar.rect.right + (screen.get_width() - side_bar.rect.right) / 2,
                           title_bar.rect.bottom + (screen.get_height() - title_bar.rect.bottom) / 2)

    # Initialize view_img
    view_img = pygame.transform.scale(effects.img_io.pil_to_pyg(img), preview_rect.size)

    def update_preview():
        if active_effect_function:
            new_img = active_effect_function(preview_image.copy(), slider)
            return numpy_to_pygame(new_img)

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
                squished = pygame.transform.scale(screen, (max(event.w, 600), max(event.h, 400)))
                screen = pygame.display.set_mode((max(event.w, 600), max(event.h, 400)), pygame.RESIZABLE)
                screen.fill(background_color)
                pygame.display.update()
                side_bar.rect.update(side_bar.rect.left, side_bar.rect.top, screen.get_size()[0] * 1 / 4, screen.get_size()[1] - title_bar.rect.bottom)
                
                img_rat = img.size[1] / img.size[0]
                img_max = (screen.get_size()[0] - side_bar.rect.right, screen.get_size()[1] - title_bar.rect.bottom)
                preview_rect = pygame.Rect(side_bar.rect.right, title_bar.rect.bottom,
                                           min(img_max[0], img_max[1] / img_rat),
                                           min(img_max[1], img_max[0] * img_rat)
                                          )
                preview_rect.center = (side_bar.rect.right + (screen.get_width() - side_bar.rect.right) / 2,
                                       title_bar.rect.bottom + (screen.get_height() - title_bar.rect.bottom) / 2)
                view_img = pygame.transform.scale(effects.img_io.pil_to_pyg(img), preview_rect.size)
                skip_frame = True
            slider.handle_event(event)
        
        # Update preview image if the slider is moved and an effect is active
        if active_effect_function:
            view_img = update_preview()
            view_img = pygame.transform.scale(view_img, (preview_rect.width, preview_rect.height))

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
        screen.blit(view_img, preview_rect.topleft)
        
        clock.tick(30)
        pygame.display.flip()

if __name__ == "__main__":
    main()