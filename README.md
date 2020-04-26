# Overview
This is to demonstrate how to use DynamoDB stream with Lambda to synchronize data change between China region & Global region which were isolated with no Global Table support.
This is for demo purpose only, you should consider using SQS to decouple from the Lambda to DynamoDB.

![image](https://github.com/totorochina/ddb-sync-lambda/blob/master/img/dynamodb_table_sync.png)


## Step by step guide
### Prepare IAM account/Role and AK/SK for both sites.
For the target site, your AK/SK should have privilege to write to target DynamoDB table.
### Create source & target DynamoDB table.
You may have to use --profile to distinguish different accounts for China & Global region.
#### Source,
```bash
aws dynamodb create-table \
    --table-name MusicCollection \
    --attribute-definitions AttributeName=Artist,AttributeType=S AttributeName=SongTitle,AttributeType=S \
    --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```
#### For the source table, enable DynamoDB stream.
```bash
aws dynamodb update-table --table-name MusicCollection \
--stream-specification "StreamEnabled=True,StreamViewType=NEW_IMAGE"
```
#### Target,
```bash
aws dynamodb create-table \
    --table-name MusicCollection \
    --attribute-definitions AttributeName=Artist,AttributeType=S AttributeName=SongTitle,AttributeType=S \
    --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```
#### Create System Manager parameter entries for target table.
```bash
aws ssm put-parameter --name "target_ak" --value "<TARGET_ACCOUNT_AK>" --type SecureString
aws ssm put-parameter --name "target_sk" --value "<TARGET_ACCOUNT_SK>" --type SecureString
```

#### Create IAM role for Lambda with access to System Manager parameter entries
With Managed Priviliege AWSLambdaBasicExecutionRole, AmazonSSMReadOnlyAccess, and take down its ARN


#### Create Lambda function and subscribe to DynamoDB stream.
##### Zip
```bash
zip function.zip index.py
```
##### Create function
```bash
aws lambda create-function --function-name ddb-lambda-sync \
--zip-file fileb://function.zip --handler index.handler --runtime python3.7 \
--role <YOUR_ROLE_FOR_LAMBDA_FUNCTION>
```
##### Publish function
```bash
aws lambda publish-version --function-name "ddb-lambda-sync"
```
##### Mapping function with event source of DynamoDB stream
```bash
aws lambda create-event-source-mapping \
    --function-name ddb-lambda-sync \
    --event-source-arn <ARN_OF_YOUR_DYNAMODB_STREAM> --starting-position LATEST
```

#### Test create an entry in source table.
```bash
aws dynamodb put-item \
    --table-name MusicCollection \
    --item file://item.json
```
#### Check the data in the target table.
```bash
aws dynamodb get-item \
    --table-name MusicCollection \
    --key file://key.json --profile zhy
```
## Limitations
Do not support migrating existing data in the table, only new changed data.

## To do
CDK + SQS

## License
This library is licensed under the MIT-0 License. See the LICENSE file.
