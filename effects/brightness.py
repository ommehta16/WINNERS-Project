from PIL import Image
import numpy as np
import time


def brightness(img:np.array, change:int) -> np.array:
    img+=change
    img = np.clip(img,0,255)
    return img

# Takes 0.060 seconds -- that's FAST
if __name__ == "__main__":
    from img_io import *
    img_arr = img_to_arr(open_img("test/chicken.webp"))
    
    start = time.time()
    new_img_arr = brightness(img_arr,200)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print(str(end-start) + " seconds")

