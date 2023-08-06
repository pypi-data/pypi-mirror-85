# TOPSIS-Python

## What is TOPSIS

Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) originated in the 1980s as a multi-criteria decision making method. TOPSIS chooses the alternative of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.


## How to use this package:



TOPSIS-Manpreet-101803174 can be run as in the following example:

### In command prompt:

```bash
>> TOPSIS data.csv "1,1,2,1" "+,-,+,-" result.csv
```




## Sample Dataset

```python



Model	Correlation	  R2	RMSE	Accuracy
M1	      0.79	     0.62	1.25	 60.89
M2	      0.66	     0.44	2.89	 63.07
M3	      0.56	     0.31	1.57     62.87
M4	      0.82	     0.67	2.68	 70.19
M5	      0.75	     0.56	1.3	     80.39

```

## Output

```python
Model   Score    Rank
-----  --------  ----
  1    0.77221     2
  2    0.225599    5
  3    0.438897    4
  4    0.523878    3
  5    0.811389    1

```
