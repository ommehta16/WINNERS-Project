from PIL import Image
import numpy as np
import math
import sys

def saturation(img:Image, value:int) -> Image:
    img = np.array(img).astype(int)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            L = 0.3 * img[y,x][0] + 0.59*img[y,x][1] + 0.11*img[y,x][2]
            img[y, x] = (value*img[y, x]) + (1-value)*L
    img = np.clip(img, 0, 255)
    Image.fromarray(img.astype(np.uint8)).save('output.png')
    return img