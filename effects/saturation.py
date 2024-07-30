from PIL import Image
import numpy as np
import math
import sys
import time

def saturation(img_arr:np.ndarray, value:float) -> np.ndarray:
    value = float(value)
        
    lum_arr = np.zeros(img_arr.shape)
    
    l_1_c = 0.3 * img_arr[:,:,0] + 0.59*img_arr[:,:,1] + 0.11*img_arr[:,:,2]
    
    for i in range(3): lum_arr[:,:,i] = l_1_c
    img_arr = value * img_arr + (1-value) * lum_arr
    
    img_arr = np.clip(img_arr, 0, 255)
    return img_arr

# Takes 0.353 seconds -- That's FAST
'''if __name__ == "__main__":
    from img_io import *
    img_arr = img_to_arr(open_img("test/chicken.webp"))
    
    start = time.time()
    new_img_arr = saturation(img_arr,5)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print(str(end-start) + " seconds")'''