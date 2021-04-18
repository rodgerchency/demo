
import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont


class WordUtil:
    
    def __init__(self, imgUrl):
        
        # img = cv2.imread(imgUrl).astype(float) / 255.0
        # img = cv2.imread(imgUrl, cv2.IMREAD_GRAYSCALE).astype(float)
        img = cv2.imdecode(np.fromfile(imgUrl,dtype=np.uint8),cv2.IMREAD_GRAYSCALE)
        print(type(img))
        # print(img.shape)
        # self.calculateWidth(img)
        # kernel_mean = (np.array([
        #     [1, 1, 1],
        #     [1, 1, 1],
        #     [1, 1, 1]]))
        kernel_sharp = (np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]]))
        
        dataConv = self.convolution(kernel_sharp, img)
        # img = Image.open(imgUrl)
        # dadaImg = img.load()
        # self.combine(dataConv, dadaImg)
        # # imgConv.save('temp.png')
        cv2.imwrite("image_sharping.jpg", dataConv)

            # dataImg = img.load()

    def calculateWidth(self, img):
        
        i_width, i_height = img.shape[0], img.shape[1]
        
        cntMap = np.ones_like(img) * 255
        valMap = []
        for y in range(i_height):
            for x in range(i_width):
                if img[y, x] < 50:
                    cnt = 1
                    for i in range(y + 1, i_height):
                        if img[i, x] < 50:
                            cnt = cnt + 1
                        else:
                            break
                    cntMap[y, x] = cnt
                    valMap.append(cnt)
        cv2.imwrite("cntMap.jpg", cntMap)
        print(valMap)

    def convolution (self, _k, _image):

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
                        pixel_x = x + (ky - 1);                
                        weighted_pixel_sum += _k[ky, kx] * _image[pixel_y, pixel_x]  
                         
                filtered[y, x] = weighted_pixel_sum / kernel_sum
        return filtered * 255

    def combine(self, data1, data2):
        print('')
