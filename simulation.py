import os
import time
import sys
import cv2
import csv
import random
import pickle
from csv import writer
import picamera
import numpy as np
import pandas as pd
from time import ctime, sleep
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split 
from sklearn import metrics

MIN_STEP = 0
MAX_STEP = 10
MIN_FOCUS = 0
IMG_SIZE = 244

ls_LAPV = []
ls_TENG = []
ls_LAPM = []
images_path = []

def TENG(img):
    """Implements the Tenengrad (TENG) focus measure operator.
    Based on the gradient of the image.
    :param img: the image the measure is applied to
    :type img: numpy.ndarray
    :returns: numpy.float32 -- the degree of focus
    """
    gaussianX = cv2.Sobel(img, cv2.CV_64F, 1, 0)
    gaussianY = cv2.Sobel(img, cv2.CV_64F, 0, 1)
    return np.mean(gaussianX * gaussianX +
                      gaussianY * gaussianY)

def LAPM(img):
    """Implements the Modified Laplacian (LAP2) focus measure
    operator. Measures the amount of edges present in the image.
    :param img: the image the measure is applied to
    :type img: numpy.ndarray
    :returns: numpy.float32 -- the degree of focus
    """
    kernel = np.array([-1, 2, -1])
    laplacianX = np.abs(cv2.filter2D(img, -1, kernel))
    laplacianY = np.abs(cv2.filter2D(img, -1, kernel.T))
    return np.mean(laplacianX + laplacianY)

def LAPV(img):
    """Implements the Variance of Laplacian (LAP4) focus measure
    operator. Measures the amount of edges present in the image.
    :param img: the image the measure is applied to
    :type img: numpy.ndarray
    :returns: numpy.float32 -- the degree of focus
    """
    return np.std(cv2.Laplacian(img, cv2.CV_64F)) ** 2


def stepDue(localMax, i):
    if abs(localMax - i) < 3:
        due = 'small'
    else:
        due = 'big'
    
    return due

def tendency(i):
    if ls_LAPV[i] <= ls_LAPV[i-1]:
        trend = 'down'
    else:
        trend = 'up'

    return trend

def ratio(i):
    if i==0:
        ratio = 0 
    else:
        ratio = ls_LAPV[i] / ls_LAPV[i-1]

    return ratio

def randomFocus(picam):
    """
    Set focus value randomly at the arducam by i2c.
    :param sf: value to set set by i2c on the camera.
    :type sf: int
    """
    sfr = random.randint(0, 10)
    sf = int(sfr*1000 / MAX_STEP)
    print("FOCUS: %d" % sfr)

    value = (sf<<4) & 0x3ff0
    dat1 = (value>>8)&0x3f
    dat2 = value & 0xf0
    os.system("i2cset -y 0 0x0c %d %d" % (dat1,dat2)) 

    return sfr

def stepFocus(sf):
    """
    Increase focus value at the arducam by i2c.
    :param sf: value to set set by i2c on the camera.
    :type sf: int
    """
    sf = int(sf*1000 / MAX_STEP)

    value = (sf<<4) & 0x3ff0
    dat1 = (value>>8)&0x3f
    dat2 = value & 0xf0
    os.system("i2cset -y 0 0x0c %d %d" % (dat1,dat2))   

def calcFocus(path):
    """
    Reads image captured and process the focus calculation
    with three different algorithms.
    :param path: absolute path of the last image taken by the camera.
    :type path: string.
    :returns: three focus measures values.
    """
    img = cv2.imread(path)

    fmLPAV = LAPV(img)
    fmTENG = TENG(img)
    fmLAPM = LAPM(img)
    
    fmLPAV = round(fmLPAV, 5)
    fmLAPM = round(fmLAPM, 5)
    fmTENG = round(fmTENG, 5)


    ls_LAPV.append(fmLPAV)
    ls_TENG.append(fmTENG)
    ls_LAPM.append(fmLAPM)

def takePhoto(picam, i, step, path):

    picam.start_preview()
    time.sleep(1)

    now = datetime.now()
    timestamp = int(datetime.timestamp(now))

    name = "IMG_"+str(timestamp)+".png"
    picam.capture(name,resize=(IMG_SIZE,IMG_SIZE))

    calcFocus(name)
    path = path+"/"+name
    images_path.append(path)

    picam.stop_preview()
    print("PHOTO %d DONE" % i)


def createCSV():
    
    csv_file = "simulation.csv"

    headers = ['STEP','LAPV','TENG', 'LAPM', 'prevF', 'nextF', 'ratio', 'trend','IMG_PATH']
    with open(csv_file, 'w', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(headers)
        for i in range(0, 3):
            trend = tendency(i)
            r = ratio(i)
            step = i+1

            if i==0:
                list_of_elem = [step, ls_LAPV[i], ls_TENG[i], ls_LAPM[i], ls_LAPV[i], ls_LAPV[i+1], r, trend, images_path[i]]
            elif i==2:
                list_of_elem = [step, ls_LAPV[i], ls_TENG[i], ls_LAPM[i], ls_LAPV[i-1], ls_LAPV[i], r, trend, images_path[i]]
            else:
                list_of_elem = [step, ls_LAPV[i], ls_TENG[i], ls_LAPM[i], ls_LAPV[i-1], ls_LAPV[i+1], r, trend, images_path[i]]

            csv_writer.writerow(list_of_elem)

if __name__ == "__main__":


    wdir = os.getcwd()
    new_dir = "/simulation"
    filename = "modelo.sav"

    os.chdir(wdir+new_dir) 
    path = os.getcwd()

    with picamera.PiCamera() as picam:


        sf = randomFocus(picam)
        rf = sf # Save randomFocus
        print("RANDOM FOCUS: %d" % rf)

        # take 3 pictures
        for i in range(0, 3):
            takePhoto(picam, i, sf, path)
            stepFocus(sf)
            sf += 1

        createCSV()

        # load the model from disk
        loaded_model = pickle.load(open(filename, 'rb'))


        col_names = ['STEP','LAPV','TENG','LAPM','prevF','nextF', 'ratio','trend','IMG_PATH']
        album = pd.read_csv('simulation.csv', header=0, names=col_names)

        album['trend'].replace({'down':0, 'up':1}, inplace=True)
        # features 
        feature_cols = ['LAPV','TENG','LAPM','prevF','nextF','ratio', 'trend']

        X_test = album[feature_cols]

        # target
        #Y_test = album.due

        result = loaded_model.predict(X_test)
        print(result)

        picam.close()
