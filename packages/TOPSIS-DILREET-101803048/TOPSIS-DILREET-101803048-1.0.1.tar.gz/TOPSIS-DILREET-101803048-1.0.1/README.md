# What is TOPSIS
TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) is one of the numerical methods of the multi-criteria decision making. This is a broadly applicable method with a simple mathematical model.It chooses the alternative of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.

## Steps used in TOPSIS
1)Normalize the given decision data
2)Find weighted normalized
3)Determine positive ideal and negative ideal solution
4)Calculate separation measures
5)Find relative closesness to ideal solution
6)Rank the preference order

##  Sample Data:
Model,Corr,Rseq,RMSE,Accuracy
M1,0.79,0.62,1.25,60.89
M2,0.66,0.44,2.89,63.07
M3,0.56,0.31,1.57,62.87
M4,0.82,0.67,2.68,70.19
M5,0.75,0.56,1.3,80.39

## Output of This Data
1,2,3,4,performance score,rank as per topsis
M1,0.79,0.62,1.25,60.89,0.7722097345612788,2
M2,0.66,0.44,2.89,63.07,0.22559875426413367,5
M3,0.56,0.31,1.57,62.87,0.43889731728018605,4
M4,0.82,0.67,2.68,70.19,0.5238778712729114,3
M5,0.75,0.56,1.3,80.39,0.8113887082429979,1
