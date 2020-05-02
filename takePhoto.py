import picamera
import os
import sys
import time
from datetime import datetime
from time import ctime, sleep



MIN_STEP = 0
MAX_STEP = 10
MIN_FOCUS = 0
IMG_SIZE = 244
BRIGHTNESS = 60

def stepFocus(sf):
    """
    Increase focus value at the arducam by i2c.
    :param sf: value to set set by i2c on the camera.
    :type sf: int
    """
    sf = int(sf*1000 / MAX_STEP)
    print("FOCUS POSITION: %d" % sf)

    value = (sf<<4) & 0x3ff0
    dat1 = (value>>8)&0x3f
    dat2 = value & 0xf0
    os.system("i2cset -y 0 0x0c %d %d" % (dat1,dat2))

def takePhoto(picam):

    picam.start_preview()
    time.sleep(1)

    now = datetime.now()
    timestamp = int(datetime.timestamp(now))

    name = "IMG_"+str(timestamp)+".png"
    picam.capture(name,resize=(IMG_SIZE,IMG_SIZE))

    #calcFocus(name)
    #path = path+"/"+name
    #images_path.append(path)

    picam.stop_preview()
    print("PHOTO DONE")

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
    picam.brightness = BRIGHTNESS
    picam.contrast = 30
    picam.vflip = True
    picam.hflip = True
    print("CONFIGURATION SET CORRECTLY")


def main(argv):

    num = len(sys.argv) - 1

    print("Number of arguments: %d" % num)

    if(num != 3):
        print("Usage: python3 takePhoto -focus (int) -due (boolean) -direction (boolean)")
        exit(1)

    rf = int(sys.argv[1])
    due = int(sys.argv[2])
    direction = int(sys.argv[3])


    with picamera.PiCamera() as picam:

        #getConfCam(picam)
        setConfCam(picam)
	    #print("RANDOM FOCUS: %d", rf)

        if due == 0 and direction == 0:
            # small step backward
            rf -= 1
            print("small step backward: %d" % rf)
        elif due == 0 and direction == 1:
            # small step forward
            rf += 1
            print("small step forward: %d" % rf)
        elif due == 1 and direction == 0:
            # big step backward
            rf -= 3
            print("big step backward: %d" % rf)
        elif due == 1 and direction == 1:
            # big step forward
            rf += 3
            print("big step fordward: %d" % rf)
        else:
            print("Do nothing")

        stepFocus(rf) # Position focus at random position tested

        takePhoto(picam)

        picam.close()


if __name__ == "__main__":
   main(sys.argv[1:])
