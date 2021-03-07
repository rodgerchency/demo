# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 09:26:27 2021

@author: rodger
"""

import cv2
import numpy as np
from MnistDataLoader import MnistDataLoader
from HOSVD import HOSVD
from MLPNetwork import MLPNetwork
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils  # 用來後續將 label 標籤轉為 one-hot-encoding  

loader = MnistDataLoader()
trainGroup = loader.getTrainGroup()
testGroup = loader.getTestGroup()
allGroup = loader.getAllGroup()

hosvd = HOSVD()

Ac = hosvd.getAc(np.array(allGroup), 28, 28, 10)

# hosvd.letsHosvd(tr)

xTrain, yTrain = loader.getTrains()
xTest, yTest = loader.getTest()

ziTrain = [[] for _ in range(len(xTrain))]
ziTest = [[] for _ in range(len(xTest))]
for i in range(len(xTrain)):
    idx = np.where(yTrain[i] == 1)[0][0]
    ziTrain[i].append(hosvd.calcZi(xTrain[i].reshape(28, 28), Ac[idx], 2000))

ziTrain = np.array(ziTrain).reshape(np.array(ziTrain).shape[0], 28)

for i in range(len(xTest)):    
    idx = np.where(yTest[i] == 1)[0][0]
    ziTest[i].append(hosvd.calcZi(xTest[i].reshape(28, 28), Ac[idx], 2000))

ziTest = np.array(ziTest).reshape(np.array(ziTest).shape[0], 28)
A = 0
idx = np.where(yTrain[i] == 1)[0][0]
for i in range(2000):
    A = A + (ziTrain[0][i] * Ac[idx][:,:,i])

cv2.imwrite('img_A' + str(i) + '.jpg', A)

# 建立簡單的線性執行的模型
model = Sequential()
# Add Input layer, 隱藏層(hidden layer) 有 256個輸出變數
model.add(Dense(units=256, input_dim=2000, kernel_initializer='normal', activation='relu'))
# Add output layer
model.add(Dense(units=10, kernel_initializer='normal', activation='softmax'))

# 編譯: 選擇損失函數、優化方法及成效衡量方式
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

mlp = MLPNetwork(xTrain = ziTrain , xTest = ziTest, yTrain = yTrain, yTest = yTest)
# mlp.training(model)