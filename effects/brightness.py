from PIL import Image
import numpy as np


def brightness(img:str, change:float):
    image = Image.open(img)
    image = np.array(image).astype(int)
    new_image = np.array(image)

    for y in range(new_image.shape[0]):
        for x in range(new_image.shape[1]):
            new_image[y,x] += change

    return new_image




