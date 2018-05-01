#!/bin/bash
set -e

default_jobs=1
NJOBS=${1:-$default_jobs}

sphinxtrain -t voxforge_ru setup
cd etc
perl -i -p -e "s/CFG_NPART = $default_jobs/CFG_NPART = $NJOBS/" sphinx_train.cfg
perl -i -p -e "s/CFG_QUEUE_TYPE = \"Queue\"/CFG_QUEUE_TYPE = \"Queue::POSIX\"/" sphinx_train.cfg
python3 dict2pickle.py

for i in {1..10}
do
	cd $i
        cp ../sphinx_train.cfg sphinx_train.cfg
	python3 everything_maker.py
	ngram-count -text corpus_train -order 3 -write voxforge_ru.count -unk
	ngram-count -lm voxforge_ru.lm -order 3 -read voxforge_ru.count -kndiscount1 -kndiscount2 -kndiscount3
	sphinx_lm_convert -i voxforge_ru.lm -o voxforge_ru.lm.bin
	cd ..
done
