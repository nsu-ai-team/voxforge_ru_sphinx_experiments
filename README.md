# voxforge_ru_sphinx
Cross-validated experiments with the **Voxforge-Ru** corpus using the **CMU Sphinx**.

## Prerequisites

Installation process of the CMU Sphinx is described in https://cmusphinx.github.io/wiki/download/ We use three packages:

- [sphinxbase-5prealpha](http://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha)
- [pocketsphinx-5prealpha](http://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha)
- [sphinxtrain-5prealpha](http://sourceforge.net/projects/cmusphinx/files/sphinxtrain/5prealpha)

Also, for the forced alignment the `sphinx3_align` program from [the Sphinx3 version 0.8](https://sourceforge.net/projects/cmusphinx/files/sphinx3/0.8/) is used.  This program should be copied to the `bin` directory of the **Sphinx 5 Prealpha** after installation of the **Sphinx3**. *Caution*: the **Sphinx 3** as well as the **Sphinx 5 prealpha** is based on the `sphinxbase` package, but the **Sphinx 3** needs the older version of the `sphinxbase`. We recommend to use the [sphinxbase 0.4.1](https://sourceforge.net/projects/cmusphinx/files/sphinxbase/0.4.1/) for the **Sphinx 3** and the [sphinxbase-5prealpha](http://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha) for the **Sphinx 5 prealpha**.

## Usage

Developed file structure is based on tutorial https://cmusphinx.github.io/wiki/tutorialam/

The experiments are configured in 10 folders, located in _voxforge_ru/etc_

You can run all experiments with

```
cd voxforge_ru
./GO_cross.sh
```

If you want to parallelize a course of experiments, execute the above-mentioned command with positive integer argument defining target number of threads, for example:

```
./GO_cross.sh 8
```

The joint results of all cross-validation folds will be written into _voxforge_ru/result_all_3gramm/results_

For cleaning all auxiliary files and directories, generated during experiments, you need to run the command

```
./GO_clean.sh
```
