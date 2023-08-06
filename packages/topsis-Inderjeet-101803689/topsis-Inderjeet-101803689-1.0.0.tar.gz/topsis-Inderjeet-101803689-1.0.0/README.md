# topsis_package
It is a python package which is used to find best among the value using mathematical model(topsis)

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install this package.

```bash
pip install topsis-Inderjeet-101803689
```

## About
TOPSIS is an acronym that stands for 'Technique of Order Preference Similarity to the Ideal Solution' and is a pretty straightforward MCDA method. As the name implies, the method is based on finding an ideal and an anti-ideal solution and comparing the distance of each one of the alternatives to those

To get started quickly, just use the following:

```bash
from topsis_pckg.topsis import topsis
topsis('file_name','Weight','Impact','outputfile_name')
```
make ensure the weights and impacts should be in "" 

eg: "1,1,1,1" and "+,-,+,-"

## Pre-requisite
The data should be enclosed in the csv file. There must be more than 2 columns

## Result
the output(outputfile_name)  is saved in the project folder with extra 2 columns with topsis score and rank.

## License
© 2020  Inderjeet Singh

[MIT](https://choosealicense.com/licenses/mit/)