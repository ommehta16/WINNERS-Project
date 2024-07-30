import pygame
from PIL import Image
import numpy as np
import sys
import math
import effects.brightness
from ui import ui_elements
import effects
import effects.convolute
import effects.dither
import effects.sharpen
import effects.sepia
import effects.hue

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# Define functions for each button action
def blur_action(img, slider: ui_elements.Slider):
    effects.convolute.Blur.gaussian(img, 16, slider.get_value())
    return img

def contrast_action(img, slider: ui_elements.Slider):
    pass # Implement contrast effect
    return img

def dither_action(img, slider: ui_elements.Slider):
    effects.dither.dither()
    return img

def sharpen_action(img, slider: ui_elements.Slider, slider2: ui_elements.Slider):
    effects.sharpen.sharpen(img, slider.get_value(), slider2.get_value())
    return img

def sepia_action(img, slider: ui_elements.Slider):
    effects.sepia.sepia(img, slider.get_value())
    return img

def soften_action(img, slider: ui_elements.Slider):
    pass
    return img

def brightness_action(img, slider: ui_elements.Slider):
    change = slider.get_value()
    img = effects.brightness.brightness(img, change)
    return img

def dog_action(img, slider: ui_elements.Slider, slider2: ui_elements.Slider, slider3: ui_elements.Slider):
    effects.convolute.EdgeDetect.dog(img, slider.get_value(), slider2.get_value(), slider3.get_value())
    return img

def hue_action(img, slider: ui_elements.Slider):
    effects.hue.hue(img, slider.get_value())
    return img

def numpy_to_pygame(np_img):
    # Convert numpy image to PIL image
    pil_image = Image.fromarray(np_img.astype('uint8'), 'RGB')
    # Convert PIL image to Pygame surface
    return pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)

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

    # Create a surface for the image preview
    preview_rect = pygame.Rect(side_bar.rect.right, title_bar.rect.bottom, screen.get_size()[0] - side_bar.rect.right, screen.get_size()[1] - title_bar.rect.bottom)
    pygame_preview_image = numpy_to_pygame(original_image)  # Display the original image initially
    pygame_preview_image = pygame.transform.scale(pygame_preview_image, (preview_rect.width, preview_rect.height))

    def update_preview():
        nonlocal pygame_preview_image
        if active_effect_function:
            new_img = active_effect_function(preview_image.copy(), slider)
            pygame_preview_image = numpy_to_pygame(new_img)
            pygame_preview_image = pygame.transform.scale(pygame_preview_image, (preview_rect.width, preview_rect.height))

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
                side_bar.rect.update(side_bar.rect.left, side_bar.rect.top, screen.get_size()[0] * 1/4, screen.get_size()[1] - title_bar.rect.bottom)
                preview_rect.update(side_bar.rect.right, title_bar.rect.bottom, screen.get_size()[0] - side_bar.rect.right, screen.get_size()[1] - title_bar.rect.bottom)
                pygame_preview_image = pygame.transform.scale(pygame_preview_image, (preview_rect.width, preview_rect.height))

            slider.handle_event(event)

        # Update preview image if the slider is moved and an effect is active
        if active_effect_function:
            update_preview()

        # UPDATE EVERYTHING
        title_bar.update(clicked)
        side_bar.update(clicked)

        # DRAW EVERYTHING
        screen.fill(background_color)
        
        title_bar.draw()
        side_bar.draw()
        slider.draw(screen)
        
        # Draw the image preview
        screen.blit(pygame_preview_image, preview_rect.topleft)
        
        clock.tick(60)
        pygame.display.flip()
        print(slider.get_value())

    pygame.quit()

if __name__ == "__main__":
    main()