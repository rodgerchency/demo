# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 20:21:48 2021

@author: rodger
"""

import cv2
import numpy as np

from keras.preprocessing import image as Image

# load the image and scale to 0..1
# image = Image.load_img('a_41.jpg', grayscale=True)
# cv2.imencode('.jpg', frame)[1].tofile('我/9.jpg')
# image = cv2.imread('a_41.jpg').astype(float) / 255.0

# image = cv2.imread('lena.png').astype(float) / 255.0

def convolution (_k, _image):

    # the weighed pixels have to be in range 0..1, so we divide by the sum of all kernel
    # values afterwards
    kernel_sum = _k.shape[0] * _k.shape[1]
    
    # fetch the dimensions for iteration over the pixels and weights
    i_width, i_height = _image.shape[0], _image.shape[1]
    k_width, k_height = _k.shape[0], _k.shape[1]
    
    # prepare the output array
    filtered = np.zeros_like(_image)
    
    # Iterate over each (x, y) pixel in the image ...
    for y in range(i_height):
        for x in range(i_width):
            weighted_pixel_sum = 0
            for ky in range(k_height):
                for kx in range(k_width):                    
                    if y - 1 < 0 or y + 1 >= i_height or x - 1 < 0 or x + 1 >= i_width:
                        continue
                    pixel_y = y + (ky - 1)
                    pixel_x = x + (ky - 1)              
                    weighted_pixel_sum += _k[ky, kx] * _image[pixel_y, pixel_x]  
                    
            filtered[y, x] = weighted_pixel_sum / kernel_sum
    
    return filtered
#
#   z1 z2 z3
#   z4 z5 z6
#   z7 z8 z9
#
def sobelFilter (_image):
    i_width, i_height = _image.shape[0], _image.shape[1]
    # prepare the output array
    filtered = np.zeros_like(_image)
    for y in range(i_height):
        for x in range(i_width):
                  
            if y - 1 < 0 or y + 1 >= i_height or x - 1 < 0 or x + 1 >= i_width:
                continue
            z1 = _image[y - 1, x - 1];
            z2 = _image[y - 1, x];
            z3 = _image[y - 1, x + 1];
            z4 = _image[y, x - 1];
            z6 = _image[y, x + 1];
            z7 = _image[y + 1, x - 1];
            z8 = _image[y + 1, x];
            z9 = _image[y + 1, x + 1];
            filtered[y, x] = abs(z7 + 2*z8 + z9 - z1 - 2*z2 - z3) + abs(z3 + 2*z6 + z9 - z1 - 2*z4 - z7)
    return filtered

for i in range(40):
    image = cv2.imdecode(np.fromfile('train/乃_' + str(i) + '.jpg', dtype=np.uint8), 1) / 255
    image_sobel = sobelFilter(image)
    kernel_mean = (np.array([[1, 1, 1],
                            [1, 1, 1],
                            [1, 1, 1]]))        
    image_sobelMean = convolution(kernel_mean, image_sobel)

    cv2.imwrite('image_sobel' + str(i) + '.jpg', kernel_mean * 255)
    cv2.imwrite('kernel_mean.jpg' + str(i) + '.jpg', image_sobelMean * 255)

# mask_sobelMean = image_sobelMean / np.linalg.norm(image_sobelMean)

# kernel_sharp = (np.array([[-1, -1, -1],
#                          [-1, 8, -1],
#                          [-1, -1, -1]]))
    
# image_sharping = convolution(kernel_sharp, image)