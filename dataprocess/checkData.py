
import os
from PIL import Image
from PIL import ImageChops 

def compare(list1, imgA):
    for img in list1:
        diff = ImageChops.difference(img, imgA)
        if diff.getbbox() is None:
            return True
    return False

# img1 = Image.open('../trainData/三_1.jpg')
# img2 = Image.open('../trainData/三_1.jpg')
# img3 = Image.open('../trainData/三_0.jpg')
# print(compare([img1],img1))
# print(compare([img1],img2))
# print(compare([img1,img3],img3))

def loadData(path):
    imgs = []
    files = os.listdir(path)
    for f in files:
        img_path = path + '/' + f
        img = Image.open(img_path)
        imgs.append(img)
    return imgs

# imgsTrain = loadData('../trainData')
imgsTest = loadData('../testData')

path = '../trainData'
files = os.listdir(path)
for f in files:
    img_path = path + '/' + f
    img = Image.open(img_path)
    if compare(imgsTest, img) == False:
        img.save('trainChina/' +  f)


    
        
    