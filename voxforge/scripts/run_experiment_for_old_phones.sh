#!/bin/bash
set -e

VOXFORGE_BASE_DIR=/home/ivan_bondarenko/voxforge_ru_asr

cd ${VOXFORGE_BASE_DIR}/voxforge_ru_asr_1_old
sphinxtrain run

cd ${VOXFORGE_BASE_DIR}/voxforge_ru_asr_2_old
sphinxtrain run

cd ${VOXFORGE_BASE_DIR}/voxforge_ru_asr_3_old
sphinxtrain run
