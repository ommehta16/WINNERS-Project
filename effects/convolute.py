from PIL import Image
import numpy as np
import math
import sys



def convolute(img,conv:np.array) -> Image:
    
    img_arr = np.array(img).astype(int)
    
    conv_x = conv.shape[1]
    conv_y = conv.shape[0]
    
    new_img = np.zeros(img_arr.shape).astype(int)
    
    for c in range(3):
        curr_channel = np.pad(img_arr[:,:,c],(conv_y//2,conv_x//2),'constant',constant_values=(0,0))
        
        for y in range(new_img.shape[0]):
            for x in range(new_img.shape[1]):
                curr_block = curr_channel[y:y+conv_y,x:x+conv_x]
                new_img[y,x,c] = np.multiply(curr_block,conv).sum()
    
    new_img = new_img.clip(0,255)
    return Image.fromarray(new_img.astype(np.uint8))

class Blur:
    
    def gaussian(img:Image,radius:int|float,sigma:float) -> Image:
        def generate_kernel(rad,sigma) -> np.array:
            arr = np.zeros((2*rad+1,2*rad+1))
            inv_sigma = 1/sigma
            d_squared = lambda x,y: x**2 + y**2
            G = lambda x,y: 0.159154943 * inv_sigma * math.exp(-0.5 * inv_sigma * d_squared(x-rad,y-rad))
            for y in range(2*rad+1):
                for x in range(2*rad+1):
                    arr[x,y] = G(x,y)
                    
            return arr/arr.sum()
        img = convolute(img,generate_kernel(radius,sigma))
        
        return img
    
    def box(img:Image, size:int|float) -> Image:
        def generate_kernel(rad) -> np.array:
            arr = np.array(1,(size*2+1,size*2+1))
            arr = arr * 1/(size*2+1)**2
            return arr
        
        img = convolute(img,generate_kernel(size))
        
        return img
    
    
class EdgeDetect:
    def dog(img:Image,r1:int|float,r2:int|float) -> Image:
        # Applies 2 gaussian blurs --> takes the difference (gaussian(img,r1)-gaussian(img,r2))
        
        return img
    
    def lapofgaussian(img:Image) -> Image:
        # Apply laplacian of gaussain (mexican hat :) )
        
        return img