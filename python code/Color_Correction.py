import numpy as np
import cv2

def cal(bgr_array,coeff):
    bgr_float = bgr_array.astype(float)

    mean_b = np.mean(bgr_float[:,:,0])
    mean_g = np.mean(bgr_float[:,:,1])
    mean_r = np.mean(bgr_float[:,:,2])
    
    std_b = np.std(bgr_float[:,:,0])
    std_g = np.std(bgr_float[:,:,1])
    std_r = np.std(bgr_float[:,:,2])
    
    S_max_b = mean_b + coeff * std_b
    S_min_b = mean_b - coeff * std_b
    S_max_g = mean_g + coeff * std_g
    S_min_g = mean_g - coeff * std_g
    S_max_r = mean_r + coeff * std_r
    S_min_r = mean_r - coeff * std_r
    
    S_max_b = np.clip(S_max_b, 0, 255)
    S_min_b = np.clip(S_min_b, 0, 255)
    S_max_g = np.clip(S_max_g, 0, 255)
    S_min_g = np.clip(S_min_g, 0, 255)
    S_max_r = np.clip(S_max_r, 0, 255)
    S_min_r = np.clip(S_min_r, 0, 255)

    print(S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r, std_b, std_g, std_r)

    return S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r

def new_color(S_max, S_min, S):
    new_pixel = ((S - S_min)/(S_max - S_min)) * 255
    new_pixel = int(np.clip(new_pixel, 0, 255))
    return new_pixel

def color_correction(S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r, height, width, bgr_array):
    for i in range(height):
        for j in range(width):
            bgr_array[i][j][0] = new_color(S_max_b, S_min_b, bgr_array[i][j][0]) #0 255
            bgr_array[i][j][1] = new_color(S_max_g, S_min_g, bgr_array[i][j][1]) #0 255
            bgr_array[i][j][2] = new_color(S_max_r, S_min_r, bgr_array[i][j][2]) #0 255
    return

input_png_path = "./UIEB_dataset/paper_image/515_img_.png"
output_png_path = "./Color_Correction.png"

img = cv2.imread(input_png_path)
bgr_array = np.array(img)

height, width, channel = bgr_array.shape
S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r = cal(bgr_array, 2.375) #coeff default value is 2.375 best = 3.2 ~ 4 //3.5 best
color_correction(S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r, height, width, bgr_array)

bgr_array = bgr_array.astype(np.uint8)

cv2.imwrite('./Color_Correction.png', bgr_array)
print(f"Save as {output_png_path} {width,height,channel}")