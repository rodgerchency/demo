# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 20:40:23 2021
@author: rodger
"""

from PIL import Image, ImageDraw
#import Image, ImageDraw

import sys
import math, random
from itertools import product
from ufarray import *

class CCLabel:

    def __init__(self, imgUrl):

        self._imgUrl = imgUrl
        self._labels = None
        self._output_img = None

        print('CCLabel')
        img = Image.open(imgUrl)
        # Threshold the image, this implementation is designed to process b+w
        # images only
        img = img.point(lambda p: p > 190 and 255)
        img = img.convert('1')
        # labels is a dictionary of the connected component data in the form:
        #     (x_coordinate, y_coordinate) : component_id
        #
        # if you plan on processing the component data, this is probably what you
        # will want to use
        #
        # output_image is just a frivolous way to visualize the components.
        (self._labels, self._output_img) = self.run(img)
        # output_img.show()
    
    def getLabels(self):
        return self.getGroup(self._labels)
    
    def getGroup(self, dict):
        group = {}
        for key, value in dict.items():
            # print(key, value)
            if value not in group:
                group[value] = []
            group[value].append(key)
        return group

    def save(self, name):        
        img = Image.open(self._imgUrl)
        group = self.getGroup(self._labels)
        for key in group:
            print(key)
            c = self.getCrop(group[key])
            temp = img.crop(c)
            # temp.save('group%i.png'%(key))
            temp.save(name + '%i.png'%(key))
       
    def scaleImg(self, img, crop):
        
        w = crop[2] - crop[0]
        h = crop[3] - crop[1]
        if w == 1:
            nMaxx = crop[2] + random.randint(0,2)
        else:
            nMaxx = crop[2] + random.randint(-1,1)
        if h == 1:
            nMaxy = crop[3] + random.randint(0,2)
        else:
            nMaxy = crop[3] + random.randint(-1,2)
        w = nMaxx - crop[0]
        h = nMaxy - crop[1]
        print((crop[0], crop[1], nMaxx, nMaxy))
        return img.resize((w, h)), (crop[0], crop[1], nMaxx, nMaxy)

    def getScaleImgs(self):
        imgsC, posesC = self.getCropImgs()
        imgS = [[] for _ in range(len(imgsC))]
        posesS = [[] for _ in range(len(imgsC))]
        for i in range(len(imgsC)):
            print('i=%i,len1=%i,len2=%i'%(i, len(imgsC), len(posesS)))
            imgs, poses = self.getScales(imgsC[i], posesC[i])
            imgS[i] = imgs
            posesS[i] = poses
        
        idxLists = self.getCombIDList(imgS)
        retImgs = self.getImgsByIDLists(idxLists, imgS, posesS)
        return retImgs

    def getScales(self, img, crop):
        imgs = []
        poses = []
        x = []
        y = []
        w = crop[2] - crop[0]
        h = crop[3] - crop[1]
        if w == 1:
            for _ in range(0,3,1):
                x.append(_)
        else:            
            for _ in range(-1,2,1):
                x.append(_)
        if h == 1:
            for _ in range(0,3,1):
                y.append(_)
        else:
            for _ in range(-1,2,1):
                y.append(_)
        for i in x:
            for j in y:
                nMaxx = crop[2] + i
                nMaxy = crop[3] + j
                w = nMaxx - crop[0]
                h = nMaxy - crop[1]
                imgs.append(img.resize((w, h)))
                poses.append((crop[0], crop[1], nMaxx, nMaxy))
        return imgs, poses

    def combinationsList(self, list1, list2):
        comb = []
        for i in list1:
            for j in list2:
                #print('%i %i'%(i, j))
                temp = []
                if type(i) == list:
                    temp = i.copy()
                else:
                    temp.append(i)
                temp.append(j)
                comb.append(temp)
        return comb

    def getCombIDList(self, lists):
        
        idxLists = self.getIndexList(lists)
        length = len(lists)
        if length == 2:
            return self.combinationsList(lists)
        elif length > 2:
            comb = idxLists[0]
            for i in range(1, len(idxLists)):
                comb = self.combinationsList(comb, idxLists[i])
            return comb
        else:
            return idxLists

    def getImgsByIDLists(self, idLists, pImgs, pPoses):
        imgs = []
        for i in range(len(idLists)):
            img = Image.new('L', (50, 50), 255)
            for j in range(len(idLists[i])):
                img.paste(pImgs[j][idLists[i][j]], pPoses[j][idLists[i][j]])
            imgs.append(img)
        return imgs


    # 回傳idx 陣列
    # ex [img1, img2, img3] = [0, 1, 2]
    def getIndexList(self, lists):
        rets = [[] for _ in range(len(lists))]
        for i in range(len(lists)):
            idx = 0
            for j in range(len(lists[i])):
                rets[i].append(idx)
                idx = idx + 1
        return rets
        
    def getCropImgs(self):
        imgs = []
        poss = []
        img = Image.open(self._imgUrl)
        group = self.getGroup(self._labels)
        for key in group:
            print(key)
            c = self.getCrop(group[key])
            temp = img.crop(c)
            imgs.append(temp)
            # poss.append((c[0], c[1]))
            poss.append(c)
        return imgs, poss

    def getCrop(self, list):
        tempX = []
        tempY = []
        for i in range(len(list)):
            tempX.append(list[i][0])  
            tempY.append(list[i][1])  
        minx = min(tempX)
        maxx = max(tempX)
        miny = min(tempY)
        maxy = max(tempY)
        print('minx=%i miny=%i maxx=%i maxy=%i'%(minx, miny, maxx, maxy))
        return (minx, miny, maxx + 1, maxy + 1)

    def run(self, img):
        data = img.load()
        width, height = img.size
    
        # Union find data structure
        uf = UFarray()
    
        #
        # First pass
        #
    
        # Dictionary of point:label pairs
        labels = {}
    
        print(width * height)
        for y, x in product(range(height), range(width)):
    
            #
            # Pixel names were chosen as shown:
            #
            #   -------------
            #   | a | b | c |
            #   -------------
            #   | d | e |   |
            #   -------------
            #   |   |   |   |
            #   -------------
            #
            # The current pixel is e
            # a, b, c, and d are its neighbors of interest
            #
            # 255 is white, 0 is black
            # White pixels part of the background, so they are ignored
            # If a pixel lies outside the bounds of the image, it default to white
            #
    
            # If the current pixel is white, it's obviously not a component...
            if data[x, y] == 255:
                pass
    
            # If pixel b is in the image and black:
            #    a, d, and c are its neighbors, so they are all part of the same component
            #    Therefore, there is no reason to check their labels
            #    so simply assign b's label to e
            elif y > 0 and data[x, y-1] == 0:
                labels[x, y] = labels[(x, y-1)]
    
            # If pixel c is in the image and black:
            #    b is its neighbor, but a and d are not
            #    Therefore, we must check a and d's labels
            elif x+1 < width and y > 0 and data[x+1, y-1] == 0:
    
                c = labels[(x+1, y-1)]
                labels[x, y] = c
    
                # If pixel a is in the image and black:
                #    Then a and c are connected through e
                #    Therefore, we must union their sets
                if x > 0 and data[x-1, y-1] == 0:
                    a = labels[(x-1, y-1)]
                    uf.union(c, a)
    
                # If pixel d is in the image and black:
                #    Then d and c are connected through e
                #    Therefore we must union their sets
                elif x > 0 and data[x-1, y] == 0:
                    d = labels[(x-1, y)]
                    uf.union(c, d)
    
            # If pixel a is in the image and black:
            #    We already know b and c are white
            #    d is a's neighbor, so they already have the same label
            #    So simply assign a's label to e
            elif x > 0 and y > 0 and data[x-1, y-1] == 0:
                labels[x, y] = labels[(x-1, y-1)]
    
            # If pixel d is in the image and black
            #    We already know a, b, and c are white
            #    so simpy assign d's label to e
            elif x > 0 and data[x-1, y] == 0:
                labels[x, y] = labels[(x-1, y)]
    
            # All the neighboring pixels are white,
            # Therefore the current pixel is a new component
            else: 
                labels[x, y] = uf.makeLabel()
    
        #
        # Second pass
        #
    
        uf.flatten()
    
        colors = {}

        # Image to display the components in a nice, colorful way
        output_img = Image.new("RGB", (width, height))
        outdata = output_img.load()

        for (x, y) in labels:
    
            # Name of the component the current point belongs to
            component = uf.find(labels[(x, y)])
            
            # Update the labels with correct information
            labels[(x, y)] = component
    
            # Associate a random color with this component 
            if component not in colors: 
                colors[component] = (random.randint(0,255), random.randint(0,255),random.randint(0,255))

            # Colorize the image
            outdata[x, y] = colors[component]
        # output_img.save('output_img.jpg')
        return (labels, output_img)