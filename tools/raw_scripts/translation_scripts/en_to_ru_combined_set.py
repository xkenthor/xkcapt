import json
import googletrans
import os

translator = googletrans.Translator()

json_path = os.path.abspath('../json_sources/combined_set.json')
json_result_path = os.path.abspath('../json_sources/ru_combined_set.json')

with open(json_path, 'r') as json_read:
    json_data = json.load(json_read)

annotation_list = json_data.get('annotations')

annotation_len = len(annotation_list)
count = 0

for annotation in annotation_list:
    caption = annotation.get('caption')
    print(caption)

    try:
        translation = translator.translate(
                                        text=caption, dest='ru', src='en').text
    except Exception as e:
        print(str(e))

    annotation.update({'caption':translation})

    count += 1
    print(translation)
    print('Переведено {} из {} аннотаций.\n'.format(count, annotation_len))

    if count%1000 == 0:
        print('> Checkpoint save ..')
        with open(json_result_path, 'w') as write_json:
            json.dump(json_data, write_json)

with open(json_result_path, 'w') as write_json:
    json.dump(json_data, write_json)
