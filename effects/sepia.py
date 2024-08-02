from PIL import Image
import numpy as np
import math
import sys
import time

def sepia(image: np.ndarray, intensity: float) -> np.ndarray:
    # applies a sepia filter which imitates vintage photos by applying a reddish-brown tone

    '''
    Parameters:
        image: The input image, as a numpy array
        intensity: the intensity of the sepia effect, calculated between 0 and 1.

    Returns:
        The image with the sepia filter applied, as a numpy array
    '''

    # ensure intensity is between 1 and 0
    intensity = min(1,max(0,intensity))

    # values taken from https://yabirgb.com/sepia_filter/
    sepia_filter = np.array([[0.393, 0.769, 0.189],
                            [0.349, 0.686, 0.168],
                            [0.272, 0.534, 0.131]])

    # apply the sepia filter to the image using dot products
    new_image = image[..., :3].dot(sepia_filter.T)

    # clip the values to be within (0, 255)
    new_image = np.clip(new_image, 0, 255)

    # interpolate the original image with the filtered image based on the value of intensity
    new_image = (image * (1 - intensity) + new_image * intensity).astype(np.uint8)

    return new_image

# Takes 0.411 seconds -- That's pretty FAST
'''if __name__ == "__main__":
    from img_io import *
    img_arr = img_to_arr(open_img("test/chicken.webp"))
    
    start = time.time()
    new_img_arr = sepia(img_arr,0.5)
    end = time.time()
    
    arr_to_img(new_img_arr).save("test/output.png")
    print(str(end-start) + " seconds")'''