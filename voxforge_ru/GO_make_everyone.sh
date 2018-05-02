#!/bin/bash
set -e

default_jobs=1
NJOBS=${1:-$default_jobs}

sphinxtrain -t voxforge_ru setup
cd etc
perl -i -p -e "s/CFG_NPART = $default_jobs/CFG_NPART = $NJOBS/" sphinx_train.cfg
perl -i -p -e "s/CFG_QUEUE_TYPE = \"Queue\"/CFG_QUEUE_TYPE = \"Queue::POSIX\"/" sphinx_train.cfg
perl -i -p -e "s/CFG_WAVFILE_SRATE = 16000.0/CFG_WAVFILE_SRATE = 8000.0/" sphinx_train.cfg
perl -i -p -e "s/CFG_NUM_FILT = 25/CFG_NUM_FILT = 15/" sphinx_train.cfg
perl -i -p -e "s/CFG_LO_FILT = 130/CFG_LO_FILT = 200/" sphinx_train.cfg
perl -i -p -e "s/CFG_HI_FILT = 6800/CFG_HI_FILT = 3500/" sphinx_train.cfg
perl -i -p -e "s/CFG_N_TIED_STATES = 200/CFG_N_TIED_STATES = 3000/" sphinx_train.cfg
perl -i -p -e "s/.lm.DMP/.lm.bin/" sphinx_train.cfg
python3 dict2pickle.py

for i in {1..10}
do
	cd $i
	python3 everything_maker.py
	ngram-count -text corpus_train -order 2 -write voxforge_ru.count
	ngram-count -lm voxforge_ru.lm -order 2 -read voxforge_ru.count -kndiscount1 -kndiscount2
	sphinx_lm_convert -i voxforge_ru.lm -o voxforge_ru.lm.bin
	cd ..
done
