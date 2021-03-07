# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 09:32:45 2021

@author: rodger
"""

import numpy as np
from tensorly import fold, unfold
from sktensor import dtensor
from sktensor import tucker

class HOSVD:

    def __init__(self): 
        print('HOSVD init')
    
    def getAc(self, tensor, width, height, lenData):

        Ac = [] #宣告二維陣列
        for i in range(lenData): #數字i從0到9，算每個數字的A1、A2、A3
            u, s = self._letsHosvd(tensor[i], width, height)
            Ai = self._findAi(u, s)
            Ac.append(Ai)
        return Ac
    
    def _letsHosvd(self, tensor, width, height):
        print('letsHosvd')
        temp = np.array(tensor)
        An = temp.reshape(temp.shape[0], width, height)
        print(An.shape)
        Ant = np.transpose(An, (1,2,0))
        print(Ant.shape)
        A = dtensor(Ant)
        #把轉換後的 tensor 進行 HOSVD分解: A = S x1 U1 x2 U2 x3 U3
        # S: core tensor
        # U1, U2, U3: 特徵矩陣
        return tucker.hosvd(A, A.shape)

    def _findAi(self, U, S):
        #計算 S x1 U1
        S_x1U1 = fold(U[0].dot(unfold(S, 0)), 0, S.shape)
        #print('<S x1 U1>.shape=', S_x1U1.shape)

        #計算 S x1 U1 x2 U2
        S_x1U1_x2U2 = fold(U[1].dot(unfold(S_x1U1, 1)), 1, S.shape)
        return S_x1U1_x2U2

    def calcZi(self, z, ai, n):
        zi = []
        # print('calcZi')
        # print(z.shape)
        # print(ai.shape)
        for i in range(n):
            # re = np.tensordot(z, ai[:,:,i]) / np.tensordot(ai[:,:,i], ai[:,:,i])
            zi.append(np.tensordot(z, ai[:,:,i]) / np.tensordot(ai[:,:,i], ai[:,:,i]))
        return zi 

    # Ac = []
    # for i in range(109): #數字i從0到9，算每個數字的A1、A2、A3
    #     u, s = letsHosvd(i)
    #     Ai = findAi(u, s)
    #     # A = fold(u[2].dot(unfold(Ai, 2)), 2, s.shape) 
    #     Ac.append(Ai)

    # ziTrain = []
    # labelTrain = []
    # ziTest = []
    # labelTest = []
    # for i in range(109):
    
    #     for j in range(len(trains[i])):
    #         ziTrain.append(calcZi(trains[i][j][:,:,0], Ac[i], 30))
    #         labelTrain.append(i)
    #     # print('finish ziTrain')
        
    #     for j in range(len(tests[i])):
    #         ziTest.append(calcZi(tests[i][j][:,:,0], Ac[i], 30))
    #         labelTest.append(i)