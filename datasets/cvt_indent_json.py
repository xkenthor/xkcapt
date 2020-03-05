import json

for filename in ['json_sources/GOOGLE_ONLY_statistic.json',
                                'json_sources/MSCOCO_ONLY_statistic.json']:
    with open(filename, 'r') as json_file:
        json_data = json.load(json_file)
    with open(filename, 'w') as json_file:
        json_data = json.dump(json_data, json_file, indent=3)
