"""
This module reads .tsv file with following cell format:

                        [ annotation | URL ]

It goes though all the cells and tries to download every picture. If the
program fails to access then the cell number is added to the list of unloaded.

Result JSON-file view:

{
    "tsv_source_fname": < string >,
    "time spent": < int >,
    "downloaded_flist": [
                            {
                                "cell_number": < int >,
                                "filename": < string >,
                                "caption": < string >
                            }, ...
                        ],
    "error_clist":  [ < int >, ... ]
}

"""

from datetime import timedelta

import os
import sys
import json
import time
import urllib.request as ureq
import argparse

def _a_parse():
    """
    This function is a simple parser. Checks if paths in arguments are right.

    Return:
    dict -- {
            'source_tsv': < string >,
            'output_json': < string >,
            'dset_pic_path': < string >,
            'continue_download': < bool >,
            'timeout_connection': < float >
            }

    """
    a_parser = argparse.ArgumentParser()
    a_parser.add_argument(
                '-s',
                '--source_tsv',
                metavar='/path/to/tsv',
                required=True,
                help='path to source tsv-file')
    a_parser.add_argument(
                '-o',
                '--output_json',
                metavar='/path/to/json',
                default='output_gdset.json',
                help='path to output json-file')

    a_parser.add_argument(
                '-d',
                '--dset_pic_path',
                metavar='/path/to/pic_save_dir',
                default='dset_pictures',
                help='directory path where pictures will be download')

    a_parser.add_argument(
                '-c',
                '--continue_download',
                metavar='True OR true OR 1 OR y OR yes',
                default="True",
                help='continue downloading from last json number'
                )
    a_parser.add_argument(
                '-t',
                '--timeout_connection',
                metavar='float',
                default=1.0,
                type=float,
                help='connection timeout for each picture'
    )

    args = vars(a_parser.parse_args())
    s_tsv_path = os.path.abspath(args.get('source_tsv'))
    o_json_path = os.path.abspath(args.get('output_json'))
    dset_pic_path = os.path.abspath(args.get('dset_pic_path'))
    continue_flag = args.get('continue_download')

    if os.path.exists(s_tsv_path) != True:
        print('\n[ERROR]: .tsv file has not found')
        sys.exit(1)

    if os.path.splitext(o_json_path)[1] != '.json':
        print('\n[ERROR]: .json file has wrong extension')
        sys.exit(1)

    if os.path.exists(os.path.split(o_json_path)[0]) != True:
        print('\n[ERROR]: .json directory does not exist')
        sys.exit(1)

    if os.path.exists(o_json_path):
        ans = input(
            '\n[ATTENTION]: .json file already exist, overwrite it? [Y/n]: ')
        if ans in {'True', 'true', '1', 't', 'y', 'yes', ''}:
            print('File will be overwritten.')
        else:
            print('Exiting..')
            sys.exit(1)

    if continue_flag in {'True', 'true', '1', 't', 'y', 'yes', ''}:
        continue_flag = True
    else:
        continue_flag = False

    if os.path.exists(dset_pic_path) != True:
        os.makedirs(dset_pic_path)

    args.update({
            'source_tsv': s_tsv_path,
            'output_json': o_json_path,
            'dset_pic_path': dset_pic_path,
            'continue_download': continue_flag
            })

    return args

def read_tsv_data(tsv_path):
    """
    This function reads tsv data from file.

    Keyword arguments:
    tsv_path -- path to tsv file to be read

    Return:
    < list > -- [ [ < string >, < string > ], ... ]

    """
    with open(tsv_path, 'r') as tsv_file:
        tsv_data = [line.strip().split('\t') for line in tsv_file]
    return tsv_data

def read_json_data(json_path):
    """
    This function reads tsv data from file.

    Keyword arguments:
    json_path -- path to json file to be read

    Return:
    < dict > -- it is understood that json will have the following format:
            {
                "tsv_source_fname": < string >,
                "time spent": < int >,
                "downloaded_flist": [
                                        {
                                            "cell_number": < int >,
                                            "filename": < string >,
                                            "caption": < string >
                                        }, ...
                                    ],
                "error_clist":  [ < int >, ... ]
            }

    """
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)

    return json_data

def save_json_data(json_path, json_info):
    """
    This function reads tsv data from file.

    Keyword arguments:
    json_path -- path to tsv file to be written
    json_info -- dict that will be saved in json file

    """
    with open(json_path, 'w') as json_file:
        json.dump(json_info, json_file)

