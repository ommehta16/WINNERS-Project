from PIL import Image
import numpy as np
import math
import sys
import time
from multiprocessing import Pool
from effects import convolute


def make_sharp_mask(intensity,power):
    # logic taken from https://blog.demofox.org/2022/02/26/image-sharpening-convolution-kernels/
    intensity = max(1, round(intensity) * 2 + 1)
    blur_filter = np.ones((intensity, intensity))
    identity = np.zeros((intensity,intensity))
    identity[intensity // 2, intensity // 2] = 1 + power # the center of identity is 1+power
    blur_filter /= intensity**2 # make the sum of blur filter 1
    filter = identity - blur_filter * power # Creates a distribution where the center point is REALLY high, and the outside is fairly low. mask sum is 0
    return filter

def sharpen(image:np.ndarray, intensity:float, power:float) -> np.ndarray:
    filter  = make_sharp_mask(intensity,power)    
    sharpened_img = convolute.convolute(image,filter) # All that sharpening is is convolution with a special filter
    sharpened_img = np.clip(sharpened_img, 0, 255).astype(int)
    return sharpened_img

# Takes 25.406 seconds -- That's kinda SLOW
if __name__ == "__main__":
    # more test code -- almost the same as the test code from other files, tests for the amount of time that this takes (and outputs so that we can check whether it worked)
    from img_io import *
    import convolute
    img_arr = img_to_arr(open_img("test/chicken.webp"))
    
    start = time.time()
    new_img_arr = sharpen(img_arr,2,2)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print(str(end-start) + " seconds")