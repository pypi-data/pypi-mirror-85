This package is implementation of topsis technique of multi-criteria decision analysis.

You can install this package using following command
pip install TOPSIS-Ishika-101803017

This packages will work on command line interface
> - import TOPSIS-Ishika-101803017 as t
> - t.topsis(InputDataFile, Weights, Impacts, resultfile)
### Input specifications
> - InputDataFile is path to your input csv file(eg inputfile.csv)
> - weights is  string in which each digit represent weight of corresponding column(eg "1,1,1,1")
> - impacts are impacts of column (eg "-,+,+,+" ) 
> - result is name of output file(eg result.csv)

## PRECAUTIONS
> No of weights and no of impacts should be equal to no. of columns in dataset excluding the first column
> Impacts must be either +ve or -ve
> Input file must contain three or more columns
> 2nd to last columns contain numeric values only

Result file contains all the columns of input file and two additional columns having TOPSIS SCORE and RANK

### EXAMPLE

>IF INPUT FILE IS AS FOLLOWS:

| Model | Correlation | RSeq | RMSE | Accuracy
| ------ | ------ | ----- | ----- | --------
| M1 | 0.79 | 0.62 | 1.25 | 60.89 
| M2 | 0.66 | 0.44 | 2.89 | 63.07
| M3 | 0.56 | 0.31 | 1.57 | 62.87
| M4 | 0.82 | 0.67 | 2.68 | 70.19
| M5 | 0.75 | 0.56 | 1.3 | 80.39

> OUTPUT FILE:

| Model | Correlation | RSeq | RMSE | Accuracy | Topsis Score | Rank
| ------ | ------ | ----- | ----- | -------- | -------- | --------
| M1 | 0.79 | 0.62 | 1.25 | 60.89 | 0.639133 | 2
| M2 | 0.66 | 0.44 | 2.89 | 63.07 | 0.212592 | 5
| M3 | 0.56 | 0.31 | 1.57 | 62.87 | 0.407846 | 4
| M4 | 0.82 | 0.67 | 2.68 | 70.19 | 0.519153 | 3
| M5 | 0.75 | 0.56 | 1.3 | 80.39 | 0.828267 | 1
