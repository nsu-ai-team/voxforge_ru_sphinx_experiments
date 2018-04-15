# voxforge_ru_sphinx
Cross-validated experiments with Voxforge-Ru corpus using the CMU Sphinx

Developed file structure is based on tutorial https://cmusphinx.github.io/wiki/tutorialam/

The experiments are configured in 10 folders, located in voxforge_ru_sphinx/voxforge_ru/etc

To run the experiments, first go to the database subdirectory and configure your database with
```
cd voxforge_ru
./GO_make_everyone.sh
```
Afterwords, the experiments could be ran with
```
./GO_cross.sh
```
The joint results of cross-validation will be located in 'voxforge_ru_sphinx/voxforge_ru/result_all_3gramm/results'
