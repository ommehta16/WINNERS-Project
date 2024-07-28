from PIL import Image
import numpy as np
import math
import sys

def sepia(img: str, intensity: float):
    if intensity < 0:
        intensity = 0
    elif intensity > 1:
        intensity = 1

    image = Image.open(img)
    image = np.array(image).astype(int)

    # values taken from https://yabirgb.com/sepia_filter/

    sepia_filter = np.array([[0.393, 0.769, 0.189],
                            [0.349, 0.686, 0.168],
                            [0.272, 0.534, 0.131]])

    new_image = image[..., :3].dot(sepia_filter.T)
    new_image = np.clip(new_image, 0, 255)

    new_image = (image * (1 - intensity) + new_image * intensity).astype(np.uint8)

    return new_image