#Chatarchiver Lambda Function (Python 3.14):

import json
import boto3

table = boto3.resource('dynamodb').Table('ChatHistory')

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['body'])
        table.put_item(Item={
            'messageId': payload['messageId'],
            'timestamp': payload['timestamp'],
            'username': payload['username'],
            'message': payload['content']
        })
    return {'statusCode': 200}