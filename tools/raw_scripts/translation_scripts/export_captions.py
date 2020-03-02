import json

json_path_en = '../json_sources/combined_set_en.json'
json_path_ru = '../json_sources/combined_set_ru_sm.json'
import_file_path = 'path_to_file'

with open(import_file_path) as import_file:
    raw_import = import_file.read()

raw_import = raw_import.split('\n')
index = 0

with open(json_path_en) as json_read:
    json_data = json.load(json_read)

for annotation in json_data.get('annotations'):
    annotation.update({'caption': raw_import[index]})
    index += 1

    if index > 1000:
        break

with open(json_path_ru, 'w') as json_write:
    json.dump(json_data, json_write)
