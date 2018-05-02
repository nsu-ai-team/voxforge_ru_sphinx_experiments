# voxforge_ru_sphinx
Cross-validated experiments with the **Voxforge-Ru** corpus using the **CMU Sphinx**

Developed file structure is based on tutorial https://cmusphinx.github.io/wiki/tutorialam/

The experiments are configured in 10 folders, located in _voxforge_ru/etc_

To run the experiments, first you need to go to the database subdirectory and configure your database with

```
cd voxforge_ru
./GO_make_everyone.sh
```

If you want to parallelize a course of experiments, execute the above-mentioned command with positive integer argument defining target number of threads, for example:

```
./GO_make_everyone.sh 8
```

Then you can run all experiments with

```
./GO_cross.sh
```

The joint results of all cross-validation folds will be written into _voxforge_ru/result_all_3gramm/results_

For cleaning all auxiliary files and directories, generated during experiments, you need to run the command

```
./GO_clean.sh
```
