import os
import time
import sys
import cv2
import csv
from csv import writer
import picamera
import numpy as np
import cpbd
from time import ctime, sleep
from datetime import datetime


MIN_STEP = 0
MAX_STEP = 10
MIN_FOCUS = 0
IMG_SIZE = 128
BRIGHTNESS = 60

ls_LAPV = []
ls_TENG = []
ls_LAPM = []
ls_S3 = []
images_path = []

def S3(img):

    res = cpbd.compute(img)
    return res


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

def minFocus(mf):
    """
    Set camera focus to its minimum value.
    :param mf: value to set by i2c on the camera.
    :type mf: int
    """
    value = (mf<<4) & 0x3ff0
    dat1 = (value>>8)&0x3f
    dat2 = value & 0xf0
    os.system("i2cset -y 0 0x0c %d %d" % (dat1,dat2))

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

def getConfCam(picam):
    #print("Shutter speed: ", picam.shutter_speed)
    #print("Saturation: ", picam.saturation)
    #print("Sharpness: ", picam.sharpness)
    #print("Framerate: ", picam.framerate)
    #print("Resolution: ", picam.resolution)
    #print("Exposure mode: ", picam.exposure_mode)
    #print("Exposure compensation: ", picam.exposure_compensation)
    #print("Contrast: ", picam.contrast)
    #print("Brightness: ", picam.brightness)
    print("--Brightness: %s --Resolution: %s" % (picam.brightness, picam.resolution))

def setConfCam(picam):
    picam.resolution = (IMG_SIZE, IMG_SIZE)
    picam.color_effects = (128,128)
    picam.brightness = BRIGHTNESS
    picam.contrast = 30
    picam.vflip = True
    picam.hflip = True
    print("CONFIGURATION SET CORRECTLY")


def updateCSV(localMaxPos):
    csv_file = "album.csv"

    if os.path.exists(csv_file):
        with open(csv_file, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            for i in range(MIN_STEP, MAX_STEP):
                due = stepDue(localMaxPos, i)
                trend = tendency(i)
                r = ratio(i)
                step = i+1

                if i==MIN_STEP:
                    list_of_elem = [step, ls_LAPV[i], ls_TENG[i], ls_LAPM[i], ls_S3[i], ls_LAPV[i], ls_LAPV[i+1], (localMaxPos-i), r, trend, images_path[i], due]
                elif i==(MAX_STEP-1):
                    list_of_elem = [step, ls_LAPV[i], ls_TENG[i], ls_LAPM[i], ls_S3[i], ls_LAPV[i-1], ls_LAPV[i], (localMaxPos-i), r, trend, images_path[i], due]
                else:
                    list_of_elem = [step, ls_LAPV[i], ls_TENG[i], ls_LAPM[i], ls_S3[i], ls_LAPV[i-1], ls_LAPV[i+1], (localMaxPos-i), r, trend, images_path[i], due]

                csv_writer.writerow(list_of_elem)

    else:
        headers = ['STEP','LAPV','TENG', 'LAPM', 'S3', 'prevF', 'nextF', 'MV_STEP', 'ratio', 'trend','IMG_PATH', 'due']
        with open(csv_file, 'w', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(headers)
            for i in range(MIN_STEP, MAX_STEP):
                due = stepDue(localMaxPos, i)
                trend = tendency(i)
                r = ratio(i)
                step = i+1

                if i==MIN_STEP:
                    list_of_elem = [step, ls_LAPV[i], ls_TENG[i], ls_LAPM[i], ls_S3[i], ls_LAPV[i], ls_LAPV[i+1], (localMaxPos-i), r, trend, images_path[i], due]
                elif i==(MAX_STEP-1):
                    list_of_elem = [step, ls_LAPV[i], ls_TENG[i], ls_LAPM[i], ls_S3[i], ls_LAPV[i-1], ls_LAPV[i], (localMaxPos-i), r, trend, images_path[i], due]
                else:
                    list_of_elem = [step, ls_LAPV[i], ls_TENG[i], ls_LAPM[i], ls_S3[i], ls_LAPV[i-1], ls_LAPV[i+1], (localMaxPos-i), r, trend, images_path[i], due]

                csv_writer.writerow(list_of_elem)


def calcFocus(path):
    """
    Reads image captured and process the focus calculation
    with three different algorithms.
    :param path: absolute path of the last image taken by the camera.
    :type path: string.
    :returns: three focus measures values.
    """
    img = cv2.imread(path, 0)

    fmLPAV = LAPV(img)
    fmTENG = TENG(img)
    fmLAPM = LAPM(img)
    fmS3 = S3(img)
    
    fmLPAV = round(fmLPAV, 5)
    fmLAPM = round(fmLAPM, 5)
    fmTENG = round(fmTENG, 5)
    fmS3 = round(fmS3, 5)

    ls_LAPV.append(fmLPAV)
    ls_TENG.append(fmTENG)
    ls_LAPM.append(fmLAPM)
    ls_S3.append(fmS3)

    return fmLPAV, fmLAPM, fmTENG, fmS3


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

if __name__ == "__main__":

    sf = MIN_FOCUS

    wdir = os.getcwd()
    new_dir = "/album-V2"

    

    if len(sys.argv) == 2:
        BRIGHTNESS = int(sys.argv[1])

    if not os.path.exists(wdir+new_dir):
        os.mkdir(wdir+new_dir) 

    os.chdir(wdir+new_dir)  

    path = os.getcwd()

    with picamera.PiCamera() as picam:

        setConfCam(picam)
        getConfCam(picam)

        minFocus(MIN_FOCUS)

        for i in range(MIN_STEP, MAX_STEP):
            takePhoto(picam, i, sf, path)
            stepFocus(sf)
            sf += 1 

        indexMax = ls_LAPV.index(max(ls_LAPV))
        print("MAX: %d POSITION: %d" % (ls_LAPV[indexMax], indexMax+1))

        updateCSV(indexMax)

        picam.close()
