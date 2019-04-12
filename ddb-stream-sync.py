from __future__ import print_function

import json
import boto3
import traceback

ddb = boto3.client('dynamodb', region_name = 'cn-northwest-1')

#print('Loading function')

event_delete = {
"Records": [
{
"eventID": "9bc813d4c24bcc307147ac25a170b44d",
"eventVersion": "1.1",
"dynamodb": {
"Keys": {
"recordId": {
"N": "0"
}
},
"ApproximateCreationDateTime": 1542016080.0,
"StreamViewType": "NEW_IMAGE",
"SequenceNumber": "4795000000000000599541765",
"SizeBytes": 9
},
"awsRegion": "cn-north-1",
"eventName": "REMOVE",
"eventSourceARN": "arn:aws-cn:dynamodb:cn-north-1:741251161495:table/ddb_stream_test/stream/2018-11-11T09:16:30.755",
"eventSource": "aws:dynamodb"
}
]
}

event_insert = {
"Records": [
{
"eventID": "880dff58ebad9ab4b164ba6d63e96d92",
"eventVersion": "1.1",
"dynamodb": {
"SequenceNumber": "3270900000000001940388956",
"Keys": {
"recordId": {
"N": "3"
}
},
"SizeBytes": 70,
"NewImage": {
"name": {
"S": "ccc"
},
"gold": {
"N": "110"
},
"level": {
"N": "3"
},
"recordId": {
"N": "3"
},
"timestamp": {
"N": "1541990916"
},
"role": {
"S": "freelancer"
}
},
"ApproximateCreationDateTime": 1541990940.0,
"StreamViewType": "NEW_IMAGE"
},
"awsRegion": "cn-north-1",
"eventName": "INSERT",
"eventSourceARN": "arn:aws-cn:dynamodb:cn-north-1:741251161495:table/ddb_stream_test/stream/2018-11-11T09:16:30.755",
"eventSource": "aws:dynamodb"
}
]
}

event = event_insert

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
            else:
                print(response)

    return 'Successfully processed {} records.'.format(len(event['Records']))

if __name__ == "__main__":
    context = None
    print(lambda_handler(event, context))
