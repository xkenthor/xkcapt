"""
This module counts word frequency in .json or .tsv files. After finishing it
    saves the results to a file.

MSCOCO .json files must have following fields:
{
    "annotations":[
        {
            "caption": < string >
        }
    ]
}

Google .tsv files must have following format:
    [ annotation | URL ]

"""
import os
import json

import nltk

def get_mscoco_wfrequency():
    """
    This function processes MSCOCO .json file and starts counting frequency of
        unique words in "annotations" -> "caption" field.

    Keyword arguments:
    filename -- < dict > MSCOCO dict file.

    Return:
    < dict > -- {
                    "word_1": < frequency_int_1 >,
                    "word_2": < frequency_int_2 >,
                    ...
                    "word_n": < frequency_int_n >
                }

    """
    main_freq_list = nltk.FreqDist('')

    count = 0
    c_len = len(annotation_list)
    for annotation in annotation_list:
        try:
            caption = annotation.get('caption')
            caption = caption.lower()
            caption = nltk.work_tokenize(caption)

            current_freq_list = nltk.FreqDist(caption)
            main_freq_list += current_freq_list


        except Exception as error:
            print('[ERROR]:', error)

        if count % 10000 == 0:
            print('Processed: {}/{}'.format(count, c_len))
            count += 1

def get_hgst_and_lwst_frequency(annotation_tuple):

    h_freq = 0
    h_word = ''
    l_freq = 9999999999999
    l_word = ''

    count = 0
    c_len = len(annotation_tuple)

    for key in annotation_tuple.keys():
        current_value = annotation_tuple.get(key)
        if current_value > h_freq:
            h_freq = current_value
            h_word = key
        if current_value < l_freq:
            l_freq = current_value
            l_word = key

        if count%10000 == 0:
            print('ghalf: {}/{}'.format(count, c_len))
        count += 1

    return {'h_freq': h_freq,
            'h_word':h_word,
            'l_freq':l_freq,
            'l_word':l_word }

if __name__ == '__main__':

    # json_path = os.path.abspath('../json_sources/combined_set.json')
    #
    # with open(json_path, 'r') as json_read:
    #     json_data = json.load(json_read)
    #
    # annotation_list = json_data.get('annotations')
    # main_freq_list = get_words_frequency(annotation_list)

    tsv_path = os.path.abspath(
                    '../../datasets/google_dataset/Train_GCC-training.tsv')

    with open(tsv_path, 'r') as tsv_file:
        annotation_list = [line.strip().split('\t') for line in tsv_file]

    main_freq_list = get_tsv_words_frequency(annotation_list)

    freq_dict = dict(main_freq_list)
    only_freq_list = list(freq_dict.values())

    with open('../json_sources/GOOGLE_ONLY_statistic.json', 'w') as write_stat:
        json.dump(freq_dict, write_stat)

    print(get_hgst_and_lwst_frequency(freq_dict))
