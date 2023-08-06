# What is TOPSIS module all about ?
Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) originated in the 1981 by Hwang and Yoon as a multi-criteria decision making method.
It is a method of compensatory aggregation that compares a set of alternatives by identifying weights for each criterion, normalising scores for each criterion and calculating the geometric distance between each alternative and the ideal alternative, which is the best score in each criterion.TOPSIS chooses the alternative of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.

This is a package to find topsis score and rank of a dataframe with only numerical values.

## Installation
```pip install TOPSIS-Karan-101853003```

## How to use it ?
Open terminal and move into directory where all your files are placed and the type :
    python topsis.py "input.csv" "1,1,1,2" "+,+,+,-" "result.csv"

## License 
© 2020 Karan Madan
This repository is licensed under the MIT license.See License for details.