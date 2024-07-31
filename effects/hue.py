from PIL import Image
import numpy as np
import math
import sys
import time

def hue(image_path:str, hue_shift:int):
    img = Image.open(image_path).convert('RGB')
    
    img_array = np.array(img)

    img_hsv = np.zeros_like(img_array, dtype=np.float32)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            r, g, b = img_array[i, j] / 255.0
            mx = max(r, g, b)
            mn = min(r, g, b)
            df = mx - mn
            if mx == mn:
                h = 0
            elif mx == r:
                h = (60 * ((g - b) / df) + 360) % 360
            elif mx == g:
                h = (60 * ((b - r) / df) + 120) % 360
            elif mx == b:
                h = (60 * ((r - g) / df) + 240) % 360
            if mx == 0:
                s = 0
            else:
                s = df / mx
            v = mx
            img_hsv[i, j] = [h, s, v]

    img_hsv[..., 0] = (img_hsv[..., 0] + hue_shift) % 360

    img_rgb = np.zeros_like(img_hsv, dtype=np.float32)
    for i in range(img_hsv.shape[0]):
        for j in range(img_hsv.shape[1]):
            h, s, v = img_hsv[i, j]
            c = v * s
            x = c * (1 - abs((h / 60) % 2 - 1))
            m = v - c
            if 0 <= h < 60:
                r, g, b = c, x, 0
            elif 60 <= h < 120:
                r, g, b = x, c, 0
            elif 120 <= h < 180:
                r, g, b = 0, c, x
            elif 180 <= h < 240:
                r, g, b = 0, x, c
            elif 240 <= h < 300:
                r, g, b = x, 0, c
            elif 300 <= h < 360:
                r, g, b = c, 0, x
            img_rgb[i, j] = [(r + m) * 255, (g + m) * 255, (b + m) * 255]

    img_rgb = img_rgb.astype(np.uint8)
    result_img = Image.fromarray(img_rgb, 'RGB')
    
    return result_img

if __name__ == "__main__":
    from img_io import *
    import convolute
    
    start = time.time()
    new_img_arr = hue("test/chicken.webp",90)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print(str(end-start) + " seconds")