import re

with open('voxforge_ru_train.transcription') as file_train:
	lines = file_train.readlines()
	words = set(re.findall('(?<=\s)[^()\s]+(?=\s)', ' ' + file_train.read()))

corpus_train = []
ids_train = ''

for line in lines:
	phrase = line.split()
	filename = phrase[-1]
	del phrase[-1]
	corpus_train += [' '.join(phrase)]
	filename = filename[1:-1]
	ids_train += '{}\n'.format(filename)

with open('corpus_train', 'w') as corpus_train_file:
	corpus_train_file.write('\n'.join(sorted(list(set(corpus_train))) + ['']))

with open('voxforge_ru_train.fileids', 'w') as ids_train_file:
	ids_train_file.write(ids_train)

vocab_train = set('\n'.join(sorted(list(set(corpus_train)))).split())

with open('voxforge_ru_test.transcription') as file_test:
	lines = file_test.readlines()

ids_test = ''

for line in lines:
	phrase = line.split()
	filename = phrase[-1][1:-1]
	ids_test += '{}\n'.format(filename)

with open('voxforge_ru_test.fileids', 'w') as ids_test_file:
	ids_test_file.write(ids_test)
	
with open('../PROMPTS_all_dict') as f:
	all_dic = dict(list([(line.split()[0], ' '.join(line.split()[1:])) for line in f.readlines()]))

phoneset = set()

with open('voxforge_ru.dic', 'w') as f:
	for word in sorted(list(vocab_train)):
		if word not in ['<s>','</s>','<sil>', '<um>', '<h>', '<l>']:
			f.writelines('{} {}\n'.format(word, all_dic[word]))
			phoneset = phoneset | set(all_dic[word].split())

with open('voxforge_ru.phone', 'w') as f:
	f.write('\n'.join(['SIL'] + sorted(list(phoneset))))