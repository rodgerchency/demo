import os
import numpy as np
from keras.utils import np_utils, plot_model
import random as Random
from keras.preprocessing import image as Image

class DataLoader:

  def __init__(self, trainPath, testPath, extraPath, useGray):
    
    self.trainPath = trainPath
    self.testPath = testPath
    self.extraPath = extraPath
    self.imgTrain = []
    self.imgTest = []
    self.labelTrain = []
    self.labelTest = []
    # Train path
    files = os.listdir(trainPath)
    allImgPaths = []
    for f in files:
        allImgPaths.append(trainPath + f)
    # Extra Path
    if extraPath is not None:
      files = os.listdir(extraPath)
      for f in files:
          allImgPaths.append(extraPath + f)
    
    Random.shuffle(allImgPaths)
    for path in allImgPaths:
        purePath = self.clearPath(path)
        img = Image.load_img(path, grayscale=useGray)
        img_array = Image.img_to_array(img)
        self.imgTrain.append(img_array)
        self.labelTrain.append(ord(purePath[0]))

    # Test path
    files = os.listdir(testPath)
    allImgPaths = []
    for f in files:
        allImgPaths.append(testPath + f)

    Random.shuffle(allImgPaths)
    for path in allImgPaths:
        purePath = self.clearPath(path)
        img = Image.load_img(path, grayscale=useGray)
        img_array = Image.img_to_array(img)
        self.imgTest.append(img_array)
        self.labelTest.append(ord(purePath[0]))
    
    # Normalized
    self.elTrain, self.oneHotTrain = self.normalizeLabel(self.labelTrain)
    self.elTest, self.oneHotTest = self.normalizeLabel(self.labelTest)
    print('train ' + str(len(self.imgTrain)) + ',' + str(len(self.oneHotTrain)))
    print('train ' + str(len(self.imgTest)) + ',' + str(len(self.oneHotTest)))
    print('elTrain:%i,elTest:%i'%(len(self.elTrain),len(self.elTest)))
    for i in range(len(self.elTrain)):
      print(self.elTrain[i] == self.elTest[i])
      print('train=%i,test=%i'%(self.elTrain[i],self.elTest[i]))

  def idxTrain(self, idx):
    return chr(self.elTrain[idx])

  def getTrains(self):
    # return (self.imgTrain), (self.oneHotTrain)
    return np.array(self.imgTrain), np.array(self.oneHotTrain)

  def getTests(self):
    return np.array(self.imgTest), np.array(self.oneHotTest)

  def clearPath(self, path):
    if self.extraPath is not None:
      return path.replace(self.trainPath, '').replace(self.testPath, '').replace(self.extraPath, '')
    else:
      return path.replace(self.trainPath, '').replace(self.testPath, '')
  
  def normalizeLabel(self, labels):      
        encodeList = []
        newLabels = []
        # 先統計
        for label in labels:
            if not label in encodeList:
                encodeList.append(label)
        encodeList.sort()
        # print(encodeList);
        for label in labels:
            newLabels.append(encodeList.index(label))
        print('newLabel max=%i,min=%i'%(max(newLabels),min(newLabels)))
        return encodeList, newLabels
  