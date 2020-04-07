"""
This module counts word frequency in .json or .tsv files. After finishing it
    saves the results to a file.

MSCOCO source .json files must have following fields:
{
    "annotations":[
        {
            "caption": < string >
        }
    ]
}

Google source .tsv files must have following format:
                                                [ annotation | URL ]

The script will save results to .json or .tsv file specified in --output_file
    path by user.

"""
import os
import sys
import json
import argparse

import nltk


def _a_parser():
    """
    This function is a simple argument parser. Checks if paths in arguments are
        right & checks if directories exist.

    Return:
    < dict > -- {
                'json_file': path to json_file OR None,
                'tsv_file': path to tsv_file OR None,
                'output_file': path to output_file
                }

    """
    a_parser = argparse.ArgumentParser()
    a_parser.add_argument(
                '-j',
                '--json_file',
                metavar='/path/to/json',
                required=False,
                help='path to source json-file if specified instead of tsv')

    a_parser.add_argument(
                '-t',
                '--tsv_file',
                metavar='/path/to/tsv',
                required=False,
                help='path to source tsv-file if specified instead of json')

    a_parser.add_argument(
                '-o',
                '--output_file',
                metavar='/path/to/output_file',
                required=False,
                help='path to output tsv if if not specified will be in ' + \
                    'script directory')

    args = vars(a_parser.parse_args())

    json_file_path = args.get('json_file')
    tsv_file_path = args.get('tsv_file')
    output_file_path = args.get('output_file')

    # source file checking
    if json_file_path is None and tsv_file_path is None:
        print('[ERROR]: No source file specified.')
        sys.exit()
    else:
        if json_file_path is not None:
            source_file_path = os.path.abspath(json_file_path)
            args.update({'json_file': source_file_path, 'tsv_file': None})
        else:
            source_file_path = os.path.abspath(tsv_file_path)
            args.update({'json_file': None, 'tsv_file': source_file_path})

    if os.path.exists(source_file_path) != True:
        print('[ERROR]: Source file path has not found.')
        sys.exit()

    if os.path.isfile(source_file_path) != True:
        print('[ERROR]: Source file is a directory.')
        sys.exit()

    # output file checking
    if output_file_path is None:
        print('\n[ATTENTION]: No output file specified. It will be saved as ' + \
                                    'wf_output_file.json in program directory.')
        output_file_path = os.path.abspath('wf_output_file.json')
    else:
        if output_file_path[-4:] != '.tsv' and output_file_path[-5:] != '.json':
            print("[ERROR]: Output file hasn't .tsv or .json extension.")
            sys.exit()
        else:
            output_file_path = os.path.abspath(output_file_path)

    if os.path.exists(output_file_path):
        ans = input(
            '\n[ATTENTION]: output file already exist, overwrite it? [Y/n]: ')
        if ans in {'True', 'true', '1', 't', 'y', 'yes', ''}:
            print('File will be overwritten.')
        else:
            print('Exiting..')
            sys.exit(1)

    args.update({'output_file': output_file_path})

    return args

def get_words_frequency(annotation_list):
    """
    This function goes through every annotation, counts words in a separate
        dictionary. Returns reverse sorted dictionary of frequency.

    Keyword arguments:
    annotation_list -- < list > of < string > list with annotations that will be
        checked.

    Return:
    < dict > -- {
                    "word_1": < int >,
                    "word_2": < int >,
                    ...
                    "word_n": < int >
                }

    """
    main_freq_list = nltk.FreqDist('')

    count = 0
    c_len = len(annotation_list)
    for caption in annotation_list:
        try:
            caption = caption.lower()
            caption = nltk.tokenize.word_tokenize(caption)

            current_freq_list = nltk.FreqDist(caption)
            main_freq_list += current_freq_list


        except Exception as error:
            print('[ERROR]:', error)

        if count % 10000 == 0:
            print('Processed: {}/{}'.format(count, c_len))

        count += 1

    main_freq_list = dict(main_freq_list)
    main_freq_list = {k: v for k, v in sorted(
                                            main_freq_list.items(),
                                            key=lambda item: item[1],
                                            reverse=True)}
    return main_freq_list

def read_tsv(tsv_path):
    """
    This method reads .tsv file with cells separated by tabs (/t) with following
        format:
                [ annotation | URL ]
        It returns list of annotations.

    Keyword arguments:
    tsv_file_path -- < string > path to tsv file.

    Return:
    < list > of < string > -- list with annotations.

    """
    with open(tsv_path, 'r') as tsv_file:
        tsv_data = tsv_file.read().split('\n')

    annotation_list = []
    for element in tsv_data:
        try:
            annotation_list.append(element.split('\t')[0])
        except Exception as error:
            print('[ATTENTION]: An error "{}" with an element: "{}"'.format(
                                                                error, element))

    return annotation_list

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

    annotation_list = []

    for annotation in json_data.get('annotations'):
        try:
            annotation_list.append(annotation.get('caption'))
        except Exception as error:
            print('[ATTENTION]: An error "{}" with an element: "{}"'.format(
                                                                error, element))

    return annotation_list

def write_json(dict_data, json_path):
    """
    This method simply writes dict to json file.

    Keyword arguments:
    dict_data -- < dict > dictionary with words frequency that will be written.
    json_path -- < string > path to json.

    """

    with open(json_path, 'w') as json_file:
        json.dump(dict_data, json_file, indent=3)

def write_tsv(dict_data, tsv_path):
    """
    This method simply writes dict to tsv file.

    Keyword arguments:
    dict_data -- < dict > dictionary with words frequency that will be written.
    tsv_path -- < string > path to tsv.

    """
    string_to_write = ''
    for key in dict_data.keys():
        string_to_write += ('{}\t{}\n'.format(key, dict_data.get(key)))

    with open(tsv_path, 'w') as tsv_file:
        tsv_file.write(string_to_write)

if __name__ == '__main__':

    args = _a_parser()

    if args.get('json_file') is not None:
        data = read_json(args.get('json_file'))
    else:
        data = read_tsv(args.get('tsv_file'))

    word_frequency = get_words_frequency(data)

    output_file = args.get('output_file')
    if os.path.splitext(output_file)[1] == '.json':
        write_json(word_frequency, output_file)
    else:
        write_tsv(word_frequency, output_file)
