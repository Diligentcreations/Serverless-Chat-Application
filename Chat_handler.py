#Chathandler Lambda Function (Python 3.14):
 

import json, boto3, os, time

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')
ACTIVE_TABLE = os.environ['ACTIVE_TABLE']
SQS_URL = os.environ['SQS_QUEUE_URL']

def get_apigw_client(domain, stage):
    endpoint = f"https://{domain}/{stage}"
    return boto3.client('apigatewaymanagementapi', endpoint_url=endpoint)

def lambda_handler(event, context):
    ctx = event['requestContext']
    cid = ctx['connectionId']
    route = ctx['routeKey']
    table = dynamodb.Table(ACTIVE_TABLE)
    apigw = get_apigw_client(ctx['domainName'], ctx['stage'])

    if route == '$connect':
        table.put_item(Item={'connectionId': cid, 'username': 'Anonymous'})
        return {'statusCode': 200}

    elif route == '$disconnect':
        user_item = table.get_item(Key={'connectionId': cid})
        user = user_item.get('Item', {}).get('username', 'Unknown')
        if user != 'Anonymous':
            broadcast(table, apigw, "System", f"{user} left the chat.")
        table.delete_item(Key={'connectionId': cid})
        return {'statusCode': 200}

    body = json.loads(event.get('body', '{}'))
    action = body.get('action')

    if action == 'setName':
        name = body.get('name', 'Unknown')
        table.update_item(
            Key={'connectionId': cid},
            UpdateExpression="set username = :u",
            ExpressionAttributeValues={':u': name}
        )
        broadcast(table, apigw, "System", f"{name} joined.")

    elif action == 'sendMessage':
        user = table.get_item(Key={'connectionId': cid}).get('Item', {}).get('username', 'Anon')
        msg = body.get('message')
        broadcast(table, apigw, user, msg)

        payload = {'messageId': ctx['requestId'], 'timestamp': int(time.time()), 'username': user, 'content': msg}
        sqs.send_message(QueueUrl=SQS_URL, MessageBody=json.dumps(payload))

    return {'statusCode': 200}

def broadcast(table, apigw, user, msg):
    conns = table.scan().get('Items', [])
    data = json.dumps({'username': user, 'message': msg}).encode('utf-8')
    for c in conns:
        try:
            apigw.post_to_connection(ConnectionId=c['connectionId'], Data=data)
        except:
            table.delete_item(Key={'connectionId': c['connectionId']})