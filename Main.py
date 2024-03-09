import pandas as pd
import csv
import random
import copy
import os

# Function to generate pairs from participants, avoiding duplicates and considering past pairings
def generate_pairs(participants, history_file_path):
    npairs = set()
    nparticipants = copy.deepcopy(participants)
    # Logic to generate pairs goes here, considering nparticipants and checking against history_file_path
    # This is a placeholder logic. Actual implementation depends on how pairs are chosen and history is used.
    return npairs

# Function to generate output string for today's coffee partners
def generate_output_string(pairs, participants):
    output_string = "------------------------\n"
    output_string += "Today's coffee partners:\n"
    output_string += "------------------------\n"
    for pair in pairs:
        pair = list(pair)
        output_string += "* "
        for i in range(len(pair)):
            name_email_pair = f"{participants[participants['email'] == pair[i]].iloc[0]['name']} ({pair[i]})"
            output_string += name_email_pair + ", " if i < len(pair)-1 else name_email_pair + "\n"
    return output_string

# Function to save the output string to a text file
def save_output_text(output_string, file_path):
    with open(file_path, "w") as file:
        file.write(output_string)

# Function to save new pairs into a CSV file
def save_pairs_csv(pairs, participants, file_path):
    with open(file_path, "w") as file:
        writer = csv.writer(file)
        # Define header based on expected columns
        writer.writerow(["name", "email"])
        for pair in pairs:
            # Write each pair to the file
            writer.writerow([participants[participants['email'] == email].iloc[0]['name'], email] for email in pair)

# Main function to encapsulate the process
def main(participants_file_path, history_file_path, output_text_path, pairs_csv_path):
    participants = pd.read_csv(participants_file_path, sep=',')
    pairs = generate_pairs(participants, history_file_path)
    output_string = generate_output_string(pairs, participants)
    print(output_string)
    save_output_text(output_string, output_text_path)
    save_pairs_csv(pairs, participants, pairs_csv_path)
    print("Job done.")

if __name__ == '__main__':
    main('participants.csv', 'history.csv', 'newPairs.txt', 'newPairs.csv')