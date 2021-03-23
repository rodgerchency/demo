# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 22:30:47 2021

@author: rodger
"""

import cv2
import numpy as np

import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import PIL
from PIL import Image

img_path = './a.jpg'
# img = Image.load_img(img_path, grayscale=True)
# img_array = Image.img_to_array(img)
img = cv2.imread(img_path)
# cv2.imwrite('testimg1.jpg', img_array);

# 圖片灰階
grayscaleimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# plt.imshow(grayscaleimg,cmap='gray')


# 圖片二值化
ret, binary = cv2.threshold(grayscaleimg, 110, 255, cv2.THRESH_BINARY) # 110這個數字可改
# plt.imshow(binary,cmap='Greys',interpolation='None')
rawimg = binary - binary[0,1] #有這欄 圖的最低就會變成0 圖會變成黑底白字
# plt.imshow(rawimg)

# counting non-zero value by row , axis y
row_nz = []
for row in rawimg.tolist():
    row_nz.append(len(row) - row.count(0))
#plt.plot(row_nz)


idx=np.array(row_nz)>(max(row_nz)/4) #截出上下的範圍
np.where(idx==1)[0][0],np.where(idx==1)[0][-1]
up_y=np.where(idx==1)[0][-1] #上界
down_y=np.where(idx==1)[0][0] #下界
rawimg1=rawimg[down_y:up_y,]
# plt.imshow(rawimg1)

# counting non-zero value by column, x axis
col_nz = []
for col in rawimg1.T.tolist():
    col_nz.append(len(col) - col.count(0))
plt.plot(col_nz)

idy=np.not_equal(col_nz,0)
record_y=[] #如果有八個數字，裡面應該要有九個格子(一開始找出七個，前後插入變九個)
for i in range(0,(len(np.where(idy==1)[0])-1)):
    # 如果下一個數是0就略過，直到找到下一個數不是0的位置
    if(np.where(idy==1)[0][i+1]-np.where(idy==1)[0][i]==1):
        pass
    else:
        record_y.append(np.where(idy==1)[0][i])

# 插入第一個非0位置跟最後一個非0的位置
record_y.insert(0,np.where(idy==1)[0][0])
record_y.append(np.where(idy==1)[0][-1])

# 檢查數字
rm_id=[]
if len(record_y)>9:
    for j in range(0,len(record_y)-1):
        temp=np.array(col_nz[record_y[j]:record_y[j+1]])
        #如果只是雜訊，就刪掉
        if sum(temp>(max(col_nz)/4))==0:
            rm_id.append(record_y[j+1])

for x in rm_id:
     record_y.remove(x)
     
for i in range(0,len(record_y)-1):
    a=binary[down_y:up_y,record_y[i]:record_y[i+1]]
    a=cv2.resize(a, (50, 50), interpolation=cv2.INTER_CUBIC)
    # img_name='rodger.jpg'
    # cv2.imwrite(img_name,a)
    plt.imshow(a)