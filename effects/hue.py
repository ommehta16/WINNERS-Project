from PIL import Image
import numpy as np
import math
import sys
import time
import cv2

# I am confuse now
# it might be better to change this from opencv to our own hsl struct
# bc otherwise integrating it into the rest of the stuff is going to be a paaaain

def rgb_to_hsv(img:np.ndarray) -> np.ndarray:
    pass

def hsv_to_rgb(img_hsv:np.ndarray) -> np.ndarray:
    pass

def hue(image:np.ndarray, hue_shift:float) -> np.ndarray:

    hue_shift = hue_shift / 360.0

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    
    hsv_image[..., 0] = (hsv_image[..., 0] / 180.0 + hue_shift) % 1.0 * 180.0

    hsv_image = hsv_image.astype(np.uint8)
    output_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    
    return output_image

# Takes (inf) seconds -- DOES NOT RUN
if __name__ == "__main__":
    from img_io import *
    img_arr = img_to_arr(open_img("test/chicken.webp"))
    
    start = time.time()
    new_img_arr = hue(img_arr,10)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print(str(end-start) + " seconds")