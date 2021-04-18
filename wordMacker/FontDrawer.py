
from PIL import Image, ImageDraw
import numpy as np

class FontDrawer:

    def __init__(self, txt, font, name):
        
        self.imgNew = None
        image = np.ones(shape=(50,50),dtype=np.uint8) * 255
        img = Image.fromarray(image)
        draw = ImageDraw.Draw(img)
        draw.text((0,0),txt,(0),font=font)
        data = img.load()
        w, h = img.size
        
        minx = 50
        miny = 50
        maxx = 0
        maxy = 0
        cnt = 0
        for x in range(w):
            for y in range(h):
                if data[x, y] < 220:
                    cnt = cnt + 1
                    if x < minx:
                        minx = x
                    if x > maxx:
                        maxx = x
                    if y < miny:
                        miny = y
                    if y > maxy:
                        maxy = y
        if cnt == 0:
            print('empty')
            return
        w = maxx - minx
        h = maxy - miny
        # img.save('%s_%i_%i.png'%(name, w, h))

        posx = int(25 - (w / 2))
        posy = int(25 - (h / 2))

        temp = img.crop((minx, miny, maxx + 1, maxy + 1))
        self.imgNew = Image.new('L', (50, 50), 255)
        self.imgNew.paste(temp, (posx,posy))
        self.imgNew.save(name)
    
    def getImg(self):
        return self.imgNew

