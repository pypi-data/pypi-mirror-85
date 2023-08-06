#Importing the libraries
import sys
import os
import logging
import pandas as pd
import math as m

weights = []
impacts = []
ideal_best = []
ideal_worst = []
column_names = []

#Normalise the dataset values by dividing each value of a column with the root of the sum of squared values of the given column
def vector_normalise(dataset):
    
    for col in range(len(column_names)):
        distance = 0
        for i in range(len(dataset)):
            distance += dataset.iloc[i][col] ** 2
        sq_root = m.sqrt(distance)
        dataset[column_names[col]] /= sq_root
    return dataset

#Find the weighted dataset by multiplying each value of the given dataset with respective column weights
def weighted_matrix(dataset):

    for k in range(len(weights)):
        dataset[column_names[k]] *= weights[k]
    return(dataset)

#Find the ideal best and ideal worst values of a given column based on the impact values
def ideal_values(dataset):

    for i in range(len(column_names)):
        if impacts[i] == '+':
            ideal_best.append(max(dataset[column_names[i]]))
            ideal_worst.append(min(dataset[column_names[i]]))
        else:
            ideal_best.append(min(dataset[column_names[i]]))
            ideal_worst.append(max(dataset[column_names[i]]))

#Calculate the performance score i.e. the topsis score for each model by finding the euclidean
#distance between a given model values and the ideal best and the ideal worst vectors
def performance_score(dataset, original_db):

    s1, s2 = [], []
    for i in range(len(dataset)):
        d1 = 0
        d2 = 0
        for j in range(len(column_names)):
            d1 += (dataset.iloc[i][j] - ideal_best[j])**2
            d2 += (dataset.iloc[i][j] - ideal_worst[j])**2
        s1.append(m.sqrt(d1))
        s2.append(m.sqrt(d2))
    original_db['Topsis Score'] = pd.Series(s2)/(pd.Series(s1) + pd.Series(s2))
    return original_db

def main():
    global column_names
    global weights
    global impacts

    #Checking whether the command line arguments are as per our requirement
    if len(sys.argv) != 5:
        logging.exception("Wrong number of parameters.")
        logging.exception("5 parameters are required.")
        logging.exception("format: python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        logging.exception("example: python topsis.py inputfile.csv “1,1,1,2” “+,+,-,+” result.csv ")
        exit(0)

    #Extracting the filename from command line argument
    path_name_data = sys.argv[1]
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, path_name_data)

    #Exception handling for the existence of the given file
    if not os.path.exists(filename):
        logging.exception("Error !! %s file Not Found"%(path_name_data))

    #Exception handling for the number of columns in dataset and the columns from 2nd contain numeric values
    df = pd.read_csv(filename)
    df1 = df.drop(['Model'], axis=1)
    column_names = list(df1.columns)
    if len(df.columns) < 3:
        logging.exception("The number of columns in the input dataset do not meet the requirements!")
    else:
        colList = df.apply(lambda x: pd.to_numeric(x, errors='coerce').notnull().all())
        for i in range(1,len(column_names)):
            if colList[i]:
                pass
            else:
                logging.exception("Error!! %s column contains non-numeric values"%column_names[i-1])

    #Exception handling for the number of weights and impacts
    for i in range(0,len(sys.argv[2])-1,2):
        if sys.argv[2][i+1] != ',':
            logging.exception("Weights are not separated by ','.")

    for i in range(0,len(sys.argv[3])-1,2):
        if sys.argv[3][i+1] != ',':
            logging.exception("Impacts are not separated by ','.")

    weights = list(sys.argv[2].split(','))
    weights = [int(i) for i in weights]
    impacts = list(sys.argv[3].split(','))
    if (len(weights) != len(column_names)) or (len(impacts) != len(column_names) or (len(weights) != len(impacts))):
        logging.exception("The number of weights or impacts provided do not meet the requirements.")
    
    #Exception handling for the value of impacts provided
    for x in impacts:
        if (x!='+') and (x!='-'):
            logging.exception("The value of the impacts provided should be either '+' or '-'.")

    #Path of the result file
    path_name_result = sys.argv[4]
    df1 = vector_normalise(df1)                                #Normalise the values of the dataframe
    df1 = weighted_matrix(df1)                                 #Find the weighted matrix for the given dataframe
    ideal_values(df1)                                          #Find the ideal best and ideal worst values for the given models
    df = performance_score(df1, df)                            #Find the topsis score of each model
    df['Rank'] = df['Topsis Score'].rank(ascending=False)      #Rank the models based on the topsis score
    df.to_csv(path_name_result, index=False)                   #Save the resulting dataframe into a csv file with the name as provided in the arguments

if __name__ == "__main__":
    main()
