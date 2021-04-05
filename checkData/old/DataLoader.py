import os
import numpy as np
from keras.utils import np_utils, plot_model
import random as Random
from keras.preprocessing import image as Image

class DataLoader:

  def __init__(self, rootPath, splitIndex, extraPath):

    self._rootPath = rootPath
    self._extraPath = extraPath
    self._images = []
    self._labels = []
    self._splitIndex = splitIndex
    
    self._trainImg = []
    self._testImg = []
    self._labelTrain = []
    self._labelTest = []
    files = os.listdir(rootPath)
    allImgPaths = []
    for d in files:
      wordFiles = os.listdir(rootPath+ d)
      for f in wordFiles:
        # path = wordFiles + '/' + f
        allImgPaths.append(rootPath + d + '/' + f)
        # self._images.append(Image.open(path))
        # self._labels.append(ord(f[0]))
    
    Random.shuffle(allImgPaths)
    for imgPath in allImgPaths:
      purePath = self.clearPath(imgPath)
      img = Image.load_img(imgPath, grayscale=True)
      img_array = Image.img_to_array(img)
      self._images.append(img_array)
      self._labels.append(ord(purePath[0]))

    self._trainImg = self._images[:self._splitIndex]
    self._labelTrain = self._labels[:self._splitIndex]
    self._testImg = self._images[self._splitIndex:]
    self._labelTest = self._labels[self._splitIndex:]
    print('train ' + str(len(self._trainImg)) + ',' + str(len(self._labelTrain)))
    print('test ' + str(len(self._testImg)) + ',' + str(len(self._labelTest)))

    allImgPaths = []
    cnt = 0
    if extraPath is not None:
      print('開始加載extraPath')
      files = os.listdir(extraPath)
      for d in files:
        wordFiles = os.listdir(extraPath + d)
        cnt = cnt + len(wordFiles)
        for f in wordFiles:
          # print(f)
          # path = wordFiles + '/' + f
          allImgPaths.append(extraPath + d + '/' + f)
    print(cnt)
    Random.shuffle(allImgPaths)
    
    for imgPath in allImgPaths:
      purePath = self.clearPath(imgPath)
      img = Image.load_img(imgPath, grayscale=True)
      img_array = Image.img_to_array(img)
      self._trainImg.append(img_array)
      self._labelTrain.append(ord(purePath[0]))
    print('train ' + str(len(self._trainImg)) + ',' + str(len(self._labelTrain)))
    
  def getTrains(self):
    return self._trainImg, self._labelTrain
    # return self._images[:self._splitIndex], self._labels[:self._splitIndex]

  def getTests(self):
    return self._testImg, self._labelTest
    # return self._images[self._splitIndex:], self._labels[self._splitIndex:]

  def clearPath(self, path):
    return path.replace(self._rootPath, '').replace(self._extraPath, '')
  