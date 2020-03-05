import os
import cv2
import numpy as np

source_dir = os.path.abspath('../_extracted/')
dest_dir = os.path.abspath('../_extracted_binarized/')

classes = os.listdir(source_dir)

file_amount = 0
for class_folder in classes:
    amount= len(os.listdir(os.path.join(source_dir, class_folder)))
    print(class_folder, amount)
    file_amount += amount

count = 0

for class_folder in classes:

    dest_class_path = os.path.join(dest_dir, class_folder)
    source_class_path = os.path.join(source_dir, class_folder)

    if os.path.exists(dest_class_path) != True:
        os.makedirs(dest_class_path)

    for filename in os.listdir(source_class_path):
        print('Image {} of {}'.format(count, file_amount))
        count += 1
        image_np = cv2.imread(os.path.join(source_class_path, filename))

        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        image_np = cv2.adaptiveThreshold(
                            src=image_np,
                            maxValue=255,
                            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            thresholdType=cv2.THRESH_BINARY,
                            blockSize=103,
                            C=3)


        cv2.imwrite(os.path.join(dest_class_path, filename), image_np)
