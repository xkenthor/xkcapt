"""
This module merges two MSCOCO json files into one. It takes two paths to json
    files as arguments.
It is worth noting that original MSCOCO dataset has the following feature:
    one picture may have two or more annotations so this module implements
    logic that preserves the correct annotation links to images

It is understood that MSCOCO json files will have following format:
{
    "info": {
        "description": "This is stable 1.0 version..",
        "url": "http://mscoco.org",
        "version": "1.0",
        "year": 2017,
        "contributor": "Microsoft COCO.group",
        "date_created": "2017-01-27 09:11:52.357474",
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
        ],
    "licenses": [
            {
                "url": "http:// ... .com"
                "id": 1,
                "name": 'Attribution-NonCommercial-ShareAlike Licence'
            }, { ... }, ...
        ],
    "annotations": [
            {
                "image_id": 203564,
                "id": 37,
                "caption": "A bicycle replica with a clock as the front wheel."
            }, { ... }, ...
        ]
    }
}

"""
import os
import sys
import json
import argparse

def _a_parse():
    """
    This function is a simple argument parser. Checks if paths in arguments are
        right & checks if directories exist.

    Return:
    < dict > -- {
                'first_json': < string >,
                'second_json': < string >,
                'result_json': < string >
                }

    """
    a_parser = argparse.ArgumentParser()
    a_parser.add_argument(
                        '-f',
                        '--first_json',
                        metavar='/path/to/json',
                        required=True,
                        help='first .json file')

    a_parser.add_argument(
                        '-s',
                        '--second_json',
                        metavar='/path/to/json',
                        required=True,
                        help='second .json file')

    a_parser.add_argument(
                        '-r',
                        '--result_json',
                        metavar='/path/to/json',
                        default='merged_result.json',
                        required=False,
                        help='path for result .json file')

    args = vars(a_parser.parse_args())
    first_json = os.path.abspath(args.get('first_json'))
    second_json = os.path.abspath(args.get('second_json'))
    result_json = os.path.abspath(args.get('result_json'))

    json_paths = [first_json, second_json, result_json]
    error_names = ['first', 'second', 'result']

    for index in range(3):
        if os.path.splitext(json_paths[index])[1] != '.json':
            print('[ERROR]: {} .json path has wrong extension.'.format(
                                                            error_names[index]))
            sys.exit(1)

    for index in range(2):
        if os.path.exists(json_paths[index]) != True:
            print('[ERROR]: {} .json file has not found.'.format(
                                                            error_names[index]))
            sys.exit(1)

    for index in range(2):
        if os.path.isfile(json_paths[index]) != True:
            print('[ERROR]: {} .json path is not a file.'.format(
                                                            error_names[index]))
            sys.exit(1)

    if os.path.exists(result_json):
        ans = input('\n[ATTENTION]: result .json file path already exist,' + \
                                                    ' overwrite it? [Y/n]: ')
        if ans in {'True', 'true', '1', 't', 'y', 'yes', ''}:
            print('File will be overwritten.')
        else:
            print('Exiting..')
            sys.exit(1)

    args.update({
                'first_json': first_json,
                'second_json': second_json,
                'result_json': result_json
                })
    return args

def read_json_file(json_path):
    """
    This function simply reads json file and return python dictionary data. If
        any problems arise, it will return None.

    Keyword arguemnts:
    json_path -- < string > path to first json

    """
    try:
        with open(json_path, 'r') as json_file:
            json_data = json.load(json_file)
    except Exception as e:
        print('[ERROR]:', e)
        json_data = None

    return json_data

def get_max_id(list_of_dicts):
    """
    This function returns max id value in dictionary list.

    Keyword arguments:
    list_of_dicts -- < list > [ < dict >, ... ]. Dict must have cell 'id':
        [
            {
                ...
                'id': < int >,
                ...
            }
        ]

    Return:
    < int > -- max id value

    """
    max_id = -1
    for d_element in list_of_dicts:
        current_id = d_element.get('id')
        if current_id > max_id:
            max_id = current_id

    return max_id

def merge_mscoco_dicts(dict_1, dict_2):
    """
    This function merges two ms coco dictionaries while maintaining annotation
        indices that point to images.
    Format of mscoco dict specified in module description.

    Keyword arguments:
    dict_1 -- < dict > that will be merged with other
    dict_2 -- < dict > that will be merged with other

    Return:
    < dict > -- merged result dict

    """
    # copying files to save original data
    dict_1 = dict_1.copy()
    dict_2 = dict_2.copy()

    images_1 = dict_1.get('images')
    annotations_1 = dict_1.get('annotations')

    images_2 = dict_2.get('images')
    annotations_2 = dict_2.get('annotations')

    current_image_id = get_max_id(images_1) + 1
    current_annotation_id = get_max_id(annotations_1) + 1

    for image_info in images_2:
        old_image_id = image_info.get('id')

        for annotation_info in annotations_2:
            if annotation_info.get('image_id') == old_image_id:
                annotation_info.update({'image_id':current_image_id})

        image_info.update({'id':current_image_id})
        current_image_id += 1

    # since annotation identifiers do not matter, we just update them
    for annotation_info in annotations_2:
        annotation_info.update({'id': current_annotation_id})
        current_annotation_id += 1

    images_1 += images_2
    annotations_1 += annotations_2

    return dict_1

if __name__ == '__main__':
    args = _a_parse()

    dict_1 = read_json_file(args.get('first_json'))
    dict_2 = read_json_file(args.get('second_json'))

    result_dict = merge_mscoco_dicts(dict_1, dict_2)

    with open(args.get('result_json'), 'w') as json_file:
        json.dump(result_dict, json_file)
