
from PIL import Image, ImageDraw
from SplitWord import SplitWord
from DataLoader import DataLoader


# splitWord = SplitWord('../wordMacker/trainFontChina/乃_1.png')
# splitWord.save('temp_')


dataLoader = DataLoader('../wordMacker/testFontChina/')
picts = dataLoader.getData()

for key in picts:
  cnt = 0
  for path in picts[key]:
      splitWord = SplitWord(path) 
      splitWord.save('%s_%i_'%(key, cnt))
      cnt = cnt + 1
