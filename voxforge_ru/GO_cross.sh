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
perl -i -p -e "s/CFG_MMIE = \"no\"/CFG_MMIE = \"yes\"/" sphinx_train.cfg
perl -i -p -e "s/CFG_CMN = 'batch'/CFG_CMN = 'current'/" sphinx_train.cfg
perl -i -p -e "s/CFG_MMIE_TYPE   = \"rand\"/CFG_MMIE_TYPE   = \"best\"/" sphinx_train.cfg
perl -i -p -e "s/CFG_MMIE_CONSTE = \"3.0\"/CFG_MMIE_CONSTE = \"3.5\"/" sphinx_train.cfg
perl -i -p -e "s/CFG_FORCEDALIGN = 'no'/CFG_FORCEDALIGN = 'yes'/" sphinx_train.cfg
cd ..
./prepare_config_file.py -s etc/sphinx_train.cfg -d etc/sphinx_train.cfg

if [ -d result_all_3gramm/ ]; then
	rm -r result_all_3gramm
fi
mkdir result_all_3gramm

unzip ./etc/voxforge_ru.lm.zip -d ./etc/

for i in {1..10}
do
        cp -a "etc/$i/voxforge_ru_test.fileids" etc/voxforge_ru_test.fileids
        cp -a "etc/$i/voxforge_ru_train.fileids" etc/voxforge_ru_train.fileids
        cp -a "etc/$i/voxforge_ru_test.transcription" etc/voxforge_ru_test.transcription
        cp -a "etc/$i/voxforge_ru_train.transcription" etc/voxforge_ru_train.transcription
	sphinxtrain run
	tail -3 result/voxforge_ru.align >> result_all_3gramm/results
done
