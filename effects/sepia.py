from PIL import Image
import numpy as np
import math
import sys
import time

def sepia(img: Image, intensity: float) -> Image:
    
    intensity = min(1,max(0,intensity))

    image = np.array(img).astype(int)

    # values taken from https://yabirgb.com/sepia_filter/

    sepia_filter = np.array([[0.393, 0.769, 0.189],
                            [0.349, 0.686, 0.168],
                            [0.272, 0.534, 0.131]])

    new_image = image[..., :3].dot(sepia_filter.T)
    new_image = np.clip(new_image, 0, 255)

    new_image = (image * (1 - intensity) + new_image * intensity).astype(np.uint8)

    return Image.fromarray(new_image)

if __name__ == "__main__": # Time test code
    rn = time.time()
    img = Image.open("test/time-transfixed.jpg")

    sepia(img,1.6).save("test/joe.png")
    print(time.time()-rn)
    
    # on Om's computer, saturation takes 0.7326478958129883 seconds (That's fairly FAST)