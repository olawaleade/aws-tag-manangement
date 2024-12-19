import boto3
from configparser import ConfigParser
from botocore.exceptions import BotoCoreError, ClientError

# Load the configuration file
config = ConfigParser()
try:
    config.read('tag_config.ini')
    if not config.sections():
        raise FileNotFoundError("The configuration file 'tag_config.ini' is empty or not properly formatted.")
except FileNotFoundError:
    print("Error: The configuration file 'tag_config.ini' was not found or is empty.")
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
for account_id in config.sections():
    # Get the tags for the current account
    tags = dict(config.items(account_id))
    tag_account(account_id, tags)
