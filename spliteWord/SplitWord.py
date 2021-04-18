
from PIL import Image, ImageDraw
#import Image, ImageDraw

import sys
import math, random
from itertools import product

class SplitWord:
    
    def __init__(self, imgUrl):
        
        self.img = Image.open(imgUrl)        
        self.c1, self.c2, self.c3, self.c4 = self.getCoreCrop(self.img)
    
    def save(self, name):        
        # self.img.crop(self.c1).save('%s_c1.png'%(name))
        # self.img.crop(self.c2).save('%s_c2.png'%(name))
        # self.img.crop(self.c3).save('%s_c3.png'%(name))
        # self.img.crop(self.c4).save('%s_c4.png'%(name))

        self.saveCent(self.img.crop(self.c1), 'testC1/%s_c1.png'%(name))
        self.saveCent(self.img.crop(self.c2), 'testC2/%s_c2.png'%(name))
        self.saveCent(self.img.crop(self.c3), 'testC3/%s_c3.png'%(name))
        self.saveCent(self.img.crop(self.c4), 'testC4/%s_c4.png'%(name))
    
    def saveCent(self, img, name):
       
        w,h = img.size       
        posx = int(12.5 - (w / 2))
        posy = int(12.5 - (h / 2))
        newImg = Image.new('L', (25, 25), 255)
        newImg.paste(img, (posx,posy))
        newImg.save(name)


    def getCoreCrop(self, img):
           
        outdata = img.load()
        minx = 50
        maxx = 0
        miny = 50
        maxy = 0
        for x in range(50):
            for y in range(50):
                if outdata[x,y] < 200:
                    if x < minx:
                        minx = x
                    if x > maxx:
                        maxx = x
                    if y < miny:
                        miny = y
                    if y > maxy:
                        maxy = y
        w = maxx - minx
        h = maxy - miny
        cenx = int(minx + (w/2))
        ceny = int(miny + (h/2)) 
        c1 = (minx, miny, cenx + 1, ceny + 1)
        c2 = (cenx, miny, maxx + 1, ceny + 1)
        c3 = (minx, ceny, cenx + 1, maxy + 1)
        c4 = (cenx, ceny, maxx + 1, maxy + 1)
        return c1, c2, c3, c4
        # return (minx, miny, maxx + 1, maxy +1)