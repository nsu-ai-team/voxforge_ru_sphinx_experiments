#!/bin/bash
set -e


if [ -d result_all_3gramm/ ]; then
	rm -r result_all_3gramm
fi
mkdir result_all_3gramm

for i in {1..10}
do
	cp -a "etc/$i/voxforge_ru.phone" etc/voxforge_ru.phone
	cp -a "etc/$i/voxforge_ru.dic" etc/voxforge_ru.dic
        cp -a "etc/$i/voxforge_ru.lm.bin" etc/voxforge_ru.lm.bin
        cp -a "etc/$i/voxforge_ru_test.fileids" etc/voxforge_ru_test.fileids
        cp -a "etc/$i/voxforge_ru_train.fileids" etc/voxforge_ru_train.fileids
        cp -a "etc/$i/voxforge_ru_test.transcription" etc/voxforge_ru_test.transcription
        cp -a "etc/$i/voxforge_ru_train.transcription" etc/voxforge_ru_train.transcription
	sphinxtrain run
	cat result/voxforge_ru.align >> result_all_3gramm/results
done
