from PIL import Image
import numpy as np

def brightness(img: np.array, change: int) -> np.array:
    # Ensure change is within the range -255 to 255
    change = np.clip(change, -255, 255)
    
    # Convert the image to int16 to prevent overflow, and make the change
    img = img.astype(np.int16) + change
    
    # Clip the values to be in the range 0-255
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8)  # Convert back to uint8


