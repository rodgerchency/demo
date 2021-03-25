
from CCLabel import CCLabel
from DataLoader import DataLoader
import os

# path = 'a.jpg'
# cclabel = CCLabel(path)

# labels = cclabel.getLabels()
# cclabel.save()

dataLoader = DataLoader('../dataprocess/total')

picts = dataLoader.getData()
for key in picts:
    print(picts[key][0])
    cclabel = CCLabel(picts[key][0])    
    if not os.path.isdir(key):
        os.mkdir(key)
    cclabel.save(key + '/' + key + '_0_')
