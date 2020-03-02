import json
import cv2
import os

json_path_ru = 'project/json_sources/combined_set_ru_sm.json'
json_path_en = 'project/json_sources/combined_set_en.json'

mpic_path = 'datasets/MSCOCO_img_dataset_2017/train2017/'
gpic_path = 'datasets/google_dataset/source_images'

with open(json_path_ru, 'r') as r_json:
    json_data_ru = json.load(r_json)

with open(json_path_en, 'r') as r_json:
    json_data_en = json.load(r_json)

num = 1

print('Pic_len:', len(json_data_ru['images']))
print('Ann_len:', len(json_data_ru['annotations']))

while num > -1:
    num = int(input('Num?: '))

    annotation = json_data_ru['annotations'][num]
    print(annotation['caption'])
    print(json_data_en['annotations'][num]['caption'])

    image_id = annotation['image_id']

    for element in json_data_ru['images']:
        if element['id'] == image_id:
            break
    else:
        print('Does not exists')
        continue

    file_name = element['file_name']
    pic_path = gpic_path if element['file_name'][:6] == 'google' else mpic_path

    cv2.imshow('current_image', cv2.imread(os.path.join(pic_path, file_name)))
    cv2.waitKey(0)

# json_path = 'datasets/google_dataset/g_captions.json'
# pic_path = 'datasets/google_dataset/source_images'

# while num > -1:
#     num = int(input('Num?: '))
#
#     annotation = json_data['result_list']
#
#     for element in annotation:
#         if element['count'] == num:
#             break
#     else:
#         print('Does not exists')
#         continue
#
#     print(element['caption'])
#     cv2.imshow('current_image', cv2.imread(os.path.join(pic_path, element['filename'])))
#     cv2.waitKey(0)
