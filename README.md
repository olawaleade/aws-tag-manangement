# CCoE
A repository for managing policies of each Public Cloud with code

## AWS

### Using AWS CLI for Tagging AWS Organization Member Account
 #### Reference
 https://docs.aws.amazon.com/organizations/latest/userguide/add-tag.html

 #### There is limitation to using CLI for tagging is that it can only tag a single member account at once

- To add or update tags to an existing resource
  ```
   aws organizations tag-resource --resource-id <account_id> --tags Key=SERVICE_NAME,Value="abc" Key=SERVICE_ID,Value="123345" Key=BILLCODETYPE,Value="BEKEY" Key=L2,Value="org1234" Key=BILLCODE,Value="12334455" Key=COMPANY_SEGMENT,Value="hq" Key=ENVIRONMENT,Value="production"

  ```
  
- To Untag existing resource
  ```
   aws organizations untag-resource --resource-id <account_id> --tag-keys Key1 Key2

  ```


### Using AWS SDK for Tagging AWS Organization Member Account
 #### Reference
 https://docs.aws.amazon.com/organizations/latest/APIReference/API_TagResource.html

 #### The Advantage of using SDK for tagging is that it can be used to tag multiple member accounts at once

## To Run on the Repo locally for Testing Purpose
 #### Reference
 https://docs.aws.amazon.com/organizations/latest/APIReference/API_TagResource.html
 
1. Clone the Repository to local machine
2. Install the dependencies
    - pip install boto3
3. Set AWS credential that has permission on Organization
    - export AWS_PROFILE=admin (with necessary permissions)


### Commands to use

1. To add or update tags to member accounts
  
  - Run this command
    ```
     python3 tag_account.py arg1
     for example python3 tag_account.py tag.json

    ```

2. To Untag existing resource
  
  - Run this command
    ```
     python3 untag_account.py arg2
     for example python3 untag_account.py untag.json
    ```

## Points to Note
- The Config.ini file consist of the Tag Keys, which are validated against the tag inputs
- Note that the arg1 and arg2 are the tags json file defined which is given as input which running the command.
- 