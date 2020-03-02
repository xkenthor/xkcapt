import json

json_path = '../json_sources/combined_set_en.json'
export_file_path = 'path_to_en_captions'

with open(json_path, 'r') as json_read:
    json_data = json.load(json_read)

long_string = ''
index = 0
max = 1000

for annotation in json_data.get('annotations'):
    long_string += (annotation.get('caption') + '\n')
    index += 1
    if index > 1000:
        break


with open(export_file_path, 'w') as file_str:
    file_str.write(long_string)
