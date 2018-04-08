#!/bin/bash
set -e

VOXFORGE_BASE_DIR=/home/ivan_bondarenko/voxforge_ru_asr

cd ${VOXFORGE_BASE_DIR}/voxforge_ru_asr_1_without_sil
sphinxtrain run

cd ${VOXFORGE_BASE_DIR}/voxforge_ru_asr_2_without_sil
sphinxtrain run

cd ${VOXFORGE_BASE_DIR}/voxforge_ru_asr_3_without_sil
sphinxtrain run
