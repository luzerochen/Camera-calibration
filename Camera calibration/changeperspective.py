# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 14:38
# @Author  : 0chen
# @FileName: changeperspective.py
# @Software: PyCharm
# @Blog    : http://www.0chen.xyz


import numpy as np
import parameters
import cv2
def extrinsic_matrix(intrinsic, homography):
    """
    计算外参矩阵
    :param intrinsic:  内参矩阵
    :param homography:  单应性矩阵
    :return:
    """
    inv = np.linalg.inv(intrinsic)
    h1 = homography[:, 0].reshape(3, 1)
    h2 = homography[:, 1].reshape(3, 1)
    h3 = homography[:, 2].reshape(3, 1)
    lam = 1/np.linalg.norm(np.dot(inv, h1))
    r1 = np.dot(lam, np.dot(inv, h1))
    r2 = np.dot(lam, np.dot(inv, h2))
    r3 = np.cross(r1.transpose(), r2.transpose()).transpose()
    t = np.dot(lam, np.dot(inv, h3))
    s = np.hstack((r1, r2, r3, t))
    extrinsic = np.vstack((s, np.array([0, 0, 0, 1])))
    extrinsic_without_r3 = np.hstack((r1, r2, t))
    return [extrinsic, extrinsic_without_r3]

def change(img, intrinsic, extrinsic, homography):
    """
    改变图片视角，放回鸟瞰的视角
    :param img:
    :param intrinsic:   3*3 matrix
    :param extrinsic:   3*3 matrix
    :param homography:  3*3 matrix
    :return:
    """
    homography_inv = np.linalg.inv(homography)
    newimg = np.zeros(img.shape, np.uint8)
    extrinsic[:3, :2] = np.eye(3, 2)
    changehomography = np.dot(intrinsic, extrinsic)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            old_img_coordinate = np.array([i, j, 1]).reshape(3, 1)
            world_coordinate = np.dot(homography_inv, old_img_coordinate)
            newimg_coordinate = np.dot(changehomography, world_coordinate)
            x = newimg_coordinate[0, 0]/newimg_coordinate[2, 0]
            y = newimg_coordinate[1, 0]/newimg_coordinate[2, 0]
            x, y = int(x), int(y)
            if 0 < x < img.shape[0] and 0 < y < img.shape[1]:
                newimg[x][y] = img[i][j]
    return newimg


if __name__ == '__main__':
    index = 10
    intrinsic, homography_matrix = parameters.getintrinsic()
    extrinsic, extrinsic_without_r3 = extrinsic_matrix(intrinsic, homography_matrix[index-1])
    filename = r'chessboard\chessboard ('+str(index)+').jpg'
    img = cv2.imread(filename)
    newimg = change(img, intrinsic, extrinsic_without_r3, homography_matrix[index-1])
    cv2.namedWindow('new img', 0)
    cv2.imshow('new img', newimg)
    cv2.waitKey(0)


