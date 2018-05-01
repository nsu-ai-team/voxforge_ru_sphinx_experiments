with open('PROMPTS_all_dict', 'r') as f:
	all_dic = {}
	for line in f.readlines():
		word = line.split()[0]
		ind = word.find('(')
		if ind != -1:
			word = word[:ind]
		try:
			all_dic[word] += [' '.join(line.split()[1:])]
		except KeyError:
			all_dic[word] = [' '.join(line.split()[1:])]

import pickle

with open('PROMPTS_all_dict.pkl', 'wb') as f:
	pickle.dump(all_dic, f)
