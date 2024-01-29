import cv2
import numpy as np

img = cv2.imread("./Color_Correction.png")

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h_channel = hsv_img[:, :, 0]
s_channel = hsv_img[:, :, 1]
v_channel = hsv_img[:, :, 2]

Blur_v = cv2.GaussianBlur(v_channel,(3,3),0.85,0.85,borderType=cv2.BORDER_REFLECT)
combined_hsv_image = cv2.merge([h_channel, s_channel, Blur_v])

cv2.imwrite("./Gaussian_Blur.png", cv2.cvtColor(combined_hsv_image, cv2.COLOR_HSV2BGR))
