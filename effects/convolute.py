from PIL import Image
import numpy as np
import math
import sys
from multiprocessing import Pool
import time

def conv_1_chnl(chl:np.ndarray,conv:np.ndarray) -> np.ndarray:
    conv_x = conv.shape[1]
    conv_y = conv.shape[0]
    
    new_chl = np.zeros(chl.shape).astype(int)
    chl = np.pad(chl,(conv_y//2,conv_x//2),'constant',constant_values=(0,0))
    
    for y in range(new_chl.shape[0]):
        for x in range(new_chl.shape[1]):
            curr_block = chl[y:y+conv_y,x:x+conv_x]
            new_chl[y,x] = np.multiply(curr_block,conv).sum()
    
    new_chl = new_chl.clip(0,255)
    return new_chl

def convolute(img_arr: np.ndarray,conv: np.ndarray) -> np.ndarray:
    
    new_img = np.zeros(img_arr.shape).astype(int)
    # mp = ~33% speed improvement on convolution
    with Pool() as pool:
        chnl_list = pool.starmap(conv_1_chnl,[(img_arr[:,:,i],conv) for i in range(3)])
    for i in range(3):
        new_img[:,:,i] = chnl_list[i] 
    
    new_img = new_img.clip(0,255)
    return new_img

class Blur:
    
    def generate_gauss_kernel(rad,sigma) -> np.ndarray:
        arr = np.zeros((2*rad+1,2*rad+1))
        inv_sigma = 1/sigma
        d_squared = lambda x,y: x**2 + y**2
        G = lambda x,y: 0.159154943 * inv_sigma * math.exp(-0.5 * inv_sigma * d_squared(x-rad,y-rad))
        for y in range(2*rad+1):
            for x in range(2*rad+1):
                arr[x,y] = G(x,y)
                
        return arr/arr.sum()

    def gaussian(img: np.ndarray,radius:float,sigma:float) -> np.ndarray:
        img = convolute(img,Blur.generate_gauss_kernel(radius,sigma))
        
        return img
    
    def box(img: np.ndarray, size:float) -> np.ndarray:
        def generate_kernel() -> np.ndarray:
            arr = np.array(1,(size*2+1,size*2+1))
            arr = arr * 1/(size*2+1)**2
            return arr
        
        img = convolute(img,generate_kernel())
        
        return img
    
    
class EdgeDetect:
    def dog(img: np.ndarray,r1:float,r2:float,prominence:float) -> np.ndarray:
        def grayscale(image: np.ndarray) -> np.ndarray:
            img = np.zeros(image.shape)
            for c in range(3):
                img[:,:,c] = 0.3 * image[:,:,0] + 0.59*image[:,:,1] + 0.11*image[:,:,2]
            return img
        
        flt = prominence*20*(Blur.generate_gauss_kernel(16,r1)-Blur.generate_gauss_kernel(16,r2))
        
        img = convolute(img,flt)
        img = grayscale(np.array(img).astype(int))
        
        img = np.clip(img,0,255)
        return img
    
    def mono_dog(img: np.ndarray,r1:float,r2:float,prominence:float) -> np.ndarray:
        flt = prominence*20*(Blur.generate_gauss_kernel(16,r1)-Blur.generate_gauss_kernel(16,r2))
        
        img_arr = conv_1_chnl(img,flt)
        img = np.clip(img_arr,0,255)
        return img
    
    
'''if __name__ == "__main__":
    rn = time.time()
    img = Image.open("test/time-transfixed.jpg")

    dogged = EdgeDetect.dog(img,2,1.5,2.5)
    dogged.save("test/dogged.png")

    #dogged = Image.open("test/dogged.png")
    
    original_arr = np.array(img).astype(int)
    dogged_arr = np.zeros(original_arr.shape)
    for i in range(3):
        dogged_arr[:,:,i] = np.array(dogged).astype(int)
    
    dogged_arr = dogged_arr * 1/255
    original_arr = original_arr*dogged_arr

    img = Image.fromarray(np.clip(original_arr,0,255).astype(np.uint8))
    img.save("test/goofed.png")

    print(time.time()-rn)'''

# Takes 36.110 seconds -- That's SLOW
if __name__ == "__main__":
    from img_io import *
    img_arr = img_to_arr(open_img("test/time-transfixed.jpg"))
    
    start = time.time()
    new_img_arr = Blur.gaussian(img_arr,16,2)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print(str(end-start) + " seconds")