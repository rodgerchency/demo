
import cv2
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import os
import math, random

from DataLoader import DataLoader
from FontDrawer import FontDrawer

fonts = os.listdir('fonts')
cnt = 0
for i in fonts:
    print(str(cnt) + ',' + i)
    cnt = cnt + 1

# dataLoader = DataLoader('../trainData/')
# HuaKangTiFan = ImageFont.truetype("HuaKangTiFan-BiaoZhunTi-1.otf", 36, 0)
# SentyPea = ImageFont.truetype("SentyPea.ttf", 36, 0)

def DrawChinese(txt,font):
    image = np.ones(shape=(50,50),dtype=np.uint8) * 255
    x = Image.fromarray(image)
    draw = ImageDraw.Draw(x)
    draw.text((20,0),txt,(0),font=font)
    # p = np.array(x)
    # p  = cv2.cvtColor(p,cv2.COLOR_RGB2BGR)
    # return p
    return x


# img = DrawChinese('乃',  ImageFont.truetype('fonts/' + fonts[0], 36, 0))
# img.save('abc.png')

# for i in range(len(fonts)):
#     FontDrawer('萬', ImageFont.truetype('fonts/' + fonts[i], 36, 0), 'part1/乃_f%i_.png'%(i))
    # img = DrawChinese('乃',  ImageFont.truetype('fonts/' + fonts[i], 36, 0))
    # img.save('part2/乃_%i.png'%(i))

# dataLoader = DataLoader('../trainData/')
# picts = dataLoader.getData()
# for key in picts:
#     cnt = 0
#     for fontPath in fonts:
#         img = DrawChinese(key,  ImageFont.truetype('fonts/' + fontPath, 36, 0))
#         img.save('parts/%s_%i.png'%(key, cnt))
#         cnt = cnt + 1

dataLoader = DataLoader('../trainData/')
picts = dataLoader.getData()
for key in picts:
    cntTr = 0
    cntTe = 0
    cnt = 0
    for i in range(len(fonts)):
        FontDrawer(key, ImageFont.truetype('fonts/' + fonts[i], 36, 0), 'totalFontChina/%s_%i.png'%(key, cnt))
        cnt = cnt + 1
        # if cntTe > 30 or random.randint(0,1) == 1:
        #     FontDrawer(key, ImageFont.truetype('fonts/' + fonts[i], 36, 0), 'trainFontChina/%s_%i.png'%(key, cntTr))
        #     cntTr = cntTr + 1
        # else:
        #     FontDrawer(key, ImageFont.truetype('fonts/' + fonts[i], 36, 0), 'testFontChina/%s_%i.png'%(key, cntTe))
        #     cntTe = cntTe + 1