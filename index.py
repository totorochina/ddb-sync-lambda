from __future__ import print_function

import json
import boto3
import traceback

ddb = boto3.client('dynamodb', region_name = 'cn-northwest-1')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    for record in event['Records']:
        print("eventID " + record['eventID'])
        print("eventName " + record['eventName'])
        #print("DynamoDB Record: " + json.dumps(record['dynamodb'], indent=2))
        #print("DynamoDB Record: " + json.dumps(record['dynamodb'], indent=2))
        #print("New Image: " + json.dumps(record['dynamodb']['NewImage']))
        #print(record['dynamodb']['Keys'])
        if record['eventName'] == 'INSERT' or record['eventName'] == 'MODIFY':
            try:
                response = ddb.put_item(
                    TableName = 'ddb_stream_test_zhy',
                    Item = record['dynamodb']['NewImage']
                )
            except Exception:
                print("cannot put_item to ddb")
                #traceback.print_exc()
                print(traceback.format_exc())
                return False
            else:
                print(response)

        if record['eventName'] == 'REMOVE':
            try:
                response = ddb.delete_item(
                    TableName = 'ddb_stream_test_zhy',
                    Key = record['dynamodb']['Keys']
                )
            except Exception:
                print("cannot delete_item to ddb")
                print(traceback.format_exc())
                return False
            else:
                print(response)

    return 'Successfully processed {} records.'.format(len(event['Records']))
