import cv2
import h5py
with h5py.File('../usps.h5', 'r') as hf:
    train = hf.get('train')
    X_tr = train.get('data')[:]
    y_tr = train.get('target')[:]
    test = hf.get('test')
    X_te = test.get('data')[:]
    y_te = test.get('target')[:]
    
    
import numpy as np

#把圖片資料分類，放在digits二維矩陣裡面
#數字0的照片就放在digits[0]，數字1的照片就放在digits[1]，依此類推...
digits = [[] for _ in range(10)]
imgTrain = []
labelTrain = []
for item in zip(y_tr, X_tr):
    dig = item[0] # dig=6
    img = item[1].reshape(16, 16) ###讀取預設為長度256的向量，轉成16*16矩陣
    digits[dig].append(img)
    imgTrain.append(img)
    labelTrain.append(dig)

#列表顯示圖片數量
imgTotal = 0
for i in range(10):
    lenOfImg = len(digits[i])
    print('數字:', i, ', 圖片數量=', lenOfImg)
    imgTotal += lenOfImg
print('-----------------------\n', '         總數量 =', imgTotal)

from sktensor import dtensor
from sktensor import tucker

def letsHosvd(n):
    #指定An=數字n的圖片陣列 (131*16*16)
    An = digits[n]

    #把 An轉置成跟課本一樣的維度 (16*16*131)
    Ant = np.transpose(An, (1,2,0))

    #把 Ant轉成 Tensor A，才能使用hosvd方法
    A = dtensor(Ant)


    #把轉換後的 tensor 進行 HOSVD分解: A = S x1 U1 x2 U2 x3 U3
    # S: core tensor
    # U1, U2, U3: 特徵矩陣
    return tucker.hosvd(A, A.shape)

from tensorly import fold, unfold

def findAi(U, S):
    #計算 S x1 U1
    S_x1U1 = fold(U[0].dot(unfold(S, 0)), 0, S.shape)
    #計算 S x1 U1 x2 U2
    S_x1U1_x2U2 = fold(U[1].dot(unfold(S_x1U1, 1)), 1, S.shape)
    return S_x1U1_x2U2

Ac = [[] for _ in range(10)] #宣告二維陣列
for i in range(10): #數字i從0到9，算每個數字的A1、A2、A3
    u, s = letsHosvd(i)
    Ac[i].append(findAi(u, s))

def calcZi(pZ, pA):
    return np.tensordot(pZ, pA) / np.tensordot(pA, pA)

imgTest = []
labelTest = []
for item in zip(y_te, X_te):
    labelTest.append(item[0])
    imgTest.append(item[1].reshape(16, 16))

zi = []
ziTrain = [[] for _ in range(len(imgTrain))]
ziTest = [[] for _ in range(len(imgTest))]
# train 
for i in range(len(imgTrain)):
    idx = labelTrain[i]
    for j in range(256):
        z = calcZi(imgTrain[i], Ac[0][0][:,:,j])
        ziTrain[i].append(z)

# test 
for i in range(len(imgTest)):
    idx = labelTest[i]
    for j in range(256):
        z = calcZi(imgTest[i], Ac[0][0][:,:,j])
        ziTest[i].append(z)
     
from keras.models import Sequential
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils  # 用來後續將 label 標籤轉為 one-hot-encoding

y_train = np.array(labelTrain)
X_train = np.array(ziTrain)
y_test = np.array(labelTest)
X_test = np.array(ziTest)

# 建立簡單的線性執行的模型
model = Sequential()
# Add Input layer, 隱藏層(hidden layer) 有 256個輸出變數
model.add(Dense(units=512, input_dim=256, kernel_initializer='normal', activation='relu'))
# Add output layer
model.add(Dense(units=10, kernel_initializer='normal', activation='softmax'))

# 編譯: 選擇損失函數、優化方法及成效衡量方式
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 將 training 的 label 進行 one-hot encoding，例如數字 7 經過 One-hot encoding 轉換後是 0000001000，即第7個值為 1
y_TrainOneHot = np_utils.to_categorical(y_train)
y_TestOneHot = np_utils.to_categorical(y_test)

# 將 training 的 input 資料轉為2維
X_train_2D = X_train.reshape(len(X_train), 256).astype('float32')  
X_test_2D = X_test.reshape(len(X_test), 256).astype('float32')  

# x_Train_norm = X_train_2D/255
# x_Test_norm = X_test_2D/255

# 進行訓練, 訓練過程會存在 train_history 變數中
train_history = model.fit(x=X_train_2D, y=y_TrainOneHot, validation_split=0.2, epochs=100, batch_size=800, verbose=2)  

# 顯示訓練成果(分數)
scores = model.evaluate(X_test_2D, y_TestOneHot)  
print()  
print("\t[Info] Accuracy of testing data = {:2.1f}%".format(scores[1]*100.0))  
