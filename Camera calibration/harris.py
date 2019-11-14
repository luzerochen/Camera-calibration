# -*- coding: utf-8 -*-
# @Time    : 2019/10/4 23:23
# @Author  : 0chen
# @FileName: harris.py
# @Software: PyCharm
# @Blog    : http://www.0chen.xyz

import cv2
import numpy as np

WINDOWSIZE = 3
K = 0.04
THRESHOLD = 0.08
def calculate_graduate(gray):
    '''
    :param gray: 图像的灰度
    :returns graduate_x, graduate_y: x轴和y轴方向的弧度导数，实际为差值
    '''
    lx, ly = gray.shape
    graduate_x = np.zeros(gray.shape)
    graduate_y = np.zeros(gray.shape)
    for i in range(lx):
        for j in range(ly):
            if i != lx-1:
                graduate_x[i][j] = gray[i+1][j]-gray[i][j]
            else:
                graduate_x[i][j] = graduate_x[i-1][j]
            if j != ly-1:
                graduate_y[i][j] = gray[i][j+1]-gray[i][j]
            else:
                graduate_y[i][j] = graduate_y[i][j-1]
    return [graduate_x, graduate_y]

def calculate_R(graduate_x, graduate_y, w_size, k):
    '''
    :param graduate_x:
    :param graduate_y:
    :param w_size:
    :param k:
    :return R: R[i][j]越大，为角点的可能性越大
    '''
    lx, ly = graduate_x.shape
    R = np.zeros((lx, ly))
    for i in range(0, lx, w_size):
        for j in range(0, ly, w_size):
            m = np.zeros((2, 2))
            if i+w_size > lx or j+w_size > ly: continue
            for x in range(i, i+w_size):
                for y in range(j, j+w_size):
                    m[0][0] += graduate_x[x][y] * graduate_x[x][y]
                    m[0][1] += graduate_x[x][y] * graduate_y[x][y]
                    m[1][0] += graduate_x[x][y] * graduate_y[x][y]
                    m[1][1] += graduate_y[x][y] * graduate_y[x][y]
                    R[i][j] = np.linalg.det(m) - pow(np.trace(m), 2) * k
    return R


def tag_corner(img, R, w_size, threshold):
    """
    R[i][j] 大于 threshold * R_max,则判定为有角点，并打上标记
    :param img:
    :param R:
    :param w_size:
    :param threshold:
    :return:
    """
    lx, ly = R.shape
    R_max = np.max(R)
    print(R_max)
    for i in range(lx):
        for j in range(ly):
            if R[i][j] > R_max*threshold:
                for x in range(i, i+w_size):
                    for y in range(j, j+w_size):
                        img[x][y] = [0, 0, 255]
    return img


if __name__ == '__main__':

    filename = r'chessboard\chessboard (1).jpg'
    img = cv2.imread(filename)
    img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    graduate_x, graduate_y = calculate_graduate(gray)
    R = calculate_R(graduate_x, graduate_y, WINDOWSIZE, K)

    img = tag_corner(img, R, WINDOWSIZE, THRESHOLD)
    cv2.namedWindow('harris', 0)
    cv2.imshow('harris', img)
    cv2.waitKey(0)
