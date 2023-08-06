# TOPSIS Package in Python

Submitted by: Satyam Verma

Roll no: 101803324

UCS538

---

## TOPSIS

TOPSIS is an acronym that stands for ‘Technique of Order Preference Similarity to the Ideal Solution’ and is a pretty straightforward MCDA method. As the name implies, the method is based on finding an ideal and an anti-ideal solution and comparing the distance of each one of the alternatives to those.

---

## How to use

The package Topsis-Satyam-101803324 can be run though the command line as follows:

```
>> pip install Topsis-Satyam-101803324
```

```
>>topsis data.csv "1,1,1,1" "+,+,-,+" result.csv
```

## Sample Input

The decision matrix should be constructed with each row representing a Model alternative, and each column representing a criterion like Accuracy, R2, Root Mean Squared Error, Correlation, and many more.

<table><thead><tr><th>Model</th><th>Correlation</th><th>R2</th><th>RMSE</th><th>Accuracy</th></tr></thead><tbody><tr><td>M1</td><td>0.79</td><td>0.62</td><td>1.25</td><td>60.89</td></tr><tr><td>M2</td><td>0.66</td><td>0.44</td><td>2.89</td><td>63.07</td></tr><tr><td>M3</td><td>0.56</td><td>0.31</td><td>1.57</td><td>62.87</td></tr><tr><td>M4</td><td>0.82</td><td>0.67</td><td>2.68</td><td>70.19</td></tr><tr><td>M5</td><td>0.75</td><td>0.56</td><td>1.3</td><td>80.39</td></tr></tbody></table>

<br>
Weights `weights` is not already normalised will be normalised later in the code.

Information of benefit positive(+) or negative(-) impact criteria should be provided in `impacts`.
<br>

## Output of this sample input

The output that will be generated from the following input data will be:

<table><thead><tr><th>Model</th><th align="right">Correlation</th><th align="center">R2</th><th>RMSE</th><th>Accuracy</th><th>Topsis Score</th><th>Rank</th></tr></thead><tbody><tr><td>M1</td><td align="right">0.79</td><td align="center">0.62</td><td>1.25</td><td>60.89</td><td>0.7722097345612788</td><td>2.0</td></tr><tr><td>M2</td><td align="right">0.66</td><td align="center">0.44</td><td>2.89</td><td>63.07</td><td>0.22559875426413367</td><td>5.0</td></tr><tr><td>M3</td><td align="right">0.56</td><td align="center">0.31</td><td>1.57</td><td>62.87</td><td>0.43889731728018605</td><td>4.0</td></tr><tr><td>M4</td><td align="right">0.82</td><td align="center">0.67</td><td>2.68</td><td>70.19</td><td>0.5238778712729114</td><td>3.0</td></tr><tr><td>M5</td><td align="right">0.75</td><td align="center">0.56</td><td>1.3</td><td>80.39</td><td>0.8113887082429979</td><td>1.0</td></tr></tbody></table>

<br>
The output file contains columns of input file along with two additional columns having **Topsis_score** and **Rank** .
Here the ranks are given as rank 1 is the best solution according to the weights and impacts given and rank 5 is the worst solution.

---
