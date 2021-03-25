
import os
from PIL import Image

class DataLoader:

    def __init__(self, path):

        self._pictPaths = {}
        files = os.listdir(path)
        for d in files:
            wordFiles = os.listdir(path + '/' + d)
            for f in wordFiles:
                if f[0] not in self._pictPaths:
                    self._pictPaths[f[0]] = []
                print(f)
                img_path = path + '/' + f
                self._pictPaths[f[0]].append(img_path)
    
    def getData(self):
        return self._pictPaths