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

find etc -type f -name "feat.params" -delete
find etc -type f -name "*.cfg" -delete
find etc -maxdepth 1 -type f -name "*.fileids" -delete
find etc -maxdepth 1 -type f -name "*.transcription" -delete

