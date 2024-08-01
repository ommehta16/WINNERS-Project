from PIL import Image
import numpy as np
import math
import sys
import time
from multiprocessing import Pool

def rgb_to_hsv(rgb) -> np.ndarray:
    r,g,b = rgb[0],rgb[1],rgb[2]
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

    return np.array([h,s,v]).astype(float)

def hsv_to_rgb(hsv) -> np.ndarray:
    h, s, v = hsv[0],hsv[1],hsv[2]
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
    
    return np.array([r+m,g+m,b+m])

def hue(img_array: np.ndarray, hue_shift:int):
    img_hsv = np.zeros_like(img_array, dtype=np.float32)
    # start = time.time()
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            img_hsv[i, j] = rgb_to_hsv(img_array[i,j]/255.0)
    # print(f"rgb to hsv: {time.time()-start} seconds")
    img_hsv[..., 0] = (img_hsv[..., 0] + hue_shift) % 360

    img_rgb = np.zeros_like(img_hsv, dtype=np.float32)
    
    # start = time.time()
    for i in range(img_hsv.shape[0]):
        for j in range(img_hsv.shape[1]):
            img_rgb[i, j] = 255 * hsv_to_rgb(img_hsv[i,j])
    # print(f"hsv to rgb: {time.time()-start} seconds")
    img_rgb = img_rgb.astype(np.uint8)
    
    return img_rgb

def hue_four(img_arr:np.ndarray,hue_shift:int):
    halfY = img_arr.shape[0]//2
    halfX = img_arr.shape[1]//2
    with Pool() as pool:
        chunks = pool.starmap(hue,[
            [img_arr[:halfY,:halfX],hue_shift], [img_arr[halfY:,:halfX],hue_shift],
            [img_arr[:halfY,halfX:],hue_shift], [img_arr[halfY:,halfX:],hue_shift],
            ])

    img_arr[:halfY,:halfX] = chunks[0]
    img_arr[halfY:,:halfX] = chunks[1]
    img_arr[:halfY,halfX:] = chunks[2]
    img_arr[halfY:,halfX:] = chunks[3]


    return img_arr

def hue_nine(img_arr:np.ndarray,hue_shift:int):
    partY = img_arr.shape[0]//3
    partX = img_arr.shape[1]//3
    with Pool() as pool:
        chunks = pool.starmap(hue,[
            [img_arr[:partY,:partX],hue_shift],         [img_arr[partY:2*partY,:partX],hue_shift], [img_arr[2*partY:,:partX],hue_shift],
            [img_arr[:partY,partX:2*partX],hue_shift],  [img_arr[partY:2*partY,partX:2*partX],hue_shift], [img_arr[2*partY:,partX:2*partX],hue_shift],
            [img_arr[:partY,2*partX:],hue_shift],       [img_arr[partY:2*partY,2*partX:],hue_shift], [img_arr[2*partY:,2*partX:],hue_shift],
            ])

    img_arr[:partY,:partX] = chunks[0]
    img_arr[partY:2*partY,:partX] = chunks[1]
    img_arr[2*partY:,:partX] = chunks[2]
    img_arr[:partY,partX:2*partX] = chunks[3]
    img_arr[partY:2*partY,partX:2*partX] = chunks[4]
    img_arr[2*partY:,partX:2*partX] = chunks[5]
    img_arr[:partY,2*partX:] = chunks[6]
    img_arr[partY:2*partY,2*partX:] = chunks[7]
    img_arr[2*partY:,2*partX:] = chunks[8]

    return img_arr

if __name__ == "__main__":
    from img_io import *
    img_arr = img_to_arr(open_img("test/chicken.webp"))
    
    img_arr = hue_nine(img_arr,56)

    Image.fromarray(img_arr.astype(np.uint8)).save("test/output.png")