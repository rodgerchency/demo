# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 16:44:42 2021

@author: rodger
"""
from keras.models import Sequential
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils  # 用來後續將 label 標籤轉為 one-hot-encoding  
from matplotlib import pyplot as plt

class MLPNetwork:

    def __init__(self, xTrain, xTest, yTrain, yTest):
        print('MLPNetwork')
        self._xTrain = xTrain
        self._xTest = xTest
        self._yTrain = yTrain
        self._yTest = yTest

    def training(self, model, size):    

        # 將 training 的 label 進行 one-hot encoding，例如數字 7 經過 One-hot encoding 轉換後是 0000001000，即第7個值為 1
        # y_TrainOneHot = np_utils.to_categorical(self._yTrain)
        # y_TestOneHot = np_utils.to_categorical(self._yTest)

        # 將 training 的 input 資料轉為2維
        X_train_2D = self._xTrain.reshape(len(self._xTrain), size).astype('float32')  
        X_test_2D = self._yTest.reshape(len(self._yTest), size).astype('float32')  

        # x_Train_norm = X_train_2D/255
        # x_Test_norm = X_test_2D/255

        # 進行訓練, 訓練過程會存在 train_history 變數中
        train_history = model.fit(x=X_train_2D, y=self._yTrain, validation_split=0.2, epochs=100, batch_size=800, verbose=2)  

        # 顯示訓練成果(分數)
        scores = model.evaluate(X_test_2D, self._yTest)
        print("\t[Info] Accuracy of testing data = {:2.1f}%".format(scores[1]*100.0))  
