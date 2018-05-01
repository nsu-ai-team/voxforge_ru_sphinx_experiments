#!/bin/bash
mkdir result_all_3gramm
for i in {1..10}
do
	cp -a etc/$i/sphinx_train.cfg etc/sphinx_train.cfg && sphinxtrain run && tail -3 result/voxforge_ru.align >> result_all_3gramm/results
done
