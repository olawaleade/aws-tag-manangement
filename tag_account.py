import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import sys
import configparser

# Check if the script is run with the correct number of arguments
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <path_to_tags.json>")
    exit(1)

# Get the path to the JSON file from the command-line argument
tags_file = sys.argv[1]

# Load the configuration file
try:
    with open(tags_file, 'r') as f:
        account_tags = json.load(f)
except FileNotFoundError:
    print(f"Error: The configuration file '{tags_file}' was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The configuration file '{tags_file}' is not a valid JSON.")
    exit(1)

# Load the config.ini file
config = configparser.ConfigParser()
try:
    config.read('config.ini')
    required_keys = config['Tags']
except KeyError:
    print("Error: The 'Tags' section is missing in the 'config.ini' file.")
    exit(1)
except FileNotFoundError:
    print("Error: The 'config.ini' file was not found.")
    exit(1)

# Validate the keys in tags.json against the keys in config.ini
required_keys_set = set(k.lower() for k in required_keys.keys())  # Convert config.ini keys to lowercase
for account_id, tags in account_tags.items():
    tag_keys_set = set(k.lower() for k in tags.keys())  # Convert tag.json keys to lowercase
    missing_keys = required_keys_set - tag_keys_set
    if missing_keys:
        print(f"Error: The following required keys are missing in account {account_id}: {', '.join(missing_keys)}")
        exit(1)
    
# Initialize a session using Amazon Organizations
client = boto3.client('organizations')

# Function to tag an account
def tag_account(account_id, tags):
    tag_list = [{'Key': k, 'Value': v} for k, v in tags.items()]
    try:
        print(f"Tagging account: {account_id} with tags: {tags}")
        client.tag_resource(
            ResourceId=account_id,
            Tags=tag_list
        )
    except (BotoCoreError, ClientError) as error:
        print(f"Error tagging account {account_id}: {error}")

# Iterate over each account in the configuration file and apply tags
for account_id, tags in account_tags.items():
    tag_account(account_id, tags)
