import os
import cv2
import numpy as np


word_dir=os.path.abspath('.')
imgfile='1.jpg'


img_mat=cv2.imread(imgfile,cv2.IMREAD_GRAYSCALE)\


def cut(mat,times=4):
    width,height=mat.shape
    width=width-width%4
    height=height-height%4
    mat=mat[:width,:height]
    return mat


def compress(mat,times=4):
    width,height=mat.shape
    new_mat=np.zeros((int(width/times),int(height/times)))
    for x in range(0,width,times):
        for y in range(0,height,times):
            sum=0
            for i in range(times):
                for j in range(times):
                    sum+=mat[x+i,y+i]
            sum/=times*times
            new_mat[int(x/times),int(y/times)]=int(sum)
    new_mat=cut(new_mat)
    return new_mat

img_mat=cut(img_mat)
steps=1
for i in range(steps):
    img_mat=compress(img_mat)

height,width=img_mat.shape
print(img_mat)


'''
盲文unicode字符对应utf十六进制编码：
八个点，从E2A080开始，A*控制最下面两个点，顺序从左到右
剩下的8*控制上面6个点64种情况，顺序从上到下从左到右
1 8
2 16
4 32
'''

ch=[]
cut_value=int((img_mat.max()+img_mat.min())/2)
boo_mat=np.array([[1 if val>cut_value else 0 for val in line] for line in img_mat])
print(boo_mat)
def load():
    for y in range(0,height,4):
        for x in range(0,width,2):
            six_offset=0
            for i in range(3):
                six_offset+=2**i*boo_mat[y+i,x]
                six_offset+=2**i*boo_mat[y+i,x+1]*8
            two_offset=1*boo_mat[y+3,x]+2*boo_mat[y+3,x+1]
            char=r'\xe2'+(hex(int('0xa0',16)+two_offset)).replace('0x','\\x')+(hex(int('0x80',16)+six_offset).replace('0x','\\x'))
            char=eval("b'{0}'".format(char))
            ch.append(bytes(char))
        ch.append(bytes('\n',encoding='utf-8'))
load()
output_file='output.txt'
os.remove(output_file)
with open(output_file,'wb') as f:
    f.writelines(ch)
