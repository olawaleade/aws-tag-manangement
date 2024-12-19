import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Load the configuration file
try:
    with open('tags.json', 'r') as f:
        tags = json.load(f)
except FileNotFoundError:
    print("Error: The configuration file 'tags.json' was not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error: The configuration file 'tags.json' is not a valid JSON.")
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
for account_id, tags in tags.items():
    tag_account(account_id, tags)
