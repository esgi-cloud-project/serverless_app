import json
import boto3
import os
import pprint 

def handler(event, context): 
    
    try:
        
        res = json.loads(event['body']);
        
        if 'action' not in res or 'client' not in res:
        
            raise Exception("Malformed data")
        
        client = boto3.client('sqs');
        

        client.send_message(
            QueueUrl=os.getenv('EVENT_SERVICE_URL'),
            MessageBody='test',
            MessageAttributes={
                'action': {
                    'StringValue': res['action'],
                    'DataType': 'String'
                },
                'client': {
                    'StringValue': res['client'],
                    'DataType': 'String'
                }
            }
        )
        
        return {
            "statusCode": 200,
            "headers" : {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "status": "succeed",
                "message": "Element have been add to the queue"
            })
        }

    except Exception as excep:
        
        return {
            "statusCode": 400,
            "headers" : {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "status": "failed",
                "message": excep.args[0]
            })
        }