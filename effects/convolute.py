from PIL import Image
import numpy as np
import math
import sys

def convolute(img:Image,conv_matrix:list[list[int]]) -> Image:
    
    # Apply the convolution matrix to the image
    # Try making this vectorized so that it's fast
    
    return img

class Blur:
    def gaussian(img:Image,radius:int|float) -> Image:
        
        # Apply the gaussian blur using `convolute(img,matrix)`
        
        return img
    
    def box(img:Image, size:int|float) -> Image:
        
        # Apply the box blur using `convolute(img,matrix)`
        
        return img
    
    
class EdgeDetect:
    def dog(img:Image,r1:int|float,r2:int|float) -> Image:
        # Applies 2 gaussian blurs --> takes the difference (gaussian(img,r1)-gaussian(img,r2))
        
        return img
    
    def lapofgaussian(img:Image) -> Image:
        # Apply laplacian of gaussain (mexican hat :) )
        
        return img