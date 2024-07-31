import boto3
import json


def backup_database(user_id):
    inputParams = {
        'status': 'backup',
        "user_id": user_id,
    }
    
    recordClient = boto3.client('lambda')
    
    response = recordClient.invoke(
        FunctionName='arn:aws:lambda:us-east-1:533267242577:function:MoniMonitor_ToDB',
        InvocationType='RequestResponse',
        Payload=json.dumps(inputParams)
    )
    
    # Read the response payload
    response_payload = json.loads(response['Payload'].read())
    response = response_payload['body']
    
