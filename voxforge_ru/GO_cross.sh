#!/bin/bash
set -e


if [ -d result_all_3gramm/ ]; then
	rm -r result_all_3gramm
fi
mkdir result_all_3gramm

for i in {1..10}
do
	cp -a "etc/$i/sphinx_train.cfg" etc/sphinx_train.cfg && cp -a "etc/$i/voxforge_ru.dic" etc/voxforge_ru.dic && sphinxtrain run && tail -3 result/voxforge_ru.align >> result_all_3gramm/results
done
