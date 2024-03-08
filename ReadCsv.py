import pandas as pd
import csv
import random
import copy
import os




# path to the CSV files with participant data
csv_path= "Coffee Partner Lottery participants.csv"
DELIMITER=','
# load all previous pairings (to avoid redundancies)
if os.path.exists(csv_path):
    with open(csv_path, "r") as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            print(row)
csvreader = csv.reader(csv_path, delimiter=',')

df = pd.read_csv(csv_path)
print(df)
print(len(df))
lendf = len(df)

def inputGroupSize(lendf):
    groupSize = 0
    groupSize = input('how much do you want your groupsize to be(between 2 and 8)')
    print(groupSize)
    try:
        groupSize= int(groupSize)
    except ValueError:
        print('input was not a number')
        inputGroupSize(lendf)
    if groupSize > 8:
        print('Choose a smaller groupsize')
        inputGroupSize(lendf)
    if groupSize > lendf:
        print('There are not enough participants, choose a groupsize smaller')
        inputGroupSize(lendf)
    
    return groupSize
#loading csv data into dataframe

inputGroupSize(lendf)


