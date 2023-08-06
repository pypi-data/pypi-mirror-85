
Project Description
-------------
TOPSIS implementation for Multi Criteria Decision Making(MCDM)

The Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS) is a multi-criteria decision analysis method, which is based on the concept that the chosen alternative should have the shortest geometric distance from the positive ideal solution (PIS)[4] and the longest geometric distance from the negative ideal solution (NIS).

The package (TOPSIS_PANKAJ_10180332) contains the python script topsis.py and it further contains the function topsis_score which has to given 4 parameters -

1. Name of input .csv file.
2. Weights of all the attributes in the form of list.
3. Impact of all the parameters(either '+' or '-') in form of list.
4. Name of output .csv file.

Note - All the column entries should be numeric only.

Example code :

import TOPSIS_PANKAJ_101803352.topsis as top

top.topsis_score('inputFile.csv', [1,1,1,1], ['+','+','-','+',],'outputFile.csv')