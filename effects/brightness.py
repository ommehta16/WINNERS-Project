from PIL import Image
import numpy as np
import time


def brightness(image:Image, change:float) -> Image:
    img = np.array(image).astype(int)

    img+=change
    
    img = np.clip(img,0,255)
    return Image.fromarray(img.astype(np.uint8))

if __name__ == "__main__": # Time test code
    rn = time.time()
    img = Image.open("test/time-transfixed.jpg")

    brightness(img,200).save("test/joe.png")
    print(time.time()-rn)
    
    # on Om's computer, brightness takes 0.19944024085998535 seconds (That's FAST!)



