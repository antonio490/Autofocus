
import os
import sys
import glob
import numpy as np
import cv2 as cv 

IMG_RESIZE = 32

def rectMask(img, kernel):
    roi = np.array([[[0, 0], [IMG_RESIZE, 0], [IMG_RESIZE, IMG_RESIZE/2], [0, IMG_RESIZE/2]]],dtype = np.int32)
    #roi = np.array([[[10, 6], [22, 6], [22, 32], [10, 32]]],dtype = np.int32)
    blurred_image = cv.GaussianBlur(img,(kernel, kernel), 0)

    # create a mask for the ROI
    mask = np.zeros(img.shape, dtype=np.uint8)
    channel_count = 1
    ignore_mask_color = (255,)*channel_count
    cv.fillPoly(mask, roi, ignore_mask_color)

    mask_inverse = np.ones(mask.shape).astype(np.uint8)*255 - mask
    image = cv.bitwise_and(blurred_image, mask) + cv.bitwise_and(img, mask_inverse)

    return image    

def triangleMask(img, kernel):
    #triangle = np.array([[[32, 0], [0, 32], [32, 32]]], np.int32)
    roi = np.array([[[32, 0], [0, 32], [32, 32]]],dtype = np.int32)
    blurred_image = cv.GaussianBlur(img,(kernel, kernel), 0)

    # create a mask for the ROI
    mask = np.zeros(img.shape, dtype=np.uint8)
    channel_count = 1
    ignore_mask_color = (255,)*channel_count
    cv.fillPoly(mask, roi, ignore_mask_color)

    mask_inverse = np.ones(mask.shape).astype(np.uint8)*255 - mask
    image = cv.bitwise_and(blurred_image, mask) + cv.bitwise_and(img, mask_inverse)

    return image


def blurImage(img, kernel):
    # apply guassian blur on src image
    dst = cv.GaussianBlur(src=img, ksize=(kernel, kernel), sigmaX=0, borderType= cv.BORDER_DEFAULT)
    return dst

def resizeImage(img):
    print('Original Dimensions : ',img.shape)
    dim = (IMG_RESIZE, IMG_RESIZE)
    # resize image
    resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
    return resized

def saveImage(img, num, mask, kernel):
    #path = '/home/antonio/Downloads/cifar-10/IMG50K/blur31/'
    path = '/home/antonio/Desktop/photos/'

    name = "IMG_" + str(mask) + "_" + str(kernel) + "_" + str(num) + ".png"
    cv.imwrite(os.path.join(path , name), img)
    print("Save %s correctly" % str(path+name))




def main(argv):

    ID = 0
    #images = glob.glob("/home/antonio/Downloads/cifar-10/IMG50K/focus/*.png")
    images = glob.glob("/home/antonio/Desktop/photos/IMG_1591711509.png")


    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))

    if len(sys.argv) < 3:
        print("Error call")
        exit(1)

    kernel = int(sys.argv[1])

    mask = int (sys.argv[2])

    for image in images:
        img = cv.imread(image, cv.IMREAD_GRAYSCALE)
        #img = resizeImage(img)

        if mask == 0:
            print("Blur image with kernel = ", kernel)
            img = blurImage(img, kernel)
        elif mask == 1:
            print("Triangle mask with kernel = ", kernel)
            img = triangleMask(img, kernel) # triangle mask
        elif mask == 2:
            print("Rectangle mask with kernel = ", kernel)
            img = rectMask(img, kernel) # rectangle centered mask
        elif mask == 3:
            print("Rectangle mask with kernel = ", kernel)
            img = rectMask(img, kernel) # top half rectangle mask
        else:
            print("Do nothing")

        saveImage(img, ID, mask, kernel)
        print("Image %s done!" % image)
        ID += 1


if __name__ == "__main__":
   main(sys.argv[1:])