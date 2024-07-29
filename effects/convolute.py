from PIL import Image
import numpy as np
import math
import sys
from multiprocessing import Pool
import time

def conv_1_chnl(chl:np.array,conv:np.array) -> np.array:
    conv_x = conv.shape[1]
    conv_y = conv.shape[0]
    
    new_chl = np.zeros(chl.shape).astype(int)
    chl = np.pad(chl,(conv_y//2,conv_x//2),'constant',constant_values=(0,0))
    
    for y in range(new_chl.shape[0]):
        for x in range(new_chl.shape[1]):
            curr_block = chl[y:y+conv_y,x:x+conv_x]
            new_chl[y,x] = np.multiply(curr_block,conv).sum()
    return new_chl

def convolute(img,conv:np.array) -> Image:
    img_arr = np.array(img).astype(int)
    
    new_img = np.zeros(img_arr.shape).astype(int)
    
    # mp = ~33% speed improvement on convolution
    with Pool() as pool:
        chnl_list = pool.starmap(conv_1_chnl,[(img_arr[:,:,i],conv) for i in range(3)])
    for i in range(3):
        new_img[:,:,i] = chnl_list[i] 
    
    new_img = new_img.clip(0,255)
    return Image.fromarray(new_img.astype(np.uint8))

class Blur:
    
    def generate_gauss_kernel(rad,sigma) -> np.array:
        arr = np.zeros((2*rad+1,2*rad+1))
        inv_sigma = 1/sigma
        d_squared = lambda x,y: x**2 + y**2
        G = lambda x,y: 0.159154943 * inv_sigma * math.exp(-0.5 * inv_sigma * d_squared(x-rad,y-rad))
        for y in range(2*rad+1):
            for x in range(2*rad+1):
                arr[x,y] = G(x,y)
                
        return arr/arr.sum()

    def gaussian(img:Image,radius:float,sigma:float) -> Image:
        img = convolute(img,Blur.generate_gauss_kernel(radius,sigma))
        
        return img
    
    def box(img:Image, size:float) -> Image:
        def generate_kernel(rad) -> np.array:
            arr = np.array(1,(size*2+1,size*2+1))
            arr = arr * 1/(size*2+1)**2
            return arr
        
        img = convolute(img,generate_kernel(size))
        
        return img
    
    
class EdgeDetect:
    def dog(img:Image,r1:float,r2:float,prominence:float) -> Image:
        def grayscale(image:np.array) -> np.array:
            img = 0.3 * image[:,:,0] + 0.59*image[:,:,1] + 0.11*image[:,:,2]
            return img
        
        flt = prominence*20*(Blur.generate_gauss_kernel(16,r1)-Blur.generate_gauss_kernel(16,r2))
        
        img = convolute(img,flt)
        img = Image.fromarray(np.clip(grayscale(np.array(img).astype(int)),0,255).astype(np.uint8))
        return img
    
    def lapofgaussian(img:Image) -> Image:
        # Apply laplacian of gaussain (mexican hat :) )
        
        return img
    
    
if __name__ == "__main__":
    rn = time.time()
    img = Image.open("test/chicken.webp")

    EdgeDetect.dog(img,2,1.5,2.5).save("test/dogged.png")
    print(time.time()-rn)