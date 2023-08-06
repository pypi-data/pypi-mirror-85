# TOPSIS-Python

## About Topsis 

(TOPSIS) stands for Techqniquie Order Preference by Similarity to Ideal Solution.It  chooses the alternative of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.


## How to use this package:



TOPSIS-YashSinghPathania-101816052 can be used with the following bash command 

### CMD:

```bash
>> TOPSIS data.csv "1,1,2,1" "+,-,+,-" result.csv
```




## Sample Dataset example use case 

```python



Model	Correlation	  R2	RMSE	Accuracy
M1	      0.79	     0.62	1.25	 60.89
M2	      0.66	     0.44	2.89	 63.07
M3	      0.56	     0.31	1.57     62.87
M4	      0.82	     0.67	2.68	 70.19
M5	      0.75	     0.56	1.3	     80.39

```

## Resultant Dataset 

```python
Model   Score    Rank
-----  --------  ----
  1    0.77221     2
  2    0.225599    5
  3    0.438897    4
  4    0.523878    3
  5    0.811389    1

```
