import cv2
import numpy as np

img = cv2.imread("./Gaussian_Blur.png")

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h_channel = hsv_img[:, :, 0]
s_channel = hsv_img[:, :, 1]
v_channel = hsv_img[:, :, 2]

kernel = np.array([[-1, -1, -1],
                  [-1, 9, -1],
                  [-1, -1, -1]])

Laplace_v = cv2.filter2D(v_channel, -1, kernel, borderType = cv2.BORDER_REFLECT)

combined_hsv_image = cv2.merge([h_channel, s_channel, Laplace_v])

cv2.imwrite("./Laplacian_Sharpening.png", cv2.cvtColor(combined_hsv_image, cv2.COLOR_HSV2BGR))