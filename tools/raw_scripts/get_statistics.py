import json
import os

json_path = os.path.abspath("../json_sources/GOOGLE_ONLY_statistic.json")

with open(json_path, 'r') as json_read:
    json_data = json.load(json_read)

h_key = ''
h_val = 0
l_key = ''
l_val = 9999999999999

for key in json_data.keys():
    value = json_data[key]
    if value < l_val:
        l_val = value
        l_key = key

    if value > h_val:
        h_val = value
        h_key = key

print('Размер словаря:', len(json_data.keys()))

print('\nСамое большое вхождение: {} - {}.'.format(h_key, h_val))
print('Самое низкое вхождение: {} - {}.\n'.format(l_key, l_val))

peak = 100

fragmentation = 30
fragment_step = int(peak / fragmentation)

fragment_list = []
count_list = []

for val in range(0, peak, fragment_step):
    fragment_list.append(val)
    count_list.append(0)

fragment_len = len(fragment_list)

for key in json_data.keys():
    quantity = json_data[key]
    for i in range(fragment_len):
        if i == fragment_len-1:
            break
        if fragment_list[i+1] > quantity:
            break
    count_list[i] += 1

for i in range(fragment_len):
    print(fragment_list[i], count_list[i])

count = 0

for key in json_data.keys():
    if json_data[key] < 10:
        count += 1
