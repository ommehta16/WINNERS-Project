from PIL import Image
import numpy as np
import math
import time
from multiprocessing import Pool
import sys

def dither_piece(img):
        filter = 255/16 * np.array([[15, 7,13, 5],
                            [3 ,11, 1, 9],
                            [12, 4,14, 6],
                            [0 , 8, 2,10]]).astype(np.float64) # <-- D4
        new_img = np.zeros(img.shape).astype(int)
        # Going 1 block at a time would defo make this more annoying
        for y in range(new_img.shape[0]):
            for x in range(new_img.shape[1]):
                if (img[y,x] > filter[y % filter.shape[0],x % filter.shape[1]]):
                    new_img[y,x] = 255
        return new_img

def dither_linear(img:np.ndarray,color:bool) -> np.ndarray:
    def grayscale(img):
        lum = 0.3 * img[:,:,0] + 0.59 * img[:,:,1] + 0.11 * img[:,:,2]
        return lum
    def chnl_1_to_3(lum):
        new_img = np.zeros((lum.shape[0],lum.shape[1],3))
        for c in range(3): new_img[:,:,c] = lum
        return new_img
    
        
    
    img = grayscale(img)
    
    filter = 255/16 * np.array([[15, 7,13, 5],
                                [3 ,11, 1, 9],
                                [12, 4,14, 6],
                                [0 , 8, 2,10]]).astype(np.float64) # <-- D4

    new_img = np.zeros(img.shape).astype(int)

    for y in range(new_img.shape[0]):
        for x in range(new_img.shape[1]):
            if (img[y,x] > filter[y % filter.shape[0],x % filter.shape[1]]):
                new_img[y,x] = 255
    return chnl_1_to_3(new_img)

def dither_parallel(img:np.ndarray,color:bool) -> np.ndarray:
    def grayscale(img):
        lum = 0.3 * img[:,:,0] + 0.59 * img[:,:,1] + 0.11 * img[:,:,2]
        return lum
    def chnl_1_to_3(lum):
        new_img = np.zeros((lum.shape[0],lum.shape[1],3))
        for c in range(3): new_img[:,:,c] = lum
        return new_img
    
        
    
    img = grayscale(img)
    size = (img.shape[0],img.shape[1])
    cutX = int(size[1]/8)*4
    cutY = int(size[0]/8)*4
    
    with Pool() as pool:
        sliced = pool.map(dither_piece,[img[:cutY,:cutX],img[:cutY,cutX:],img[cutY:,:cutX],img[cutY:,cutX:]])
    img[:cutY,:cutX] = sliced[0]
    img[:cutY,cutX:] = sliced[1]
    img[cutY:,:cutX] = sliced[2]
    img[cutY:,cutX:] = sliced[3]
    img = chnl_1_to_3(img)

    return img

if __name__ == "__main__":
    from img_io import *
    img_arr = img_to_arr(open_img("test/chicken.webp"))
    
    start = time.time()
    new_img_arr = dither_linear(img_arr,False)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print("Linear took " + str(end-start) + " seconds")

    img_arr = img_to_arr(open_img("test/chicken.webp"))
    
    start = time.time()
    new_img_arr = dither_parallel(img_arr,False)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print("Parallel took " +  str(end-start) + " seconds")

# def dither_color(img):

#     filter = 255/16 * np.array([[15, 7,13, 5],
#                                 [3 ,11, 1, 9],
#                                 [12, 4,14, 6],
#                                 [0 , 8, 2,10]]).astype(np.float64) # <-- D4

#     new_img = np.zeros(img.shape).astype(int)

#     # Going 1 block at a time would defo make this more annoying
#     for y in range(new_img.shape[0]):
#         for x in range(new_img.shape[1]):
#             for c in range(3):
#                 if (img[y,x,c] > filter[y % filter.shape[0],x % filter.shape[1]]):
#                     new_img[y,x,c] = 255
#     return new_img

# def dither_gray(img):
#     # filter = np.array([ [191,63],
#     #                     [127,0],]).astype(np.float64) # <-- D2

#     filter = 255/16 * np.array([[15, 7,13, 5],
#                                 [3 ,11, 1, 9],
#                                 [12, 4,14, 6],
#                                 [0 , 8, 2,10]]).astype(np.float64) # <-- D4

#     new_img = np.zeros(img.shape).astype(int)

#     # Going 1 block at a time would defo make this more annoying
#     for y in range(new_img.shape[0]):
#         for x in range(new_img.shape[1]):
#             if (img[y,x,0] > filter[y % filter.shape[0],x % filter.shape[1]]):
#                 new_img[y,x] = 255
#     return new_img

# img = Image.open("ex_img.jpg")
# img = np.array(img).astype(int) #auto-opens as np.uint8 (short)
# img = grayscale(img)

# img = dither_gray(img)

# Image.fromarray(img.astype(np.uint8)).save(f'dithered.png')
