import json
import boto3
import os
import pprint 

def handler(event, context): 
    
    try:
        
        res = json.loads(event['body']);
        
        if 'id' not in res or 'quantity' not in res:
        
            raise Exception("Malformed data")
        
        client = boto3.client('sqs');
        

        client.send_message(
            QueueUrl=os.getenv('EVENT_SERVICE_URL'),
            MessageBody='test',
            MessageAttributes={
                'id': {
                    'StringValue': res['id'],
                    'DataType': 'String'
                },
                'quantity': {
                    'StringValue': str(res['quantity']),
                    'DataType': 'Number'
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