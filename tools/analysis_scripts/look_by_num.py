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

def _a_parse():
    """
    This function is a simple argument parser. Checks if paths in arguments are
        right & checks if directories exist.

    Return:
    < dict > -- {
                }

    """
    a_parser = argparse.ArgumentParser()
    a_parser.add_argument(
                '--mscoco_file',
                metavar='/path/to/mscoco.json',
                required=True,
                help='path to source mscoco file')

    a_parser.add_argument(
                '--image_dir_list',
                metavar='/path/to/img_dir_1, /path/to/img_dir_2',
                nargs='+',
                required=True,
                help='list of paths to image directories')

    a_parser.add_argument(
                '--ru_mscoco_file',
                metavar='/path/to/ru_mscoco.json',
                required=False,
                help='path to source ru_mscoco file')

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

if __name__ == '__main__':
    args = _a_parse()

    print('[ARGS]:', args)
