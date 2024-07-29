from PIL import Image
import numpy as np
import math
import sys

def soften(img: Image, value:int):
    img = np.array(img).astype(int)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            L = 0.11 / value  * img[y,x][0] + 0.3 / value img[y,x][1] + 0.59 / valueimg[y,x][2]
            img[y, x] = (valueimg[y, x]) + (1-value)L

    img = np.clip(img, 0, 255)
    Image.fromarray(img.astype(np.uint8)).save('output.png')
    return img
