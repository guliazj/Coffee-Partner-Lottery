import pandas as pd
import csv
import random
import os

# Define paths and headers for files
participants_csv = "participants.csv"
header_name = "Your name:"
header_email = "Your e-mail:"
conversation_starters_csv = "conversationstarters.csv"
messages_path = "Coffee Partner Lottery messages"
group_size = 2

# Function to load conversation starters from a CSV file
def load_conversation_starters(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        return [row["conversation starter:"] for row in csv.DictReader(file)]

# Function to load participants from a CSV file
def load_participants(filename):
    formdata = pd.read_csv(filename, sep=',')
    return list(set(formdata[header_email])), formdata

# Function to generate groups of participants
def generate_groups(participants, size):
    random.shuffle(participants)
    # Initially form groups based on the desired size
    groups = [participants[i:i + size] for i in range(0, len(participants), size)]
    
    # If the last group has only one participant, redistribute that participant
    if len(groups) > 1 and len(groups[-1]) == 1:
        # Take the last participant and try to fit them into an existing group without exceeding size + 1
        lone_participant = groups.pop()
        for group in groups[:-1]:  # Avoid modifying the second to last group initially
            if len(group) < size:
                group.extend(lone_participant)
                break
        else:
            # If all other groups are at max size, add to the second to last group, slightly exceeding the desired size
            groups[-1].extend(lone_participant)
    return groups

# Function to generate and save messages for each group, including a conversation starter

def generate_and_save_messages(groups, formdata, starters, output_path):
    starter = random.choice(starters)
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        for i, group in enumerate(groups, 1):
            names = ' & '.join([formdata[formdata[header_email] == email].iloc[0][header_name] for email in group])
            message = f"Hello {names},\n\nYou've been matched for this round of the Coffee Partner Lottery.\n\n" f"Conversation Starter: {starter}\n\nEnjoy your conversation!"
            file_path = os.path.join(output_path, f"group_{i}.txt")
            with open(file_path, "w", encoding='utf-8') as file:
                file.write(message)
            print(f"Message saved to: {file_path}")
    except Exception as e:
        print(f"Error saving messages: {e}")

# Load conversation starters and participants
conversation_starters = load_conversation_starters(conversation_starters_csv)
participants, formdata = load_participants(participants_csv)

# Generate groups and messages
groups = generate_groups(participants, group_size)
generate_and_save_messages(groups, formdata, conversation_starters, messages_path)

# Note: Direct execution of group generation and message saving in this script. Adjust paths as needed.