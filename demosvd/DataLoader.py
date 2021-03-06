# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 12:41:10 2020

@author: rodger
"""

import os
import numpy as np
from keras.preprocessing import image as Image
from keras.utils import np_utils, plot_model
import random as Random

class DataLoader:

    def __init__(self, w, h):
        
        # self._w = 50; self._h = 50
        self._w = w; self._h = h
        self._area = self._w * self._h
        self._currIdx = 0

        print(self._w, self._h)

        # train data
        trainFiles = os.listdir('./trainData')
        print(len(trainFiles))
        # Train DataSet
        self._trainImages=[[] for _ in range(109)]
        self._trainFileNames = [[] for _ in range(109)]
        lastName = ''
        idx = -1
        for f in trainFiles:
            img_path = './trainData/' + f
            if lastName != f[0]:
                if idx == -1:
                    idx = 0
                else:
                    idx = idx + 1                
                self._trainFileNames[idx] = f[0]
                lastName = f[0]
            img = Image.load_img(img_path, grayscale=True)
            img_array = Image.img_to_array(img)
            self._trainImages[idx].append(img_array)
        
        # test data
        testFiles = os.listdir('./testData')
        print(len(testFiles))
        # Train DataSet
        self._testImages=[[] for _ in range(109)]
        self._testFileNames = [[] for _ in range(109)]
        lastName = ''
        idx = -1
        for f in testFiles:
            img_path = './testData/' + f
            if lastName != f[0]:    
                if idx == -1:
                    idx = 0
                else:
                    idx = idx + 1                            
                self._testFileNames[idx] = f[0]
                lastName = f[0]
            img = Image.load_img(img_path, grayscale=True)
            img_array = Image.img_to_array(img)
            self._testImages[idx].append(img_array)
        # 檢查資料
        # for i in range(109):            
        #     # print(self._trainFileNames[i] == self._testFileNames[i])
        #     print( i , ",",len(self._trainImages[i]) , len(self._testImages[i]))
        
    def getTrainDigits(self):
        return self._trainImages
    
    def getTestDigits(self):
        return self._testImages
    
    def getLabel(self, idx):
        return self._trainFileNames[idx]
        

