# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 09:26:27 2021

@author: rodger
"""

import cv2
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils  # 用來後續將 label 標籤轉為 one-hot-encoding  

from MnistDataLoader import MnistDataLoader

from HOSVD import HOSVD

from tensorly import fold, unfold

loader = MnistDataLoader()
trainGroup = loader.getTrainGroup()
testGroup = loader.getTestGroup()
allGroup = loader.getAllGroup()

# hosvd = HOSVD()

# Ac = hosvd.getAc(np.array(allGroup), 28, 28, 1)
# u, s = hosvd._letsHosvd(allGroup[0], 28, 28)
# ai = hosvd._findAi(u, s)
# A = fold(u[2].dot(unfold(ai, 2)), 2, s.shape) 
# cv2.imwrite('img_train0.jpg', A[:,:,0])