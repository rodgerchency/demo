
import cv2
from DataLoader import DataLoader

# dataLoader = DataLoader('../dataprocess/trainChina/', '../dataprocess/trainChina/', '../dataprocess/newTrainChina/')
dataLoader = DataLoader('../dataprocess/trainChina/', '../dataprocess/trainChina/', None)

x_train, y_train = dataLoader.getTrains()
x_test, y_test = dataLoader.getTests()

for i in range(10):
    print(x_train[i].shape)
    cv2.imwrite('test%i.jpg'%i, x_train[i])
    print(str(i) + dataLoader.idxTrain(i))
