# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 10:55
# @Author  : 0chen
# @FileName: getcorner.py
# @Software: PyCharm
# @Blog    : http://www.0chen.xyz

import cv2
import numpy as np

def pointtofile(worlds_coordinate, pictures_coordinate):
    with open('data/picturepoint.txt', 'w') as file:
        for imgpoints in pictures_coordinate:
            imgpoints = imgpoints.tolist()
            for points in imgpoints:
                file.write("{} {}\n".format(points[0][1], points[0][0]))
    with open('data/worldpoint.txt', 'w') as file:
        for imgpoints in worlds_coordinate:
            imgpoints = imgpoints.tolist()
            for points in imgpoints:
                file.write("{} {} {}\n".format(points[1], points[0], points[2]))

WEIGH = 7
HIGH = 7
if __name__ == '__main__':

    world_coordinate = np.zeros((WEIGH*HIGH, 3), np.float32)
    world_coordinate[:, :2] = np.mgrid[0:WEIGH, 0:HIGH].T.reshape(-1, 2)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    pictures_coordinate, worlds_coordinate = [], []
    for i in range(1, 11, 1):
        filename = r'chessboard\chessboard ('+str(i)+').jpg'
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (WEIGH, HIGH), None)
        if ret is True:
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            worlds_coordinate.append(world_coordinate)
            pictures_coordinate.append(corners)

    pointtofile(worlds_coordinate, pictures_coordinate)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(worlds_coordinate, pictures_coordinate, gray.shape[::-1], None, None)
    # mtx 内参数矩阵
    # dist 畸变系数
    # rvecs 旋转向量
    # tvecs 平移向量
