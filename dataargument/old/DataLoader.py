import os
from PIL import Image
import numpy as np

class DataLoader:

    def __init__(self, path):

        self._pictPaths = {}
        files = os.listdir(path)
        print(len(files))
        for d in files:
            wordFiles = os.listdir(path + '/' + d)
            print(d + ',' + str(len(wordFiles)))
            for f in wordFiles:
                if f[0] not in self._pictPaths:
                    self._pictPaths[f[0]] = []
                # print(f)
                img_path = path + '/' + f[0] + '/' + f
                self._pictPaths[f[0]].append(img_path)
    
    def getData(self):
        return self._pictPaths
    
    def save(self, path):
        npObj = np.array(self._pictPaths)
        
        np.save(path, npObj)