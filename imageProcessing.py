
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kurtosis


plt.figure(figsize=(12,12), constrained_layout=False)



img_f = cv.imread("/home/antonio/Desktop/Autofocus/album-V2/IMG_1593334899.png", 0) # Focus image
img_b = cv.imread("/home/antonio/Desktop/Autofocus/album-V2/IMG_1593334921.png", 0) # Blur image

img2_f = cv.imread("/home/antonio/Desktop/Autofocus/album-V2/IMG_1593336724.png", 0) # Focus image
img2_b = cv.imread("/home/antonio/Desktop/Autofocus/album-V2/IMG_1593336745.png", 0) # Blur image


# Imagen 1 blur
f = np.fft.fft2(img_b)
fshift = np.fft.fftshift(f)
spectrum_b = 20*np.log(np.abs(fshift))

# Imagen 1 focus
f = np.fft.fft2(img_f)
fshift = np.fft.fftshift(f)
spectrum_f = 20*np.log(np.abs(fshift))

# Imagen 2 blur
f = np.fft.fft2(img2_b)
fshift = np.fft.fftshift(f)
spectrum_b2 = 20*np.log(np.abs(fshift))

# Imagen 2 focus
f = np.fft.fft2(img2_f)
fshift = np.fft.fftshift(f)
spectrum_f2 = 20*np.log(np.abs(fshift))

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

plt.subplot(241), plt.imshow(img_b, "gray"), plt.title("natural blur image"), plt.xticks([]), plt.yticks([])
#plt.subplot(242), plt.imshow(np.log(1 + np.abs(img_b2))), plt.title("natural blur spectrum")
plt.subplot(242), plt.imshow(spectrum_b, cmap="gray"), plt.title("natural blur spectrum"), plt.xticks([]), plt.yticks([])



plt.subplot(243), plt.imshow(img_f, "gray"), plt.title("focus image"), plt.xticks([]), plt.yticks([])
#plt.subplot(244), plt.imshow(np.log(1 + np.abs(img_f2))), plt.title("focus spectrum")
plt.subplot(244), plt.imshow(spectrum_f, cmap="gray"), plt.title("focus spectrum"), plt.xticks([]), plt.yticks([])

# Segunda fila

plt.subplot(245), plt.imshow(img2_b, "gray"), plt.title("natural blur image"), plt.xticks([]), plt.yticks([])
plt.subplot(246), plt.imshow(spectrum_b2, cmap="gray"), plt.title("natural blur spectrum"), plt.xticks([]), plt.yticks([])

plt.subplot(247), plt.imshow(img2_f, "gray"), plt.title("focus image"), plt.xticks([]), plt.yticks([])
plt.subplot(248), plt.imshow(spectrum_f2, cmap="gray"), plt.title("focus spectrum"), plt.xticks([]), plt.yticks([])

#plt.subplot(245), plt.imshow(img2_b, "gray"), plt.title("Gaussian blur image")
#plt.subplot(246), plt.imshow(np.log(1 + np.abs(img2_b2))), plt.title("Gaussian blur spectrum")

#plt.subplot(247), plt.imshow(img2_f, "gray"), plt.title("focus image")
#plt.subplot(248), plt.imshow(np.log(1 + np.abs(img2_f2))), plt.title("focus spectrum")

plt.show()