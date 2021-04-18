
import cv2
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import os
import math, random
from PIL import ImageChops 
from fontTools.ttLib import TTFont

from DataLoader import DataLoader
from FontDrawer import FontDrawer
from WordUtil import WordUtil

# wordUtil = WordUtil('../dataprocess/trainChina/乃_1.jpg')
# wordUtil = WordUtil('乃0.jpg')
path = 'testFontChina/'
dataLoader = DataLoader(path)
picts = dataLoader.getData()
for key in picts:
    cnt = 0
    for path in picts[key]:
        WordUtil(path, 'testFontEdge/%s_%i.png'%(key, cnt))
        cnt = cnt + 1



fonts = os.listdir('fonts')
cnt = 0
for i in fonts:
    # print(str(cnt) + ',' + i)
    cnt = cnt + 1

# dataLoader = DataLoader('../trainData/')
# HuaKangTiFan = ImageFont.truetype("HuaKangTiFan-BiaoZhunTi-1.otf", 36, 0)
# SentyPea = ImageFont.truetype("SentyPea.ttf", 36, 0)

def DrawChinese(txt,font):
    print(font)
    image = np.ones(shape=(50,50),dtype=np.uint8) * 255
    x = Image.fromarray(image)
    draw = ImageDraw.Draw(x)
    draw.text((20,0),txt,(0),font=font)
    # p = np.array(x)
    # p  = cv2.cvtColor(p,cv2.COLOR_RGB2BGR)
    # return p
    return x

def hasWord(fontName, txt):
    fontType = os.path.join("fonts", fontName)
    font = TTFont(fontType)
    uniMap = font['cmap'].tables[0].ttFont.getBestCmap()
    # print (ord(txt) in uniMap.keys())
    return (ord(txt) in uniMap.keys())
# def compare(list1, imgA):
#     cnt = 0
#     for img in list1:
#         diff = ImageChops.difference(img, imgA)
#         if diff.getbbox() is None:
#             return True, cnt        
#         cnt = cnt + 1
    
#     return False, -1

# img = DrawChinese('乃',  ImageFont.truetype('fonts/' + fonts[0], 36, 0))
# img.save('abc.png')


# imgs = []
# for i in range(len(fonts)):
#     if hasWord(fonts[i], '薩'):
#         fontDrawer = FontDrawer('薩', ImageFont.truetype('fonts/' + fonts[i], 36, 0), 'part1/乃_f%i_.png'%(i))
#     # print(fonts[i])
#     if  fontDrawer.getImg() is None:
#         continue
#     hasSame, idx = compare(imgs, fontDrawer.getImg())
#     if not hasSame:
#         imgs.append(fontDrawer.getImg())
#     else:
#         print('%i have same pic %i'%(i, idx))


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

# dataLoader = DataLoader('../trainData/')
# picts = dataLoader.getData()
# for key in picts:
#     cntTr = 0
#     cntTe = 0
#     cnt = 0
#     for i in range(len(fonts)):
#         # FontDrawer(key, ImageFont.truetype('fonts/' + fonts[i], 36, 0), 'totalFontChina/%s_%i.png'%(key, cnt))
#         cnt = cnt + 1
#         if cntTe > 15 or random.randint(0,1) == 1:
#             FontDrawer(key, ImageFont.truetype('fonts/' + fonts[i], 36, 0), 'trainFontChina/%s_%i.png'%(key, cntTr))
#             cntTr = cntTr + 1
#         else:
#             FontDrawer(key, ImageFont.truetype('fonts/' + fonts[i], 36, 0), 'testFontChina/%s_%i.png'%(key, cntTe))
#             cntTe = cntTe + 1

# dataLoader = DataLoader('../trainData/')
# picts = dataLoader.getData()
# for key in picts:
#     cntTr = 0
#     cntTe = 0
#     cnt = 0
#     for i in range(len(fonts)):
#         if hasWord(fonts[i], key) == False:
#             continue
#         # FontDrawer(key, ImageFont.truetype('fonts/' + fonts[i], 36, 0), 'totalFontChina/%s_%i.png'%(key, cnt))
#         cnt = cnt + 1
#         if cntTe > 15 or random.randint(0,1) == 1:
#             FontDrawer(key, ImageFont.truetype('fonts/' + fonts[i], 36, 0), 'trainFontChina/%s_%i.png'%(key, cntTr))
#             cntTr = cntTr + 1
#         else:
#             FontDrawer(key, ImageFont.truetype('fonts/' + fonts[i], 36, 0), 'testFontChina/%s_%i.png'%(key, cntTe))
#             cntTe = cntTe + 1