from shutil import copy
import random
import cv2
import os


source_dir = '/normal_binarized/train'
dest_dir = '/extracted_binarized_mixed'

max = 0
for folder_name in os.listdir(dest_dir):
    current_length = len(os.listdir(os.path.join(dest_dir, folder_name)))
    if current_length > max:
        max = current_length

for folder_name in os.listdir(dest_dir):
    print('Current_folder_name:', folder_name)
    current_path = os.path.join(dest_dir, folder_name)

    for file_name in os.listdir(current_path):
        if cv2.imread(os.path.join(current_path, file_name)) is None:
            print('Troubles with {} - {}.'.format(current_path, file_name))


    # current_length = len(os.listdir(current_path))
    #
    # source_filelist = os.listdir(os.path.join(source_dir, folder_name))
    # for i in range(max - current_length):
    #     s_path = os.path.join(source_dir, folder_name, source_filelist[i+500])
    #     d_path = os.path.join(current_path, source_filelist[i+500])
    #     copy(s_path, d_path)
    #     print('Copied:', s_path, d_path)
