# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 09:14:49 2021

@author: rodger
"""

import cv2
import os
import numpy as np
from keras.preprocessing import image as Image
from keras.utils import np_utils, plot_model
import random as Random
from tensorflow.examples.tutorials.mnist import input_data


class MnistDataLoader:

    def __init__(self):        
        # number 1 to 10 data
        self._mnist = input_data.read_data_sets('../MNIST_data', one_hot=True)
        self._trainImages = [[] for _ in range(10)]
        self._testImages = [[] for _ in range(10)]
        self._AllImages =[[] for _ in range(10)]
        imgTrain = self._mnist.train.images
        labelsTrain = self._mnist.train.labels
        for i in range(len(labelsTrain)):
            idx = np.where(labelsTrain[i] == 1)[0][0]
            self._trainImages[idx].append(imgTrain[idx])
            self._AllImages[idx].append(imgTrain[idx])

        imgTest = self._mnist.test.images
        labelsTest = self._mnist.test.labels
        for i in range(len(labelsTest)):
            idx = np.where(labelsTest[i] == 1)[0][0]
            self._testImages[idx].append(imgTest[idx])
            self._AllImages[idx].append(imgTest[idx])
        
        # print('檢查資料')
        # print(np.array(self._trainImages).shape)
        # print(np.array(self._testImages).shape)

    def getTrainGroup(self):
        return self._trainImages
    
    def getTestGroup(self):
        return self._testImages
    
    def getAllGroup(self):
        return self._AllImages
    
    def getTrains(self):
        return self._mnist.train.images, self._mnist.train.labels
    
    def getTest(self):
        return self._mnist.test.images, self._mnist.test.labels
