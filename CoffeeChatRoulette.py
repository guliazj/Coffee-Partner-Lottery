import pandas as pd
import csv
import random
import os

# Define paths and headers for files
participants_csv = "participants.csv"
header_name = "Your name:"
header_email = "Your e-mail:"
conversation_starters_csv = "conversationstarters.csv"
messages_path = "Coffee Chat Roulette messages"
feedback_csv = "feedback.csv"  # Path to store feedback data


# Function to load conversation starters from a CSV file
def load_conversation_starters(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        return [row["conversation starter:"] for row in csv.DictReader(file)]

# Function to load participants from a CSV file
def load_participants(filename):
    formdata = pd.read_csv(filename, sep=',')
    return list(set(formdata[header_email])), formdata

# Function to input group size
def input_group_size(len_df):
    #loop until a valid input is received
    while True:  
        try:
            group_size = int(input('Enter your desired group size (between 2 and 8): '))
            #print to the user
            print(group_size)  
            
            if group_size < 2:
                print('Group size too small. Please choose a number between 2 and 8.')
            elif group_size > 8:
                print('Group size too large. Please choose a number between 2 and 8.')
            elif group_size > len_df:
                print(f'There are not enough participants. Choose a group size smaller than or equal to {len_df}.')
            else:
                return group_size  
            # Valid input; return the group size

          # Catch non-integer inputs  
        except ValueError:  
            print('Input was not a number. Please enter a valid integer between 2 and 8.')


# Function to generate groups of participants
def generate_groups(participants):
    len_df = len(participants)
    group_size = input_group_size(len_df)
    random.shuffle(participants)
    # Initially form groups based on the desired size
    groups = [participants[i:i + group_size] for i in range(0, len(participants), group_size)]
    
    # If the last group has only one participant, redistribute that participant
    if len(groups) > 1 and len(groups[-1]) == 1:
        # Take the last participant and try to fit them into an existing group without exceeding size + 1
        lone_participant = groups.pop()
        for group in groups[:-1]:  # Avoid modifying the second to last group initially
            if len(group) < group_size:
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
            message = f"Hello {names},\n\nYou've been matched for this round of the Coffee Chat Roulette.\n\n" f"Conversation Starter: {starter}\n\nEnjoy your conversation!\nPlease send an email and provide feedback for your group.\nYour feedback can be about your group members and the overall experience."
            file_path = os.path.join(output_path, f"group_{i}.txt")
            with open(file_path, "w", encoding='utf-8') as file:
                file.write(message)
            print(f"Message saved to: {file_path}")
    except Exception as e:
        print(f"Error saving messages: {e}")
        
# Function to collect feedback for a specific group
def collect_feedback(group, formdata):
    feedback_data = []
    for email in group:
        feedback = input(f"Please provide feedback for the coffee meeting group with {formdata[formdata[header_email] == email].iloc[0][header_name]}: ")
        feedback_data.append({"Email": email, "Feedback": feedback})
    return feedback_data

# Function to save feedback data to a CSV file
def save_feedback(feedback_data, output_path):
    try:
        with open(output_path, "w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Email", "Feedback"])
            writer.writeheader()
            writer.writerows(feedback_data)
        print(f"Feedback data saved to: {output_path}")
    except Exception as e:
        print(f"Error saving feedback data: {e}")
        
# Function to ask for feedback and save it
def ask_and_save_feedback():
    # Ask if the user wants to provide feedback
    leave_feedback = input("Do you want to leave feedback for the coffee meetings? (yes/no): ").lower()
    if leave_feedback == "yes":
        # Check if all meetings are done
        all_meetings_done = input("Are all meetings done? (yes/no): ").lower()
        while all_meetings_done != "yes":
            wait_for_meetings = input("Meetings are not done yet. Do you want to wait? (yes/no): ").lower()
            if wait_for_meetings == "no":
                print("Exiting program.")
                return
            all_meetings_done = input("Are all meetings done now? (yes/no): ").lower()
        
        # Check if feedback has been received
        feedback_received = input("Have you received any emails with feedback on the groups? (yes/no): ").lower()
        if feedback_received == "yes":
            # Collect and save feedback for each group
            for group in groups:
                feedback_data = collect_feedback(group, formdata)
                save_feedback(feedback_data, feedback_csv)
        else:
            print("No feedback received. Exiting program.")
    else:
        print("No feedback provided. Exiting program.")

# Load conversation starters and participants
conversation_starters = load_conversation_starters(conversation_starters_csv)
participants, formdata = load_participants(participants_csv)

# Generate groups and messages
groups = generate_groups(participants)
generate_and_save_messages(groups, formdata, conversation_starters, messages_path)

# Call the function to ask for feedback and save it
ask_and_save_feedback()
