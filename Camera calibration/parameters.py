# -*- coding: utf-8 -*-
# @Time    : 2019/10/10 15:55
# @Author  : 0chen
# @FileName: parameters.py
# @Software: PyCharm
# @Blog    : http://www.0chen.xyz

import numpy as np
def readpoint():
    """
    读取getcorner计算出的角点坐标，以及世界坐标
    :return:
    """
    with open('data/picturepoint.txt', 'r') as file:
        datastr = file.read().split('\n')
    picturepoint = []
    for point in datastr[:-1]:
        picturepoint.append(point.split())
    picturepoint = np.array(picturepoint, dtype=float)

    with open('data/worldpoint.txt', 'r') as file:
        datastr = file.read().split('\n')
    worldpoint = []
    for point in datastr[:-1]:
        worldpoint.append(point.split())
    worldpoint = np.array(worldpoint, dtype=float)
    return [picturepoint, worldpoint]


def homographymatrix(p_point, w_point):
    """
    计算单应性矩阵
    :param p_point: 图像像素坐标
    :param w_point: 世界坐标
    :return homography_matrix: 返回单应性矩阵
    """
    A, B = [], []
    for i in range(p_point.shape[0]):
        x, y = p_point[i]
        a, b, c = w_point[i]
        A.append([a, b, 1, 0, 0, 0, -a * x, -b * x])
        A.append([0, 0, 0, a, b, 1, -a * y, -b * y])
        B.append([x])
        B.append([y])
    A = np.array(A)
    B = np.array(B)
    X = np.linalg.lstsq(A, B)[0]
    X = np.vstack((X, [1])).reshape(3, 3)
    return X

def Vij(H, i, j):
    return np.array([H[0, i] * H[0, j],
                     H[0, i] * H[1, j] + H[1, i] * H[0, j],
                     H[1, i] * H[1, j],
                     H[2, i] * H[0, j] + H[0, i] * H[2, j],
                     H[2, i] * H[1, j] + H[1, i] * H[2, j],
                     H[2, i] * H[2, j]]).reshape(1, 6)



def tocoefficient(h):
    v01 = Vij(h, 0, 1)
    v00 = Vij(h, 0, 0)
    v11 = Vij(h, 1, 1)
    return np.array(np.vstack((v01, v00-v11)))


def intrinsic_parameters(b):
    """
    :param b:
    :return intrinsic_parameters: return the intrinsic matrix
    """
    vc = (b[1] * b[3] - b[0] * b[4]) / (b[0] * b[2] - b[1] * b[1])
    l = b[5] - (b[3] * b[3] + vc * (b[1] * b[2] - b[0] * b[4])) / b[0]
    alpha = np.sqrt((l / b[0]))
    beta = np.sqrt(((l * b[0]) / (b[0] * b[2] - b[1] * b[1])))
    gamma = -1 * ((b[1]) * (alpha * alpha) * (beta / l))
    uc = (gamma * vc / beta) - (b[3] * (alpha * alpha) / l)

    intrinsic = np.array([[alpha, gamma, vc],
                          [0, beta, uc],
                          [0, 0, 1.0]])
    return intrinsic


def getintrinsic():
    picturepoint, worldpoint = readpoint()
    coefficient = None
    homography = []
    for i in range(0, picturepoint.shape[0], WEIGH * HIGH):
        p_point = picturepoint[i:i + WEIGH * HIGH]
        w_point = worldpoint[i:i + WEIGH * HIGH]
        homography_matrix = homographymatrix(p_point, w_point)
        homography.append(homography_matrix)
        if coefficient is None:
            coefficient = tocoefficient(homography_matrix)
        else:
            coefficient = np.vstack((coefficient, tocoefficient(homography_matrix)))

    u, s, vh = np.linalg.svd(coefficient)
    b = vh[np.argmin(s)]
    return [intrinsic_parameters(b), homography]


WEIGH = 7
HIGH = 7
if __name__ == '__main__':
    intrinsic_parameters, _ = getintrinsic()
    print(intrinsic_parameters)