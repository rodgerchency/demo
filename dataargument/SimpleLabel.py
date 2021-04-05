from PIL import Image, ImageDraw

class SimpleLabel:

    def __init__(self, imgUrl):
        self._imgUrl = imgUrl

    
    def getScaleImgs(self):
        img = Image.open(self._imgUrl)
        crop = self.getCoreCrop()
        temp = img.crop(crop)
        imgMove, posesMove = self.getSimpleMoves(temp, crop)
        imgsScale = []
        posesScale = []
        for i in range(len(imgMove)):
            imgs, poses = self.getSimpleScales(imgMove[i], posesMove[i])
            imgsScale = imgsScale + imgs
            posesScale = posesScale + poses
        retImgs = []
        for i in range(len(imgsScale)):
            imgNew = Image.new('L', (50, 50), 255)
            imgNew.paste(imgsScale[i], posesScale[i])
            retImgs.append(imgNew)
        return retImgs

    def getSimpleMoves(self, img, crop):
        lx = crop[0]
        ly = crop[1]
        rx = crop[2]
        ry = crop[3]
        x = []
        y = []
        imgs = []
        poses = []
        if lx == 0:
          x = [2, 3]
        elif rx == 51:
          x = [-2, -3]
        else:
          x = [-1, -2, 1, 2]
        if ly == 0:
          y = [2, 3]
        elif ry == 51:
          y = [-2, -3]
        else:
          y = [-1, -2, 1, 2]
        for i in x:
            for j in y:
              if i == 0 and y == 0:
                continue
              lx = crop[0] + i
              ly = crop[1] + j
              rx = crop[2] + i
              ry = crop[3] + j
              imgs.append(img)
              poses.append((lx, ly, rx, ry))
        return imgs, poses   

    def getSimpleScales(self, img, crop):
        imgs = []
        poses = []
        x = []
        y = []
        w = crop[2] - crop[0]
        h = crop[3] - crop[1]
        if w == 1:
            x = [2]
        else:
            x = [-3, 3]
        if h == 1:
            y = [2]
        else:
            y = [-3, 3]
        for i in x:
            for j in y:
              if i == 0 and y == 0:
                continue
              nMaxx = crop[2] + i
              nMaxy = crop[3] + j
              w = nMaxx - crop[0]
              h = nMaxy - crop[1]
              imgs.append(img.resize((w, h)))
              poses.append((crop[0], crop[1], nMaxx, nMaxy))
        return imgs, poses

    def getCoreCrop(self):
        img = Image.open(self._imgUrl)    
        outdata = img.load()
        minx = 50
        maxx = 0
        miny = 50
        maxy = 0
        for x in range(50):
            for y in range(50):
                if outdata[x,y] < 200:
                    if x < minx:
                        minx = x
                    if x > maxx:
                        maxx = x
                    if y < miny:
                        miny = y
                    if y > maxy:
                        maxy = y
        return (minx, miny, maxx + 1, maxy +1)

    