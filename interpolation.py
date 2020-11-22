import scipy as sp
import cv2
import numpy as np
import scipy.misc

def test(first, second, out):
    data_frame1 = sp.misc.imread(first, mode='L')
    data_frame3 = sp.misc.imread(second, mode='L')
    data_frame2 = (data_frame1 + data_frame3) / 2
    output = np.round(data_frame2).astype(np.uint8)
    cv2.imwrite(out, output)

df1 = open('output_1/first_1.txt','r')
df2 = open('output_1/second_1.txt','r')
df3 = open('output_1/out_1.txt','r')
cnt = 0
for i,j,k in zip(df1,df2,df3):
    print(cnt,'th image')
    cnt += 1
    first = i.strip()
    second = j.strip()
    out = k.strip()
        
    test(first, second, out)