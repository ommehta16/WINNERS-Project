from PIL import Image
import numpy as np
import math
import sys
import time
from multiprocessing import Pool


def sharpen_chnl(chl,filt,intense):
    sharp_chl = np.zeros_like(chl,dtype=float)
    for y in range(intense // 2, chl.shape[0] - intense // 2):
        for x in range(intense // 2, chl.shape[1] - intense // 2):
            sharp_chl[y-intense//2:y+intense//2 + 1,
                            x-intense//2:x+intense//2 + 1
                    ] += chl[y, x] * filt
    return sharp_chl

def sharpen(img:Image, intensity:float, power:float) -> Image:
    image = np.array(img).astype(int)
    image = np.clip(image, 0, 255)
    new_image = np.array(image)

    intensity = max(1, round(intensity) * 2 + 1)
    # logic taken from https://blog.demofox.org/2022/02/26/image-sharpening-convolution-kernels/
    blur_filter = np.zeros((intensity, intensity))
    identity = blur_filter.copy()
    identity[intensity // 2, intensity // 2] = 1 + power

    blur_filter = (blur_filter + 1) * (1/intensity**2)
    filter = identity - blur_filter * power
    new_image = np.pad(new_image, ((intensity // 2,), (intensity // 2,), (0,)))
    sharpened_img = np.zeros_like(new_image, dtype=float)
    
    with Pool() as pool:
        chnl_list = pool.starmap(sharpen_chnl,[(new_image[:,:,c],filter,intensity) for c in range(3)])
    for c in range(3):
        sharpened_img[:,:,c] = chnl_list[c]

    sharpened_img = sharpened_img[intensity // 2:new_image.shape[0] - intensity // 2,
                                  intensity // 2:new_image.shape[1] - intensity // 2]
    return Image.fromarray(np.clip(sharpened_img, 0, 255).astype(np.uint8))

if __name__ == "__main__": # Time test code
    rn = time.time()
    img = Image.open("time-transfixed.jpg")

    sharpen(img,1,1).save("joe.png")
    print(time.time()-rn)
    
    # on Om's computer, sharpening takes 8.622666835784912 seconds (That's pretty meh)