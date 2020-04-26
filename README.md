# Overview
This is to demonstrate how to use DynamoDB stream with Lambda to synchronize data change between China region & Global region which were isolated with no Global Table support.
This is for demo purpose only, you should consider using SQS to decouple from the Lambda to DynamoDB.

![image](https://github.com/totorochina/ddb-sync-lambda/blob/master/img/dynamodb_table_sync.png)


## Step by step guide
### Prepare IAM account/Role and AK/SK for both sites.
For the target site, your AK/SK should have privilege to write to target DynamoDB table.
### Create source & target DynamoDB table.
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

#### Create Lambda function and subscribe to DynamoDB stream.

#### Test create an entry in source table.

#### Check the data in the target table.

## Limitations
Do not support migrating existing data in the table, only new changed data.

## To do
CDK + SQS

## License
This library is licensed under the MIT-0 License. See the LICENSE file.
