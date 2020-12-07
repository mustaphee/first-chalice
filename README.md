# first-chalice
This is a test run on AWS Chalice project

https://hq3g4cexoi.execute-api.eu-west-2.amazonaws.com/api/

This creates a directory using the hypothetical `platform_name`  and stores in
an in-memory db. With the platform name, you can now generate a direct upload 
policy link from the client side.

## Setup
- Clone this project 
- Create a virtualenvironment
- Install the requirements.txt
- Add your BUCKET_ID to the enironment variable
- Setup your AWS credentials
- Deploy

## Test
Just run 
```pytest tests

