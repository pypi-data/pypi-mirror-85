# TOPSIS_101866010

By: Pranav Anand-101866010

**Title:Multiple Criteria Decision Making using TOPSIS**

### What is TOPSIS:
TOPSIS is an acronym that stands for 'Technique of Order Preference Similarity to the Ideal Solution' and is a pretty straightforward MCDA method. It is a multi-criteria decision analysis method, which was originally developed by Ching-Lai Hwang and Yoon in 1981 with further developments by Yoon in 1987, and Hwang, Lai and Liu in 1993.

### How to install the TOPSIS package

pip install TOPSIS_101866010

### For Calculating the TOPSIS Score

Topsis data.csv "0.25,0.25,0.25,0.25" "-,+,+,+" result.csv

### Input File(Example:data.csv):
Argument used to pass the path of the input file which conatins a dataset having different fields and to perform the topsis mathematical operations

### Weights(Example:"0.25,0.25,0.25,0.25")
The weights to assigned to the different parameters in the dataset should be passed in the argument.It must be seperated by ','.

### Impacts(Example:"-,+,+,+"):
The impacts are passed to consider which parameters have a positive impact on the decision and which one have the negative impact.Only '+' and '-' values should be passed and should be seperated with ',' only

### Output File(Example:result.csv):
This argument is used to pass the path of the result file where we want the rank and score to be stored
