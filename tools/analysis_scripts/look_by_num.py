"""
This module provides the ability to verify the correct mapping of annotations
    and pictures.
It was created in case if during the process of manipulating files, the
    position of the annotations in the "Signature" field has changed and does
    not match the indicated picture.

"""
import os
import sys
import json
import argparse

import cv2
import numpy

def _a_parse():
    """
    This function is a simple argument parser. Checks if paths in arguments are
        right & checks if directories exist.

    Return:
    < dict > -- {
                    'mscoco_file': < string >,
                    'image_dir_list': < list > of < string >,
                    'ru_mscoco_file': < string >
                }

    """
    a_parser = argparse.ArgumentParser()
    a_parser.add_argument(
                '--mscoco_file',
                metavar='/path/to/mscoco.json',
                required=True,
                help='path to source mscoco json file')

    a_parser.add_argument(
                '--image_dir_list',
                metavar='/path/to/img_dir_1 /path/to/img_dir_2',
                nargs='+',
                required=True,
                help='list of paths to image directories')

    a_parser.add_argument(
                '--ru_mscoco_file',
                metavar='/path/to/ru_mscoco.json',
                required=False,
                help='path to source ru_mscoco json file')

    args = vars(a_parser.parse_args())
    mscoco_file = os.path.abspath(args.get('mscoco_file'))
    image_dir_list = args.get('image_dir_list')
    ru_mscoco_file = args.get('ru_mscoco_file')

    if args.get('ru_mscoco_file') is not None:
        ru_mscoco_file = os.path.abspath(ru_mscoco_file)
        if os.path.exists(ru_mscoco_file) != True:
            print('\n[ERROR]: ru_mscoco_file does not exists.')
            sys.exit(1)

        if os.path.isfile(ru_mscoco_file) != True:
            print('\n[ERROR]: ru_mscoco_file is not a file.')
            sys.exit(1)

    if os.path.exists(mscoco_file) != True:
        print('\n[ERROR]: mscoco_file does not exists.')
        sys.exit(1)

    if os.path.isfile(mscoco_file) != True:
        print('\n[ERROR]: mscoco_file is not a file.')
        sys.exit(1)

    for image_dir in image_dir_list:
        if os.path.exists(image_dir) != True:
            print('\n[ERROR]: < {} > does not exists.'.format(image_dir))
            sys.exit(1)

        if os.path.isdir(image_dir) != True:
            print('\n[ERROR]: < {} > is not a directory.'.format(image_dir))
            sys.exit(1)

    args = {'mscoco_file': mscoco_file,
            'image_dir_list': image_dir_list,
            'ru_mscoco_file': ru_mscoco_file}

    return args

def read_json(json_path):
    """
    This method reads MSCOCO .json files that must have following fields:
            {
                "annotations":[
                    {
                        "caption": < string >
                    }
                ]
            }

        It returns list of annotations.

    Keyword arguments:
    json_file_path -- < string > path to json file.

    Return:
    < list > of < string > -- list with annotations.

    """

    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)

    return json_data

def find_picture(image_dir_list, filename):
    """
    This method searches filename in every image directory from list. If it
        finds 1 or more it reads them and returns list of dicts with name and
        numpy array (image).

    Keyword arguments:
    image_dir_list -- < list > of < dict >
    filename -- < string > filename of image to find.

    Return:
    < list > of < dict > -- images that has been found.
        [
            {
                'path': < string >,
                'image': < numpy.ndarray >
            }, ...
        ]

    """
    result_list = []

    for image_dir in image_dir_list:
        path = os.path.join(image_dir, filename)
        if os.path.exists(path):
            if os.path.isfile(path):
                result_list.append({'path':path, 'image': cv2.imread(path)})

    return result_list