def _print_current_info(tsv_index, tsv_len, time_spent, time_left):
    """
    This function displays information about the current download.

    Keyword arguments:
    info -- < dict > information that will be displayed

    """
    print('Current index: {} of {}.'.format(tsv_index, tsv_len))
    print('Time since the start of the download: {}'.format(time_spent))
    print('Estimated time to complete the download: {}'.format(time_left))

def start_downloading(args):
    """
    This function starts downloading.

    Keyword arguments:
    args -- {
            'source_tsv': < string >,
            'output_json': < string >,
            'dset_pic_path': < string >,
            'continue_download': < bool >,
            'timeout_connection': < float >
            }
    """

    o_json_path = args.get('output_json')
    t_timeout = args.get('timeout_connection')
    dset_pic_path = args.get('dset_pic_path')

    tsv_data = read_tsv_data(args.get('source_tsv'))
    tsv_len = len(tsv_data)
    tsv_index = 0

    json_data = None
    pic_name = 'dataset_pic_{}.jpg'
    z_indent = len(str(tsv_len))

    if args.get('continue_download'):
        if os.path.isfile(o_json_path):
            json_data = read_json_data(o_json_path)

            if len(json_data.get('downloaded_flist')) > 0:
                flist_last = json_data.get('downloaded_flist')[-1].get(
                                                                'cell_number')
            else:
                flist_last = 0

            if len(json_data.get('error_clist')) > 0:
                clist_last = json_data.get('error_clist')[-1]
            else:
                clist_last = 0

            if flist_last > clist_last:
                tsv_index = flist_last + 1
            elif flist_last < clist_last:
                tsv_index = clist_last + 1
            else:
                tsv_index = 0

        else:
            print('[ATTENTION]: continue_download flag is true but .json ' \
            'file has not found. Download will start from beginning.')

    if json_data is None:
        json_data = {
            "tsv_source_fname": os.path.split(args.get('source_tsv'))[1],
            "time_spent": 0,
            "downloaded_flist": [],
            "error_clist":  []
        }
        save_json_data(o_json_path, json_data)


    start_time = time.time()
    time_spent = json_data.get('time_spent')
    downloaded_flist = json_data.get('downloaded_flist')
    error_clist = json_data.get('error_clist')

    print('\nThe paths are:\n')
    print('.tsv-file path:', args.get('source_tsv'))
    print('.json-file path:', args.get('output_json'))
    print('Dataset pics path:', args.get('dset_pic_path'))
    print(
         '\nFound {} cells. Current index: {}.\nStarting download...\n'.format(
                                                tsv_len, tsv_index))

    for tsv_index in range(tsv_index, tsv_len):

        current_cell = tsv_data[tsv_index]

        try:
            resource = ureq.urlopen(current_cell[1], timeout=t_timeout)
            current_filename = pic_name.format(str(tsv_index).zfill(z_indent))

            with open(os.path.join(
                        dset_pic_path, current_filename), 'wb') as current_pic:
                current_pic.write(resource.read())

            downloaded_flist.append({
                                    "cell_number": tsv_index,
                                    "filename": current_filename,
                                    "caption": current_cell[0]
                                    })
        except Exception as e:
            print('Trouble with link:', current_cell[1])
            error_clist.append(tsv_index)

        if tsv_index%100 == 0:
            delta_time = round(time_spent + (time.time()-start_time))
            seconds_left = round(delta_time/(tsv_index+1)*(tsv_len-tsv_index))

            _print_current_info(
                                tsv_index,
                                tsv_len,
                                str(timedelta(seconds=delta_time)),
                                str(timedelta(seconds=seconds_left))
                                )
            if tsv_index%1000 == 0:
                json_data.update({'time_spent': delta_time})
                save_json_data(o_json_path, json_data)
                print('\nSaved json_data info.\n')


    save_json_data(o_json_path, json_data)
    error_len = len(error_clist)
    success_len = len(downloaded_flist)

    print('\nDownloading has completed.')
    print('\n\nTotal:\n\tDownloaded successfuly: {} of {} images.\n'.format(
                                                success_len, tsv_len))
    print('Connection error percentage: {}%.'.format(
                                             round(100/tsv_len*error_len, 2)))

if __name__ == '__main__':

    args = _a_parse()
    start_downloading(args)
