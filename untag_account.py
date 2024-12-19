import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import configparser
import sys

# Check if the script is run with the correct number of arguments
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <path_to_tags.json>")
    exit(1)

# Get the path to the JSON file from the command-line argument
untag_file = sys.argv[1]

# Load the untag.json file
try:
    with open(untag_file, 'r') as f:
        account_tags = json.load(f)
except FileNotFoundError:
    print(f"Error: The configuration file '{untag_file}' was not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: The configuration file '{untag_file}' is not a valid JSON.")
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

# Validate the keys in untag.json against the keys in config.ini
required_keys_set = set(k.lower() for k in required_keys.keys())  # Convert config.ini keys to lowercase
for account_id, tag_keys in account_tags.items():
    tag_keys_set = set(k.lower() for k in tag_keys)  # Convert untag.json keys to lowercase
    invalid_keys = tag_keys_set - required_keys_set
    if invalid_keys:
        print(f"Error: The following keys in account {account_id} are not valid according to 'config.ini': {', '.join(invalid_keys)}")
        exit(1)

# Initialize a session using Amazon Organizations
client = boto3.client('organizations')

# Function to untag an account
def untag_account(account_id, tag_keys):
    try:
        print(f"Untagging account: {account_id} with tags: {tag_keys}")
        client.untag_resource(
            ResourceId=account_id,
            TagKeys=tag_keys
        )
    except (BotoCoreError, ClientError) as error:
        print(f"Error untagging account {account_id}: {error}")

# Iterate over each account in the configuration file and remove tags
for account_id, tag_keys in account_tags.items():
    untag_account(account_id, tag_keys)