def find_caption_element(mscoco_data, caption_id):
    """
    This method finds element with specified id of caption. Returns dict with
        pair of keys extracted from "images" & "annotations".

    Keyword argumnets:
    mscoco_data -- < dict > with following fields:
        {
            "images": [
                    {
                        "licence": < int >,
                        "file_name": < filename.jpg >,
                        "coco_url": "http://mscoco.org/images/391895",
                        "height": 360,
                        "width": 640,
                        "date_captured": "2017-11-14 11:18:45",
                        "flick_url": < url >,
                        "id": 391895
                    }, { ... }, ...
                ]
            "annotations": [
                    {
                        "image_id": 391895,
                        "id": 37,
                        "caption": "A bicycle replica with a clock."
                    }, { ... }, ...
                ]
            }
        }
    id -- < int > id of searching caption.

    Return:
    < dict > -- "images" and "annotations" fields elements
        {
            "image": [
                    {
                        "licence": < int >,
                        "file_name": < filename.jpg >,
                        "coco_url": "http://mscoco.org/images/391895",
                        "height": 360,
                        "width": 640,
                        "date_captured": "2017-11-14 11:18:45",
                        "flick_url": < url >,
                        "id": 391895
                    },
            "annotation": {
                        "image_id": 391895,
                        "id": 37,
                        "caption": "A bicycle replica with a clock."
                    }
        }

    """
    for annotation in mscoco_data.get('annotations'):
        if annotation.get('id') == caption_id:
            break
    else:
        return None

    image_id = annotation.get('image_id')

    for image_info in mscoco_data.get('images'):
        if image_info.get('id') == image_id:
            break
    else:
        image_info = None

    return {'annotation':annotation, 'image':image_info}

def input_cycle(mscoco_data, image_dir_list, ru_mscoco_data=None):
    """
    This method loops over user input. Accesses the specified cell, reads
        annotation with the image & shows them. If ru_mscoco_data specified
        then its annotation displays too.

    Keyword arguments:
    mscoco_data -- < dict > with following fields:
        {
            "images": [
                    {
                        "file_name": < filename.jpg >,
                        "id": 391895
                    }, { ... }, ...
                ]
            "annotations": [
                    {
                        "image_id": 391895,
                        "id": 37,
                        "caption": "A bicycle replica with a clock."
                    }, { ... }, ...
                ]
            }
        }
    image_dir_list: < list > of < string > paths to image directories.
    ru_mscoco_file -- < dict > with fields described above (mscoco_data)

    """
    user_input = '-2'
    print('\nIf you want to quit write "exit".\n')

    while user_input != 'exit':
        user_input = input('Enter caption id: > ')

        if user_input == 'exit':
            break

        try:
            user_input = abs(int(user_input))
            caption_element = find_caption_element(mscoco_data, user_input)
            if caption_element is None:
                print('\nImage with specified cell has not found.\n')
            else:
                print('Caption:', caption_element['annotation']['caption'])

                if ru_mscoco_data is not None:
                    try:
                        print('RU-Caption:', find_caption_element(
                                        ru_mscoco_data,
                                        user_input)['annotation']['caption'])

                    except Exception as error_2:
                        print('\n[RU-Caption ERROR]: {}.\n'.format(error_2))

                try:
                    image_info_list = find_picture(image_dir_list,
                                        caption_element['image']['file_name'])

                except Exception as error_2:
                    image_info_list = None
                    print('\n[img-info-ERROR]: {}.\n'.format(error_2))

                if image_info_list is not None:
                    if len(image_info_list) > 0:
                        for image_info in image_info_list:
                            print('Path:', image_info.get('path'))

                            cv2.destroyAllWindows()
                            if image_info.get('image') is not None:
                                cv2.imshow(image_info.get('path'),
                                            image_info.get('image'))
                                cv2.waitKey(100)
                        print()
                    else:
                        print('\n[ATTENTION]: Image has not found.\n')

        except Exception as error:
            print('\n[ERROR]: {}.\n'.format(error))
            user_input = '-2'

if __name__ == '__main__':

    args = _a_parse()
    mscoco_data = read_json(args.get('mscoco_file'))

    if args.get('ru_mscoco_file') is not None:
        ru_mscoco_data = read_json(args.get('ru_mscoco_file'))
    else:
        ru_mscoco_data = None

    input_cycle(mscoco_data, args.get('image_dir_list'), ru_mscoco_data)
    cv2.destroyAllWindows()
