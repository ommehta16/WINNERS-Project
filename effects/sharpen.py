from PIL import Image
import numpy as np
import math
import sys
import time
from scipy.ndimage import convolve

def sharpen(image, intensity: float, power: float) -> np.ndarray:
    new_image = np.array(image)

    intensity = max(1, round(intensity) * 2 + 1)
    # Logic taken from https://blog.demofox.org/2022/02/26/image-sharpening-convolution-kernels/
    blur_filter = np.zeros((intensity, intensity))
    identity = blur_filter.copy()
    identity[intensity // 2, intensity // 2] = 1 + power

    blur_filter = (blur_filter + 1) * (1 / intensity ** 2)
    filter = identity - blur_filter * power

    sharpened_img = np.zeros_like(new_image, dtype=float)
    
    # Apply convolution for each channel
    for c in range(3):
        sharpened_img[:, :, c] = convolve(new_image[:, :, c], filter, mode='reflect')
    
    sharpened_img = np.clip(sharpened_img, 0, 255)
    return sharpened_img.astype(np.uint8)
