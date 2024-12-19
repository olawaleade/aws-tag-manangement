import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Load the configuration file
try:
    with open('untags.json', 'r') as f:
        tags = json.load(f)
except FileNotFoundError:
    print("Error: The configuration file 'untags.json' was not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error: The configuration file 'untags.json' is not a valid JSON.")
    exit(1)

# Initialize a session using Amazon Organizations
client = boto3.client('organizations')

# Function to tag an account
def untag_account(account_id, tag_keys):
    tag_list = [{'Key': k, 'Value': v} for k, v in tags.items()]
    try:
        print(f"Untagging account: {account_id} with tags: {tag_keys}")
        client.untag_resource(
            ResourceId=account_id,
            TagKeys=tag_keys
        )
    except (BotoCoreError, ClientError) as error:
        print(f"Error untagging account {account_id}: {error}")

# Iterate over each account in the configuration file and apply tags
for account_id, tag_keys in tags.items():
    untag_account(account_id, tag_keys)
