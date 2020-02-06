import json
import boto3
import os
import pprint 

def handler(event, context): 
    
    try:
        
        res = json.loads(event['body']);
        
        if 'id' not in res or 'name' not in res or 'price' not in res or 'description' not in res or 'grade' not in res:
        
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
                'name': {
                    'StringValue': str(res['name']),
                    'DataType': 'String'
                }
                'price': {
                    'StringValue': str(res['price']),
                    'DataType': 'Number'
                }
                'description': {
                    'StringValue': str(res['description']),
                    'DataType': 'String'
                }
                'grade': {
                    'StringValue': str(res['grade']),
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