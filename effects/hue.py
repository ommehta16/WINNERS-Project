from PIL import Image
import numpy as np
import math
import sys
import time
import cv2

def hue(image:str, hue_shift:float):

    hue_shift = hue_shift / 360.0

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    
    hsv_image[..., 0] = (hsv_image[..., 0] / 180.0 + hue_shift) % 1.0 * 180.0

    hsv_image = hsv_image.astype(np.uint8)
    output_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    
    return output_image