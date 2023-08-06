Package name = TOPSIS-Aryan-101803035

# About the project
As the name suggests, this package implements TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) which is a multi-criteria decision analysis method (MCDA or MCDM), which is a technique based on the concept that the chosen alternative should have the shortest geometric distance from the positive ideal solution (PIS) and the longest geometric distance from the negative ideal solution (NIS). 

This package hence provides with the TOPSIS score according to which a model's relative rank with  respect to other models with same number of entries is also provided.


### Installation

Install the package using pip as follows :

```sh
$ pip install TOPSIS-Aryan-101803035
```

### How to run in command prompt
First go to the directory (using cd following by your directory command) where it has been installed (prefreably the directory will be in main python folder -> Libs -> site-packages -> yourpackagename) then run the following commands : 
```sh
$ python TOPSIS.py <InputDataFile> <Weights> <Impacts> <ResultFileName>
```
Eg: 
```sh
$ python TOPSIS.py data.csv “1,1,1,2” “+,+,-,+” result.csv
```
