
import os
import sys
import glob
import numpy as np
import cv2 as cv 

IMG_RESIZE = 32

def rectMask(img, kernel):
    roi = np.array([[[0, 0], [32, 0], [32, 16], [0, 16]]],dtype = np.int32)

    roi = np.array([[[10, 6], [22, 6], [22, 32], [10, 32]]],dtype = np.int32)

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

'''
def blurMask():
    #Python: cv2.bitwise_and(src1, src2[, dst[, mask]]) → dst

    blurred = cv.GaussianBlur(original, (kernel,kernel), 0)

    #create MASK
    original[0:500, 0:500] = blurred[0:500, 0:500]
    #cv2.imwrite('cvBlurredOutput.jpg', original)
'''

def blurImage(img, kernel, dev):
    # apply guassian blur on src image
    dst = cv.GaussianBlur(src=img, ksize=(kernel, kernel), sigmaX=dev, sigmaY=2, borderType= cv.BORDER_DEFAULT)
    return dst

def resizeImage(img):
    print('Original Dimensions : ',img.shape)
    dim = (IMG_RESIZE, IMG_RESIZE)
    # resize image
    resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
    return resized

def saveImage(img, num):
    path = '/home/antonio/Downloads/cifar-10/IMG50K/maskBlur3/'
    name = "IMG_" + str(num) + ".png"
    cv.imwrite(os.path.join(path , name), img)
    print("Save %s correctly" % str(path+name))


images = glob.glob("/home/antonio/Downloads/cifar-10/IMG50K/gray/*.png")



#img = cv.imread("/home/antonio/Downloads/cifar-10/IMG50K/gray/IMG_0.png",cv.IMREAD_GRAYSCALE)


#imgFiltered = mask(img, 0, 0, 32, 16, kernel) # upper rectangle

#imgFiltered = triangleMask(img, kernel)

# mask(img, 10, 6, 22, 0, kernel) # rectangle centered

#cv.imshow("blur result", imgFiltered)
#cv.waitKey(0)
#cv.destroyAllWindows()

def main(argv):

    ID = 0
    images = glob.glob("/home/antonio/Downloads/cifar-10/IMG50K/gray/*.png")

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
            img = blurImage(img, kernel, kernel)
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

        saveImage(img, ID)
        print("Image %s done!" % image)
        ID += 1


if __name__ == "__main__":
   main(sys.argv[1:])