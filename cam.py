import os
import time
import sys
import cv2
import picamera
from time import ctime, sleep
from datetime import datetime


MIN_F = 0
MAX_F = 10

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
    picam.brightness = 20
    picam.contrast = 30
    picam.vflip = True
    picam.hflip = True
    print("CONFIGURATION SET CORRECTLY")

def takePhoto(picam, i, sf):
    picam.start_preview()
    time.sleep(2)
    picam.capture("IMG_"+str(sf)+"_"+str(i)+".png",resize=(244,244))
    picam.stop_preview()
    print("PHOTO TAKEN")

if __name__ == "__main__":

    mf = 4
    sf = mf
    today = datetime.now()

    dir = os.getcwd()
    new_dir = dir + "_" + today.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')
    
    os.mkdir(new_dir)
    os.chdir(new_dir)

    with picamera.PiCamera() as picam:

        getConfCam(picam)
        setConfCam(picam)

        minFocus(mf)

        for i in range(MIN_F, MAX_F):
            sf += 100
            takePhoto(picam, i, sf)
            stepFocus(sf)

	picam.close()
