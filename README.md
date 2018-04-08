# voxforge_ru_sphinx
Experiments with Voxforge-Ru corpus using the CMU Sphinx

Developed file structure is based on tutorial https://cmusphinx.github.io/wiki/tutorialam/

Each fold is provided by the corresponding directory **voxforge_ru_asr_<_number_>**, where <_number_> is 1, 2 or 3.

First of all, find the file **voxforge_ru_asr_<_number_>/etc/sphinx_train.cfg**. Search for the following lines in this file:

```$CFG_BASE_DIR = "/home/ivan_bondarenko/voxforge_ru_asr/voxforge_ru_asr_1";

$CFG_SPHINXTRAIN_DIR = "/usr/local/lib/sphinxtrain";

$CFG_BIN_DIR = "/usr/local/libexec/sphinxtrain";

$CFG_SCRIPT_DIR = "/usr/local/lib/sphinxtrain/scripts";
```

Change these paths in compliance with location of your cloned project and Sphinx installation directories.
