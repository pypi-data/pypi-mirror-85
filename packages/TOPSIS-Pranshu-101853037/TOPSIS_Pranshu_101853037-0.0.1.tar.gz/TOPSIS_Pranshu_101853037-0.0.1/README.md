### TOPSIS
# It is a method of compensatory aggregation that compares a set of alternatives by identifying weights for each criterion, normalising scores for each criterion and calculating the geometric distance between each alternative and the ideal alternative, which is the best score in each criterion.

Installation
>>pip install TOPSIS_Pranshu_101853037

How to run in command prompt

>>from TOPSIS_Pranshu_101853037.topsis import topsis

>>topsis("data.csv","1,1,1,2","+,+,-,+","result.csv")

Input File (data.csv)
Input file contain three or more columns
First column is the object/variable name (e.g. M1, M2, M3, M4,...)
From 2nd to last columns contain numeric values only
Output File (result.csv)
Result file contains all the columns of input file and two additional columns having TOPSIS SCORE and RANK

License
MIT
