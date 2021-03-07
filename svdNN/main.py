# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 21:28:00 2021

@author: rodger
"""
import os
import cv2
import tensorflow as tf
import numpy as np
from numpy import linalg
from numpy.linalg import svd

from tensorly import fold, unfold

from sktensor import dtensor
from sktensor import tucker

from DataLoader import DataLoader

len_data = 109
loader = DataLoader(50, 50)
trains = loader.getTrainDigits()
tests = loader.getTestDigits()

def letsHosvd(n):
    # print('letsHosvd')
    temp = np.array(trains[n] + tests[n])
    An = temp.reshape(temp.shape[0],50,50)
    # print(An.shape)
    Ant = np.transpose(An, (1,2,0))
    # print(Ant.shape)
    A = dtensor(Ant)
    #把轉換後的 tensor 進行 HOSVD分解: A = S x1 U1 x2 U2 x3 U3
    # S: core tensor
    # U1, U2, U3: 特徵矩陣
    return tucker.hosvd(A, A.shape)

def findAi(U, S):
    #計算 S x1 U1
    S_x1U1 = fold(U[0].dot(unfold(S, 0)), 0, S.shape)
    #print('<S x1 U1>.shape=', S_x1U1.shape)

    #計算 S x1 U1 x2 U2
    S_x1U1_x2U2 = fold(U[1].dot(unfold(S_x1U1, 1)), 1, S.shape)
    return S_x1U1_x2U2

def calcZi(z, ai, n):
    zi = []
    # print('calcZi')
    # print(z.shape)
    # print(ai.shape)
    for i in range(n):
        # re = np.tensordot(z, ai[:,:,i]) / np.tensordot(ai[:,:,i], ai[:,:,i])
        zi.append(np.tensordot(z, ai[:,:,i]) / np.tensordot(ai[:,:,i], ai[:,:,i]))
    return zi 

Ac = []
for i in range(109): #數字i從0到9，算每個數字的A1、A2、A3
    u, s = letsHosvd(i)
    Ai = findAi(u, s)
    # A = fold(u[2].dot(unfold(Ai, 2)), 2, s.shape) 
    Ac.append(Ai)


##########################
# Test 
##########################
# trImg = trains[0][0].reshape(50, 50)
# cv2.imwrite('img_tr_00.jpg', trImg)

# Zi = calcZi(trImg, Ac[0], 30)
# A=0
# for i in range(1):
#     A = A + (Zi[i] * Ac[0][:,:,i])
     
# cv2.imwrite('img_A.jpg', A)


ziTrain = []
labelTrain = []
ziTest = []
labelTest = []
for i in range(109):
   
    for j in range(len(trains[i])):
        ziTrain.append(calcZi(trains[i][j][:,:,0], Ac[i], 30))
        labelTrain.append(i)
    # print('finish ziTrain')
    
    for j in range(len(tests[i])):
        ziTest.append(calcZi(tests[i][j][:,:,0], Ac[i], 30))
        labelTest.append(i)
    
    # print('finish ziTest')


from keras.models import Sequential
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils  # 用來後續將 label 標籤轉為 one-hot-encoding  
from matplotlib import pyplot as plt

y_train = np.array(labelTrain)
X_train = np.array(ziTrain)
y_test = np.array(labelTest)
X_test = np.array(ziTest)

# 建立簡單的線性執行的模型
model = Sequential()
# Add Input layer, 隱藏層(hidden layer) 有 256個輸出變數
model.add(Dense(units=30, input_dim=30, kernel_initializer='normal', activation='relu'))
# Add output layer
model.add(Dense(units=109, kernel_initializer='normal', activation='softmax'))

# 編譯: 選擇損失函數、優化方法及成效衡量方式
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 將 training 的 label 進行 one-hot encoding，例如數字 7 經過 One-hot encoding 轉換後是 0000001000，即第7個值為 1
y_TrainOneHot = np_utils.to_categorical(y_train)
y_TestOneHot = np_utils.to_categorical(y_test)

# 將 training 的 input 資料轉為2維
X_train_2D = X_train.reshape(len(X_train), 30).astype('float32')  
X_test_2D = X_test.reshape(len(X_test), 30).astype('float32')  

# x_Train_norm = X_train_2D/255
# x_Test_norm = X_test_2D/255

# 進行訓練, 訓練過程會存在 train_history 變數中
train_history = model.fit(x=X_train_2D, y=y_TrainOneHot, validation_split=0.2, epochs=100, batch_size=800, verbose=2)  

# 顯示訓練成果(分數)
scores = model.evaluate(X_test_2D, y_TestOneHot)  
print()  
print("\t[Info] Accuracy of testing data = {:2.1f}%".format(scores[1]*100.0))  

# # 預測(prediction)
# X = x_Test_norm[0:10,:]
# predictions = model.predict_classes(X)
# # get prediction result
# print(predictions)