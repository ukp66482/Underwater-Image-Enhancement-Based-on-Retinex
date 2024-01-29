%%%%%%%%This is a demo for the usage of PCQI with default settings%%%%%%%%%%%%%%%%%%
clc;
clear;


input_folder = './raw-890';
ref_folder = './reference-890';
filepaths = dir(fullfile(input_folder,'*.png'));

ave_pcqi = 0;
for num = 1 : length(filepaths)

    im1=imread(fullfile(input_folder,filepaths(num).name));
    im2=imread(fullfile(ref_folder,filepaths(num).name));

    im1=double(rgb2gray(im1));
    im2=double(rgb2gray(im2));

    [mpcqi,pcqi_map]=PCQI(im1,im2);
    ave_pcqi = ave_pcqi + mpcqi;
end
ave_pcqi = ave_pcqi / 890.0



