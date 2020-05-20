
import os
import sys
import glob
import numpy as np
import cv2 as cv 

IMG_RESIZE = 224
ID = 0

def blurImage(img):
    # apply guassian blur on src image
    dst = cv.GaussianBlur(img,(5,5),cv.BORDER_DEFAULT)
    return dst

def resizeImage(img):
    print('Original Dimensions : ',img.shape)
    dim = (IMG_RESIZE, IMG_RESIZE)
    # resize image
    resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
    return resized

def saveImage(img, num):
    path = '/home/antonio/Desktop/Autofocus/allsnaps/preprocess/'
    name = "IMG_" + str(ID) + ".jpg"
    cv.imwrite(os.path.join(path , name), img)
    print("Save %s correctly" % str(path+name))


images = glob.glob("/home/antonio/Desktop/Autofocus/allsnaps/*.jpg")

for image in images:
    img = cv.imread(image, cv.IMREAD_GRAYSCALE)
    img = resizeImage(img)
    img = blurImage(img)
    saveImage(img, ID)
    print("Image %s done!" % image)
    ID += 1
