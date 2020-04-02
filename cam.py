import os
import time
import sys
import cv2
import csv
from csv import writer
import picamera
import numpy as np
from time import ctime, sleep
from datetime import datetime


MIN_STEP = 0
MAX_STEP = 10
MIN_FOCUS = 4

def minFocus(mf):
    value = (mf<<4) & 0x3ff0
    dat1 = (value>>8)&0x3f
    dat2 = value & 0xf0
    os.system("i2cset -y 0 0x0c %d %d" % (dat1,dat2))

def stepFocus(sf):
    value = (sf<<4) & 0x3ff0
    dat1 = (value>>8)&0x3f
    dat2 = value & 0xf0
    os.system("i2cset -y 0 0x0c %d %d" % (dat1,dat2))

def getConfCam(picam):
    print("Shutter speed: ", picam.shutter_speed)
    print("Saturation: ", picam.saturation)
    print("Sharpness: ", picam.sharpness)
    print("Framerate: ", picam.framerate)
    print("Resolution: ", picam.resolution)
    print("Exposure mode: ", picam.exposure_mode)
    print("Exposure compensation: ", picam.exposure_compensation)
    print("Contrast: ", picam.contrast)
    print("Brightness: ", picam.brightness)
    print("ISO: ", picam.ISO)
    print("Veritical flip: ", picam.vflip)
    print("Horizontal flip: ", picam.hflip)

def setConfCam(picam):
    picam.resolution = (244, 244)
    picam.color_effects = (128,128)
    picam.brightness = 50
    picam.contrast = 30
    picam.vflip = True
    picam.hflip = True
    print("CONFIGURATION SET CORRECTLY")

def insertRowCSV(step, fmeasure, path):
    list_of_elem = [step, fmeasure, path]
    csv_file = "album.csv"

    print("insertRow")
    with open(csv_file, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)



def calcFocus(path):
    print("measure focus LAPL")
    img = cv2.imread(path)
    fm = np.std(cv2.Laplacian(img, cv2.CV_64F)) ** 2
    return fm


def takePhoto(picam, i, sf, path):

    print("START PHOTO")
    picam.start_preview()
    time.sleep(1)

    now = datetime.now()
    timestamp = int(datetime.timestamp(now))

    name = "IMG_"+str(timestamp)+".png"
    picam.capture(name,resize=(244,244))

    fmeasure = calcFocus(name)
    path = path+"/"+name

    insertRowCSV(sf, fmeasure, path) # Insert row into csv 

    picam.stop_preview()
    print("PHOTO TAKEN")

if __name__ == "__main__":

    sf = MIN_FOCUS

    wdir = os.getcwd()
    new_dir = "/album"

    if not os.path.exists(wdir+new_dir):
        os.mkdir(wdir+new_dir) # create new folder to store all photos

    os.chdir(wdir+new_dir) # move inside the new folder 

    path = os.getcwd()

    with picamera.PiCamera() as picam:

        getConfCam(picam)
        setConfCam(picam)

        minFocus(MIN_FOCUS)

        for i in range(MIN_STEP, MAX_STEP):
            sf += 100
            takePhoto(picam, i, sf, path)
            stepFocus(sf)

    picam.close()
