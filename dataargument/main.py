
from CCLabel import CCLabel
from SimpleLabel import SimpleLabel
from DataLoader import DataLoader
from DataModel import DataModel
import os
from PIL import Image
import random
from itertools import combinations
import numpy as np

# dataModel = DataModel('../dataprocess/total/', '../dataprocess/new/', 3188)

# dataLoader = DataLoader('../dataprocess/total')
# dataLoader.save('../dataprocess/total')
# test = np.load('../dataprocess/total.npy' ,allow_pickle=True)
# 創建資料夾
# dataLoader = DataLoader('../dataprocess/total')
# picts = dataLoader.getData()
# newRoot = '../dataprocess/newOri'
# if not os.path.isdir(newRoot):
#     os.mkdir(newRoot)
# for key in picts:
#   if not os.path.isdir(newRoot + '/' + key):
#     os.mkdir(newRoot + '/' + key)

# 紀錄已完成項目
# dataLoader = DataLoader('../dataprocess/new')
# picts = dataLoader.getData()
# cnt = 0
# haveDone = []
# for key in picts:
#   # haveDone[key] = 1
#   haveDone.append(key)
#   print(str(cnt) + ',' + key + ',' + str(len(picts[key])))
#   cnt = cnt + 1


# needs = ['諦','諸','識','身','道','遠','阿','除','集','離','顛','香','鼻',]
# 資料擴增
# dataLoader = DataLoader('../dataprocess/total')
# newRoot = '../dataprocess/new'
# picts = dataLoader.getData()
# for key in picts:
#   print(key)
#   # if key in haveDone:
#   #   continue
#   # if key not in needs:
#   #     continue
#   cnt = 0
#   for pathPic in picts[key]:
#     print(pathPic)
#     cclabel = CCLabel(pathPic)
#     imgs = cclabel.getScaleImgs()
#     if imgs is not None:
#       print(len(imgs))
#       lens = len(imgs)
#       if lens > 120:
#         lens = 120
#       for i in range(lens):
#         imgs[i].save(newRoot + '/' + key + '/' + key + '_' + str(cnt) + '_' + str(i) + '.jpg')
#     else:
#         print(pathPic + ' is None')
#     cnt = cnt + 1

# 資料擴增Ori
# dataLoader = DataLoader('../dataprocess/total')
# newRoot = '../dataprocess/newOri'
# picts = dataLoader.getData()
# for key in picts:
#   print(key)
#   # if key in haveDone:
#   #   continue
#   cnt = 0
#   for pathPic in picts[key]:
#     simpleLabel = SimpleLabel(pathPic)
#     imgs = simpleLabel.getScaleImgs()
#     if imgs is not None:
#       print(len(imgs))
#       lens = len(imgs)
#       if lens > 120:
#         lens = 120
#       for i in range(lens):
#         imgs[i].save(newRoot + '/' + key + '/' + key + '_' + str(cnt) + '_' + str(i) + '.jpg')
#     cnt = cnt + 1
    
# path = '../dataprocess/total/三/三_1.jpg'
# img = Image.open(path)
# img.crop((20, 17, 31, 19)).save('crop.jpg')
# cclabel = CCLabel(path)

# imgs = cclabel.getScaleImgs()

# def func(list1,list2):
#     comb = []
#     for i in list1:
#         for j in list2:
#             #print('%i %i'%(i, j))
#             temp = []
#             if type(i) == list:
#                 temp = i.copy()
#             else:
#                 temp.append(i)
#             temp.append(j)
#             comb.append(temp)
#     return comb            
        
# comb = func([0,1,2], [0,1,2])
# comb = func(comb, [0,1,2])

# labels = cclabel.getLabels()
# for i in range(100): 
#     imgs, poss = cclabel.getCropImgs()
#     img = Image.new('L', (50, 50), 255)
#     img.paste(imgs[0], poss[0])
#     img.paste(imgs[1], poss[1])
#     img.paste(imgs[2], poss[2])
#     img.save('new%i.jpg'%(i))


# cnt = 0
# for img in imgs:
#     img.save('img%i.jpg'%cnt)
#     cnt = cnt + 1
    
# img = Image.new('L', (50, 50), 255)
# img.paste(imgs[0], poss[0])
# img.paste(imgs[1], poss[1])
# img.paste(imgs[2], poss[2])
# img.save('new.jpg')


# cclabel.save()

# dataLoader = DataLoader('../dataprocess/total')

# picts = dataLoader.getData()
# for key in picts:
#     print(picts[key][0])
#     cclabel = CCLabel(picts[key][0])    
#     if not os.path.isdir(key):
#         os.mkdir(key)
#     cclabel.save(key + '/' + key + '_0_')
