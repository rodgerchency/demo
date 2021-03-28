
from CCLabel import CCLabel
from DataLoader import DataLoader
import os
from PIL import Image
import random
from itertools import combinations

path = '../dataprocess/total/三/三_1.jpg'
# img = Image.open(path)
# img.crop((20, 17, 31, 19)).save('crop.jpg')
cclabel = CCLabel(path)

imgs = cclabel.getScaleImgs()

for i in range(729):
    imgs[i].save('new%i.jpg'%(i))

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
