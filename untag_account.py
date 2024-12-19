import boto3
from configparser import ConfigParser
from botocore.exceptions import BotoCoreError, ClientError

# Load the untagging configuration file
config = ConfigParser()
try:
    config.read('untag_config.ini')  # Use the untagging-specific config file
    if not config.sections():
        raise FileNotFoundError("The configuration file 'untag_config.ini' is empty or not properly formatted.")
except FileNotFoundError:
    print("Error: The configuration file 'untag_config.ini' was not found or is empty.")
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
for account_id in config.sections():
    # Get the tag keys for the current account
    tag_keys = config.get(account_id, 'tags').split(',')  # Split the comma-separated list into a Python list
    tag_keys = [key.strip() for key in tag_keys]  # Remove any extra whitespace
    untag_account(account_id, tag_keys)
