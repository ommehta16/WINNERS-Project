from PIL import Image
import numpy as np
import math
import sys
import time
from multiprocessing import Pool
from effects import convolute


def sharpen_chnl(chl:np.ndarray,filt:np.ndarray,radius) -> np.ndarray:
    sharp_chl = np.zeros_like(chl,dtype=float)
    for y in range(radius, chl.shape[0] - radius):
        for x in range(radius, chl.shape[1] - radius):
            sharp_chl[y-radius:y+radius + 1,
                      x-radius:x+radius + 1
                    ] += chl[y, x] * filt
    return sharp_chl
def make_sharp_mask(intensity,power):
    # logic taken from https://blog.demofox.org/2022/02/26/image-sharpening-convolution-kernels/
    intensity = max(1, round(intensity) * 2 + 1)
    blur_filter = np.ones((intensity, intensity))
    identity = np.zeros((intensity,intensity))
    identity[intensity // 2, intensity // 2] = 1 + power
    blur_filter /= intensity**2
    filter = identity - blur_filter * power
    return filter

def sharpen(image:np.ndarray, intensity:float, power:float) -> np.ndarray:
    filter  = make_sharp_mask(intensity,power)    
    sharpened_img = convolute.convolute(image,filter)
    sharpened_img = np.clip(sharpened_img, 0, 255).astype(int)
    return sharpened_img

# Takes 25.406 seconds -- That's kinda SLOW
if __name__ == "__main__":
    from img_io import *
    import convolute
    img_arr = img_to_arr(open_img("test/chicken.webp"))
    
    start = time.time()
    new_img_arr = sharpen(img_arr,2,2)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print(str(end-start) + " seconds")