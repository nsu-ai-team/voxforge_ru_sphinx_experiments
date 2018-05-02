#!/bin/bash
set -e


if [ -d bwaccumdir/ ]; then
	rm -r bwaccumdir
fi
if [ -d model_architecture/ ]; then
	rm -r model_architecture
fi
if [ -d model_parameters/ ]; then
        rm -r model_parameters
fi
if [ -d qmanager/ ]; then
	rm -r qmanager
fi
if [ -d result/ ]; then
	rm -r result
fi
if [ -d trees/ ]; then
	rm -r trees
fi
if [ -d logdir/ ]; then
        rm -r logdir
fi

if [ -f voxforge_ru.html ]; then
	rm voxforge_ru.html
fi
if [ -f etc/PROMPTS_all_dict.pkl ]; then
	rm etc/PROMPTS_all_dict.pkl
fi

find etc -type f -name "*.dic" -delete
find etc -type f -name "*.cfg" -delete
find etc -type f -name "*.fileids" -delete
find etc -type f -name "*.phone" -delete
find etc -type f -name "*.count" -delete
find etc -type f -name "*.lm" -delete
find etc -type f -name "*.lm.bin" -delete
find etc -type f -name "corpus_train" -delete
if [ -f etc/*.transcription ]; then
	rm etc/*.transcription
fi
