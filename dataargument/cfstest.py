from PIL import Image
p = Image.open("1.png")
# 注意位置顺序为左、上、右、下
cuts = [(20,20,40,70),(60,20,90,70),(100,10,130,60),(140,20,170,50)]
# for i,n in enumerate(cuts,1):
#  temp = p.crop(n) # 调用crop函数进行切割
#  temp.save("cut%s.png" % i)
 
def binarizing(img,threshold):
  """传入image对象进行灰度、二值处理"""
  img = img.convert("L") # 转灰度
  pixdata = img.load()
  w, h = img.size
  # 遍历所有像素，大于阈值的为黑色
  for y in range(h):
    for x in range(w):
      if pixdata[x, y] < threshold:
        pixdata[x, y] = 0
      else:
        pixdata[x, y] = 255
  return img

def vertical(img):
  """传入二值化后的图片进行垂直投影"""
  pixdata = img.load()
  w,h = img.size
  ver_list = []
  # 开始投影
  for x in range(w):
    black = 0
  for y in range(h):
    if pixdata[x,y] == 0:
      black += 1
  ver_list.append(black)
  # 判断边界
  l,r = 0,0
  flag = False
  cuts = []
  for i,count in enumerate(ver_list):
    # 阈值这里为0
    if flag is False and count > 0:
      l = i
      flag = True
    if flag and count == 0:
      r = i-1
      flag = False
      cuts.append((l,r))
  return cuts
 
p = Image.open('1.png')
b_img = binarizing(p,200)
v = vertical(b_img)

import queue
 
def cfs(img):
  """传入二值化后的图片进行连通域分割"""
  pixdata = img.load()
  w,h = img.size
  print('w=%i'%w)
  print('h=%i'%h)

  visited = set()
  q = queue.Queue()
  offset = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
  cuts = []
  for x in range(w):
    for y in range(h):
      x_axis = []
      #y_axis = []
      # print(pixdata[x,y])
      if pixdata[x,y] == 0 and (x,y) not in visited:
        q.put((x,y))
        visited.add((x,y))
      while not q.empty():
        x_p, y_p = q.get()
        for x_offset, y_offset in offset:
          x_c, y_c = x_p + x_offset, y_p + y_offset
          if (x_c,y_c) in visited:
            continue
          visited.add((x_c,y_c))
          try:
            # print(pixdata[x_c,y_c])
            if pixdata[x_c,y_c] == 0:
              q.put((x_c,y_c))
              x_axis.append(x_c)
              #y_axis.append(y_c)
          except:
              print('pass')
              pass
      if x_axis:
        min_x,max_x = min(x_axis),max(x_axis)
        # print("min_x=%i"%min_x)
        # print("max_x=%i"%max_x)
        if max_x - min_x > 3:
          # 宽度小于3的认为是噪点，根据需要修改
          cuts.append((min_x,max_x))
  return cuts

p = Image.open('1.png')
b_img = binarizing(p,200)
cuts = cfs(b_img)

for i in range(len(cuts)):
  cuts[i].save("cut%s.png"%i)