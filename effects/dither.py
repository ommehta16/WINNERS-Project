from PIL import Image
import numpy as np
import math
import time
import sys

def dither(img:np.ndarray) -> np.ndarray:
    
    # DITHER THE IMAGE
    
    return img

if __name__ == "__main__":
    from img_io import *
    img_arr = img_to_arr(open_img("test/chicken.webp"))
    
    start = time.time()
    new_img_arr = dither(img_arr)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print(str(end-start) + " seconds")