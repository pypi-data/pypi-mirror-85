# TOPSIS Package in Python

Submitted by: Vedant Gupta

Roll no: 101803329

UCS538

* * *
## Concept of TOPSIS

TOPSIS is an acronym that stands for Technique of Order Preference Similarity to the Ideal Solution and is a pretty straightforward MCDA method. As the name implies, the method is based on finding an ideal and an anti-ideal solution and comparing the distance of each one of the alternatives to those.

* * *

## How to use

The package TOPSIS-Vedant-101803329 can be run though the command line as follows:
```
>> pip install TOPSIS-Vedant-101803329==1
```
```
>> python
>>>from topsis_cal.topsiscode import topsis
>>>topsis("data.csv","1,1,1,2","+,+,-,+")
```
<br>

## Sample dataset

The decision matrix (`a`) should be constructed with each row representing a Model alternative, and each column representing a criterion like Accuracy, R<sup>2</sup>, Root Mean Squared Error, Correlation, and many more.

Model | Correlation | R<sup>2</sup> | RMSE | Accuracy
------------ | ------------- | ------------ | ------------- | ------------
M1 |	0.79 | 0.62	| 1.25 | 60.89
M2 |  0.66 | 0.44	| 2.89 | 63.07
M3 |	0.56 | 0.31	| 1.57 | 62.87
M4 |	0.82 | 0.67	| 2.68 | 70.19
M5 |	0.75 | 0.56	| 1.3	 | 80.39

Weights (`w`) is not already normalised will be normalised later in the code.

Information of benefit positive(+) or negative(-) impact criteria should be provided in `I`.

<br>

## Output

```
Model   Score    Rank
-----  --------  ----
  1    0.639133    2
  2    0.212592    5
  3    0.407846    4
  4    0.519153    3
  5    0.828267    1
```
<br>
The rankings are displayed in the form of a table using a package 'tabulate', with the 1st rank offering us the best decision, and last rank offering the worst decision making, according to TOPSIS method.

