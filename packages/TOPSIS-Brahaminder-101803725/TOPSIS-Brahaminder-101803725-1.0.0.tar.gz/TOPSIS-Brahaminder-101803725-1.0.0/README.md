# About Topsis
TOPSIS stands for Technique for Oder Preference by Similarity to Ideal Solution. It is a method of compensatory aggregation that compares a set of alternatives by identifying weights for each criterion, normalising scores for each criterion and calculating the geometric distance between each alternative and the ideal alternative, which is the best score in each criterion. An assumption of TOPSIS is that the criteria are monotonically increasing or decreasing. In this Python package Vector Normalization has been implemented.


## Installation
```pip install TOPSIS-Brahaminder-101803725```

## How to use it
Open terminal and type following query
```python topsis input_filename.csv "w1,w2,w3,w4" "i1,i2,i3,i4" result.csv```
 w1,w2,w3,w,4 represent weights and i1,i2,i3,i4 represents impacts.w1,w2,w3,w4 can be float/integer form while i1,i2,i3,i4 can be either '+' or '-'
Rank 1 in the result.csv file will denote the best decision

## License

© 2020 Brahaminder Garg

This repository is licensed uder the MIT license.
See LICENSE for details.