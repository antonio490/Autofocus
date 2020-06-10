
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


plt.figure(figsize=(12,12), constrained_layout=False)

img_b = cv.imread("/home/antonio/Desktop/photos/IMG_1591718605.png", 0) # Blur image
img_f = cv.imread("/home/antonio/Desktop/photos/IMG_1591718593.png", 0) # Focus image

img2_b = cv.imread("/home/antonio/Desktop/IMG_0_9_1.png", 0) # Blur image
img2_f = cv.imread("/home/antonio/Desktop/IMG_3_9_0.png", 0) # Focus image


# Imagen 1
img_b2 = np.fft.fft2(img_b)
img_f2 = np.fft.fft2(img_f)

img_b3 = np.fft.fftshift(img_b2)
img_f3 = np.fft.fftshift(img_f2)

# Imagen 2
img2_b2 = np.fft.fft2(img2_b)
img2_f2 = np.fft.fft2(img2_f)

img2_b3 = np.fft.fftshift(img2_b2)
img2_f3 = np.fft.fftshift(img2_f2)

# Primera fila

plt.subplot(241), plt.imshow(img_b, "gray"), plt.title("natural blur image")
plt.subplot(242), plt.imshow(np.log(1 + np.abs(img_b2))), plt.title("natural blur spectrum")

plt.subplot(243), plt.imshow(img_f, "gray"), plt.title("focus image")
plt.subplot(244), plt.imshow(np.log(1 + np.abs(img_f2))), plt.title("focus spectrum")

# Segunda fila

plt.subplot(245), plt.imshow(img2_b, "gray"), plt.title("Gaussian blur image")
plt.subplot(246), plt.imshow(np.log(1 + np.abs(img2_b2))), plt.title("Gaussian blur spectrum")

plt.subplot(247), plt.imshow(img2_f, "gray"), plt.title("focus image")
plt.subplot(248), plt.imshow(np.log(1 + np.abs(img2_f2))), plt.title("focus spectrum")

plt.show()