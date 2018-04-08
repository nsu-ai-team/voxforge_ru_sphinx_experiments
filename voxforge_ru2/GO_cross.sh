#!/bin/bash
cd /media/dino/DATA/ASR/voxforge_ru
mkdir /media/dino/DATA/ASR/voxforge_ru/result_all_3gramm
for i in {1..10}
do
	cp -a /media/dino/DATA/ASR/voxforge_ru/etc/$i/sphinx_train.cfg /media/dino/DATA/ASR/voxforge_ru/etc/sphinx_train.cfg && sphinxtrain run && tail -3 /media/dino/DATA/ASR/voxforge_ru/result/voxforge_ru.align >> /media/dino/DATA/ASR/voxforge_ru/result_all_3gramm/results
done
