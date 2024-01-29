clc;
clear;


input_folder = './raw-890';
filepaths = dir(fullfile(input_folder,'*.png'));

ave_entropy = 0;
for num = 1 : length(filepaths)
    disp(filepaths(num).name)
    im=imread(fullfile(input_folder,filepaths(num).name));
    grayim = rgb2gray(im);
    ave_entropy = ave_entropy + entropy(grayim);
end
ave_entropy = ave_entropy / 890.0