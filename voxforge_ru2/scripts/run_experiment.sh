#!/bin/bash
set -e

VOXFORGE_BASE_DIR=/home/ivan_bondarenko/voxforge_ru_asr

cd ${VOXFORGE_BASE_DIR}/voxforge_ru_asr_1
sphinxtrain run

cd ${VOXFORGE_BASE_DIR}/voxforge_ru_asr_2
sphinxtrain run

cd ${VOXFORGE_BASE_DIR}/voxforge_ru_asr_3
sphinxtrain run
