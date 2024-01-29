import numpy as np
import cv2
import os

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

def replaceZeroes(data):
    min_nonzero = min(data[np.nonzero(data)])
    data[data == 0] = min_nonzero
    return data

def read_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            if img is not None:
                images.append(img)
    return images

#input_png_path = "./raw.png"
#output_png_path = "./result.png"

for filename in os.listdir("../UIEB_dataset/paper_image"):
    if filename.endswith(('.png', '.jpg')):
        img_path = os.path.join("../UIEB_dataset/paper_image", filename)
        output_png_path = os.path.join("../output_2.375", filename)
        print(img_path, output_png_path)
        img = cv2.imread(img_path)

    bgr_array = np.array(img)

    #Color_Correction
    height, width, channel = bgr_array.shape
    S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r = cal(bgr_array, 2.375) #coeff default value is 2.375 best = 3.2 ~ 4 //3.5 best
    color_correction(S_max_b, S_min_b, S_max_g, S_min_g, S_max_r, S_min_r, height, width, bgr_array)

    bgr_array = bgr_array.astype(np.uint8)

    #Gaussian_Blur
    hsv_img = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(hsv_img)

    Blur_v = cv2.GaussianBlur(v_channel,(3,3),0.85,0.85,borderType=cv2.BORDER_REFLECT)

    #Laplacian_Sharpening
    kernel = np.array([[-1, -1, -1],
                    [-1, 9, -1],
                    [-1, -1, -1]])

    Laplace_v = cv2.filter2D(Blur_v, -1, kernel, borderType = cv2.BORDER_REFLECT)

    #Retinex
    S = v_channel
    L = Blur_v
    L_sharpen = Laplace_v
    R = S / L
    result = R * L_sharpen

    result[result > 255] = 255
    result[result < 0] = 0
    result = result.astype(np.uint8)

    #Finish
    combined_hsv_image = cv2.merge([h_channel, s_channel, result])
    cv2.imwrite(output_png_path, cv2.cvtColor(combined_hsv_image, cv2.COLOR_HSV2BGR))
    print("Save")