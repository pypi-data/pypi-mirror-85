# TOPSIS\_Shruti\_101803512

## What is TOPSIS ?
The Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS) is a multi-criteria decision analysis method

### How to use the package
TOPSIS_Shruti_101803512 package should be used as:
### In command prompt

>\>> pip install TOPSIS_Shruti_101803512

>\>> python 
>\>> import TOPSIS_Shruti_101803512 as t
>\>> t.topsis_evaluation(<InputDataFile>,<Weights>,<Impacts>,<ResultFileName>)
>\>> t.topsis_evaluation("data.csv","1,1,1,2","+,+,-,+","result.csv")

### Some instructions:
> • Input file must contain three or more columns.
> • From 2nd to last columns must contain numeric values only (Handling of non-numeric values)
> • Number of weights, number of impacts and number of columns (from 2nd to last columns) must
be same.
> • Impacts must be either +ve or -ve.
> • Impacts and weights must be separated by ‘,’ (comma).

## Example:
The dataset upon which topsis is to be performed is taken as folows. It will be in the form of a csv file.
#### Sample Input

| Model | Corr | Rseq | RMSE | Accuracy |
|-------|------|------|------|----------|
| M1    | 0.79 | 0.62 | 1.25 | 60.89    |
| M2    | 0.66 | 0.44 | 2.89 | 63.07    |
| M3    | 0.56 | 0.31 | 1.57 | 62.87    |
| M4    | 0.82 | 0.67 | 2.68 | 70.19    |
| M5    | 0.75 | 0.56 | 1.3  | 80.39    |

The following output with performance score and rank will be produced in a result(csv file) file and printed as output. 1st rank offering us the best decision, and last rank offering the worst decision making, according to TOPSIS method.
#### OUTPUT

| Model | Corr | Rseq | RMSE | Accuracy | Topsis Score        | Rank |
|-------|------|------|------|----------|---------------------|------|
| M1    | 0.79 | 0.62 | 1.25 | 60.89    | 0.6391330141342587  | 2    |
| M2    | 0.66 | 0.44 | 2.89 | 63.07    | 0.21259182969277918 | 5    |
| M3    | 0.56 | 0.31 | 1.57 | 62.87    | 0.4078456776130516  | 4    |
| M4    | 0.82 | 0.67 | 2.68 | 70.19    | 0.5191532395007472  | 3    |
| M5    | 0.75 | 0.56 | 1.3  | 80.39    | 0.8282665851935813  | 1    |
