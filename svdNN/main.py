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


ziTrain = [[] for _ in range(109)]
ziTest = [[] for _ in range(109)]
for i in range(109):
   
    for j in range(len(trains[i])):
        ziTrain[i].append(calcZi(trains[i][j][:,:,0], Ac[i], 30))
    print('finish ziTrain')
    
    for j in range(len(tests[i])):
        ziTest[i].append(calcZi(tests[i][j][:,:,0], Ac[i], 30))
    
    print('finish ziTest')
