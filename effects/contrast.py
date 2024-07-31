from PIL import Image
import numpy as np
import img_io

def contrast(img: np.array, change: float) -> np.array:
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            img[y,x] = ((change/100)*img[y,x]) + (1-(change/100))*127 #decreasing contrast
                                           
    return np.clip(img,0,255).astype(int)

if __name__ == "__main__":
    img = np.array(Image.open("/Users/armaanthadani/Desktop/Work/Tufts/Final_Project/WINNERS-Project/effects/chicken.webp"))
    change = 200 # Example change value
    contrasted_img = contrast(img_io.img_to_arr(img), change)
    Image.fromarray(contrasted_img.astype(np.uint8)).save("contrasted_image.jpg")