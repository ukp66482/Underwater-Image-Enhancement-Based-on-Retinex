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
    print(S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r, std_b, std_g, std_r)

    return S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r

def new_color(S_max, S_min, S):
    if(S_min <= S <= S_max):
        x = S_max - S_min
        if 0 <= x <= 61:
            a = 4.75
        elif 61 <= x <= 73:
            a = 3.8125
        elif 74 <= x <= 86:
            a = 3.1875
        elif 87 <= x <= 99:
            a = 2.75
        elif 100 <= x <= 112:
            a = 2.375
        elif 113 <= x <= 125:
            a = 2.125
        elif 126 <= x <= 138:
            a = 1.9375
        elif 139 <= x <= 151:
            a = 1.75
        elif 152 <= x <= 164:
            a = 1.625
        elif 165 <= x <= 177:
            a = 1.5
        elif 178 <= x <= 190:
            a = 1.375
        elif 191 <= x <= 203:
            a = 1.3125
        elif 204 <= x <= 216:
            a = 1.1875
        elif 217 <= x <= 229:
            a = 1.125
        elif 230 <= x <= 242:
            a = 1.0625
        else:
            a = 1.0                                                           
        new_pixel = (S - S_min) * a
    elif(S > S_max):
        new_pixel = (S - S_min) * 1
    else:
        new_pixel = (S - S_min) * 4.75        
#    elif(S > S_max):
#        if(S_max >= 255):
#            new_pixel = 255
#        else:
#            new_pixel = S_max
#    else:
#        if(S_max <= 0):
#            new_pixel = 0
#        else:
#            new_pixel = S_min

    return new_pixel

def color_correction(S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r, height, width, bgr_array):
    for i in range(height):
        for j in range(width):
            bgr_array[i][j][0] = new_color(S_max_b, S_min_b, bgr_array[i][j][0]) #0 255
            bgr_array[i][j][1] = new_color(S_max_g, S_min_g, bgr_array[i][j][1]) #0 255
            bgr_array[i][j][2] = new_color(S_max_r, S_min_r, bgr_array[i][j][2]) #0 255
    return

input_png_path = "./15003.png"
output_png_path = "./Color_Correction.png"

img = cv2.imread(input_png_path)
bgr_array = np.array(img)

height, width, channel = bgr_array.shape
S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r = cal(bgr_array, 3.5) #coeff default value is 2.375 best = 3.2 ~ 4 //3.5 best
color_correction(S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r, height, width, bgr_array)

bgr_array = bgr_array.astype(np.uint8)

cv2.imwrite('./Color_Correction.png', bgr_array)
print(f"Save as {output_png_path} {width,height,channel}")