from PIL import Image, ImageFilter
import numpy as np

def soften(image_path, blur_radius=5, lighten_factor=1.75):
    # test case: effects.soften.soften("test/output.png").save('output.png')
    img = Image.open(image_path)
    blurred_img = img.filter(ImageFilter.GaussianBlur(blur_radius))
    img_array = np.array(blurred_img)
    img_array = np.clip(img_array * lighten_factor, 0, 255).astype(np.uint8)
    lightened_img = Image.fromarray(img_array)
    return lightened_img
    
