import boto3
import json

def update_item(user_id, record_id, update_attributes) -> None:

    inputParams = {
        'status': 'modify',
        "user_id"   : user_id,
        "record_id" : record_id,
        "update_attributes" : update_attributes
    }

    recordClient = boto3.client('lambda')
    response = recordClient.invoke(
        FunctionName='arn:aws:lambda:us-east-1:533267242577:function:MoniMonitor_ToDB',
        InvocationType='RequestResponse',
        Payload=json.dumps(inputParams)
    )
    response_payload = json.loads(response['Payload'].read())
    response = response_payload['body']