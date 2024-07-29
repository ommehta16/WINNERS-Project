from PIL import Image
import numpy as np
import math
import sys
import time

def saturation(img:Image, value:float) -> Image:
    value = float(value)
        
    img_arr = np.array(img)
    lum_arr = np.zeros(img_arr.shape)
    
    l_1_c = 0.3 * img_arr[:,:,0] + 0.59*img_arr[:,:,1] + 0.11*img_arr[:,:,2]
    
    for i in range(3): lum_arr[:,:,i] = l_1_c
    img_arr = value * img_arr + (1-value) * lum_arr
    
    img_arr = np.clip(img_arr, 0, 255)
    return Image.fromarray(img_arr.astype(np.uint8))

if __name__ == "__main__": # Time test code
    rn = time.time()
    img = Image.open("time-transfixed.jpg")

    saturation(img,1).save("joe.png")
    print(time.time()-rn)
    
    # on Om's computer, saturation takes 0.594005823135376 seconds (That's pretty FAST)