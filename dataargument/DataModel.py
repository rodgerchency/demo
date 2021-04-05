import os
import numpy as np
from keras.utils import np_utils, plot_model
import random as Random
from keras.preprocessing import image as Image
from keras.utils import np_utils  # 用來後續將 label 標籤轉為 one-hot-encoding

class DataModel:
  
    def __init__(self, rootPath, extraPath, splitIndex):    
        self._idxTrain = 0
        self._idxTest = 0

        self._rootPath = rootPath
        self._extraPath = extraPath    
        self._splitIndex = splitIndex
        
        self._imgPath = []
        self._labels = []
        self._trainPath = []
        self._testPath = []
        self._trainLabel = []
        self._testLabel = []
        files = os.listdir(rootPath)
        allImgPaths = []
        for d in files:
            wordFiles = os.listdir(rootPath+ d)
            for f in wordFiles:
                allImgPaths.append(rootPath + d + '/' + f)
        
        # 先用rootPath創建testData
        Random.shuffle(allImgPaths)
        for imgPath in allImgPaths:
            # new/三/三_0_1.jpg, newOri/三/三_0_1.jpg
            purePath = self.clearPath(imgPath)
            self._imgPath.append(imgPath)
            self._labels.append(ord(purePath[0]))

        self._trainPath = self._imgPath[:self._splitIndex]
        self._trainLabel = self._labels[:self._splitIndex]
        self._testPath = self._imgPath[self._splitIndex:]
        self._testLabel = self._labels[self._splitIndex:]
        print('train ' + str(len(self._trainPath)) + ',' + str(len(self._trainLabel)))
        print('test ' + str(len(self._testPath)) + ',' + str(len(self._testLabel)))

        allImgPaths = []
        cnt = 0
        if extraPath is not None:
            print('開始加載extraPath')
            files = os.listdir(extraPath)
            for d in files:
                wordFiles = os.listdir(extraPath + d)
                cnt = cnt + len(wordFiles)
                for f in wordFiles:
                    allImgPaths.append(extraPath + d + '/' + f)
        print(cnt)
        Random.shuffle(allImgPaths)
        
        for imgPath in allImgPaths:
            purePath = self.clearPath(imgPath)
            self._trainPath.append(imgPath)
            self._trainLabel.append(ord(purePath[0]))
        print('train ' + str(len(self._trainPath)) + ',' + str(len(self._trainLabel)))

        self._encodeTrain, trainLabelNor = self.normalizeLabel(self._trainLabel)
        self._encodeTest, testLabelNor = self.normalizeLabel(self._testLabel)
        self._labelTrainOneHot = np_utils.to_categorical(trainLabelNor)
        self._labelTestOneHot = np_utils.to_categorical(testLabelNor)
    
    # 回傳train Img
    def getNextTrain(self, batchSize):

        while True:
            if self._idxTrain >= len(self._trainPath):
                self._idxTrain = 0
            tempPaths = self._trainPath[self._idxTrain:self._idxTrain + batchSize]
            imgs = None
            for path in tempPaths:
                img = Image.load_img(path, grayscale=True)
                img_array = Image.img_to_array(img)
                imgs.append(img_array)
            
            returnLabels = self._labelTrainOneHot[self._idxTrain:self._idxTrain + batchSize]
            self._idxTrain = self._idxTrain + batchSize
            yield np.array(imgs),  returnLabels

    # 回傳train Img
    def getNextTest(self, batchSize):
        
        while True:    
            if self._idxTest >= len(self._testPath):
                self._idxTest = 0
            tempPaths = self._testPath[self._idxTest:self._idxTest + batchSize]
            imgs = None
            for path in tempPaths:
                img = Image.load_img(path, grayscale=True)
                img_array = Image.img_to_array(img)
                imgs.append(img_array)
            
            returnLabels = self._labelTestOneHot[self._idxTest:self._idxTest + batchSize]
            self._idxTest = self._idxTest + batchSize
            yield np.array(imgs),  returnLabels
        
    def clearPath(self, path):
        return path.replace(self._rootPath, '').replace(self._extraPath, '')
  
    def normalizeLabel(self, labels):
        encodeList = []
        newLabels = []
        # 先統計
        for label in labels:
            if not label in encodeList:
                encodeList.append(label)
    #     print(encodeList);
        for label in labels:
            newLabels.append(encodeList.index(label))
        return encodeList, newLabels