import os

transliterate_dict = {'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
					'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
					'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
					'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
					'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch',
					'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': "''", 'Ы': 'Y', 'Ь': "'",
					'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
					'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
					'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
					'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
					'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
					'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
					'ш': 'sh', 'щ': 'shch', 'ъ': "''", 'ы': '', 'ь': "'",
					'э': 'e', 'ю': 'yu', 'я': 'ya'}

lp_dict = {'А':'A', 'В':'B', 'Е':'E', 'К':'K', 'М':'M', 'Н':'H',
			'О':'O', 'Р':'P', 'С':'C', 'Т':'T', 'У':'y', 'Х':'X',
			'а':'A', 'в':'B', 'е':'E', 'к':'K', 'м':'M', 'н':'H',
			'о':'O', 'р':'P', 'с':'C', 'т':'T', 'у':'y', 'х':'X'}

def transl_rus_to_eng(name):
	"""
	This function converts Сyrillic symbols to the identical in pronunciation
		in Latin.

	Keyword arguments:
	label -- string that will be converted

	Return:
	converted string
	"""
	new_name = ''
	for letter in name:
		c_n = ord(letter)
		if c_n > 1039 and c_n < 1104:
			new_name += transliterate_dict.get(letter)
		else:
			new_name += letter
	return new_name

def convert_plate_symb_ru_to_en(label):
	"""
	This function converts Сyrillic symbols to the identical in appearance
		in Latin.

	Keyword arguments:
	label -- string that will be converted

	Return:
	converted string
	"""

	new_label = ''

	for letter in label:
		c_n = ord(letter)
		if c_n > 1039 and c_n < 1104:
			new_label += lp_dict.get(letter)
		else:
			new_label += letter
	return new_label
