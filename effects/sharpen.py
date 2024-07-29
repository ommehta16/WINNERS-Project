from PIL import Image
import numpy as np
import math
import sys
import time

def sharpen(img:str, intensity:float):
    image = Image.open(img)
    image = np.array(image).astype(int)
    image = np.clip(image, 0, 255)
    new_image = np.array(image)

    intensity = max(1, round(intensity) * 2 + 1)
    # logic taken from https://blog.demofox.org/2022/02/26/image-sharpening-convolution-kernels/
    blur_filter = np.zeros((intensity, intensity))
    identity = blur_filter.copy()
    identity[intensity // 2, intensity // 2] = 2

    blur_filter = blur_filter + 1
    filter = identity - blur_filter * (1/intensity**2)
    new_image = np.pad(new_image, ((intensity // 2,), (intensity // 2,), (0,)))
    sharpened_img = np.zeros_like(new_image, dtype=float)

    for ch in range(3):
      for y in range(intensity // 2, new_image.shape[0] - intensity // 2):
          for x in range(intensity // 2, new_image.shape[1] - intensity // 2):
              sharpened_img[y-intensity//2:y+intensity//2 + 1,
                            x-intensity//2:x+intensity//2 + 1,
                            ch] += new_image[y, x, ch] * filter

    out = sharpened_img[intensity // 2:new_image.shape[0] - intensity // 2,
                        intensity // 2:new_image.shape[1] - intensity // 2]

    min_value = min(0, np.min(out))
    max_value = max(255, np.max(out))
    out = (out - min_value) / (max_value - min_value)
    return out

