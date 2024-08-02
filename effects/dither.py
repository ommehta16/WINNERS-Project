from PIL import Image
import numpy as np
import math
import time
from multiprocessing import Pool
import sys

def dither_chl(img:np.ndarray) -> np.ndarray:
    filter = 255/16 * np.array([[15, 7,13, 5],
                                [3 ,11, 1, 9],
                                [12, 4,14, 6],
                                [0 , 8, 2,10]]).astype(np.float64) # <-- D4
    
    new_img = np.zeros(img.shape).astype(int)
    for y in range(new_img.shape[0]):
        for x in range(new_img.shape[1]):
            if (img[y,x] > filter[y % filter.shape[0],x % filter.shape[1]]): # Use mod with the filter shape so that we can iterate over it in a straight line instead of a series of boxes
                new_img[y,x] = 255
    return new_img
def dither(img:np.ndarray,color:bool) -> np.ndarray:
    def grayscale(img):
        lum = 0.3 * img[:,:,0] + 0.59 * img[:,:,1] + 0.11 * img[:,:,2]
        return lum
    def chnl_1_to_3(lum):
        new_img = np.zeros((lum.shape[0],lum.shape[1],3))
        for c in range(3): new_img[:,:,c] = lum
        return new_img
    if color:
        with Pool() as pool:
            chls = pool.map(dither_chl,[img[:,:,i] for i in range(3)]) # Split it into 3 channels and dither each of those seperately
        for c in range(3):
            img[:,:,c] = chls[c] # set each channel
    else:
        img = grayscale(img)
        img = dither_chl(img)
        img = chnl_1_to_3(img)
        # Convert it back to 3 channels so that the rest of the program doesn't throw a fit
    return img

if __name__ == "__main__":
    # Test code! Shows you how fast/slow this is!
    # 11.582612991333008 seconds on Om's computer
    from img_io import *
    img_arr = img_to_arr(open_img("test/chicken.webp"))
    
    start = time.time()
    new_img_arr = dither(img_arr,True)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print(str(end-start) + " seconds")
