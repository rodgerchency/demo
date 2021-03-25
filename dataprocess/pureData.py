
# 把資料集中到新的資料夾，並且屏除重複的圖片
import os
from PIL import Image
from PIL import ImageChops 

def compare(list1, imgA):
    for img in list1:
        diff = ImageChops.difference(img, imgA)
        if diff.getbbox() is None:
            return True
    return False

def read(path, dicts):
    files = os.listdir(rootPath)
    for f in files:
        if f[0] not in dicts:
            dicts[f[0]] = []
        img_path = rootPath + '/' + f
        img_array = Image.open(img_path)
        if not compare(dicts[f[0]], img_array):
            dicts[f[0]].append(img_array)
    return dicts

rootPath = '../trainData'

picts = {}
picts = read('../trainData', picts)
picts = read('../testData', picts)



for key in picts:
    if not os.path.isdir(key):
        os.mkdir(key)
    for i in range(len(picts[key])):
        picts[key][i].save(key + '/' + key + '_' + str(i) + '.jpg')


