import cv2
import numpy as np

def replaceZeroes(data):
    min_nonzero = min(data[np.nonzero(data)])
    data[data == 0] = min_nonzero
    return data

Src_img = cv2.imread("./Color_Correction.png")
Blur_img = cv2.imread("./Gaussian_Blur.png")
Sharpen_img = cv2.imread("./Laplacian_Sharpening.png")

Src_hsv_img = cv2.cvtColor(Src_img,cv2.COLOR_BGR2HSV)
Blur_hsv_img = cv2.cvtColor(Blur_img, cv2.COLOR_BGR2HSV)
Sharpen_hsv_img = cv2.cvtColor(Sharpen_img, cv2.COLOR_BGR2HSV)


h_channel = Src_hsv_img[:, :, 0]
s_channel = Src_hsv_img[:, :, 1]

S = Src_hsv_img[:, :, 2]
L = Blur_hsv_img[:, :, 2]

L_sharpen = Sharpen_hsv_img[:, :, 2]
R = S / L
result = R * L_sharpen

result[result > 255] = 255
result[result < 0] = 0
result = result.astype(np.uint8)

combined_hsv_image = cv2.merge([h_channel, s_channel, result])
cv2.imwrite("./Retinex.png", cv2.cvtColor(combined_hsv_image, cv2.COLOR_HSV2BGR))
