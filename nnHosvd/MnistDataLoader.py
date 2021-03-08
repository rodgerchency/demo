import numpy as np
import tensorflow as tf

class MnistDataLoader:

    def __init__(self):
      
        (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
        self._trains = train_images
        self._tests = test_images
        self._trainLabels = train_labels
        self._testLabels = test_labels
        # number 1 to 10 data        
        self._trainImages = [[] for _ in range(10)]
        self._testImages = [[] for _ in range(10)]
        self._AllImages =[[] for _ in range(10)]
        imgTrain = train_images
        labelsTrain = train_labels
        for i in range(len(labelsTrain)):
            idx = labelsTrain[i]
            self._trainImages[idx].append(imgTrain[idx])
            self._AllImages[idx].append(imgTrain[idx])

        imgTest = test_images
        labelsTest = test_labels
        for i in range(len(labelsTest)):
            idx = labelsTest[i]
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
        return self._trains, self._trainLabels
    
    def getTest(self):
        return self._tests, self._testLabels