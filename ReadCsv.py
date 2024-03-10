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

#loading csv data into dataframe

def input_group_size(len_df):
    while True:  # Loop until valid input is received
        try:
            group_size = int(input('Enter your desired group size (between 2 and 8): '))
            print(group_size)  # Echo the input back to the user
            
            if group_size < 2:
                print('Group size too small. Please choose a number between 2 and 8.')
            elif group_size > 8:
                print('Group size too large. Please choose a number between 2 and 8.')
            elif group_size > len_df:
                print(f'There are not enough participants. Choose a group size smaller than or equal to {len_df}.')
            else:
                return group_size  # Valid input; return the group size
            
        except ValueError:  # Catch non-integer inputs
            print('Input was not a number. Please enter a valid integer between 2 and 8.')

inputGroupSize(lendf)


