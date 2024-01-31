clc;
clear all;
close all;



input_folder = '../output_2.375';
filepaths = dir(fullfile(input_folder,'*.png'));

ave_uiqm = 0;
ave_uciqe = 0;
for num = 1 : length(filepaths)
    disp(filepaths(num).name)
    image= imread(fullfile(input_folder,filepaths(num).name));
    ave_uiqm = ave_uiqm + UIQM(image);
    ave_uciqe =  ave_uciqe + UCIQE(image);
    
end
%ave_uiqm = ave_uiqm / 890.0;
%ave_uciqe = ave_uciqe / 890.0;
