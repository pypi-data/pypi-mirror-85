## TOPSIS-Kushagra-101803625
  --Calculate TOPSIS Score and rank them.

## Installation
```sh
>> pip install TOPSIS-Kushagra-101803625==1.0.3
```
## How to use it?
```sh
>> TOPSIS data.csv "1,1,1,2" "+,+,-,+" result.csv
```

## Input File(data.csv)
 - Input file contain three or more columns
 - First column is the object/variable name (e.g. M1, M2, M3)
 - From 2nd to last columns contain numeric values only
 
## Output File(result.csv)

Result file contains all the columns of input file and two additional columns having TOPSIS SCORE and RANK
 
## Check the following-

- Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.
- Impacts must be either +ve or -ve.
- Impacts and weights must be separated by ,(comma).

## License
2020 Kushagra Goel
This repository is licensed under the MIT license. See LICENSE for details.

