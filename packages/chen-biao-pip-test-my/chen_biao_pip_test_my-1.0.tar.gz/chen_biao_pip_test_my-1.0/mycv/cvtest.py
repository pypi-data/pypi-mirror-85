# -*- encoding: utf-8 -*-
"""
@File    : cvtest.py
@Time    : 2020/11/9 21:21
@Author  : biao chen
@Email   : 1259319710@qq.com
@Software: PyCharm
"""
import cv2
import os
import numpy as np


def readImg(ImgPath, Channel=3):
    if type(ImgPath) != type("test"):
        print("TypeError: expect ImgPath to be a string, get {}!".format(type(ImgPath)))
    if type(Channel) != type(1):
        print("TypeError: expect Channel to be a int, get {}!".format(type(Channel)))
    if not os.path.exists(ImgPath):
        print("PathError: Path is not exists!")
        return None
    if Channel == 3:
        return cv2.imread(ImgPath, 1)
    elif Channel == 1:
        return cv2.imread(ImgPath, 0)
    else:
        print("ChannelError: The number of channels can only be =3 or =1!")
        return None


def showImg(windowName, img, isTransform=False):
    if type(windowName) != type("test"):
        print("TypeError: expect ImgPath to be a string, get {}!".format(type(windowName)))
        return
    if type(img) != type(np.array([1, 2])):
        print("TypeError: expect Channel to be a numpy.array, get {}!".format(type(img)))
        return
    if type(isTransform) != type(True):
        print("TypeError: expect Channel to be a bool, get {}!".format(type(isTransform)))
        return
    if isTransform:
        cv2.namedWindow(windowName, cv2.WINDOW_FREERATIO)
    cv2.imshow(windowName, img)



