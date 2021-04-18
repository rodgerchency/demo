import numpy as np
from PIL import Image,ImageDraw,ImageFont


class WordUtil:
    
    def __init__(self, imgUrl, name):
        
        # img = cv2.imread(imgUrl).astype(float) / 255.0    
        
        img = Image.open(imgUrl)
        kernel_sharp = (np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]]))
        
        dataEdge = self.convolution(kernel_sharp, img)       
        imgNew = self.combine(dataEdge, img)
        # return imgNew
        imgNew.save(name)

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
        i_width, i_height = _image.size
        # i_width, i_height = _image.shape[0], _image.shape[1]
        k_width, k_height = _k.shape[0], _k.shape[1]
        
        
        imgData = _image.load()
        # prepare the output array
        filtered = np.zeros_like(_image)
        output_img = Image.new("RGB", (i_width, i_height))
        outdata = output_img.load()
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
                        weighted_pixel_sum += _k[ky, kx] * imgData[pixel_x, pixel_y]  
                         
                # filtered[y, x] = weighted_pixel_sum / kernel_sum
                val = int (weighted_pixel_sum / kernel_sum)
                # if val > 2:
                #     val = 255
                if val > 50:
                    val = 255
                outdata[x, y] = (val, 0, 0)
        # return filtered * 255
        return output_img

    def combine(self, img1, img2):
        
        width, height = img1.size
        output_img = Image.new("RGB", (width, height))
        outdata = output_img.load()
        data1 = img1.load()
        data2 = img2.load()
        for x in range(width):
            for y in range(height):
                # outdata[x, y] = data1[x, y]
                if data1[x, y][0] == 255:
                    outdata[x, y] = (255, 0, 0)
                else:
                    outdata[x, y] = (data2[x, y], data2[x, y], data2[x, y])
        return output_img
