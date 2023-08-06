# TOPSIS Package in Python

Submitted by: Karanbir singh

Roll no: 101803235

Data science

* * *
## Concept of TOPSIS

TOPSIS is an acronym that stands for ‘Technique of Order Preference Similarity to the Ideal Solution’ and is a pretty straightforward MCDA method. As the name implies, the method is based on finding an ideal and an anti-ideal solution and comparing the distance of each one of the alternatives to those.

* * *

## How to use

The package TOPSIS-Karanbir-101803235 can be run though the command line as follows:
```
>> pip install TOPSIS-Karanbir-101803235==0.1
```
```
>> python
>>>from topsis_analysis.topsispackage import topsis
>>>topsis("data.csv","1,1,1,2","+,+,-,+","output.csv")
```
> **Note:**
> 
> *   Usages: 
>     
>       topsis( <**InputDataFile**> <**Weights**> <**Impacts**> <**ResultFileName**>)
> *   **Input File**:
>     
>     > *   Input file contain three or more columns.
>     > *   First column is the object/variable name (e.g. M1, M2, M3, M4……) .
>     > *   From 2nd to last columns contain numeric values only.
> *   **Output File**:
>     
>     > *   Result file contains all the columns of input file and two additional columns having TOPSIS SCORE and RANK
> *   The output is created in the form of csv file and stored and also it is displayed.
> *   The impacts given in the command line should be either ‘+’ or ‘–’ depending if you want to maximise the column parameter or minimise it.

## Sample Input

Here is a sample set of data which can be used for the following package:

<table><thead><tr><th>Model</th><th>Correlation</th><th>R2</th><th>RMSE</th><th>Accuracy</th></tr></thead><tbody><tr><td>M1</td><td>0.79</td><td>0.62</td><td>1.25</td><td>60.89</td></tr><tr><td>M2</td><td>0.66</td><td>0.44</td><td>2.89</td><td>63.07</td></tr><tr><td>M3</td><td>0.56</td><td>0.31</td><td>1.57</td><td>62.87</td></tr><tr><td>M4</td><td>0.82</td><td>0.67</td><td>2.68</td><td>70.19</td></tr><tr><td>M5</td><td>0.75</td><td>0.56</td><td>1.3</td><td>80.39</td></tr></tbody></table>

## Output of this sample input

The output that will be generated from the following input data will be:

<table><thead><tr><th>Model</th><th align="right">Correlation</th><th align="center">R2</th><th>RMSE</th><th>Accuracy</th><th>Topsis Score</th><th>Rank</th></tr></thead><tbody><tr><td>M1</td><td align="right">0.79</td><td align="center">0.62</td><td>1.25</td><td>60.89</td><td>0.6391330141342590</td><td>2.0</td></tr><tr><td>M2</td><td align="right">0.66</td><td align="center">0.44</td><td>2.89</td><td>63.07</td><td>0.21259182969277900</td><td>5.0</td></tr><tr><td>M3</td><td align="right">0.56</td><td align="center">0.31</td><td>1.57</td><td>62.87</td><td>0.4078456776130520</td><td>4.0</td></tr><tr><td>M4</td><td align="right">0.82</td><td align="center">0.67</td><td>2.68</td><td>70.19</td><td>0.5191532395007470</td><td>3.0</td></tr><tr><td>M5</td><td align="right">0.75</td><td align="center">0.56</td><td>1.3</td><td>80.39</td><td>0.8282665851935810</td><td>1.0</td></tr></tbody></table>

Here the ranks are given as rank 1 is the best solution according to the weights and impacts given and rank 5 is the worst solution.

* * *
