

#Author: Chi-Wei Chiang
#載入資料集
import h5py
with h5py.File('usps.h5', 'r') as hf:
    train = hf.get('train')
    X_tr = train.get('data')[:]
    y_tr = train.get('target')[:]
    test = hf.get('test')
    X_te = test.get('data')[:]
    y_te = test.get('target')[:]
    
#把圖片資料分類，放在digits二維矩陣裡面
#數字0的照片就放在digits[0]，數字1的照片就放在digits[1]，依此類推...
digits = [[] for _ in range(10)]
for item in zip(y_tr, X_tr):
    dig = item[0] # dig=6
    img = item[1].reshape(16, 16) ###讀取預設為長度256的向量，轉成16*16矩陣
    digits[dig].append(img)

#列表顯示圖片數量
imgTotal = 0
for i in range(10):
    lenOfImg = len(digits[i])
    print('數字:', i, ', 圖片數量=', lenOfImg)
    imgTotal += lenOfImg
print('-----------------------\n', '         總數量 =', imgTotal)