from PIL import Image
import numpy as np
from effects import img_io

def invert(img: np.array, change: float) -> np.array:
    '''`change`: 0 = full gray, 100 = full color, -100 = fully inverted'''
    # This is really the same thing as contrast
    gray = np.zeros(img.shape).astype(int)
    gray = gray + 127
    change /= 100
    img = change*img + (1-change)*gray
                                           
    return np.clip(img,0,255).astype(np.uint8)

if __name__ == "__main__":
    img = np.array(Image.open("/Users/armaanthadani/Desktop/Work/Tufts/Final_Project/WINNERS-Project/effects/chicken.webp"))
    change = 200 # Example change value
    contrasted_img = invert(img_io.img_to_arr(img), change)
    Image.fromarray(contrasted_img.astype(np.uint8)).save("contrasted_image.jpg")
