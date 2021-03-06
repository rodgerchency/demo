# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 10:14:06 2021

@author: rodger
"""

import numpy as np
from keras.preprocessing import image
from keras.utils import np_utils, plot_model
from numpy import loadtxt

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import random;
import cv2;

from DataLoader import DataLoader


import matplotlib.pyplot as plt
import pandas as pd 

tf.reset_default_graph()

len_data = 109
w = 50; h = 50
# w = 300; h = 300
area = w * h

loader = DataLoader(w, h)

digits = loader.getTrainDigits()
tests = loader.getTestDigits()

import tensorflow as tf
import numpy as np


from sktensor import dtensor
from sktensor import tucker

def letsHosvd(n):
    #指定An=數字n的圖片陣列 (131*16*16)
    # print('letsHosvd ', n, ',', digits.shape, digits[n].shape)
    An = np.array(digits[n]).reshape(41,50,50)

    #把 An轉置成跟課本一樣的維度 (16*16*131)
    Ant = np.transpose(An, (1,2,0))

    #把 Ant轉成 Tensor A，才能使用hosvd方法
    A = dtensor(Ant)


    #把轉換後的 tensor 進行 HOSVD分解: A = S x1 U1 x2 U2 x3 U3
    # S: core tensor
    # U1, U2, U3: 特徵矩陣
    return tucker.hosvd(A, A.shape)

from tensorly import fold, unfold

def findAi(U, S):
    #計算 S x1 U1
    S_x1U1 = fold(U[0].dot(unfold(S, 0)), 0, S.shape)
    #print('<S x1 U1>.shape=', S_x1U1.shape)

    #計算 S x1 U1 x2 U2
    S_x1U1_x2U2 = fold(U[1].dot(unfold(S_x1U1, 1)), 1, S.shape)
    #print('<S x1 U1 x2 U2>.shape=', S_x1U1_x2U2.shape)

    A1 = S_x1U1_x2U2[:,:,0] #mean value of different 3's
    A2 = S_x1U1_x2U2[:,:,1] #the dominating directions of variation from the "mean value"
    A3 = S_x1U1_x2U2[:,:,2] #the dominating directions of variation from the "mean value"
    
    return A1, A2, A3

Ac = [[] for _ in range(len_data)] #宣告二維陣列
for i in range(len_data): #數字i從0到9，算每個數字的A1、A2、A3
    u, s = letsHosvd(i)
    A1, A2, A3 = findAi(u, s)
    Ac[i].append(A1) #數字 i的A1
    Ac[i].append(A2) #數字 i的A2
    Ac[i].append(A3) #數字 i的A3

def calcZi(pZ, pA):
    return np.tensordot(pZ, pA) / np.tensordot(pA, pA)

def recognize(pZ, pA):
    result = -1
    residual = 0
    for i in range(len_data):
        #取出A1、A2、A3
        A1 = pA[i][0]
        A2 = pA[i][1]
        A3 = pA[i][2]
        
        #計算z1、z2、z3，z是純量數值
        z1 = calcZi(pZ, A1)
        z2 = calcZi(pZ, A2)
        z3 = calcZi(pZ, A3)
        
        #把zi跟Ai分別相乘
        z1A1 = z1*(A1)
        z2A2 = z2*(A2)
        z3A3 = z3*(A3)
        
        #求距離r
        r = np.linalg.norm(pZ-(z1A1+z2A2+z3A3), ord='fro')
        
        #如果距離比上次計算更小，表示這次結果更接近
        if (r < residual or result == -1):
            result = i
            residual = r
    
    return result

import matplotlib.pyplot as plt
plt.gray()
fig, ax = plt.subplots(10,3,figsize = (7,30))

correct = 0
wrong = 0

for i in range(109):
    # print(i, ",", np.array(tests[i]).shape)
    for j in range(len(tests[i])):
        teImg = tests[i][j].reshape(50, 50)    
        result = recognize(teImg, Ac)
        # print(result)
        if (result == i):
            correct += 1
        else:
            if (wrong < 10):
                ax[wrong][0].set(title = "input:" + str(i))
                ax[wrong][0].imshow(teImg)
                ax[wrong][1].set(title = "guess:" + str(result))
                ax[wrong][1].imshow(Ac[result][0].reshape(50, 50))
                ax[wrong][2].set(title = "answer:" + str(i))
                ax[wrong][2].imshow(Ac[i][0].reshape(50, 50))
            wrong += 1
# for item in zip(y_te, x_te):
#     teImg = item[1].reshape(16, 16)
#     result = recognize(teImg, Ac)
#     if (result == item[0]):
#         correct += 1
#     else:
#         if (wrong < 10):
#             ax[wrong][0].set(title = "input:" + str(item[0]))
#             ax[wrong][0].imshow(teImg)
#             ax[wrong][1].set(title = "guess:" + str(result))
#             ax[wrong][1].imshow(Ac[result][0].reshape(16, 16))
#             ax[wrong][2].set(title = "answer:" + str(item[0]))
#             ax[wrong][2].imshow(Ac[item[0]][0].reshape(16, 16))
#         wrong += 1

print('答對=', correct, ', 答錯=', wrong, ', 辨認率=', np.round(correct/(correct+wrong), 3), '%\n')
print('辨認錯誤情形參考如下(前10次比對):')