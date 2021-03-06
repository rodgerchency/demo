# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 10:51:25 2021

@author: rodger
"""

import os
import numpy as np
from numpy import linalg
from numpy.linalg import svd

import tensorly as tl
from tensorly import fold, unfold

A = np.array([[1, 3], [2, 4]])
B = np.array([[5, 7], [6, 8]])
# T = np.array([
#     [[1, 3], [2, 4]],
#     [[5, 7], [6, 8]]
# ])
tensor = tl.tensor([
    [[1, 3], [2, 4]],
    [[5, 7], [6, 8]]
])
M = np.array([[10, 0], [0, 100], [1, 1]])
tensorM = tl.tensor(M)
x = tl.tenalg.multi_mode_dot(tensor,tensorM,2)
