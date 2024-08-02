from PIL import Image
import numpy as np
from effects import img_io

def contrast(img: np.array, change: float) -> np.array:
    '''`change` is a value where 0 is fully gray and 100 is full color'''
    # lerp between gray and the full color image: use change as the value to lerp by
    gray = np.zeros(img.shape).astype(int)
    gray = gray + 127 #gray is filled with just (127,127,127) for the entire array
    change /= 100
    img = change*img + (1-change)*gray
                                           
    return np.clip(img,0,255).astype(np.uint8)

if __name__ == "__main__":
    img = np.array(Image.open("/Users/armaanthadani/Desktop/Work/Tufts/Final_Project/WINNERS-Project/effects/chicken.webp"))
    change = 200 # Example change value
    contrasted_img = contrast(img_io.img_to_arr(img), change)
    Image.fromarray(contrasted_img.astype(np.uint8)).save("contrasted_image.jpg")