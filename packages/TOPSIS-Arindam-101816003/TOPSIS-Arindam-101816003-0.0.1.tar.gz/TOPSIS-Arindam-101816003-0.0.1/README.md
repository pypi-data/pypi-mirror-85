# TOPSIS-Python

Submitted By: **Arindam Sharma**

## What is TOPSIS

**T**echnique for **O**rder **P**reference by **S**imilarity to **I**deal
**S**olution (TOPSIS) originated in the 1980s as a multi-criteria decision
making method. TOPSIS chooses the alternative of shortest Euclidean distance
from the ideal solution, and greatest distance from the negative-ideal
solution. More details at [wikipedia](https://en.wikipedia.org/wiki/TOPSIS).

<br>

## How to use this package:

```
>> topsis data.csv "1,1,1,1" "+,+,-,+" output.csv
```

<br>

## Sample dataset

The decision matrix (`a`) should be provided with more than two columns and should be in .csv format.

Model | Correlation | R<sup>2</sup> | RMSE | Accuracy
------------ | ------------- | ------------ | ------------- | ------------
M1 |	0.79 | 0.62	| 1.25 | 60.89
M2 |  0.66 | 0.44	| 2.89 | 63.07
M3 |	0.56 | 0.31	| 1.57 | 62.87
M4 |	0.82 | 0.67	| 2.68 | 70.19
M5 |	0.75 | 0.56	| 1.3	 | 80.39

Weights (`w`) and impacts (either + or -)  should also be provided alogn with.

<br>

## Output

The output comes out in a csv file as the format given below :
```
Model | Correlation | R<sup>2</sup> | RMSE | Accuracy | Topsis Score | Rank
------------ | ------------- | ------------ | ------------- | ------------
M1 |	0.79 | 0.62	| 1.25 | 60.89 | 0.639133 | 2
M2 |  0.66 | 0.44	| 2.89 | 63.07 | 0.212592 | 5
M3 |	0.56 | 0.31	| 1.57 | 62.87 | 0.407846 | 4
M4 |	0.82 | 0.67	| 2.68 | 70.19 | 0.519153 | 3
M5 |	0.75 | 0.56	| 1.3	 | 80.39 | 0.828267 | 1

```