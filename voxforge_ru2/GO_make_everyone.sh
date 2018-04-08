#!/bin/bash

for i in {1..10}
do
	cd /media/dino/DATA/ASR/voxforge_ru/etc/$i
	python3 everything_maker.py
	ngram-count -text corpus_train -order 3 -write voxforge_ru.count -unk
	ngram-count -lm voxforge_ru.lm -order 3 -read voxforge_ru.count -kndiscount1 -kndiscount2 -kndiscount3
	sphinx_lm_convert -i voxforge_ru.lm -o voxforge_ru.lm.bin
done
