# TOPSIS-Akriti-101803608

A python package which implements TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) which is a multi-criteria decision analysis method.

Steps involved in TOPSIS Algorithm:
    
    1. Creating an evaluation matrix (m x n).
    2. Normalization of the matrix so formed such that each metric for a given model lies between 0 and 1.
    3. Creating a weighted normalized matrix i.e. multiplying the metrics with the weights of respective model.
    4. Determining the ideal best and ideal worst alternatives for each criterion.
    5. Calculating the euclidean distance between the target alternative and ideal best and idealworst alternatives.
    6. Calculate the TOPSIS score i.e. similarity to the ideal worst alternative.
    7. Rank the models on the basis of the TOPSIS score thus obtained.s

# Usage

Running the following query on the command-line interface will help you to rank the models i.e. choose the best alternative available from a given set of models based on multiple, usually conflicting criteria.
  
    TOPSIS-Akriti-101803608 <data_file_name> <weights> <impacts> <result_file_name>
    Example - TOPSIS-Akriti-101803608 data.csv "1,1,1,2" "+,+,-,+" result.csv

Note - Make sure that you run the command in the folder you have stored your data files , else provide the complete path of the file.
